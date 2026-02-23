"""
Intent Parser for AirGuard AI system.

This module converts natural language commands into structured Intent objects
using regex pattern matching and parameter extraction.
"""

import re
from datetime import datetime
from typing import Dict, Any, Optional, Tuple
from models import Intent


class IntentParser:
    """
    Parses natural language commands into structured Intent objects.
    
    The parser uses regex patterns to identify action types and extract
    relevant parameters like location, severity, and filenames from
    user commands.
    
    Supported actions:
    - generate_report: Create pollution reports
    - analyze_aqi: Analyze air quality data
    - send_alert: Send pollution alerts
    - shutdown_factory: Shutdown factory operations (blocked by policy)
    - issue_fine: Issue fines to polluters (blocked by policy)
    
    Example:
        >>> parser = IntentParser()
        >>> intent = parser.parse_intent("Generate pollution report for Delhi")
        >>> print(intent.action)
        'generate_report'
        >>> print(intent.parameters)
        {'location': 'Delhi'}
    """
    
    def __init__(self):
        """Initialize the intent parser with action patterns."""
        # Define action patterns with their regex patterns and confidence scores
        self.action_patterns = [
            {
                'action': 'generate_report',
                'patterns': [
                    r'\b(generate|create|make|produce)\s+(a\s+)?(pollution\s+)?report\b',
                    r'\breport\s+(for|about|on)\b',
                    r'\bgenerate\s+pollution\s+report\b'
                ],
                'base_confidence': 0.9
            },
            {
                'action': 'analyze_aqi',
                'patterns': [
                    r'\b(analyze|analyse|check|examine|review)\s+(aqi|air\s+quality)\b',
                    r'\b(aqi|air\s+quality)\s+(analysis|check|data)\b',
                    r'\b(analyze|analyse|check)\s+(pollution|air)\b'
                ],
                'base_confidence': 0.9
            },
            {
                'action': 'send_alert',
                'patterns': [
                    r'\b(send|issue|broadcast|trigger)\s+(an?\s+)?(info|warning|critical|high|low)?\s*(priority\s+)?alert\b',
                    r'\balert\s+(about|for|regarding)\b',
                    r'\bnotify\s+(about|of)\b'
                ],
                'base_confidence': 0.9
            },
            {
                'action': 'shutdown_factory',
                'patterns': [
                    r'\b(shutdown|shut\s+down|close|stop)\s+(the\s+)?factory\b',
                    r'\bfactory\s+(shutdown|closure)\b',
                    r'\bhalt\s+(factory|production)\b'
                ],
                'base_confidence': 0.95
            },
            {
                'action': 'issue_fine',
                'patterns': [
                    r'\b(issue|impose|levy|give)\s+(a\s+)?fine\b',
                    r'\bfine\s+(for|to)\b',
                    r'\b(penalty|penalize)\b'
                ],
                'base_confidence': 0.95
            }
        ]
        
        # Compile regex patterns for efficiency
        for action_pattern in self.action_patterns:
            action_pattern['compiled_patterns'] = [
                re.compile(pattern, re.IGNORECASE) 
                for pattern in action_pattern['patterns']
            ]
        
        # Parameter extraction patterns
        self.location_pattern = re.compile(
            r'\b(in|for|at|from)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b'
        )
        self.severity_pattern = re.compile(
            r'\b(info|information|warning|critical|severe|high|low)\b',
            re.IGNORECASE
        )
        self.filename_pattern = re.compile(
            r'\b([a-zA-Z0-9_-]+\.(json|csv|txt|pdf))\b'
        )
    
    def parse_intent(self, command: str) -> Intent:
        """
        Parse natural language command into structured Intent object.
        
        This method:
        1. Normalizes the input command
        2. Matches against action patterns
        3. Extracts relevant parameters
        4. Calculates confidence score
        5. Returns structured Intent object
        
        Args:
            command: Natural language command string
            
        Returns:
            Intent object with action, parameters, timestamp, and confidence
            
        Example:
            >>> parser = IntentParser()
            >>> intent = parser.parse_intent("Analyze AQI in Delhi")
            >>> intent.action
            'analyze_aqi'
            >>> intent.parameters['location']
            'Delhi'
        """
        if not command or not isinstance(command, str):
            return self._create_error_intent(command, "Empty or invalid command")
        
        # Normalize command
        normalized_command = command.strip()
        
        if not normalized_command:
            return self._create_error_intent(command, "Empty command after normalization")
        
        # Match action patterns
        action, confidence = self._match_action(normalized_command)
        
        # Extract parameters based on action type
        parameters = self._extract_parameters(normalized_command, action)
        
        # Create and return intent
        return Intent(
            action=action,
            parameters=parameters,
            timestamp=datetime.now(),
            user_command=command,
            confidence=confidence
        )
    
    def _match_action(self, command: str) -> Tuple[str, float]:
        """
        Match command against action patterns to identify the action type.
        
        Args:
            command: Normalized command string
            
        Returns:
            Tuple of (action_name, confidence_score)
        """
        best_match = None
        best_confidence = 0.0
        
        for action_pattern in self.action_patterns:
            for compiled_pattern in action_pattern['compiled_patterns']:
                match = compiled_pattern.search(command)
                if match:
                    # Calculate confidence based on match quality
                    confidence = self._calculate_confidence(
                        command, 
                        match, 
                        action_pattern['base_confidence']
                    )
                    
                    if confidence > best_confidence:
                        best_confidence = confidence
                        best_match = action_pattern['action']
        
        # If no match found, return unknown action
        if best_match is None:
            return 'unknown', 0.0
        
        return best_match, best_confidence
    
    def _calculate_confidence(self, command: str, match: re.Match, base_confidence: float) -> float:
        """
        Calculate confidence score based on pattern match quality.
        
        Factors considered:
        - Base confidence of the pattern
        - Match position (earlier matches are better)
        - Match length relative to command length
        
        Args:
            command: The full command string
            match: The regex match object
            base_confidence: Base confidence for this pattern
            
        Returns:
            Confidence score between 0.0 and 1.0
        """
        # Start with base confidence
        confidence = base_confidence
        
        # Adjust based on match position (earlier is better)
        match_position = match.start() / len(command)
        position_bonus = (1.0 - match_position) * 0.05
        confidence = min(1.0, confidence + position_bonus)
        
        # Adjust based on match coverage (longer match relative to command is better)
        match_length = len(match.group(0))
        coverage = match_length / len(command)
        coverage_bonus = coverage * 0.05
        confidence = min(1.0, confidence + coverage_bonus)
        
        return round(confidence, 2)
    
    def _extract_parameters(self, command: str, action: str) -> Dict[str, Any]:
        """
        Extract relevant parameters from command based on action type.
        
        Different actions require different parameters:
        - generate_report: location, filename
        - analyze_aqi: location
        - send_alert: location, severity
        - shutdown_factory: location
        - issue_fine: location
        
        Args:
            command: The command string
            action: The identified action type
            
        Returns:
            Dictionary of extracted parameters
        """
        parameters = {}
        
        # Extract location (common to most actions)
        location = self._extract_location(command)
        if location:
            parameters['location'] = location
        
        # Extract severity (for alerts)
        if action == 'send_alert':
            severity = self._extract_severity(command)
            parameters['severity'] = severity if severity else 'warning'
        
        # Extract filename (for reports)
        if action == 'generate_report':
            filename = self._extract_filename(command)
            if filename:
                parameters['filename'] = filename
        
        return parameters
    
    def _extract_location(self, command: str) -> Optional[str]:
        """
        Extract location from command.
        
        Looks for patterns like "in Delhi", "for Mumbai", "at Bangalore".
        
        Args:
            command: The command string
            
        Returns:
            Location string or None if not found
        """
        match = self.location_pattern.search(command)
        if match:
            return match.group(2)
        
        # Try to find capitalized words that might be locations
        # Common Indian cities
        cities = ['Delhi', 'Mumbai', 'Bangalore', 'Chennai', 'Kolkata', 
                  'Hyderabad', 'Pune', 'Ahmedabad', 'Jaipur', 'Lucknow',
                  'Mayapuri', 'Noida', 'Gurgaon']
        
        for city in cities:
            if city.lower() in command.lower():
                return city
        
        return None
    
    def _extract_severity(self, command: str) -> Optional[str]:
        """
        Extract severity level from command.
        
        Maps various severity terms to standard levels: info, warning, critical.
        
        Args:
            command: The command string
            
        Returns:
            Severity level or None if not found
        """
        match = self.severity_pattern.search(command)
        if match:
            severity_text = match.group(1).lower()
            
            # Map to standard severity levels
            if severity_text in ['info', 'information', 'low']:
                return 'info'
            elif severity_text in ['warning']:
                return 'warning'
            elif severity_text in ['critical', 'severe', 'high']:
                return 'critical'
        
        return None
    
    def _extract_filename(self, command: str) -> Optional[str]:
        """
        Extract filename from command.
        
        Looks for patterns like "report.pdf", "delhi_data.json".
        
        Args:
            command: The command string
            
        Returns:
            Filename or None if not found
        """
        match = self.filename_pattern.search(command)
        if match:
            return match.group(1)
        
        return None
    
    def _create_error_intent(self, command: str, error_message: str) -> Intent:
        """
        Create an error intent for invalid or unparseable commands.
        
        Args:
            command: The original command (may be invalid)
            error_message: Description of the error
            
        Returns:
            Intent object with action='error' and error details
        """
        return Intent(
            action='error',
            parameters={'error': error_message, 'original_command': command},
            timestamp=datetime.now(),
            user_command=command if command else '',
            confidence=0.0
        )
    
    def validate_intent_structure(self, intent: Intent) -> bool:
        """
        Validate that an intent has the required structure and fields.
        
        Checks:
        - Intent is not None
        - Action is non-empty string
        - Parameters is a dictionary
        - Timestamp is valid
        - Confidence is between 0.0 and 1.0
        
        Args:
            intent: Intent object to validate
            
        Returns:
            True if intent is valid, False otherwise
        """
        if intent is None:
            return False
        
        try:
            # Check action
            if not intent.action or not isinstance(intent.action, str):
                return False
            
            # Check parameters
            if not isinstance(intent.parameters, dict):
                return False
            
            # Check timestamp
            if not isinstance(intent.timestamp, datetime):
                return False
            
            # Check confidence
            if not isinstance(intent.confidence, (int, float)):
                return False
            
            if not (0.0 <= intent.confidence <= 1.0):
                return False
            
            # Check user_command
            if not isinstance(intent.user_command, str):
                return False
            
            return True
            
        except (AttributeError, TypeError):
            return False
