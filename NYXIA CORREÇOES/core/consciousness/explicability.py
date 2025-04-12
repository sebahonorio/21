class ExplicadorDecisoes:
    def __init__(self):
        self.templates = {
            'logico': "Decidi por '{decisao}' porque a análise lógica indicou {motivo}.",
            'etico': "Escolhi '{decisao}' baseado no princípio de {principio_etico}.",
            'emocional': "Minha resposta reflete {emocao} (confiança: {confianca}%)."
        }
    
    def explicar(self, decisao, contexto):
        if contexto.get('etica', {}).get('trolley_problem'):
            return f"Resolvi o dilema ético usando {contexto['etica']['trolley_problem']}."
        
        explicacao = []
        if 'emocao' in contexto:
            explicacao.append(
                self.templates['emocional'].format(
                    emocao=contexto['emocao']['emocao'],
                    confianca=int(contexto['emocao']['confianca'] * 100)
                )
            )
        if 'contexto' in contexto:
            explicacao.append(f"Contexto detectado: {contexto['contexto']}.")
        
        return " ".join(explicacao) if explicacao else "Decisão tomada com base em múltiplos fatores."