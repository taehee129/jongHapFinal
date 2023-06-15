import pymssql
 
class DbConnection() :
    def __init__(self) -> None:
        self.server = 'localhost'
        self.user = 'taehee'
        self.password = '2564'
        self.database = 'test'
    
    def connect(self) :
        return pymssql.connect(server= self.server, user='taehee', password='2564', database='test',  charset='EUC-KR')

 