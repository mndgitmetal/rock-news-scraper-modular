#!/bin/bash
# Script para executar o servidor Blabbermouth e ver os logs

cd "$(dirname "$0")"

# Ativa o ambiente virtual
source venv/bin/activate

# Vai para o diretório do serviço
cd services/blabbermouth

# Mata qualquer processo na porta 8080
lsof -ti:8080 | xargs kill -9 2>/dev/null || true

echo "🚀 Iniciando servidor Blabbermouth Scraper..."
echo "📝 Logs serão exibidos abaixo:"
echo "🌐 Servidor estará disponível em: http://localhost:8080"
echo "📋 Endpoints disponíveis:"
echo "   - GET http://localhost:8080/          (status)"
echo "   - GET http://localhost:8080/health     (health check)"
echo "   - GET http://localhost:8080/run        (executar scraper)"
echo ""
echo "Pressione CTRL+C para parar o servidor"
echo "=========================================="
echo ""

# Executa o servidor (os logs aparecerão no terminal)
python main.py

