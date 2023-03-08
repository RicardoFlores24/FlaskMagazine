from flask import request, redirect, render_template, Blueprint, flash, session
from app.decorators import login_required
from app.models.magazines import Magazine
from app.models.users import User

magazines = Blueprint('magazines', __name__, template_folder='templates')


@magazines.route('/add-magazine', methods=["GET", "POST"])
@login_required
def new_magazine():
    username = session['username']
    usuario = session['usuario_id']
    if request.method == 'POST':
        is_valid = Magazine.validar_usuario(request.form)
        print(is_valid)
        if is_valid:
            title = request.form.get('title')
            description = request.form.get('description')
            print(title, description)
            new_quote = {
                "title": title,
                "description": description,
                "users_id": usuario
            }
            id = Magazine.save(new_quote)
            flash("Successfully Added Magazine", "success")
            return redirect('/home')
    return render_template('new-magazine.html')


@magazines.route('/show/<int:id>')
@login_required
def magazine_detail_view(id):
    # usuario = session['usuario_id']

    magazine = Magazine.get_by_id(int(id))
    print('===========> result', magazine)
    return render_template('magazines.html', magazine=magazine)


@magazines.route('/delete-magazine/<int:id>')
@login_required
def delete_magazine(id):
    username = session['username']
    usuario = session['usuario_id']
    if id:
        Magazine.delete(int(id))
        flash("Successfully Deleted Magazine", "info")
    return redirect('/update')
