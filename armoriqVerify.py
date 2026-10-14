class ArmorIQVerifier:

    def verify_action(self, intent, policy_decision):
        """
        External governance validation layer
        """

        if not policy_decision.allowed:
            return {
                "approved": False,
                "reason": "Policy violation"
            }

        # ArmorIQ runtime validation simulation
        risk_score = self.compute_risk(intent)

        if risk_score > 0.8:
            return {
                "approved": False,
                "reason": "High governance risk detected"
            }

        return {
            "approved": True,
            "reason": "ArmorIQ approved"
        }

    def compute_risk(self, intent):
        sensitive_actions = [
            "modify_official_report",
            "lift_factory_ban",
            "delete_enforcement_record"
        ]

        if intent.action in sensitive_actions:
            return 0.95

        return 0.2