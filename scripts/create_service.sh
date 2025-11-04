#!/bin/bash
# Script para criar um novo serviço baseado no template do Blabbermouth

if [ -z "$1" ]; then
    echo "❌ Uso: ./create_service.sh <nome-do-servico>"
    echo "Exemplo: ./create_service.sh bravewords"
    exit 1
fi

SERVICE_NAME="$1"
TEMPLATE_DIR="services/blabbermouth"
NEW_DIR="services/${SERVICE_NAME}"

if [ -d "$NEW_DIR" ]; then
    echo "❌ Serviço $SERVICE_NAME já existe!"
    exit 1
fi

echo "📦 Criando serviço $SERVICE_NAME..."

# Copia template
cp -r "$TEMPLATE_DIR" "$NEW_DIR"

# Atualiza referências no código
sed -i '' "s/BlabbermouthScraper/${SERVICE_NAME^}Scraper/g" "$NEW_DIR/scraper.py"
sed -i '' "s/blabbermouth/${SERVICE_NAME}/g" "$NEW_DIR/main.py"
sed -i '' "s/Blabbermouth/${SERVICE_NAME^}/g" "$NEW_DIR/main.py"

echo "✅ Serviço $SERVICE_NAME criado em $NEW_DIR"
echo "📝 Edite $NEW_DIR/scraper.py para ajustar a lógica de scraping"

