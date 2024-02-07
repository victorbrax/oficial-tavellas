from flask import jsonify, render_template, request
from flask_login import login_required

from app.controllers.bike.home.f_bike import BikeForms
from app.controllers.auth.accounts.utils.protector import role_required
from app.models.bike.home.m_bike import Bike
from app.models.cliente.home.m_cliente import Cliente

from . import bp


@bp.route("dono/<id_cliente>")
@login_required
@role_required(["admin"])
def whose_bike(id_cliente: int=0):
    
    bikes = Bike.query.filter_by(cliente_id=id_cliente).all()

    bikesArray = []

    for bike in bikes:
        bikeObj = {}
        bikeObj["id"] = bike.id
        bikeObj["descricao"] = bike.descricao
        bikesArray.append(bikeObj)

    return jsonify({"bikes": bikesArray})