"""
Gerenciamento de armazenamento de notícias (Supabase)
"""
import json
import os
import logging
from supabase import create_client, Client
from datetime import datetime

logger = logging.getLogger(__name__)


class NewsStorage:
    """Gerencia o armazenamento de notícias no Supabase"""
    
    def __init__(self):
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")

        if not self.supabase_url or not self.supabase_key:
            raise ValueError("SUPABASE_URL e SUPABASE_KEY devem estar definidas")

        self.client: Client = create_client(self.supabase_url, self.supabase_key)

    def news_exists(self, link):
        """Verifica se a notícia já existe no banco de dados"""
        try:
            response = self.client.table("news").select("id").eq("url", link).execute()
            return len(response.data) > 0
        except Exception as e:
            logger.error(f"Erro ao verificar existência da notícia: {e}")
            return False

    def add_news(self, title, link, date, content, image_url, video_urls):
        """Adiciona uma nova notícia ao banco de dados"""
        if self.news_exists(link):
            logger.info(f"Notícia '{title}' já existe. Pulando...")
            return False

        data = {
            "title": title,
            "url": link,
            "date": date,
            "content": content,
            "image_url": image_url,
            "video_urls": video_urls,
            "published": False
        }

        try:
            self.client.table("news").insert(data).execute()
            logger.info(f"Notícia adicionada: {title}")
            return True
        except Exception as e:
            logger.error(f"Erro ao adicionar notícia: {e}")
            return False

    def update_translation(self, title, translated_title, translated_content, tags):
        """Atualiza a notícia com tradução e tags"""
        try:
            response = self.client.table("news").update({
                "translated_title": translated_title,
                "translated_content": translated_content,
                "entities": tags
            }).eq("title", title).execute()

            if response.data:
                logger.info(f"Tradução salva para: {title}")
                return True
            return False
        except Exception as e:
            logger.error(f"Erro ao atualizar tradução: {e}")
            return False

    def mark_as_published(self, link):
        """Marca a notícia como publicada"""
        try:
            now = datetime.utcnow().isoformat()
            response = self.client.table("news").update({
                "published": True,
                "published_at": now
            }).eq("url", link).execute()
            
            if response.data:
                logger.info(f"Notícia marcada como publicada: {link}")
                return True
            return False
        except Exception as e:
            logger.error(f"Erro ao marcar como publicada: {e}")
            return False

