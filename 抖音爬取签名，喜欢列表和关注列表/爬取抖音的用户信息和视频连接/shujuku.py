from sqlalchemy import create_engine
from sqlalchemy import Column,Integer,String,Text
from sqlalchemy.orm import sessionmaker,scoped_session
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine(
    "mysql+pymysql://root:root@127.0.0.1:3306/test?charset=utf8mb4",
    #超过连接池大小外最多可以创建的连接数
    max_overflow=500,
    #连接池的大小
    pool_size=100,
    #是否显示开发信息
    echo=False,
)

class Tik(Base):
    __tablename__ = 'tik'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(40))
    user_id = Column(String(40))
    intro = Column(Text())
    fans = Column(String(50))

Base.metadata.create_all(engine)
session = sessionmaker(engine)
sess = scoped_session(session)