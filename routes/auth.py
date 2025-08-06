from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.usuario import Usuario

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        usuario_model = Usuario()
        usuario = usuario_model.autenticar(username, password)
        
        if usuario:
            session['user_id'] = usuario['ID_USUARIO']
            session['username'] = usuario['USERNAME']
            session['nome'] = usuario['NOME']
            session['estado'] = usuario['ESTADO']
            session['codigo_vendedor'] = usuario.get('CODIGO_VENDEDOR')
            
            return redirect(url_for('produtos.listar'))
        else:
            flash('Usuário ou senha incorretos!', 'error')
    
    return render_template('login.html')

@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

def login_required(f):
    """Decorator para rotas que requerem login"""
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function