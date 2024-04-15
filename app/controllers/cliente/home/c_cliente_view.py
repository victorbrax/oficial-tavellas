from flask import jsonify, render_template, request
from flask_login import login_required

from app.controllers.cliente.home.f_cliente import ClienteForms
from app.controllers.auth.accounts.utils.protector import role_required
from app.models.cliente.home.m_cliente import Cliente

from . import bp


@bp.route("/view")
@login_required
@role_required(["admin"])
def cliente():
    return render_template("cliente/home/v_cliente_view.html")

@bp.route('/data_cliente')
@login_required
@role_required(["admin"])
def data_cliente():
    return {'data': [cliente.to_dict() for cliente in Cliente.query], 'is_createble': Cliente.is_createble()}

@bp.route('/render_cliente', methods=["GET", "POST"])
@login_required
@role_required(["admin"])
def render_cliente(): # Renderização
    method = request.args.get('method')
    value = request.args.get('value')
    modal_data = {}

    match method:
        case "POST":
            modal_data["title"] = "Novo Registro"
            modal_data["body"] = "Preencha o formulário abaixo."
 
            forms = ClienteForms()
            return render_template('cliente/home/mr_cliente_view.html', method=method, forms=forms, modal_data=modal_data)

        case "PUT":
            modal_data["title"] = "Formulário de Edição"
            modal_data["body"] = "Preencha o formulário abaixo."
        
            cliente = Cliente.query.get(value)
            forms = ClienteForms(obj=cliente)
            return render_template('cliente/home/mr_cliente_view.html', method=method, value=value, forms=forms, modal_data=modal_data)

        case "DELETE":
            modal_data["title"] = "Cuidado!"
            modal_data["body"] = f"Você tem certeza de que quer apagar o registro de valor: {value}?"
            return render_template('cliente/home/mr_cliente_view.html', method=method, value=value, modal_data=modal_data)
        
        case "DETAIL":
            cliente = Cliente.query.get(value)

            modal_data["title"] = "Dados do Cliente!"
            modal_data["nome"] = cliente.nome
            modal_data["data_adesao"] = cliente.data_criacao
            modal_data["cep"] = cliente.cep
            modal_data["rua"] = cliente.rua
            modal_data["numero"] = cliente.numero
            modal_data["bairro"] = cliente.bairro
            modal_data["telefone"] = cliente.telefone
            modal_data["estado"] = cliente.estado
            modal_data["cidade"] = cliente.cidade

            modal_data["celular"] = cliente.celular


            return render_template('cliente/home/mr_cliente_view.html', method=method, value=value, modal_data=modal_data)
        
        case _:
            return render_template('cliente/home/mr_cliente_view.html', method=None, modal_data=modal_data)
        

@bp.route('/logic_cliente', methods=["GET", "POST"])
@login_required
@role_required(["admin"])
def logic_cliente(): # Regra de Negócio
    method = request.args.get('method')
    value = request.args.get('value')

    forms = ClienteForms()

    match method:
        case "POST":
            if forms.validate_on_submit():
                cliente = Cliente(
                    nome = forms.nome.data,
                    celular = forms.celular.data,
                    email = forms.email.data,
                    telefone = forms.telefone.data,
                    cep = forms.cep.data,
                    rua = forms.rua.data,
                    bairro = forms.bairro.data,
                    numero = forms.numero.data,
                    cidade = forms.cidade.data,
                    estado = forms.estado.data
                    )
                cliente.save()
                return jsonify(success=True, message="cliente criada com sucesso.")
            else:
                print(forms.errors)
        
        case "PUT":
            cliente = Cliente.query.get(value)
            if forms.validate_on_submit():
                cliente.nome = forms.nome.data
                cliente.celular = forms.celular.data
                cliente.email = forms.email.data
                cliente.telefone = forms.telefone.data
                cliente.cep = forms.cep.data
                cliente.rua = forms.rua.data
                cliente.bairro = forms.bairro.data
                cliente.numero = forms.numero.data
                cliente.cidade = forms.cidade.data
                cliente.estado = forms.estado.data
                cliente.edit()
                return jsonify(success=True, message="cliente editada com sucesso.")
            else:
                print(forms.errors)
        
        case "DELETE":
            cliente = Cliente.query.get(value)
            cliente.delete()
            return jsonify(success=True, message="cliente deletado com sucesso.")

        case "XPTO":
            cliente = Cliente.query.get(value)
            cliente.nome = cliente.nome.swapcase()
            cliente.edit()
            return jsonify(success=True, message="cliente revisada com sucesso.")

    return jsonify(success=False, error="Chamada sem condicional.")        