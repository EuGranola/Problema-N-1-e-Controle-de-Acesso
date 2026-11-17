from flask import Flask
from .controllers import auth_bp, main_bp

app = Flask(__name__, template_folder='views')

app.secret_key = 'shield_chave_secreta_nivel_omega_ifsp'

app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)