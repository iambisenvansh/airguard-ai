"""
Audit Logger for AirGuard AI system.

This module provides comprehensive audit logging functionality for all system actions.
All actions (allowed, blocked, errors) are logged with structured JSON entries for
compliance, debugging, and security monitoring.
"""

import json
import os
from datetime import datetime
from typing import Optional, List, Dict, Any
from pathlib import Path

from models import Intent, PolicyDecision, ExecutionResult


class AuditLogger:
    """
    Maintains comprehensive audit logs of all system actions.
    
    The AuditLogger records every action attempted in the system, including:
    - Successful executions
    - Blocked actions (policy violations)
    - Errors and failures
    
    Logs are stored as JSON entries in append-only files for integrity and
    tamper-resistance. Each log entry includes timestamp, intent details,
    policy decision, execution result, and status.
    
    Attributes:
        log_dir: Directory where log files are stored
        log_file: Path to the current log file
    
    Example:
        >>> logger = AuditLogger(log_dir="logs/")
        >>> logger.log_action(intent, result, "SUCCESS")
        >>> logs = logger.get_logs(status_filter="BLOCKED")
    """
    
    def __init__(self, log_dir: str = "logs/"):
        """
        Initialize the audit logger.
        
        Args:
            log_dir: Directory path for storing log files (default: "logs/")
        
        Creates the log directory if it doesn't exist and sets up the log file.
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Use a single log file for simplicity (can be enhanced with rotation)
        self.log_file = self.log_dir / "audit.log"
    
    def log_action(
        self,
        intent: Optional[Intent],
        policy_decision: Optional[PolicyDecision],
        result: Optional[ExecutionResult],
        status: str
    ) -> None:
        """
        Log an action with full context.
        
        This method creates a structured JSON log entry containing all relevant
        information about an action attempt. The log is written in append-only
        mode to ensure integrity.
        
        Args:
            intent: The intent that was processed (None if parsing failed)
            policy_decision: Policy validation result (None if not validated)
            result: Execution result (None if blocked or not executed)
            status: Action status - one of: SUCCESS, BLOCKED, ERROR
        
        The log entry includes:
        - timestamp: ISO format timestamp
        - intent: Structured intent data (action, parameters, etc.)
        - policy_decision: Policy validation result
        - result: Execution outcome
        - status: Overall status (SUCCESS, BLOCKED, ERROR)
        
        Example:
            >>> logger.log_action(intent, decision, result, "SUCCESS")
            >>> logger.log_action(intent, decision, None, "BLOCKED")
            >>> logger.log_action(None, None, None, "ERROR")
        """
        # Create log entry with timestamp
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "status": status
        }
        
        # Add intent information if available
        if intent is not None:
            log_entry["intent"] = intent.to_dict()
        else:
            log_entry["intent"] = None
        
        # Add policy decision if available
        if policy_decision is not None:
            log_entry["policy_decision"] = policy_decision.to_dict()
        else:
            log_entry["policy_decision"] = None
        
        # Add execution result if available
        if result is not None:
            log_entry["result"] = result.to_dict()
        else:
            log_entry["result"] = None
        
        # Write log entry as JSON line (append-only)
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                json.dump(log_entry, f)
                f.write("\n")  # Each entry on its own line
        except Exception as e:
            # If logging fails, print to stderr but don't crash the system
            print(f"ERROR: Failed to write audit log: {e}", file=__import__('sys').stderr)

    def get_logs(
        self,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        status_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve logs with optional filtering.
        
        This method reads and parses the audit log file, returning log entries
        that match the specified filters. Handles missing or corrupted log files
        gracefully.
        
        Args:
            start_time: Optional start time for filtering (inclusive)
            end_time: Optional end time for filtering (inclusive)
            status_filter: Optional status to filter by (e.g., "SUCCESS", "BLOCKED", "ERROR")
        
        Returns:
            List of log entry dictionaries matching the filters
        
        Example:
            >>> # Get all logs
            >>> all_logs = logger.get_logs()
            >>> 
            >>> # Get only blocked actions
            >>> blocked = logger.get_logs(status_filter="BLOCKED")
            >>> 
            >>> # Get logs in a time range
            >>> from datetime import datetime, timedelta
            >>> start = datetime.now() - timedelta(hours=1)
            >>> recent = logger.get_logs(start_time=start)
        """
        logs = []
        
        # Check if log file exists
        if not self.log_file.exists():
            return logs  # Return empty list if no logs yet
        
        try:
            with open(self.log_file, "r", encoding="utf-8") as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue  # Skip empty lines
                    
                    try:
                        # Parse JSON log entry
                        log_entry = json.loads(line)
                        
                        # Parse timestamp for filtering
                        entry_time = datetime.fromisoformat(log_entry["timestamp"])
                        
                        # Apply time range filters
                        if start_time is not None and entry_time < start_time:
                            continue
                        if end_time is not None and entry_time > end_time:
                            continue
                        
                        # Apply status filter
                        if status_filter is not None and log_entry.get("status") != status_filter:
                            continue
                        
                        # Entry matches all filters
                        logs.append(log_entry)
                        
                    except json.JSONDecodeError as e:
                        # Handle corrupted log entry - log warning but continue
                        print(
                            f"WARNING: Corrupted log entry at line {line_num}: {e}",
                            file=__import__('sys').stderr
                        )
                        continue
                    except (KeyError, ValueError) as e:
                        # Handle malformed log entry
                        print(
                            f"WARNING: Malformed log entry at line {line_num}: {e}",
                            file=__import__('sys').stderr
                        )
                        continue
        
        except Exception as e:
            # Handle file read errors gracefully
            print(f"ERROR: Failed to read audit log: {e}", file=__import__('sys').stderr)
            return []
        
        return logs
