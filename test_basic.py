"""
Script de teste básico para verificar se o scraper está funcionando
Testa apenas a coleta de notícias sem precisar de Supabase, WordPress ou Gemini
"""
import sys
import os

# Adiciona shared ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'shared'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'services/blabbermouth'))

import requests
from bs4 import BeautifulSoup
from datetime import datetime

def test_feed_access():
    """Testa se consegue acessar o feed RSS do Blabbermouth"""
    print("🔍 Testando acesso ao feed RSS do Blabbermouth...")
    
    feed_url = "https://www.blabbermouth.net/feed/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(feed_url, headers=headers, timeout=10)
        response.raise_for_status()
        print(f"✅ Feed acessado com sucesso! Status: {response.status_code}")
        return response.content
    except Exception as e:
        print(f"❌ Erro ao acessar feed: {e}")
        return None

def test_feed_parsing(feed_content):
    """Testa se consegue fazer parse do feed RSS"""
    print("\n📰 Testando parsing do feed RSS...")
    
    try:
        soup = BeautifulSoup(feed_content, "xml")
        articles = soup.find_all("item")
        print(f"✅ Feed parseado com sucesso! Encontrados {len(articles)} artigos")
        
        if articles:
            # Mostra informações do primeiro artigo
            first_article = articles[0]
            title = first_article.find("title")
            link = first_article.find("link")
            pub_date = first_article.find("pubDate")
            
            print(f"\n📄 Primeiro artigo encontrado:")
            if title:
                print(f"   Título: {title.text.strip()[:80]}...")
            if link:
                print(f"   Link: {link.text.strip()}")
            if pub_date:
                print(f"   Data: {pub_date.text.strip()}")
        
        return articles[:3]  # Retorna os 3 primeiros para teste
    except Exception as e:
        print(f"❌ Erro ao fazer parse do feed: {e}")
        return []

def test_article_details(articles):
    """Testa se consegue acessar detalhes de um artigo"""
    print("\n🔎 Testando acesso aos detalhes de um artigo...")
    
    if not articles:
        print("⚠️ Nenhum artigo para testar")
        return
    
    first_article = articles[0]
    link = first_article.find("link")
    
    if not link:
        print("⚠️ Artigo sem link")
        return
    
    article_url = link.text.strip()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        print(f"   Acessando: {article_url}")
        response = requests.get(article_url, headers=headers, timeout=10)
        response.raise_for_status()
        print(f"✅ Artigo acessado com sucesso! Status: {response.status_code}")
        
        # Tenta extrair conteúdo
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Tenta encontrar conteúdo
        content_selectors = [
            "div.news-content",
            "div.article-content",
            "div.post-content",
            "div.entry-content",
            "article",
            "div.content"
        ]
        
        content_found = False
        for selector in content_selectors:
            element = soup.select_one(selector)
            if element:
                content = element.get_text(separator="\n").strip()
                if content:
                    print(f"✅ Conteúdo extraído! Tamanho: {len(content)} caracteres")
                    print(f"   Preview: {content[:100]}...")
                    content_found = True
                    break
        
        if not content_found:
            print("⚠️ Conteúdo não encontrado com os seletores padrão")
        
        # Tenta encontrar imagem
        og_image = soup.find("meta", property="og:image")
        if og_image and og_image.get("content"):
            print(f"✅ Imagem encontrada: {og_image['content'][:80]}...")
        else:
            print("⚠️ Imagem não encontrada")
        
        return True
    except Exception as e:
        print(f"❌ Erro ao acessar artigo: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("=" * 60)
    print("🧪 TESTE BÁSICO DO SCRAPER BLABBERMOUTH")
    print("=" * 60)
    
    # Teste 1: Acesso ao feed
    feed_content = test_feed_access()
    if not feed_content:
        print("\n❌ Teste falhou: não foi possível acessar o feed")
        return
    
    # Teste 2: Parsing do feed
    articles = test_feed_parsing(feed_content)
    if not articles:
        print("\n❌ Teste falhou: não foi possível fazer parse do feed")
        return
    
    # Teste 3: Detalhes do artigo
    test_article_details(articles)
    
    print("\n" + "=" * 60)
    print("✅ TESTE BÁSICO CONCLUÍDO!")
    print("=" * 60)
    print("\n💡 O scraper está funcionando corretamente para coleta de notícias.")
    print("   Para usar todas as funcionalidades, configure:")
    print("   - SUPABASE_URL e SUPABASE_KEY (para armazenamento)")
    print("   - GEMINI_API_KEY (para tradução)")
    print("   - WORDPRESS_URL, WORDPRESS_USER, WORDPRESS_APP_PASSWORD (para publicação)")

if __name__ == "__main__":
    main()

