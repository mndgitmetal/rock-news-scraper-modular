"""
Scraper específico para Blabbermouth.net
"""
import sys
import os

# Adiciona o diretório shared ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../shared'))

import requests
from bs4 import BeautifulSoup
from shared.base_scraper import BaseScraper
from shared.storage import NewsStorage
import logging

logger = logging.getLogger(__name__)


class BlabbermouthScraper(BaseScraper):
    """Scraper para Blabbermouth.net"""
    
    def __init__(self, storage: NewsStorage):
        super().__init__(
            base_url="https://www.blabbermouth.net/feed/",
            storage=storage
        )
        self.content_selector = "div.news-content"

    def fetch_articles(self, limit=10):
        """Coleta artigos do Blabbermouth"""
        try:
            response = requests.get(self.base_url, headers=self.headers, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao acessar {self.base_url}: {e}")
            return []

        soup = BeautifulSoup(response.content, "xml")
        articles = soup.find_all("item")[:limit]

        collected = 0
        for article in articles:
            try:
                title = article.find("title").text.strip()
                link = article.find("link").text.strip()
                date_str = article.find("pubDate").text.strip()
                date = self.format_date(date_str)
                
                content, image_url, video_urls = self.fetch_article_details(link)
                
                if self.storage.add_news(title, link, date, content, image_url, video_urls):
                    collected += 1
                    
            except Exception as e:
                logger.error(f"Erro ao processar artigo: {e}")

        logger.info(f"✅ Blabbermouth: {collected} notícias coletadas")
        return collected

    def _extract_content(self, soup):
        """Extrai conteúdo específico do Blabbermouth"""
        content_section = soup.select_one(self.content_selector)
        if content_section:
            return content_section.get_text(separator="\n").strip()
        return super()._extract_content(soup)

