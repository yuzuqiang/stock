from sqlalchemy import create_engine
import tushare as ts

df = ts.get_tick_data('600848', date='2014-12-22')
engine = create_engine('mysql://root:770607@127.0.0.1/stock?charset=utf8')
df.to_sql('tick_data',engine)
