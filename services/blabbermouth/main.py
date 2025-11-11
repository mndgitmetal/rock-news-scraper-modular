"""
Serviço FastAPI para scraper do Blabbermouth
Cada execução: coleta -> traduz -> publica
"""
import sys
import os

# Workaround para Python 3.9.6 - corrige erro do importlib.metadata
# Deve ser aplicado ANTES de qualquer outro import
try:
    import importlib_metadata
    # Substitui importlib.metadata pelo backport
    sys.modules['importlib.metadata'] = importlib_metadata
except ImportError:
    # Se importlib_metadata não estiver disponível, tenta usar o nativo
    try:
        import importlib.metadata
        if not hasattr(importlib.metadata, 'packages_distributions'):
            # Se não tiver o atributo, tenta usar o backport
            try:
                import importlib_metadata
                sys.modules['importlib.metadata'] = importlib_metadata
            except ImportError:
                pass
    except ImportError:
        pass

from dotenv import load_dotenv

# Adiciona o diretório raiz do projeto ao path para importar shared
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)

from fastapi import FastAPI, BackgroundTasks
from shared.config import logger
from shared.storage import NewsStorage
from shared.translator import Translator
from shared.wordpress import WordPressPublisher
from scraper import BlabbermouthScraper

# Carrega variáveis de ambiente
# Primeiro carrega .env, depois .env.local (sobrescreve valores)
# Sempre procura no diretório raiz do projeto
env_path = os.path.join(project_root, '.env')
env_local_path = os.path.join(project_root, '.env.local')

if os.path.exists(env_path):
    load_dotenv(dotenv_path=env_path)
if os.path.exists(env_local_path):
    load_dotenv(dotenv_path=env_local_path, override=True)  # override=True sobrescreve valores

app = FastAPI(title="Blabbermouth Scraper", version="1.0.0")

LIMIT_PER_RUN = int(os.getenv("LIMIT_PER_RUN", "10"))


def run_scraper_job():
    """Executa o job completo: coletar -> traduzir -> publicar"""
    try:
        # 1. Inicializa componentes
        storage = NewsStorage()
        translator = Translator()
        wordpress = WordPressPublisher()
        scraper = BlabbermouthScraper(storage)

        # 2. Coleta notícias
        logger.info("🕷️ Coletando notícias do Blabbermouth...")
        collected = scraper.fetch_articles(limit=LIMIT_PER_RUN)
        
        if collected == 0:
            logger.info("Nenhuma notícia nova coletada")
            return

        # 3. Busca notícias sem tradução do Supabase
        logger.info("🌎 Traduzindo notícias...")
        # TODO: Implementar busca de notícias sem tradução
        
        # 4. Publica no WordPress
        logger.info("📝 Publicando no WordPress...")
        # TODO: Implementar publicação de notícias traduzidas
        
        logger.info("✅ Processo concluído!")
        
    except Exception as e:
        logger.error(f"❌ Erro no job: {e}", exc_info=True)
        raise


@app.get("/")
def home():
    return {
        "service": "blabbermouth-scraper",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/run")
def run_scraper(background_tasks: BackgroundTasks):
    """Endpoint para executar o scraper (retorna imediatamente)"""
    background_tasks.add_task(run_scraper_job)
    return {
        "status": "accepted",
        "message": "Scraper iniciado em background",
        "service": "blabbermouth",
        "limit": LIMIT_PER_RUN
    }


@app.get("/health")
def health():
    """Health check"""
    return {"status": "healthy", "service": "blabbermouth-scraper"}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8080"))
    # Configuração do uvicorn para exibir logs detalhados
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=port,
        log_level="info",
        access_log=True
    )
