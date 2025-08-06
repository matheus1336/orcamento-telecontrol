from config.database import DatabaseConfig

class Produto:
    def __init__(self):
        self.db = DatabaseConfig()
    
    def buscar_produtos(self, termo_busca="", estado="", limit=50):
        """Busca produtos no banco Oracle com filtros"""
        query = """
        SELECT 
            p.codigo_produto,
            p.descricao,
            p.preco_base,
            p.unidade,
            t.st_percentage,
            t.ipi_percentage,
            t.icms_percentage,
            t.pis_percentage,
            t.cofins_percentage,
            p.ativo
        FROM produtos p
        LEFT JOIN tributacao t ON p.codigo_produto = t.codigo_produto 
                                AND t.estado = :estado
        WHERE p.ativo = 'S'
        """
        
        params = {'estado': estado}
        
        if termo_busca:
            query += " AND (UPPER(p.codigo_produto) LIKE :termo OR UPPER(p.descricao) LIKE :termo)"
            params['termo'] = f"%{termo_busca.upper()}%"
        
        query += " ORDER BY p.descricao FETCH FIRST :limit ROWS ONLY"
        params['limit'] = limit
        
        return self.db.execute_query(query, params)
    
    def obter_produto_por_codigo(self, codigo, estado):
        """Obtém produto específico com tributação do estado"""
        query = """
        SELECT 
            p.codigo_produto,
            p.descricao,
            p.preco_base,
            p.unidade,
            COALESCE(t.st_percentage, 0) as st_percentage,
            COALESCE(t.ipi_percentage, 0) as ipi_percentage,
            COALESCE(t.icms_percentage, 0) as icms_percentage,
            COALESCE(t.pis_percentage, 0) as pis_percentage,
            COALESCE(t.cofins_percentage, 0) as cofins_percentage
        FROM produtos p
        LEFT JOIN tributacao t ON p.codigo_produto = t.codigo_produto 
                                AND t.estado = :estado
        WHERE p.codigo_produto = :codigo
        AND p.ativo = 'S'
        """
        
        result = self.db.execute_query(query, {
            'codigo': codigo,
            'estado': estado
        })
        
        return result[0] if result else None
    
    def calcular_preco_com_tributos(self, preco_base, tributos):
        """Calcula preço com todos os tributos"""
        st = preco_base * (tributos.get('st_percentage', 0) / 100)
        ipi = preco_base * (tributos.get('ipi_percentage', 0) / 100)
        icms = preco_base * (tributos.get('icms_percentage', 0) / 100)
        pis = preco_base * (tributos.get('pis_percentage', 0) / 100)
        cofins = preco_base * (tributos.get('cofins_percentage', 0) / 100)
        
        total_tributos = st + ipi + icms + pis + cofins
        preco_com_tributos = preco_base + total_tributos
        
        return {
            'preco_base': preco_base,
            'st': st,
            'ipi': ipi,
            'icms': icms,
            'pis': pis,
            'cofins': cofins,
            'total_tributos': total_tributos,
            'preco_com_tributos': preco_com_tributos
        }