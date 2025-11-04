"""
Publicação de notícias no WordPress
"""
import requests
import os
import base64
import logging
from requests.auth import HTTPBasicAuth

logger = logging.getLogger(__name__)


class WordPressPublisher:
    """Gerencia publicação de notícias no WordPress"""
    
    def __init__(self):
        self.url = os.getenv("WORDPRESS_URL", "").rstrip("/")
        self.user = os.getenv("WORDPRESS_USER")
        self.password = os.getenv("WORDPRESS_APP_PASSWORD") or os.getenv("WORDPRESS_PASSWORD")
        
        if not all([self.url, self.user, self.password]):
            raise ValueError("Configurações do WordPress incompletas")
        
        self.posts_endpoint = f"{self.url}/wp-json/wp/v2/posts"
        self.media_endpoint = f"{self.url}/wp-json/wp/v2/media"
        self.tags_endpoint = f"{self.url}/wp-json/wp/v2/tags"
        
        # Autenticação Basic Auth
        auth_string = f"{self.user}:{self.password}"
        auth_encoded = base64.b64encode(auth_string.encode()).decode()
        
        self.headers = {
            "Authorization": f"Basic {auth_encoded}",
            "Content-Type": "application/json"
        }

    def get_published_titles(self):
        """Obtém títulos dos posts já publicados"""
        try:
            response = requests.get(
                f"{self.posts_endpoint}?per_page=100",
                headers=self.headers,
                timeout=10
            )
            if response.status_code == 200:
                return {post["title"]["rendered"] for post in response.json()}
        except Exception as e:
            logger.error(f"Erro ao buscar posts: {e}")
        return set()

    def upload_image(self, image_url):
        """Faz upload de imagem para o WordPress"""
        try:
            img_response = requests.get(image_url, timeout=10)
            img_response.raise_for_status()
            
            files = {
                'file': ('image.jpg', img_response.content, 'image/jpeg')
            }
            
            response = requests.post(
                self.media_endpoint,
                headers={"Authorization": self.headers["Authorization"]},
                files=files,
                timeout=30
            )
            
            if response.status_code == 201:
                return response.json().get("id")
        except Exception as e:
            logger.error(f"Erro ao fazer upload da imagem: {e}")
        return None

    def create_or_get_tag(self, tag_name):
        """Cria ou obtém uma tag"""
        try:
            # Busca tag existente
            response = requests.get(
                f"{self.tags_endpoint}?search={tag_name}",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                tags = response.json()
                for tag in tags:
                    if tag["name"].lower() == tag_name.lower():
                        return tag["id"]
            
            # Cria nova tag
            response = requests.post(
                self.tags_endpoint,
                json={"name": tag_name},
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 201:
                return response.json().get("id")
        except Exception as e:
            logger.error(f"Erro ao criar/buscar tag: {e}")
        return None

    def publish_post(self, title, content, image_url=None, tags=None):
        """Publica um post no WordPress"""
        published_titles = self.get_published_titles()
        
        if title in published_titles:
            logger.info(f"Post já existe: {title}")
            return False

        post_data = {
            "title": title,
            "content": content,
            "status": "publish"
        }

        # Adiciona imagem destacada
        if image_url:
            image_id = self.upload_image(image_url)
            if image_id:
                post_data["featured_media"] = image_id

        # Adiciona tags
        if tags:
            tag_ids = []
            for tag in tags:
                tag_id = self.create_or_get_tag(tag)
                if tag_id:
                    tag_ids.append(tag_id)
            if tag_ids:
                post_data["tags"] = tag_ids

        try:
            response = requests.post(
                self.posts_endpoint,
                json=post_data,
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 201:
                logger.info(f"Post publicado: {title}")
                return True
            else:
                logger.error(f"Erro ao publicar: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            logger.error(f"Erro ao publicar post: {e}")
            return False

