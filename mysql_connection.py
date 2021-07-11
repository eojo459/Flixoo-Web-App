import mysql.connector


class mySQLConnection():

    def createConnection(self):

        # connect to mySQL DB
        db = mysql.connector.connect(
            host="hostName",
            user="username",
            password="mypass",
            database="mydb")

        return db