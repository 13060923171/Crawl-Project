#创建我们的引擎
from sqlalchemy import create_engine
#为数据库创建一些类
from sqlalchemy import Column,Integer,String,Text
#创建一个包，把引擎包含进去，解决线性安全问题
from sqlalchemy.orm import sessionmaker,scoped_session
#创建一个基类
from sqlalchemy.ext.declarative import declarative_base

#创建一个基类
BASE = declarative_base()
#创建一个数据库的引擎，去调用我们的数据库
engine = create_engine(
    "mysql+pymysql://root:root@127.0.0.1:3306/test",
    #超过连接池大小外最多可以创建的连接数
    max_overflow=500,
    #连接池的大小
    pool_size=100,
    #是否显示开发信息
    echo=True,
)
#创建一个类并且调用基类
class House(BASE):
    #数据库中表的名字
    __tablename__ = 'house'
    #数据库存储数据类型的形式
    id = Column(Integer,primary_key=True,autoincrement=True)
    block = Column(String(125))
    title = Column(String(125))
    rent = Column(String(125))
    data = Column(Text())
    data2 = Column(Text())
    data3 = Column(Text())
    data4 = Column(Text())
    data5 = Column(Text())

#创建数据表，也就第一次有效，第二次创建相同的数据表则失效
BASE.metadata.create_all(engine)
#sessionmaker是把引擎包含进去，为了方便我们创建一个事物
Session = sessionmaker(engine)
#把Session包含起来，为了避免线性安全问题,一般你是写多线程的时候才需要用到
sess = scoped_session(Session)