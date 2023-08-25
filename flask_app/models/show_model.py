from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user_model
import pprint
from flask import flash


db = "tv_shows_schema"

class Show:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.network = data['network']
        self.release_date = data['release_date']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = None


    @classmethod
    def show_save(cls, data):
        query = """ INSERT INTO shows(title, network, release_date, description, user_id)
        VALUES(%(title)s, %(network)s, %(release_date)s, %(description)s, %(user_id)s);
        """
        results = connectToMySQL(db).query_db(query, data)
        return results

    @classmethod
    def get_all_shows(cls):
        query = """SELECT * FROM shows
        LEFT JOIN users ON shows.user_id = users.id
        """
        results = connectToMySQL(db).query_db(query)
        all_shows=[]
        for row in results:
            show = cls(row)
            user_data = {
                "id":row['users.id'],
                "first_name":row['first_name'],
                "last_name":row['last_name'],
                "email":row['email'],
                "password":row['password'],
                "created_at":row['created_at'],
                "updated_at":row['updated_at']
            }
            user_instance=user_model.User(user_data)
            show.user = user_instance
            all_shows.append(show)
        return all_shows
    
    @classmethod
    def update_car(cls, data):
        query = """UPDATE shows
        SET title = %(title)s, network =%(network)s, release_date=%(release_date)s
        WHERE id = %(id)s;
        """
        results = connectToMySQL(db).query_db(query, data)
        return results


    @classmethod
    def delete(cls, data):
        query="""DELETE FROM shows
        WHERE id=%(id)s;
        """
        results=connectToMySQL(db).query_db(query,data)
        return results

    @classmethod
    def get_show_by_id(cls, id):
        data={"id": id}
        query = """SELECT * FROM shows
        LEFT JOIN users ON shows.user_id = users.id
        WHERE shows.id = %(id)s;
        """
        results = connectToMySQL(db).query_db(query, data)
        all_shows=[]
        for row in results:
            show = cls(row)
            user_data = {
                "id":row['users.id'],
                "first_name":row['first_name'],
                "last_name":row['last_name'],
                "email":row['email'],
                "password":row['password'],
                "created_at":row['created_at'],
                "updated_at":row['updated_at']
            }
            user_instance=user_model.User(user_data)
            show.user = user_instance
            all_shows.append(show) 
        return all_shows[0]



    @staticmethod
    def validation(data):
        is_valid = True
        if not data['title'] or len(data['title']) < 3:
            flash("Title must not be left blank; at least 3 characters long", "show_error")
            is_valid=False
        if not data['network'] or len(data['network']) < 3:
            flash("Network must not be left blank; at least 3 characters long", "show_error")
            is_valid=False
        if not data['release_date']:
            flash("Release Date field must not be left blank", "show_error")
            is_valid=False
        if not data['description'] or len(data['description']) < 3:
            flash("Description must not be left blank; at least 3 characters long", "show_error")
            is_valid=False
        return is_valid
        