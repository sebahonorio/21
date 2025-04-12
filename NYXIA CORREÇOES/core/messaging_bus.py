# NYXIA/core/messaging_bus.py
"""
Message Bus: Um barramento simples para que diferentes módulos se comuniquem.
Utilizaremos um padrão publish/subscribe.
"""

from collections import defaultdict
import threading

class MessageBus:
    def __init__(self):
        # Dicionário para armazenar assinaturas: { tópico: [lista de funções callback] }
        self.subscribers = defaultdict(list)
        # Lock para garantir a integridade em ambientes multithread
        self.lock = threading.Lock()

    def subscribe(self, topic: str, callback):
        """
        Inscreve uma função callback para um tópico específico.
        :param topic: Nome do tópico.
        :param callback: Função que será chamada quando uma mensagem for publicada.
        """
        with self.lock:
            self.subscribers[topic].append(callback)

    def publish(self, topic: str, message):
        """
        Publica uma mensagem para um tópico.
        :param topic: Nome do tópico.
        :param message: Mensagem que será enviada.
        """
        with self.lock:
            callbacks = self.subscribers.get(topic, [])
        for callback in callbacks:
            try:
                callback(message)
            except Exception as e:
                print(f"Erro ao chamar o callback do tópico '{topic}': {e}")

# Teste local (executar este arquivo para testar o Message Bus)
if __name__ == '__main__':
    def exemplo_callback(mensagem):
        print(f"Recebido: {mensagem}")

    bus = MessageBus()
    bus.subscribe('saudacao', exemplo_callback)
    bus.publish('saudacao', "Olá, Nyxia!")
