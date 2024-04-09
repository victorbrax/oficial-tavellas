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
        
        case _:
            return render_template('cliente/home/mr_cliente_view.html', method=None, modal_data=modal_data)
        

@bp.route('/logic_cliente', methods=["GET", "POST"])
@login_required
@role_required(["admin"])
def logic_cliente(): # Regra de Negócio
    method = request.args.get('method')
    value = request.args.get('value')
    json = request.get_json()

    nome = json.get('nomeCliente')
    celular = json.get('celularCliente')
    telefone = json.get('telefoneCliente')
    cep = json.get('cepCliente')
    logradouro = json.get('logradouroCliente')
    estado = json.get('estadoCliente')
    cidade = json.get('cidadeCliente')
    bairro = json.get('bairroCliente')
    numero = json.get('numeroCliente')
    complemento = json.get('complementoCliente')

    match method:
        case "POST":
            cliente = Cliente(nome=nome, celular=celular, telefone=telefone, email=nome, cep=cep, rua=logradouro, bairro=bairro, numero=numero, complemento=complemento, estado=estado, cidade=cidade)
            cliente.save()
            return jsonify(success=True, message="cliente criada com sucesso.")
        
        case "PUT":
            cliente = Cliente.query.get(value)
            cliente.nome = nome
            cliente.celular = celular
            cliente.telefone = telefone
            cliente.cep = cep
            cliente.rua = logradouro
            cliente.bairro = bairro
            cliente.numero = numero
            cliente.complemento = complemento
            cliente.estado = estado
            cliente.cidade = cidade
            cliente.edit()
            return jsonify(success=True, message="cliente editada com sucesso.")
        
        case "DELETE":
            cliente = Cliente.query.get(value)
            cliente.delete()
            return jsonify(success=True, message="cliente deletado com sucesso.")

        # case "XPTO":
        #     cliente = Cliente.query.get(value)
        #     cliente.nome = cliente.nome.swapcase()
        #     cliente.edit()
        #     return jsonify(success=True, message="cliente revisada com sucesso.")

    return jsonify(success=False, error="Chamada sem condicional.")        