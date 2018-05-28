import psycopg2
from copy import deepcopy

class connector(object):
    def __init__(self, ip, dbname, user, password, *args, **kwargs):
        self.ip = ip
        self.dbname = dbname
        self.user   = user
        self.password = password
        self.cursor = ''
        self.conn = ''

    def set_cursor(self):
        string_to_connect = "host=" + self.ip + " dbname=" + self.dbname + " user=" + self.user + " password="+ self.password
        self.conn = psycopg2.connect(string_to_connect)
        self.cursor = self.conn.cursor()
        return self

    def method(self,sql_string,_one=None,_all=None): # _one  == none or _all = none
        # cur = self.set_cursor()
        self.cursor.execute(sql_string)
        self.conn.commit()
        if _one != None and _all == None:
            return self.cursor.fetchone()
        elif _one == None and _all != None :
            return self.cursor.fetchall()
        else:
            return "you dont correctly use type output"

def main():
    connect_obj = connector('localhost','indexing_address','indexer','123456').set_cursor()
    sql_string = """INSERT INTO indexing (blockid,txid,attr) VALUES ('1','abc','{"a":"b"}') """ 
    print (connect_obj.method(sql_string=sql_string))

if __name__ == "__main__":
    main()

