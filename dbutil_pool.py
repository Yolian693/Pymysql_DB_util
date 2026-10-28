# Advanced 数据库连接池（Pool）,dbutils 库
# 先安装连接池库
# pip install dbutils

import pymysql
from dbutils.pooled_db import PooledDB

class DBUtil:
    def __init__(self, **kwargs):
        # 默认配置
        config = {
            'host':'127.0.0.1',
            'port':3306,
            'user':'ur_name',
            'password':'ur_password',
            'database':'ur_db',
            'charset':'utf8mb4'
        }
        config.update(kwargs)

        # 创建连接池
        self.pool = PooledDB(
            creator=pymysql,
            maxconnections=10, # 池子里最多放 10 个连接
            mincached=2,      # 启动时先建 2 个连接备用
            **config
        )

    def get_conn(self):
        # 从池子里拿一个连接出来
        return self.pool.connection()

    def query_all(self, sql, *args):
        con = self.get_conn()
        cursor = con.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute(sql, args)
            return cursor.fetchall()
        except Exception as e:
            print(e)
            return []
        finally:
            cursor.close()
            con.close() # 这里的 close 不是真关闭，而是把连接还回池子！