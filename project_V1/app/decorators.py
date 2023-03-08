from flask import session, redirect, flash
from functools import wraps

# def login_required(ruta):
#
#     def wrapper(*args, **kwargs):
#         if 'username' not in session:
#             flash('Usted no tiene acceso a esta parte del sitio', 'error')
#             return redirect('/auth')
#         resp = ruta(*args, **kwargs)
#         return resp
#
#     return wrapper


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if 'username' not in session:
            flash('Usted no tiene acceso a esta parte del sitio', 'error')
            return redirect('/')
        # Otherwise continue with the route function
        return f(*args, **kwargs)

    return decorated_function