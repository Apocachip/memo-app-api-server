from http import HTTPStatus
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from mysql.connector.errors import Error
from mysql_connection import get_connection
import mysql.connector

class MemoListResource(Resource) :

    @jwt_required
    def post(self) :

        data = request.get_json()

        user_id = get_jwt_identity()

        try :
            connection = get_connection()

            query = '''insert into memo
                    (title, date, description, user_id)
                    values
                    (%s, %s, %s);
                    '''
            record = (data['title'], data['date'], data['description'], user_id)

            cursor = connection.cursor()

            cursor.execute(query, record)

            connection.commit()

            cursor.close()
            connection.close()

        except mysql.connector.Error as e :
            print(e)
            cursor.close()
            connection.close()
            return {"error" : str(e)}, 503

        return {"result" : "success"}, 200