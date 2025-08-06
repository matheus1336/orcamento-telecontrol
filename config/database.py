import oracledb
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseConfig:
    def __init__(self):
        self.username = os.getenv('matheus')
        self.password = os.getenv('J29#d+K7')
        self.dsn = os.getenv('s14dbs:1521/orcl')  # host:port/service_name
        
    def get_connection(self):
        try:
            connection = oracledb.connect(
                user=self.username,
                password=self.password,
                dsn=self.dsn,
                encoding="UTF-8"
            )
            return connection
        except oracledb.Error as error:
            print(f"Erro na conexão: {error}")
            return None
    
    def execute_query(self, query, params=None):
        connection = self.get_connection()
        if not connection:
            return None
        
        try:
            cursor = connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            
            result = []
            for row in rows:
                result.append(dict(zip(columns, row)))
            
            return result
        except oracledb.Error as error:
            print(f"Erro na consulta: {error}")
            return None
        finally:
            cursor.close()
            connection.close()