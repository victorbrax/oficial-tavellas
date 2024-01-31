#!/usr/bin/env python
# -*-coding:utf-8 -*-

'''
@Arquivo :   c_consolidador_rateio.py
@Criacao :   2024/01/29 17:36:29
@Autor   :   Rafael dos Santos 
@Desc    :   Consolidar arquivos de rateio em um unico arquivo, somando os valores de acordo com o codigo de barras e loja
'''

import os
from uuid import uuid4

import pandas as pd
from flask import render_template, request, send_from_directory
from flask_login import login_required

from app.controllers.auth.accounts.utils.protector import role_required

from . import bp

RATEIO_CONSOLIDADO = os.path.join(os.getcwd(), "app", "public", "financeiro", "consolidador_rateio", "files", "xls")


@bp.route("/consolidar_rateio", methods=["GET", "POST"])
@login_required
@role_required(["financeiro", "user"])
def consolidar_excels():
    if request.method == "GET":
        return render_template("financeiro/consolidador_rateio/v_consolidador_rateio.html")
    
    files = request.files.getlist('files')
    if len(files) == 0:
        return render_template("financeiro/consolidador_rateio/v_consolidador_rateio.html")
    dfs = []
    for file in files:
        df = pd.read_excel(file)
        dfs.append(df)

    df = pd.concat(dfs, ignore_index=True)
    consolidado = df.drop_duplicates(subset=["Codigo Barras", "Loja"], ignore_index=False).copy()
    consolidado["Valor"] = consolidado.apply(lambda x: df.loc[(df["Codigo Barras"] == x["Codigo Barras"]) & 
                                                              (df["Loja"] == x["Loja"]), "Valor"].values.sum(), axis=1)

    file = f"{uuid4()}.xls"
    path = os.path.join(RATEIO_CONSOLIDADO, file)

    consolidado.to_excel(path, index=False, engine="openpyxl")

    url_download = f'consolidar_rateio/{file}'
    return render_template("financeiro/consolidador_rateio/v_consolidador_rateio.html", url_download=url_download)


@bp.route("/consolidar_rateio/<path:filename>", methods=["GET", "POST"])
@login_required
@role_required(["financeiro", "user"])
def download(filename):
    return send_from_directory(RATEIO_CONSOLIDADO, filename, as_attachment=True)