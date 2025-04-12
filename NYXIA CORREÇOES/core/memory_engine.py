from langchain.memory import ConversationBufferMemory
from langchain.vectorstores import SQLiteVSS
from langchain.embeddings import HuggingFaceEmbeddings
import os

class MemoriaLongoPrazo:
    def __init__(self):
        self.embedding = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-small")
        self.db_path = "nyxia_memoria.db"
        if not os.path.exists(self.db_path):
            self.db = SQLiteVSS.from_texts(
                texts=[""],
                embedding=self.embedding,
                table="memoria",
                database=self.db_path
            )
        else:
            self.db = SQLiteVSS(embedding=self.embedding, database=self.db_path, table="memoria")

    def salvar_interacao(self, input_text, output_text):
        self.db.add_texts([f"Human: {input_text}\nAI: {output_text}"])

def criar_memoria():
    print("🧠 Inicializando memória (curto + longo prazo)...")
    memoria = ConversationBufferMemory()
    memoria_lp = MemoriaLongoPrazo()
    return memoria, memoria_lp  # Retorna ambos os tipos de memória