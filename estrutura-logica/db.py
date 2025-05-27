import os
import psycopg2
from urllib.parse import urlparse

def get_connection():
    """
    Retorna uma conexão ativa com o banco de dados PostgreSQL.
    Usa a variável de ambiente DATABASE_URL, se existir.
    Caso contrário, usa valores padrão para desenvolvimento local.
    """
    
    database_url = os.environ.get('DATABASE_URL')

    if not database_url:
        print("DATABASE_URL environment variable not set!")
        print("WARNING: Using hardcoded connection for development outside Docker.")
        
        try:
            return psycopg2.connect(
                dbname="sistema_desp",
                user="raissa",
                password="Lima042!",
                host="localhost",
                port="5432"
            )
        except psycopg2.Error as e:
            print(f"Erro na conexão local: {e}")
            raise

    try:
        url = urlparse(database_url)
        print(f"Connecting to DB via URL: {database_url}")
        return psycopg2.connect(
            dbname=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
    except psycopg2.Error as e:
        print(f"Erro na conexão com URL: {e}")
        raise