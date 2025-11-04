FROM python:3.11-slim

WORKDIR /app

# Copia código compartilhado primeiro
COPY shared /app/shared

# Copia código do serviço
COPY . /app/services/blabbermouth

# Instala dependências
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Define o diretório de trabalho para o serviço
WORKDIR /app/services/blabbermouth

# Expõe porta
EXPOSE 8080

# Comando de execução
CMD ["python", "main.py"]
