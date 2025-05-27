# Usa a imagem base oficial do PostgreSQL
FROM postgres:13

# Copia o script de inicialização de tabelas para o diretório de entrypoint
# O caminho de origem 'tabelas-banco-dados.sql' é relativo ao CONTEXTO de build,
# que no seu docker-compose.yml está definido como ./banco-dados.
COPY tabelas-banco-dados.sql /docker-entrypoint-initdb.d/

