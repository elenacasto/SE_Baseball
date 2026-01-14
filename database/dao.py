from ctypes import HRESULT

from database.DB_connect import DBConnect
from model.team import Team


class DAO:

    @staticmethod
    def get_years():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT year
                    FROM team 
                    WHERE year >= '1980'
                    ORDER BY year """
        cursor.execute(query)
        years = [row['year'] for row in cursor]

        cursor.close()
        conn.close()
        return years

    @staticmethod
    def get_teams(year):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ SELECT id, team_code, name
                    FROM team
                    WHERE year = %s """
        cursor.execute(query, (year,))
        for row in cursor:
            result.append(Team(row['id'], row['team_code'], row['name']))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_salaries(year):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """ SELECT SUM(salary) as somma_salary, team_id
                    FROM salary
                    WHERE year = %s 
                    GROUP BY team_id """
        cursor.execute(query, (year,))
        result = {row['team_id']: row['somma_salary'] for row in cursor}

        cursor.close()
        conn.close()
        return result