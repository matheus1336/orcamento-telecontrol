from flask import Blueprint, render_template, request, jsonify, session
from models.produto import Produto
from routes.auth import login_required

produtos = Blueprint('produtos', __name__)

@produtos.route('/produtos')
@login_required
def listar():
    return render_template('produtos.html')

@produtos.route('/api/produtos/buscar')
@login_required
def buscar_produtos():
    termo = request.args.get('termo', '')
    estado = session.get('estado', '')
    
    produto_model = Produto()
    produtos = produto_model.buscar_produtos(termo, estado)
    
    return jsonify(produtos)

@produtos.route('/api/produtos/<codigo>')
@login_required
def obter_produto(codigo):
    estado = session.get('estado', '')
    
    produto_model = Produto()
    produto = produto_model.obter_produto_por_codigo(codigo, estado)
    
    if produto:
        return jsonify(produto)
    else:
        return jsonify({'error': 'Produto não encontrado'}), 404