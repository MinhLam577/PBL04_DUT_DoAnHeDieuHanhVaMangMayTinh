from App.Model.DBConfig import MySQLConnector
from App.Model.E_User import User
class ModelUser:
    def __init__(self):
        pass
    def getAllUser(self):
        try:
            with MySQLConnector() as mycon:
                sql = "SELECT * FROM User"
                result = self.executeDB(mycon, sql)
                if(result == None):
                    return None
                return result
        except Exception as e:
            print("Error getAllUser: " + str(e))
    def deleteUser(self, id):
        try:
            mycon = MySQLConnector()
            sql = "DELETE FROM User WHERE IDUser = '" + str(id) + "'"
            res = self.executeUpdateDB(mycon, sql)
            if(res):
                return True
            return False
        except Exception as e:
            print("Error deleteUser: " + str(e))
    def getAllUser(self):
        try:
            mycon = MySQLConnector()
            sql = "SELECT * FROM User"
            res = self.executeDB(mycon, sql)
            if(res):
                return res
            return None
        except Exception as e:
            print("Error getAllUser: " + str(e))
    def executeUpdateDB(self, mycon, query):
        try:
            cursor = mycon.con.cursor()
            cursor.execute(query)
            mycon.con.commit()
            cursor.close()
            mycon.con.close()
            return True
        except Exception as e:
            print("executeUpdateDB Error:" + str(e))
    def executeDB(self, mycon, query):
        try:    
            cursor = mycon.con.cursor()
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print("executeDB Error:" + str(e))