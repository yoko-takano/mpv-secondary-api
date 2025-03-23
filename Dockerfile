# Define a imagem base
FROM python:3.12

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos de requisitos
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código-fonte
COPY . .

# Define o comando padrão para produção (caso não use docker-compose)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
