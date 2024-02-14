from flask import jsonify, render_template, request
from flask_login import login_required

from app.controllers.reparo.home.f_reparo import ReparoForms
from app.controllers.auth.accounts.utils.protector import role_required
from app.models.reparo.home.m_reparo import Reparo

from . import bp


@bp.route("/view")
@login_required
@role_required(["admin"])
def reparo():
    return render_template("reparo/home/v_reparo_view.html")

@bp.route('/data_reparo')
@login_required
@role_required(["admin"])
def data_reparo():
    return {'data': [reparo.to_dict() for reparo in Reparo.query], 'is_createble': Reparo.is_createble()}

@bp.route('/render_reparo', methods=["GET", "POST"])
@login_required
@role_required(["admin"])
def render_reparo(): # Renderização
    method = request.args.get('method')
    value = request.args.get('value')
    modal_data = {}

    match method:
        case "POST":
            modal_data["title"] = "Novo Registro"
            modal_data["body"] = "Preencha o formulário abaixo."
 
            forms = ReparoForms()
            return render_template('reparo/home/mr_reparo_view.html', method=method, forms=forms, modal_data=modal_data)

        case "PUT":
            modal_data["title"] = "Formulário de Edição"
            modal_data["body"] = "Preencha o formulário abaixo."
        
            reparo = Reparo.query.get(value)
            forms = ReparoForms(obj=reparo)
            return render_template('reparo/home/mr_reparo_view.html', method=method, value=value, forms=forms, modal_data=modal_data)

        case "DELETE":
            modal_data["title"] = "Cuidado!"
            modal_data["body"] = f"Você tem certeza de que quer apagar o registro de valor: {value}?"
            return render_template('reparo/home/mr_reparo_view.html', method=method, value=value, modal_data=modal_data)
        
        case _:
            return render_template('reparo/home/mr_reparo_view.html', method=None, modal_data=modal_data)
        

@bp.route('/logic_reparo', methods=["GET", "POST"])
@login_required
@role_required(["admin"])
def logic_reparo(): # Regra de Negócio
    method = request.args.get('method')
    value = request.args.get('value')

    forms = ReparoForms()

    match method:
        case "POST":
            print("chegou no post")
            if forms.validate_on_submit():
                reparo = Reparo(
                    nome = forms.nome.data,
                    preco = forms.preco.data,
                    qtd_horas = forms.qtd_horas.data,
                    )
                reparo.save()
                return jsonify(success=True, message="Reparo criado com sucesso.")
            else:
                print(forms.errors)
        
        case "PUT":
            reparo = Reparo.query.get(value)
            if forms.validate_on_submit():
                reparo.nome = forms.nome.data
                reparo.preco = forms.preco.data
                reparo.qtd_horas = forms.qtd_horas.data
                reparo.edit()
                return jsonify(success=True, message="Reparo editado com sucesso.")
            else:
                print(forms.errors)
        
        case "DELETE":
            reparo = Reparo.query.get(value)
            reparo.delete()
            return jsonify(success=True, message="Reparo deletado com sucesso.")

    return jsonify(success=False, error="Chamada sem condicional.")        