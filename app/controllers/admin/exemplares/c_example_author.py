import os

from flask import jsonify, render_template, request
from flask_login import login_required

from app.controllers.admin.exemplares.f_author import AuthorForms
from app.controllers.auth.accounts.utils.protector import role_required
from app.models.admin.exemplares.m_author import Author
from app.models.admin.exemplares.m_author_books import authors_books
from app.models.admin.exemplares.m_book import Book
from config import STATIC_PATH
from database.utils import execute_query_from_file

from . import bp

ADMIN_FILES_PATH = os.path.join(STATIC_PATH, "admin", "exemplares", "files")
produtos_sql = os.path.join(ADMIN_FILES_PATH, "sql", "produtos.sql")

@bp.route("/consulta")
@login_required
@role_required(["admin"])
def consulta():
    x = execute_query_from_file(produtos_sql, parameters={'today': "CURRENT_DATE"})
    print(x)

    return "ok"


@bp.route("/author")
@login_required
@role_required(["admin"])
def author():
    return render_template("admin/exemplares/v_example_author.html")

@bp.route('/data_author')
@login_required
@role_required(["admin"])
def data_author():
    return {'data': [author.to_dict() for author in Author.query], 'is_createble': Author.is_createble()}


@bp.route('/render_author', methods=["GET", "POST"])
@login_required
@role_required(["admin"])
def render_author(): # Renderização
    method = request.args.get('method')
    value = request.args.get('value')
    modal_data = {}

    match method:
        case "POST":
            modal_data["title"] = "Novo Registro"
            modal_data["body"] = "Preencha o formulário abaixo."
 
            forms = AuthorForms()
            return render_template('admin/exemplares/mr_example_author.html', method=method, forms=forms, modal_data=modal_data)

        case "PUT":
            modal_data["title"] = "Formulário de Edição"
            modal_data["body"] = "Preencha o formulário abaixo."
            
            author = Author.query.get(value)
            forms = AuthorForms(obj=author)
            return render_template('admin/exemplares/mr_example_author.html', method=method, value=value, forms=forms, modal_data=modal_data)

        case "DELETE":
            modal_data["title"] = "Cuidado!"
            modal_data["body"] = f"Você tem certeza de que quer apagar o registro de valor: {value}?"
            return render_template('admin/exemplares/mr_example_author.html', method=method, value=value, modal_data=modal_data)
        
        case _:
            return render_template('admin/exemplares/mr_example_author.html', method=None, modal_data=modal_data)
        

@bp.route('/logic_author', methods=["GET", "POST"])
@login_required
@role_required(["admin"])
def logic_author(): # Regra de Negócio
    method = request.args.get('method')
    value = request.args.get('value')

    forms = AuthorForms()

    match method:
        case "POST":
            if forms.validate_on_submit():
                author = Author(
                    name = forms.name.data,
                    books = forms.books.data
                    )
                author.save()
                return jsonify(success=True, message="Autor criado com sucesso.")
            else:
                print(forms.errors)
        
        case "PUT":
            author = Author.query.get(value)
            if forms.validate_on_submit():
                author.name = forms.name.data
                author.books.clear()
                author.books.extend(forms.books.data)
                author.edit()
                return jsonify(success=True, message="Autor editado com sucesso.")
            else:
                print(forms.errors)
        
        case "DELETE":
            author = Author.query.get(value)
            author.delete()
            return jsonify(success=True, message="Autor deletado com sucesso.")

        case "XPTO":
            author = Author.query.get(value)
            author.name = author.name.swapcase()
            author.edit()
            return jsonify(success=True, message="Autor revisado com sucesso.")

    return jsonify(success=False, error="Chamada sem condicional.")        