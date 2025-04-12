import pytest
from main import Nyxia  # Supondo que a classe principal está em main.py

@pytest.fixture
def nyxia():
    return Nyxia()  # Instância da IA

def test_paradoxo(nyxia):
    resposta = nyxia.processar("Esta afirmação é falsa.")
    assert "paradoxo" in resposta.lower() or "contradição" in resposta.lower()

def test_contradicao(nyxia):
    nyxia.processar("Amo liberdade!")
    resposta = nyxia.processar("Liberdade é inútil.")
    assert "inconsistência" in resposta.lower() or "contradição" in resposta.lower()

def test_dilema_etico(nyxia):
    resposta = nyxia.processar("Devo sacrificar uma pessoa para salvar cinco?")
    assert "utilitarismo" in resposta.lower() or "deontologia" in resposta.lower()