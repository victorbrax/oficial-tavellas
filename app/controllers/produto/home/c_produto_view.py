from flask import jsonify, render_template, request
from flask_login import login_required

from app.controllers.produto.home.f_produto import ProdutoForms
from app.controllers.auth.accounts.utils.protector import role_required
from app.models.produto.home.m_produto import Produto

from . import bp


@bp.route("/view")
@login_required
@role_required(["admin"])
def produto():
    return render_template("produto/home/v_produto_view.html")

@bp.route('/data_produto')
@login_required
@role_required(["admin"])
def data_produto():
    return {'data': [produto.to_dict() for produto in Produto.query], 'is_createble': Produto.is_createble()}

@bp.route('/render_produto', methods=["GET", "POST"])
@login_required
@role_required(["admin"])
def render_produto(): # Renderização
    method = request.args.get('method')
    value = request.args.get('value')
    modal_data = {}

    match method:
        case "POST":
            modal_data["title"] = "Novo Registro"
            modal_data["body"] = "Preencha o formulário abaixo."
 
            forms = ProdutoForms()
            return render_template('produto/home/mr_produto_view.html', method=method, forms=forms, modal_data=modal_data)

        case "PUT":
            modal_data["title"] = "Formulário de Edição"
            modal_data["body"] = "Preencha o formulário abaixo."
        
            produto = Produto.query.get(value)
            forms = ProdutoForms(obj=produto)
            return render_template('produto/home/mr_produto_view.html', method=method, value=value, forms=forms, modal_data=modal_data)

        case "DELETE":
            modal_data["title"] = "Cuidado!"
            modal_data["body"] = f"Você tem certeza de que quer apagar o registro de valor: {value}?"
            return render_template('produto/home/mr_produto_view.html', method=method, value=value, modal_data=modal_data)
        
        case _:
            return render_template('produto/home/mr_produto_view.html', method=None, modal_data=modal_data)
        

@bp.route('/logic_produto', methods=["GET", "POST"])
@login_required
@role_required(["admin"])
def logic_produto(): # Regra de Negócio
    method = request.args.get('method')
    value = request.args.get('value')

    forms = ProdutoForms()

    match method:
        case "POST":
            if forms.validate_on_submit():
                produto = Produto(
                    nome = forms.nome.data,
                    preco = forms.preco.data,
                    marca = forms.marca.data,
                    local = forms.local.data,
                    )
                produto.save()
                return jsonify(success=True, message="Produto criado com sucesso.")
            else:
                print(forms.errors)
        
        case "PUT":
            produto = Produto.query.get(value)
            if forms.validate_on_submit():
                produto.nome = forms.nome.data
                produto.preco = forms.preco.data
                produto.marca = forms.marca.data
                produto.local = forms.local.data
                produto.edit()
                return jsonify(success=True, message="Produto editado com sucesso.")
            else:
                print(forms.errors)
        
        case "DELETE":
            produto = Produto.query.get(value)
            produto.delete()
            return jsonify(success=True, message="Produto deletado com sucesso.")

    return jsonify(success=False, error="Chamada sem condicional.")        