from database.DB_connect import DBConnect
from model.team import Team


class DAO:

    @staticmethod
    def get_year():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT year
                    FROM team
                    WHERE year >= 1980
                    ORDER BY year """
        cursor.execute(query)

        years = [row['year'] for row in cursor]

        cursor.close()
        conn.close()
        return years

    @staticmethod
    def get_teams(year):
        conn = DBConnect.get_connection()

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT t.id, t.team_code, t.name
                    FROM team t 
                    WHERE t.year = %s """

        cursor.execute(query, (year,))

        teams = [Team(id=row['id'], team_code=row['team_code'], name=row['name']) for row in cursor]

        cursor.close()
        conn.close()
        return teams

    @staticmethod
    def get_salaries(min_year):
        conn = DBConnect.get_connection()
        result = {}
        cursor = conn.cursor(dictionary=True)
        query = """ SELECT team_id, SUM(salary) as totale
                    FROM salary
                    WHERE year = %s 
                    GROUP BY team_id """
        cursor.execute(query, (min_year,))
        for row in cursor:
            result = {row['team_id']: row['totale']}

        cursor.close()
        conn.close()
        return result
