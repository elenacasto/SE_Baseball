from database.DB_connect import DBConnect
from model.team import Team


class DAO:

    @staticmethod
    def get_year(min_year):
        conn = DBConnect.get_connection()

        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ SELECT year
                    FROM teams
                    WHERE year >= 1980
                    ORDER BY year """
        cursor.execute(query, (min_year,))

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_teams(min_year):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT t.id, t.team_code, t.name
                    FROM team t 
                    WHERE t.year = %s """

        cursor.execute(query, (min_year,))

        for row in cursor:
            anno_str = row['year'].replace(",", "")
            anno = int(anno_str)
            team = Team(id=row['id'], team_code=row['team_code'], name=row['name'], salary=row['somma_salario'], year=anno)
            result.append(team)

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_salaries(min_year):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ SELECT team_id, SUM(salary) as totale
                    FROM teams  
                    WHERE year = %s 
                    GROUP BY team_id """
        cursor.execute(query, (min_year,))
        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result
