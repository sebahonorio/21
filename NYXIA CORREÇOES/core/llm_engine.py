from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, BitsAndBytesConfig
from langchain_huggingface import HuggingFacePipeline
import torch

class MotorLLM:
    def __init__(self):
        self.model_name = "microsoft/Phi-3-mini-4k-instruct"  # Modelo leve para CPU
        self.llm = self.carregar_modelo()
    
    def carregar_modelo(self):
        print("🔌 Carregando modelo (4-bit quantizado)...")
        
        # Configuração para quantização 4-bit (reduz uso de RAM)
        nf4_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
        )
        
        tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            quantization_config=nf4_config,
            device_map="auto"  # Automaticamente usa CPU se GPU não estiver disponível
        )
        
        pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=150,
            temperature=0.7,
            do_sample=True
        )
        
        return HuggingFacePipeline(pipeline=pipe)