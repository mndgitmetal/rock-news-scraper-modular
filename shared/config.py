"""
Configurações compartilhadas
"""
import os
import logging
from dotenv import load_dotenv

# Carrega variáveis de ambiente
# Primeiro carrega .env, depois .env.local (sobrescreve valores)
load_dotenv()  # Carrega .env se existir
# Tenta carregar .env.local a partir do diretório raiz do projeto
import sys
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_local_path = os.path.join(project_root, '.env.local')
if os.path.exists(env_local_path):
    load_dotenv(dotenv_path=env_local_path)

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

