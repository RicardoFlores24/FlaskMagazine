from flask import request, redirect, render_template, Blueprint, flash, session
from app.models.users import User
from app.decorators import login_required
from app import bcrypt
from app.models.magazines import Magazine

auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/')
def ruta_inicio():
    if 'username' in session:
        return redirect('/home')
    return render_template('auth.html')


@auth.route('/registro/usuario', methods=['POST'])
def registro_usuario():
    is_valid = User.validar_usuario(request.form)
    print(f"is_valid:{is_valid}")
    if not is_valid:
        print('No valido')
        return redirect('/')

    nuevo_usuario = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(nuevo_usuario)
    print(id)
    if not id:
        flash("Email ya existe.", "error")
        return redirect('/')
    session['username'] = request.form['first_name']
    session['usuario_id'] = id
    flash("Successfully registered", "success")
    return redirect('/home')


@auth.route("/login", methods=['POST'])
def login():
    data = {
        "email": request.form['email']
    }
    usuario = User.get_by_email(data)
    if not usuario:
        flash("Email o password inválido", "error")
        return redirect("/")

    if not bcrypt.check_password_hash(usuario.password, request.form['password']):
        flash("Email o password inválido", "error")
        return redirect("/")
    session['usuario_id'] = usuario.id
    session['username'] = usuario.first_name
    flash("Successfully logged in", "success")
    return redirect('/home')


@auth.route('/home')
@login_required
def welcome():
    usuario = session['usuario_id']
    usuarios = User.get_by_id(session['usuario_id'])
    magazines = Magazine.get_all()
    print('magazines===========>', magazines)
    return render_template('home.html', usuario=usuario, usuarios=usuarios,magazines=magazines)


@auth.route('/update', methods=['GET', 'POST'])
@login_required
def change_pass():
    usuario = session['usuario_id']
    usuarios = User.get_by_id(session['usuario_id'])
    magazines = Magazine.get_all_user(user_id=usuario)
    print('magazines',)
    if request.method == "POST":
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        result = User.update(user_id=usuario, first_name=first_name, last_name=last_name, email=email)
        print(result)
        flash("Successfully updated user", "info")
        return redirect('/home')
    return render_template('changepwd.html', usuarios=usuarios, magazines=magazines)


@auth.route('/logout')
def cerrar_sesion():
    session.clear()
    flash("Successfully logged out", "success")
    return redirect('/')
