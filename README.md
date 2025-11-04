# 🎸 Rock News Scraper - Arquitetura Modular

## 🏗️ **Arquitetura**

Cada scraper roda como um **serviço independente** no Google Cloud Run, permitindo:
- ⏰ **Agendamento individual** por site
- 🔧 **Manutenção independente** 
- 📈 **Escalabilidade separada**
- 🚀 **Deploy isolado**

## 📁 **Estrutura do Projeto**

```
rock-news-scraper-modular/
│
├── shared/                    # Código compartilhado
│   ├── base_scraper.py      # Classe base para scrapers
│   ├── storage.py            # Gerenciamento Supabase
│   ├── translator.py         # Tradução com Gemini AI
│   ├── wordpress.py          # Publicação WordPress
│   └── config.py             # Configurações
│
├── services/                  # Serviços individuais
│   ├── blabbermouth/
│   │   ├── main.py           # Endpoint FastAPI
│   │   ├── scraper.py        # Scraper específico
│   │   └── Dockerfile
│   ├── bravewords/
│   ├── metalinjection/
│   ├── loudwire/
│   ├── metaltalk/
│   └── metalsucks/
│
└── requirements.txt
```

## 🚀 **Como Usar**

### **1. Configuração Local**

```bash
# Clone o projeto
cd rock-news-scraper-modular

# Instale dependências
pip install -r requirements.txt

# Configure variáveis de ambiente
cp .env.example .env.local
# Edite .env.local com suas credenciais
```

### **2. Testar Localmente**

```bash
# Testar serviço do Blabbermouth
cd services/blabbermouth
python main.py

# Ou via curl
curl http://localhost:8080/run
```

### **3. Deploy no Cloud Run**

```bash
# Deploy do Blabbermouth
gcloud run deploy blabbermouth-scraper \
  --source services/blabbermouth \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars-from-file .env.local

# Criar agendamento
gcloud scheduler jobs create http blabbermouth-scraper \
  --schedule "0 8,12,16,20 * * *" \
  --uri "https://blabbermouth-scraper-xxx.run.app/run" \
  --http-method GET \
  --region us-central1
```

## ⏰ **Exemplo de Agendamento**

```yaml
blabbermouth:    "0 8,12,16,20 * * *"   # 4x por dia
bravewords:      "0 9,13,17,21 * * *"   # 4x por dia
metalinjection:  "0 10,14,18,22 * * *"   # 4x por dia
loudwire:        "0 11,15,19,23 * * *"   # 4x por dia
metaltalk:       "0 7,13,19 * * *"      # 3x por dia
metalsucks:      "0 8,14,20 * * *"      # 3x por dia
```

## 📦 **Criar Novo Scraper**

1. Copie o diretório `services/blabbermouth` como template
2. Atualize `scraper.py` com a lógica específica do site
3. Ajuste `main.py` se necessário
4. Deploy e configure agendamento

## 🔧 **Variáveis de Ambiente**

Veja `.env.example` para todas as variáveis necessárias.

