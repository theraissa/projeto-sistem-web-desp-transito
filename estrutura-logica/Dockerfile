# Use uma imagem base Python leve
FROM python:3.9-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo requirements.txt primeiro para aproveitar o cache do Docker
# O caminho é relativo ao CONTEXTO de build (que será a raiz do projeto)
COPY estrutura-logica/requirements.txt . 

# Instala as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação Flask e a pasta interfaces
# Os caminhos são relativos ao CONTEXTO de build (raiz do projeto)
COPY estrutura-logica/ /app/estrutura-logica/
COPY interfaces/ /app/interfaces/

# Define a variável de ambiente FLASK_APP (diz ao Flask onde encontrar o aplicativo)
ENV FLASK_APP=estrutura-logica/app.py

# Define Flask para rodar em modo de desenvolvimento (opcional, bom para depuração)
ENV FLASK_ENV=development

# Desabilita o cache de código (opcional, pode ajudar com hot-reloading em desenvolvimento)
ENV PYTHONUNBUFFERED=1

# Expõe a porta que a aplicação Flask roda (padrão 5000)
EXPOSE 5000

# Comando para rodar a aplicação Flask
# --host 0.0.0.0 torna o servidor acessível de fora do container
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]