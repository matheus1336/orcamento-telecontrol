from flask import Blueprint, render_template, request, jsonify, session
from models.produto import Produto
from routes.auth import login_required
import json

orcamento = Blueprint('orcamento', __name__)

@orcamento.route('/orcamento')
@login_required
def criar():
    return render_template('orcamento.html')

@orcamento.route('/api/orcamento/calcular', methods=['POST'])
@login_required
def calcular_orcamento():
    data = request.get_json()
    produtos_selecionados = data.get('produtos', [])
    estado = session.get('estado', '')
    
    produto_model = Produto()
    orcamento_calculado = []
    
    total_geral = 0
    total_tributos_geral = 0
    total_frete_geral = 0
    total_markup_geral = 0
    
    for item in produtos_selecionados:
        codigo = item['codigo']
        quantidade = float(item['quantidade'])
        percentual_frete = float(item.get('frete', 0))
        percentual_markup = float(item.get('markup', 0))
        
        produto = produto_model.obter_produto_por_codigo(codigo, estado)
        
        if produto:
            # Calcular preço com tributos
            calculo_tributos = produto_model.calcular_preco_com_tributos(
                produto['PRECO_BASE'], produto
            )
            
            # Calcular valores por quantidade
            preco_base_total = calculo_tributos['preco_base'] * quantidade
            tributos_total = calculo_tributos['total_tributos'] * quantidade
            preco_com_tributos_total = calculo_tributos['preco_com_tributos'] * quantidade
            
            # Calcular frete e markup
            valor_frete = preco_com_tributos_total * (percentual_frete / 100)
            valor_markup = preco_com_tributos_total * (percentual_markup / 100)
            
            # Preço final
            preco_final_total = preco_com_tributos_total + valor_frete + valor_markup
            
            item_orcamento = {
                'codigo': produto['CODIGO_PRODUTO'],
                'descricao': produto['DESCRICAO'],
                'quantidade': quantidade,
                'unidade': produto['UNIDADE'],
                'preco_base_unitario': produto['PRECO_BASE'],
                'preco_base_total': preco_base_total,
                'tributos': {
                    'st': calculo_tributos['st'] * quantidade,
                    'ipi': calculo_tributos['ipi'] * quantidade,
                    'icms': calculo_tributos['icms'] * quantidade,
                    'pis': calculo_tributos['pis'] * quantidade,
                    'cofins': calculo_tributos['cofins'] * quantidade,
                    'total': tributos_total
                },
                'percentual_frete': percentual_frete,
                'valor_frete': valor_frete,
                'percentual_markup': percentual_markup,
                'valor_markup': valor_markup,
                'preco_final_total': preco_final_total
            }
            
            orcamento_calculado.append(item_orcamento)
            
            # Somar totais gerais
            total_geral += preco_final_total
            total_tributos_geral += tributos_total
            total_frete_geral += valor_frete
            total_markup_geral += valor_markup
    
    resumo = {
        'itens': orcamento_calculado,
        'totais': {
            'subtotal_produtos': total_geral - total_frete_geral - total_markup_geral,
            'total_tributos': total_tributos_geral,
            'total_frete': total_frete_geral,
            'total_markup': total_markup_geral,
            'total_geral': total_geral
        },
        'vendedor': {
            'nome': session.get('nome'),
            'codigo': session.get('codigo_vendedor'),
            'estado': session.get('estado')
        }
    }
    
    return jsonify(resumo)

@orcamento.route('/orcamento/resultado')
@login_required
def resultado():
    return render_template('resultado.html')