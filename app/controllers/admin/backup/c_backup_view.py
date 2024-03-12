from flask import render_template, request, jsonify

from flask import render_template
from flask_login import login_required

from app.controllers.auth.accounts.utils.protector import role_required


from .backup_functions import get_backups_info, create_backup, restore_from_backup, delete_backup
from . import bp



@bp.route("/view")
@login_required
@role_required(["admin"])
def backup():
    return render_template("admin/backup/v_backup_view.html")

@bp.route('/data_backup', methods=["GET", "POST"])
# @login_required
# @role_required(["admin"])

def data_backup():
    
    backups = get_backups_info()

    return {'data': backups}


@bp.route('/render_backup', methods=["GET", "POST"])
@login_required
@role_required(["admin"])
def render_backup(): # Renderização
    method = request.args.get('method')
    value = request.args.get('value')
    modal_data = {}

    match method:
        case "POST":
            modal_data["title"] = "Novo Backup"
            modal_data["body"] = "Você tem certeza de que deseja criar um novo checkpoint de backup?"
 
            return render_template('admin/backup/mr_backup_view.html', method=method, modal_data=modal_data)

        case "DELETE":
            modal_data["title"] = "Cuidado!"
            modal_data["body"] = f"Você tem certeza de que quer apagar o backup: {value}?"
            return render_template('admin/backup/mr_backup_view.html', method=method, value=value, modal_data=modal_data)
        
        case _:
            return render_template('admin/backup/mr_backup_view.html', method=None, modal_data=modal_data)
       

@bp.route('/logic_backup', methods=["GET", "POST"])
# @login_required
# @role_required(["admin"])
def logic_backup(): # Regra de Negócio
    method = request.args.get('method')
    value = request.args.get('value')

    match method:
        case "POST":
            create_backup()
            return jsonify(success=True, message="cliente criada com sucesso.")
        
        case "DELETE":
            delete_backup(value)
            return jsonify(success=True, message="cliente deletado com sucesso.")

        case "XPTO":
            restore_from_backup(value)
            return jsonify(success=True, message="cliente revisada com sucesso.")

    return jsonify(success=False, error="Chamada sem condicional.")        