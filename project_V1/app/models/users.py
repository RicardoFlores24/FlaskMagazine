from flask import flash
from app.models.connection import connectToMySQL
from app import bcrypt

import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')



# create_table = '''
# create table if not exists users  (
#     id int auto_increment primary key,
#     first_name varchar(255) not null,
#     last_name varchar(255) not null,
#     email varchar(255) not null unique,
#     password varchar(255) not null,
# )
# '''
# connectToMySQL().query_db(create_table)



class User:
    db_name = 'mydb'
    campos = ['first_name', 'last_name', 'email', 'password']
    modelo = 'users'

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']

    @classmethod
    def get_by_email(cls, data):

        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)

        if len(results) < 1:
            return False
        return User(results[0])

    @classmethod
    def get_by_id(cls, usuario_id):
        data = {
            "id": usuario_id
        }
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)

        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def authenticated_user_by_input(cls, usuario_input):

        valid = True
        existing_user = cls.get_by_email(usuario_input["email"])

        password_valid = True

        if not existing_user:
            valid = False

        else:

            data = {
                "email": usuario_input["email"]
            }
            query = "SELECT password FROM users WHERE email = %(email)s;"
            hashed_pw = connectToMySQL(cls.db_name).query_db(query, data)[0]["password"]

            password_valid = bcrypt.check_password_hash(hashed_pw, usuario_input['password'])

            if not password_valid:
                valid = False

        if not valid:
            flash("Email o contraseña inválidos.","error")
            return False

        return existing_user

    @staticmethod
    def validar_usuario(usuario):
        is_valid = True
        first_name = usuario['first_name'].strip()
        if first_name == '':
            flash('El first_name no puede estar vacío', 'error')
            is_valid = False
        if len(usuario['first_name']) < 3:
            flash('El nombre debe contener al menos 3 caracteres', 'error')
            is_valid = False
        last_name = usuario['last_name'].strip()
        if last_name == '':
            flash('El last_name no puede estar vacío', 'error')
            is_valid = False
        if len(usuario['last_name']) < 3:
            flash('El apellido debe contener al menos 3 caracteres', 'error')
            is_valid = False
        if not EMAIL_REGEX.match(usuario['email']):
            is_valid = False
            flash("Email inválido", "danger")
        if len(usuario['password']) < 8:
            is_valid = False
            flash('Password debe tener al menos 8 carácteres', 'error')
        if usuario['password'] != usuario['confirm_password']:
            is_valid = False
            flash("Las password no coinciden", "error")
        return is_valid

    @classmethod
    def save(cls, data):

        campos_header = ','.join(cls.campos)
        campos_datos = [f'%({i})s' for i in cls.campos]
        campos_datos = ','.join(campos_datos)

        query = f"""
                        INSERT INTO {cls.modelo} ({campos_header})
                        VALUES ({campos_datos});
                        """
        print(query)
        resultado = connectToMySQL(cls.db_name).query_db(query, data)
        print("RESULTADO: ", resultado)
        return resultado

    @classmethod
    def update(cls, user_id, first_name, last_name, email):
        data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "id": user_id
        }
        query = f"UPDATE {cls.modelo} SET first_name = %(first_name)s, last_name = %(last_name)s,email = %(email)s  WHERE id = %(id)s;"
        resultado = connectToMySQL(cls.db_name).query_db(query, data)

        return resultado
