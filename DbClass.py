class DbClass:
    def __init__(self):
        import mysql.connector as connector

        self.__dsn = {
            "host": "localhost",
            "user": "thibault",
            "passwd": "macbookPRO1",
            "db": "WateroMatic"
        }

        self.__connection = connector.connect(**self.__dsn)
        self.__cursor = self.__connection.cursor()

    def getDatum(self):
        # Query zonder parameters
        sqlQuery = "SELECT DATE_FORMAT(Datum, '%d/%m/%Y %H:%i') from Data"
        
        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        li = [x[0] for x in result]
        return li

    def getTemperatuur(self):
        # Query zonder parameters
        sqlQuery = "SELECT Temperatuur FROM Data"

        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        li = [x[0] for x in result]
        return li

    def getReservoir(self):
        # Query zonder parameters
        sqlQuery = "SELECT Reservoir_liter FROM Data"

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


