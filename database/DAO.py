from database.DB_connect import DBConnect
from model.genre import Genre
from model.track import Track


class DAO:
    def __init__(self):
        pass

    @staticmethod
    def get_all_genres():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select * from genre g order by GenreId """
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(Genre(**row))
        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def get_tracks(genreId):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select t.* from track t , genre g where t.GenreId = g.GenreId and g.GenreId = %s"""
        cursor.execute(query, (genreId,))
        result = []
        for row in cursor:
            result.append(Track(**row))
        cursor.close()
        cnx.close()
        return result
