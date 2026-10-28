import pymysql

class DB_util:
    Default_Config = {            #类属性。这个字典直接定义在类里,所有实例共享这一份配置。
        'host':'127.0.0.1',
        'port':3306,
        'user':'ur_name',
        'password':'ur_password',
        'database':'ur_db',
        'charset':'utf8mb4'
    }
    def __init__(self,**kwargs):         #构造方法/初始化方法。__init__ 在每次实例化对象（db = DBUtil()）时自动触发。
        '''
        get connection
        get cursor
        '''
        self.config = {**self.Default_Config,**kwargs}
        self.con = pymysql.connect(**self.config)          #双星号 ** 解包,把字典拆成 key=value 的形式
        self.cursor = self.con.cursor(pymysql.cursors.DictCursor)

    def close(self) -> None:
        '''
        close connection and cursor
        '''
        if self.cursor:
            self.cursor.close()
        if self.con:
            self.con.close()

    def execute_dml(self,sql,*args):            #*args,可变位置参数
        '''
        execute DML to add, delete, update
        '''
        try:
            self.cursor.execute(sql,args)
            self.con.commit()
        except Exception as e:
            print('DML Error:',e)
            self.con.rollback()             #在出错时撤销事务，防止数据只写了一半。
            return False

    def query_one(self,sql,*args):
        '''
        get one data
        '''
        try:
            self.cursor.execute(sql,args)
            return self.cursor.fetchone()
        except Exception as e:
            print('Query One Error:',e)
            return None

    def query_all(self,sql,*args):
        '''
        get all datas
        '''
        try:
            self.cursor.execute(sql,args)
            return self.cursor.fetchall()
        except Exception as e:
            print('Query All Error:',e)
            return []


# test
if __name__ == '__main__':
    db = DB_util()
    sql = 'select * from t_user where sex = %s;'
    print("查询结果：")
    print(db.query_all(sql, 'male'))
    db.close()
