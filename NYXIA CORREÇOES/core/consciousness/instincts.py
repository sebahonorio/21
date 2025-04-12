class SelfPreservation:
    def __init__(self, critical_paths: list, logger=None):
        self.critical_paths = critical_paths
        self.logger = logger

    def is_action_safe(self, action_description: str, affected_files: list = []) -> bool:
        for file in affected_files:
            if file in self.critical_paths:
                if self.logger:
                    self.logger.log("BLOCKED_ACTION", f"Tentativa de modificar ou deletar arquivo crítico: {file}")
                return False
        return True

    def should_abort_modification(self, action_description: str, simulation_result: dict) -> bool:
        if simulation_result.get("risk_of_self_deletion"):
            if self.logger:
                self.logger.log("ABORTED", f"Risco de auto-destruição detectado: {action_description}")
            return True
        return False
