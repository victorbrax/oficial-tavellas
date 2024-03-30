import calendar
import locale
from datetime import datetime

from flask import render_template
from flask_login import login_required

from app.models.bike.home.m_bike import Bike
from app.models.cliente.home.m_cliente import Cliente
from app.models.produto.home.m_produto import Produto
from app.models.servico.home.m_servico import Servico
from database import db

from . import bp

locale.setlocale(locale.LC_TIME, 'pt_BR')

@bp.route("/")
@login_required
def home():

    mes_atual = datetime.now().month
    nome_mes = calendar.month_name[mes_atual].capitalize()

    clientes_registrados = db.session.query(Cliente).count()
    clientes_do_mes = db.session.query(Cliente).filter(db.func.extract('month', Cliente.data_criacao) == mes_atual).count()
    bikes_registradas = db.session.query(Bike).count()
    bikes_do_mes = db.session.query(Bike).filter(db.func.extract('month', Bike.data_criacao) == mes_atual).count()
    produtos_registrados = db.session.query(Produto).count()
    servicos_registrados = db.session.query(Servico).count()
    servicos_pendentes = db.session.query(Servico).filter(Servico.status == 'Em Andamento').count()

    print(nome_mes)

    home_data = {
        "nome_mes": nome_mes,
        "servicos_registrados": servicos_registrados,
        "servicos_pendentes": servicos_pendentes,
        "clientes_registrados": clientes_registrados,
        "clientes_do_mes": clientes_do_mes,
        "bikes_registradas": bikes_registradas,
        "bikes_do_mes": bikes_do_mes,
        "produtos_registrados": produtos_registrados
    }

    return render_template("home/inicio/v_index.html", home_data=home_data)