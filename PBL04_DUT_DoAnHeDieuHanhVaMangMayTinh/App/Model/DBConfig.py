from mysql import connector
class MySQLConnector:
    con = None
    def __init__(self):
        self.con=connector.connect(
            host="localhost",
            user="root",
            password="",
            database="pbl04"
        )