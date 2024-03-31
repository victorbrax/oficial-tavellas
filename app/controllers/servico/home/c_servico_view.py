from flask import jsonify, render_template, request
from flask_login import login_required

from app.controllers.servico.home.f_servico import ServicoForms
from app.controllers.auth.accounts.utils.protector import role_required
from app.models.servico.home.m_servico import Servico

from . import bp


@bp.route("/view")
@login_required
@role_required(["admin"])
def servico():
    return render_template("servico/home/v_servico_view.html")

@bp.route('/data_servico')
@login_required
@role_required(["admin"])
def data_servico():
    return {'data': [servico.to_dict() for servico in Servico.query], 
            'is_createble': Servico.is_createble()}

@bp.route('/render_servico', methods=["GET", "POST"])
@login_required
@role_required(["admin"])
def render_servico(): # Renderização
    method = request.args.get('method')
    value = request.args.get('value')
    modal_data = {}

    match method:
        case "POST":
            modal_data["title"] = "Novo Registro"
            modal_data["body"] = "Preencha o formulário abaixo."
 
            forms = ServicoForms()
            return render_template('servico/home/mr_servico_view.html', method=method, forms=forms, modal_data=modal_data)

        case "PUT":
            modal_data["title"] = "Formulário de Edição"
            modal_data["body"] = "Preencha o formulário abaixo."
        
            servico = Servico.query.get(value)
            forms = ServicoForms(obj=servico)
            return render_template('servico/home/mr_servico_view.html', method=method, value=value, forms=forms, modal_data=modal_data)

        case "DELETE":
            modal_data["title"] = "Cuidado!"
            modal_data["body"] = f"Você tem certeza de que quer apagar o registro de valor: {value}?"
            return render_template('servico/home/mr_servico_view.html', method=method, value=value, modal_data=modal_data)
        
        case _:
            return render_template('servico/home/mr_servico_view.html', method=None, modal_data=modal_data)
        

@bp.route('/logic_servico', methods=["GET", "POST"])
@login_required
@role_required(["admin"])
def logic_servico(): # Regra de Negócio
    method = request.args.get('method')
    value = request.args.get('value')



    forms = ServicoForms()

    match method:
        case "POST":
            if forms.validate_on_submit():
                servico = Servico(
                    data_inicio = forms.data_inicio.data,
                    data_fim = forms.data_fim.data,
                    reparos = forms.reparos.data,
                    produtos = forms.produtos.data,
                    cliente = forms.cliente.data,
                    bike = forms.bike.data,
                    )
                
                servico.update_status() # Iniciar o primeiro Status
                servico.update_preco_total() # Somar os Preços dos Produtos e Reparos do Serviço
                servico.save()
                return jsonify(success=True, message="Servico criado com sucesso.")
            else:
                print(forms.errors)
        
        case "PUT":
            servico = Servico.query.get(value)
            if forms.validate_on_submit():
                servico.data_inicio = forms.data_inicio.data
                servico.data_fim = forms.data_fim.data
                servico.reparos = forms.reparos.data
                servico.produtos = forms.produtos.data
                servico.cliente = forms.cliente.data
                servico.bike = forms.bike.data
                servico.update_preco_total()
                servico.edit()
                return jsonify(success=True, message="Serviço editado com sucesso.")
            else:
                print(forms.errors)
        
        case "DELETE":
            servico = Servico.query.get(value)
            servico.delete()
            return jsonify(success=True, message="Serviço deletado com sucesso.")

        case "XPTO":
            servico = Servico.query.get(value)
            servico.update_status()
            servico.edit()
            return jsonify(success=True, message="Serviço revisado com sucesso.")

    return jsonify(success=False, error="Chamada sem condicional.")        