"""
Tradução de notícias usando Google Gemini AI
"""
import os
import logging
import google.generativeai as genai

logger = logging.getLogger(__name__)


class Translator:
    """Gerencia tradução de notícias com Gemini AI"""
    
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY não foi definida")

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-2.0-flash-lite")

    def translate_text(self, text):
        """Traduz texto para português"""
        if not text.strip():
            return ""

        prompt = f"Analise o {text}, e retorne somente a tradução em portugues sem mais textos e/ou comentários adicionais, pois estamos publicando no wordpress"
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            logger.error(f"Erro na tradução: {e}")
            return text

    def extract_tags(self, text):
        """Extrai tags relevantes do texto"""
        prompt = f"""
        Analise o seguinte texto e extraia palavras-chave relevantes como bandas, artistas, festivais, 
        eventos, álbuns e termos relacionados ao rock e heavy metal. 

        Retorne as palavras separadas por vírgulas, limitado até 10 palavras.

        Texto: {text}
        """

        try:
            response = self.model.generate_content(prompt)
            tags = response.text.strip().split(", ")
            return [tag.strip() for tag in tags if tag]
        except Exception as e:
            logger.error(f"Erro ao extrair tags: {e}")
            return []

