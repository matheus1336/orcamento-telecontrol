from config.database import DatabaseConfig

class Usuario:
    def __init__(self):
        self.db = DatabaseConfig()
    
    def autenticar(self, username, password):
        """Autentica usuário no sistema existente"""
        query = """
        SELECT 
            u.id_usuario,
            u.nome,
            u.username,
            u.estado,
            u.ativo,
            v.codigo_vendedor
        FROM usuarios u
        LEFT JOIN vendedores v ON u.id_usuario = v.id_usuario
        WHERE u.username = :username 
        AND u.password = :password
        AND u.ativo = 'S'
        """
        
        result = self.db.execute_query(query, {
            'username': username,
            'password': password  # Em produção, usar hash
        })
        
        return result[0] if result else None
    
    def obter_por_id(self, user_id):
        """Obtém dados do usuário por ID"""
        query = """
        SELECT 
            u.id_usuario,
            u.nome,
            u.username,
            u.estado,
            v.codigo_vendedor
        FROM usuarios u
        LEFT JOIN vendedores v ON u.id_usuario = v.id_usuario
        WHERE u.id_usuario = :user_id
        AND u.ativo = 'S'
        """
        
        result = self.db.execute_query(query, {'user_id': user_id})
        return result[0] if result else None