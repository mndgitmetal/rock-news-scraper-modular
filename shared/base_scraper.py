"""
Classe base para todos os scrapers
"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import logging

logger = logging.getLogger(__name__)


class BaseScraper:
    """Classe base para scraping de sites de notícias de rock/metal"""
    
    def __init__(self, base_url, storage):
        self.base_url = base_url
        self.storage = storage
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def get_html(self, url):
        """Obtém o HTML de uma URL"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.error(f"Erro ao acessar {url}: {e}")
            return None

    def parse_html(self, html):
        """Converte HTML em BeautifulSoup"""
        return BeautifulSoup(html, "html.parser")

    def fetch_articles(self, limit=10):
        """Método abstrato - deve ser implementado por cada scraper"""
        raise NotImplementedError("Cada scraper deve implementar fetch_articles")

    def fetch_article_details(self, url):
        """Extrai detalhes completos de um artigo"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Erro ao acessar {url}: {e}")
            return "", "", []

        soup = BeautifulSoup(response.content, "html.parser")

        # Extrai conteúdo
        content = self._extract_content(soup)
        
        # Extrai imagem principal
        image_url = self._extract_main_image(soup)
        
        # Extrai vídeos
        video_urls = self._extract_videos(soup)

        return content, image_url, video_urls

    def _extract_content(self, soup):
        """Extrai o conteúdo do artigo - pode ser sobrescrito"""
        # Tenta diferentes seletores comuns
        selectors = [
            "div.news-content",
            "div.article-content",
            "div.post-content",
            "div.entry-content",
            "article",
            "div.content"
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text(separator="\n").strip()
        
        return ""

    def _extract_main_image(self, soup):
        """Extrai a imagem principal do artigo"""
        # Tenta og:image primeiro
        og_image = soup.find("meta", property="og:image")
        if og_image and og_image.get("content"):
            return og_image["content"]
        
        # Tenta imagem destacada
        img = soup.find("img", class_=lambda x: x and ("featured" in x.lower() or "main" in x.lower()))
        if img and img.get("src"):
            return img["src"]
        
        return ""

    def _extract_videos(self, soup):
        """Extrai URLs de vídeos do YouTube"""
        video_urls = []
        for iframe in soup.find_all('iframe'):
            src = iframe.get('src', '')
            if src and ('youtube.com' in src or 'youtu.be' in src):
                video_urls.append(src)
        return video_urls

    def format_date(self, date_str):
        """Formata data para ISO 8601"""
        formats = [
            "%a, %d %b %Y %H:%M:%S %z",
            "%a, %d %b %Y %H:%M:%S %Z",
            "%Y-%m-%d %H:%M:%S"
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt).isoformat()
            except ValueError:
                continue
        
        logger.warning(f"Formato de data inválido: {date_str}")
        return date_str

