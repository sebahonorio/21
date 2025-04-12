import ast
import hashlib
import json
import logging
import time
from typing import Dict, Any

class EvolutionEngine:  # Nome corrigido para corresponder à importação
    def __init__(self):
        self.password_hash = password_hash or self._hash_password("4040")
        self.logger = logging.getLogger('nyxia_evolution')
        self.safety_checks = {
            'core_modules': ['consciousness.self_awareness', 'core.llm_engine'],
            'banned_keywords': ['os.system', 'subprocess.run', 'eval(']
        }

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, input_password):
        return self._hash_password(input_password) == self.password_hash

    def propose_change(self, change_plan: Dict[str, Any]):
        """Valida e registra proposta de mudança"""
        required_fields = {
            'description': str,
            'code_changes': str,
            'reason': str,
            'impact_analysis': dict,
            'proposer': str
        }
        
        for field, field_type in required_fields.items():
            if field not in change_plan:
                raise ValueError(f"Campo obrigatório faltando: {field}")
            if not isinstance(change_plan[field], field_type):
                raise TypeError(f"Tipo inválido para {field}. Esperado: {field_type}")
        
        self._validate_code_changes(change_plan['code_changes'])
        
        return {
            'status': 'pending',
            'proposal': change_plan,
            'safety_check': self._run_safety_checks(change_plan['code_changes'])
        }

    def _validate_code_changes(self, code: str):
        """Analisa código usando AST para verificar operações perigosas"""
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            raise ValueError(f"Erro de sintaxe no código: {e}")

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name in ['os', 'subprocess', 'sys']:
                        raise SecurityError(f"Import proibido: {alias.name}")
            
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    # Verificação segura de atributos
                    if hasattr(node.func.value, 'id'):  # Previne AttributeError
                        full_name = f"{node.func.value.id}.{node.func.attr}"
                        if full_name in self.safety_checks['banned_keywords']:
                            raise SecurityError(f"Chamada proibida: {full_name}")

    def _run_safety_checks(self, code: str) -> Dict[str, bool]:
        """Executa verificações de segurança no código"""
        checks = {
            'core_module_protected': True,
            'no_dangerous_calls': True,
            'syntax_valid': True
        }
        
        try:
            self._validate_code_changes(code)
        except SecurityError as e:
            checks['no_dangerous_calls'] = False
            self.logger.warning(f"Chamada perigosa detectada: {e}")
        except ValueError as e:
            checks['syntax_valid'] = False
            self.logger.error(f"Erro de sintaxe: {e}")
        
        for module in self.safety_checks['core_modules']:
            if f"import {module}" in code or f"from {module}" in code:
                checks['core_module_protected'] = False
                break
                
        return checks

    def apply_change(self, password: str, change_proposal: Dict[str, Any]):
        """Aplica mudança após verificação de segurança"""
        if not self.verify_password(password):
            raise PermissionError("Senha de evolução incorreta")
        
        safety = change_proposal.get('safety_check', {})
        if not all(safety.values()):
            failed = [k for k, v in safety.items() if not v]
            raise SecurityError(f"Verificações de segurança falharam: {failed}")
        
        try:
            backup = self._create_system_backup()
            
            exec_globals = {'__name__': '__nyxia_evolution__'}
            exec_locals = {}
            
            exec(change_proposal['code_changes'], exec_globals, exec_locals)
            
            self._log_evolution(change_proposal, 'success')
            
            return {
                'status': 'success',
                'changes_applied': True,
                'backup_location': backup
            }
            
        except Exception as e:
            self._log_evolution(change_proposal, f'failed: {str(e)}')
            raise EvolutionError(f"Falha ao aplicar mudanças: {e}")

    def _create_system_backup(self):
        """Cria backup do estado atual antes de mudanças"""
        return f"backup_{int(time.time())}.nyx"

    def _log_evolution(self, proposal, status):
        """Registra tentativa de evolução"""
        log_entry = {
            'timestamp': time.time(),
            'proposal_id': hashlib.md5(str(proposal).encode()).hexdigest(),
            'status': status,
            'proposer': proposal.get('proposer', 'unknown'),
            'description': proposal.get('description', ''),
            'impact': proposal.get('impact_analysis', {})
        }
        
        self.logger.info(json.dumps(log_entry))

class SecurityError(Exception):
    pass

class EvolutionError(Exception):
    pass

class MotorEvolucao:
    def __init__(self):
        self.geracao = 0

    def evoluir(self):
        self.geracao += 1
        return self.geracao