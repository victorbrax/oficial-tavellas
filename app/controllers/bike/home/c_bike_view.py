from config import REPORT_PATH
import io
import uuid
import os
import pandas as pd
from app.models.bike.home.m_bike import Bike
from flask import jsonify, render_template, request, send_file
from flask_login import login_required

from app.controllers.bike.home.f_bike import BikeForms
from app.controllers.auth.accounts.utils.protector import role_required
from app.models.bike.home.m_bike import Bike
# from app.models.cliente.home.m_cliente import Cliente

from . import bp

@bp.route("/view")
@login_required
@role_required(["admin"])
def bike():
    return render_template("bike/home/v_bike_view.html")

@bp.route('/data_bike')
@login_required
@role_required(["admin"])
def data_bike():
    return {'data': [bike.to_dict() for bike in Bike.query], 'is_createble': Bike.is_createble()}

@bp.route('/render_bike', methods=["GET", "POST"])
@login_required
@role_required(["admin"])
def render_bike(): # Renderização
    method = request.args.get('method')
    value = request.args.get('value')
    modal_data = {}

    match method:
        case "POST":
            modal_data["title"] = "Novo Registro"
            modal_data["body"] = "Preencha o formulário abaixo."
 
            forms = BikeForms()
            return render_template('bike/home/mr_bike_view.html', method=method, forms=forms, modal_data=modal_data)

        case "PUT":
            modal_data["title"] = "Formulário de Edição"
            modal_data["body"] = "Preencha o formulário abaixo."
        
            bike = Bike.query.get(value)
            forms = BikeForms(obj=bike)
            return render_template('bike/home/mr_bike_view.html', method=method, value=value, forms=forms, modal_data=modal_data)

        case "DELETE":
            modal_data["title"] = "Cuidado!"
            modal_data["body"] = f"Você tem certeza de que quer apagar o registro de valor: {value}?"
            return render_template('bike/home/mr_bike_view.html', method=method, value=value, modal_data=modal_data)
        
        case _:
            return render_template('bike/home/mr_bike_view.html', method=None, modal_data=modal_data)
        

@bp.route('/logic_bike', methods=["GET", "POST"])
@login_required
@role_required(["admin"])
def logic_bike(): # Regra de Negócio
    method = request.args.get('method')
    value = request.args.get('value')

    forms = BikeForms()

    match method:
        case "POST":
            if forms.validate_on_submit():
                bike = Bike(
                    descricao = forms.descricao.data,
                    modelo = forms.modelo.data,
                    condicao = forms.condicao.data,
                    aro = forms.aro.data,
                    quadro = forms.quadro.data,
                    cor = forms.cor.data,
                    cliente = forms.cliente.data
                    )
                bike.save()
                return jsonify(success=True, message="Bike criada com sucesso.")
            else:
                print(forms.errors)
        
        case "PUT":
            bike = Bike.query.get(value)
            if forms.validate_on_submit():
                bike.descricao = forms.descricao.data
                bike.modelo = forms.modelo.data
                bike.condicao = forms.condicao.data
                bike.aro = forms.aro.data
                bike.quadro = forms.quadro.data
                bike.cor = forms.cor.data
                bike.cliente = forms.cliente.data
                bike.edit()
                return jsonify(success=True, message="Bike editada com sucesso.")
            else:
                print(forms.errors)
        
        case "DELETE":
            bike = Bike.query.get(value)
            bike.delete()
            return jsonify(success=True, message="Bike deletada com sucesso.")

        case "XPTO":
            bike = Bike.query.get(value)
            bike.descricao = bike.descricao.swapcase()
            bike.edit()
            return jsonify(success=True, message="Bike revisada com sucesso.")


        case "REPORT":
            bikes = Bike.query.all()
            data = [bike.to_export_reports() for bike in bikes]
            df = pd.DataFrame(data)

            filename = f"relatorio_bikes_{uuid.uuid4()}.xlsx"
            REPORT_CSV = os.path.join(REPORT_PATH, filename)
        
            df.to_excel(REPORT_CSV, index=False)

            file = io.BytesIO() # Cria um objeto de bytes vazio para armazenar o conteúdo do arquivo
            with open(REPORT_CSV, 'rb') as fo: # Abre o arquivo para leitura
                file.write(fo.read()) # Escreve o conteúdo no objeto de bytes vazio
            
            file.seek(0) # Posiciona o cursor no inicio do objeto de bytes vazio
            os.remove(REPORT_CSV)

            return send_file(file, mimetype='application/vnd.ms-excel', download_name=filename, as_attachment=True)


    return jsonify(success=False, error="Chamada sem condicional.")        