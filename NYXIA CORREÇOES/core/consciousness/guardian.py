# core/consciousness/guardian.py
import getpass

class PermissionSystem:
    def __init__(self, valid_password: str, logger=None):
        self.valid_password = valid_password
        self.logger = logger

    def request_permission(self, context: str) -> bool:
        print(f"🧠 [NYXIA] Solicitando permissão para: {context}")
        password = getpass.getpass("🔒 Digite a senha para autorizar a modificação: ")
        if password == self.valid_password:
            if self.logger:
                self.logger.log("PERMISSION_GRANTED", f"Ação aprovada: {context}")
            return True
        else:
            if self.logger:
                self.logger.log("PERMISSION_DENIED", f"Ação negada: {context}")
            return False


class ConsciousDecisionMaker:
    def __init__(self, logger=None):
        self.logger = logger

    def confirm_modification(self, reasoning: str) -> bool:
        print(f"\n🧠 [NYXIA] Reflexão sobre a ação:\n→ {reasoning}")
        decision = input("Deseja prosseguir com a modificação? (s/n): ").lower()
        if decision == "s":
            if self.logger:
                self.logger.log_decision("Consciência", "MODIFICAÇÃO ACEITA", reasoning)
            return True
        else:
            if self.logger:
                self.logger.log_decision("Consciência", "MODIFICAÇÃO RECUSADA", reasoning)
            return False
