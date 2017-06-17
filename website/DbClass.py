class DbClass:
    def __init__(self):
        import mysql.connector as connector

        self.__dsn = {
            "host": "localhost",
            "user": "thibault",
            "passwd": "password",
            "db": "WateroMatic"
        }

        self.__connection = connector.connect(**self.__dsn)
        self.__cursor = self.__connection.cursor()

    def getDatum(self):
        # Query zonder parameters
        sqlQuery = "SELECT DATE_FORMAT(Datum, '%d/%m/%Y %H:%i') FROM (SELECT Datum FROM Data ORDER BY ID DESC LIMIT 6) sub ORDER BY Datum ASC"
        
        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        li = [x[0] for x in result]
        return li

    def getTemperatuur(self):
        # Query zonder parameters
        sqlQuery = "SELECT t.Temperatuur FROM (SELECT * FROM Data ORDER BY id DESC LIMIT 6) AS t ORDER BY t.id ASC;"

        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        li = [x[0] for x in result]
        return li

    def getReservoir(self):
        # Query zonder parameters
        sqlQuery = "SELECT t.Reservoir_liter FROM (SELECT * FROM Data ORDER BY id DESC LIMIT 6) AS t ORDER BY t.id ASC;"

        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        li = [x[0] for x in result]
        return li

    def getVerbruikTotaal(self):
        # Query zonder parameters
        sqlQuery = "SELECT SUM(Verbruik_liter) FROM Data"

        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        li = [x[0] for x in result]
        li2 = str(li)[1:-1]
        return li2

    def getPass(self, voorwaarde):
        # Query zonder parameters
        sqlQuery = "SELECT password FROM Gebruikers WHERE user = '{param1}'"
        sqlCommand = sqlQuery.format(param1=voorwaarde)

        self.__cursor.execute(sqlCommand)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        li = [x[0] for x in result]
        li2 = str(li)[1:-1]
        li3 = li2.replace("'","")
        return li3

