from flask import jsonify, render_template, request
from flask_login import login_required

from app.controllers.admin.exemplares.f_uzuario import UzuarioForms
from app.controllers.auth.accounts.utils.protector import role_required
from app.models.admin.exemplares.m_uzuario import Uzuario

from . import bp


@bp.route("/uzuario")
@login_required
@role_required(["admin"])
def uzuario():
    return render_template("admin/exemplares/v_example_uzuario.html")

@bp.route('/data_uzuario')
@login_required
@role_required(["admin"])
def data_uzuario():
    return {'data': [user.to_dict() for user in Uzuario.query], 'is_createble': Uzuario.is_createble()}


@bp.route('/render_uzuario', methods=["GET", "POST"])
@login_required
@role_required(["admin"])
def render_uzuario(): # Renderização
    method = request.args.get('method')
    value = request.args.get('value')
    modal_data = {}

    match method:
        case "POST": # modalChoiceButton = POST
            modal_data["title"] = "Novo Registro"
            modal_data["body"] = "Preencha o formulário abaixo."
 
            forms = UzuarioForms()
            return render_template('admin/exemplares/mr_example_uzuario.html', method=method, forms=forms, modal_data=modal_data)

        case "PUT": # modalChoiceButton = PUT
            modal_data["title"] = "Formulário de Edição"
            modal_data["body"] = "Preencha o formulário abaixo."
            
            user = Uzuario.query.get(value)
            forms = UzuarioForms(obj=user)
            return render_template('admin/exemplares/mr_example_uzuario.html', method=method, value=value, forms=forms, modal_data=modal_data)

        case "DELETE": # modalChoiceButton = DELETE
            modal_data["title"] = "Cuidado!"
            modal_data["body"] = f"Você tem certeza de que quer apagar o registro de valor: {value}?"
            return render_template('admin/exemplares/mr_example_uzuario.html', method=method, value=value, modal_data=modal_data)
        
        case _:
            return render_template('admin/exemplares/mr_example_uzuario.html', method=None, modal_data=modal_data)
        

@bp.route('/logic_uzuario', methods=["GET", "POST"])
@login_required
@role_required(["admin"])
def logic_uzuario(): # Regra de Negócio
    method = request.args.get('method')
    value = request.args.get('value')

    forms = UzuarioForms()

    match method:
        case "POST": # ModalSubmitAPI = POST
            if forms.validate_on_submit():
                user = Uzuario(
                    name = forms.name.data,
                    email = forms.email.data,
                    age = forms.age.data,
                    address = forms.address.data,
                    phone = forms.phone.data
                    )
                user.save()
                return jsonify(success=True, message="Usuário criado com sucesso.")
            else:
                print(forms.errors)
        
        case "PUT": # ModalSubmitAPI = PUT
            user = Uzuario.query.get(value)
            if forms.validate_on_submit():
                user.name = forms.name.data
                user.email = forms.email.data
                user.age = forms.age.data
                user.address = forms.address.data
                user.phone = forms.phone.data
                user.edit()
                return jsonify(success=True, message="Usuário editado com sucesso.")
            else:
                print(forms.errors)
        
        case "DELETE": # ModalSubmitAPI = DELETE
            user = Uzuario.query.get(value)
            user.delete()
            return jsonify(success=True, message="Usuário deletado com sucesso.")

        case "XPTO": # WithoutModalSubmitAPI = XPTO
            user = Uzuario.query.get(value)
            user.name = user.name.swapcase()
            user.edit()
            return jsonify(success=True, message="Usuário revisado com sucesso.")

    return jsonify(success=False, error="Chamada sem condicional.")        