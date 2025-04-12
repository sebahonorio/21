# NYXIA/core/logs/logger.py
import logging
import os

# Formato do log
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
# Local do arquivo de log
LOG_FILE = os.path.join(os.path.dirname(__file__), 'nyxia.log')

def setup_logger():
    # Cria ou obtém o logger
    logger = logging.getLogger("NyxiaLogger")
    logger.setLevel(logging.DEBUG)

    # Cria o formatador
    formatter = logging.Formatter(LOG_FORMAT)

    # Handler para exibir no console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Handler para gravar em arquivo
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

# Logger global para toda a aplicação
logger = setup_logger()

if __name__ == '__main__':
    logger.info("Nyxia Logger configurado com sucesso!")
