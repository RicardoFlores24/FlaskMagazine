from flask import flash
from app.models.connection import connectToMySQL
from app.models.users import User

# create_table = '''
# create table if not exists magazine  (
#     id int auto_increment primary key,
#     title varchar(255) not null,
#     description varchar(255) not null,
#     creator_id int not null,
#     foreign key (creator_id) references users(id)
#
# )
# '''
# connectToMySQL().query_db(create_table)

# middle_table = '''
# create table if not exists users_magazine  (
#     user_id int not null,
#     magazine_id int not null,
#     primary key(user_id, magazine_id),
#     foreign key (user_id) references users(id) on delete cascade,
#     foreign key (magazine_id) references magazine(id)  on delete cascade
#
# )
# '''
# connectToMySQL().query_db(middle_table)


class Magazine:
    db_name = 'mydb'
    # db_name='sesion_y_registro'
    campos = ['title', 'description', 'users_id']
    modelo = 'magazine'

    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.users_id = data['users_id']

    @classmethod
    def get_all_user(cls, user_id):
        data = {
            "users_id": user_id
        }
        query = f"SELECT * FROM {cls.modelo} WHERE users_id = %(users_id)s;"
        quotes = connectToMySQL(cls.db_name).query_db(query, data)

        print('======>', quotes)

        usuario = []
        for b in quotes:
            usuario.append(cls(b))
        print('quotes===>>', usuario)
        return usuario

    @classmethod
    def get_all(cls):

        query = f"SELECT * FROM {cls.modelo}"
        quotes = connectToMySQL(cls.db_name).query_db(query)

        print('======>', quotes)
        user_lst = [i['users_id'] for i in quotes]
        print('====>', user_lst)
        username_lst = [f"{User.get_by_id(i).first_name} {User.get_by_id(i).last_name}" for i in user_lst]
        # print(username_lst)
        final_quotes = []
        for quote, name in zip(quotes, username_lst):
            quote['name'] = name
            final_quotes.append(quote)


        return final_quotes


    @classmethod
    def get_by_id(cls, magazine_id):
        data = {
            "id": magazine_id
        }
        query = f"SELECT * FROM {cls.modelo} WHERE id = %(id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)

        user_lst = [i['users_id'] for i in result]
        print('====>', user_lst)
        username_lst = [f"{User.get_by_id(i).first_name} {User.get_by_id(i).last_name}" for i in user_lst]
        final_quotes = []
        for quote, name in zip(result, username_lst):
            quote['name'] = name
            final_quotes.append(quote)
        return final_quotes[0]

    @staticmethod
    def validar_usuario(usuario):
        is_valid = True
        title = usuario['title'].strip()
        if title == '':
            flash('El quotedby no puede estar vacío', 'error')
            is_valid = False
        if len(title) < 2:
            flash('El nombre debe contener al menos 2 caracteres', 'error')
            is_valid = False
        description = usuario['description'].strip()
        if description == '':
            flash('El message no puede estar vacío', 'error')
            is_valid = False
        if len(description) < 10:
            flash('El apellido debe contener al menos 10 caracteres', 'error')
            is_valid = False
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
    def delete(cls, magazine_id):
        data = {
            "id": magazine_id
        }
        query = f"DELETE FROM {cls.modelo}  WHERE id = %(id)s;"
        resultado = connectToMySQL(cls.db_name).query_db(query, data)

        return resultado

