#!/bin/bash
# Script para deploy e configuração de agendamento de todos os serviços

PROJECT_ID="first-fuze-448812-f6"
REGION="us-central1"

SERVICES=(
    "blabbermouth:0 8,12,16,20 * * *"
    "bravewords:0 9,13,17,21 * * *"
    "metalinjection:0 10,14,18,22 * * *"
    "loudwire:0 11,15,19,23 * * *"
    "metaltalk:0 7,13,19 * * *"
    "metalsucks:0 8,14,20 * * *"
)

for service_config in "${SERVICES[@]}"; do
    IFS=':' read -r service_name schedule <<< "$service_config"
    
    echo "🚀 Deployando $service_name..."
    
    # Deploy no Cloud Run
    gcloud run deploy "${service_name}-scraper" \
        --source "services/${service_name}" \
        --region "$REGION" \
        --project "$PROJECT_ID" \
        --allow-unauthenticated \
        --memory 512Mi \
        --timeout 540s \
        --max-instances 1
    
    # Obtém URL do serviço
    SERVICE_URL=$(gcloud run services describe "${service_name}-scraper" \
        --region "$REGION" \
        --project "$PROJECT_ID" \
        --format "value(status.url)")
    
    echo "📅 Criando agendamento para $service_name..."
    
    # Cria ou atualiza job do Scheduler
    gcloud scheduler jobs create http "${service_name}-scraper" \
        --schedule "$schedule" \
        --uri "${SERVICE_URL}/run" \
        --http-method GET \
        --region "$REGION" \
        --project "$PROJECT_ID" \
        --time-zone "America/Sao_Paulo" \
        --description "Scraper automático para ${service_name}" \
        || gcloud scheduler jobs update http "${service_name}-scraper" \
            --schedule "$schedule" \
            --uri "${SERVICE_URL}/run" \
            --region "$REGION" \
            --project "$PROJECT_ID"
    
    echo "✅ $service_name configurado: $SERVICE_URL"
    echo ""
done

echo "🎉 Todos os serviços foram deployados e agendados!"

