from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
engine = create_engine(
    "mysql+pymysql://root:root@127.0.0.1:3306/test",
    #超过连接池大小外最多可以创建的连接数
    max_overflow=500,
    #连接池的大小
    pool_size=100,
    #是否显示开发信息
    echo=False,
)
#创建一个基类
BASE= declarative_base()

class Song(BASE):
    #定义这个数据库表的名字
    __tablename__ = 'song'
    #设置一些对应的值
    song_id = Column(Integer,primary_key=True,autoincrement=True)
    singer_name= Column(String(50))
    song_name = Column(String(64))
    song_ablum = Column(String(64))
    song_number = Column(String(50))
    song_mid = Column(String(50))


#把引擎加入基类里面
BASE.metadata.create_all(engine)
DBsession = sessionmaker(bind=engine)
SQLsession = scoped_session(DBsession)