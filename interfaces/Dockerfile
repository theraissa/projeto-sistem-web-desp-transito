# Usa uma imagem base super leve com Nginx
FROM nginx:alpine

# Copia seus arquivos do projeto (HTML, CSS, JS) para a pasta pública do Nginx
COPY . /usr/share/nginx/html

# Expõe a porta 80 (do Nginx)
EXPOSE 80

# Comando padrão do Nginx para rodar em foreground (necessário em Docker)
CMD ["nginx", "-g", "daemon off;"]
