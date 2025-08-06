from flask import Flask, session, redirect, url_for
import os
from dotenv import load_dotenv

# Importar blueprints
from routes.auth import auth
from routes.produtos import produtos  
from routes.orcamento import orcamento

# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'sua-chave-secreta-aqui')

# Registrar blueprints
app.register_blueprint(auth, url_prefix='/')
app.register_blueprint(produtos, url_prefix='/')
app.register_blueprint(orcamento, url_prefix='/')

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('produtos.listar'))
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)