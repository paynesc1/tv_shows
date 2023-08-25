from flask_app.config.mysqlconnection import connectToMySQL
import pprint
from flask_app.models import show_model
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$'
)

db = "tv_shows_schema"

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.show=[]

    @classmethod
    def user_save(cls, data):
        query = """ INSERT INTO users(first_name, last_name, email, password)
        VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """
        results = connectToMySQL(db).query_db(query, data)
        return results
        

    @classmethod
    def get_user_by_id(cls, id):
        data = {"id":id}
        query = """SELECT * FROM users
            WHERE id = %(id)s;
            """
        results = connectToMySQL(db).query_db(query, data)
        if not results:
            return None
        return cls(results[0])

    @classmethod
    def get_user_by_email(cls, data):
        query = """SELECT * FROM users
            WHERE email=%(email)s;
        """
        results = connectToMySQL(db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])


    @staticmethod
    def validation(data):
        is_valid = True
        if len(data['first_name']) < 2:
            flash("First Name must include at least 2 characters", "registration_error")
            is_valid = False
        if len(data['last_name']) < 2:
            flash("Last Name must include at least 2 characters", "registration_error")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address.", "registration_error")
            is_valid = False
        #check to see if email in database
        query = """SELECT * FROM users
                WHERE email = %(email)s;
                """
        results = connectToMySQL(db).query_db(query, data)
        if results:
            flash("Invalid email address", "registration_error")
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash("Passwords don't match.", "registration_error")
            is_valid = False
        return is_valid
        






