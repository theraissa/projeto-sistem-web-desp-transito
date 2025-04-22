# Usa uma imagem base super leve com Nginx
FROM nginx:alpine

# Instala o git dentro do container
RUN apk update && apk add git

# Clona o repositório
RUN git clone https://github.com/theraissa/projeto-sistem-web-desp-transito.git

# Copia seus arquivos do projeto (HTML, CSS, JS) para a pasta pública do Nginx
COPY . /usr/share/nginx/html

# Expõe a porta 80 (do Nginx)
EXPOSE 80