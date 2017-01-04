from functools import partial
import time
#from sqlalchemy import create_engine
from multiprocessing import Pool, cpu_count
import tushare as ts
import get_date as gd

#engine = create_engine('mysql://root:770607@127.0.0.1/tickdata?charset=utf8')
def get_tick(s = ['600000', '2016-12-29']):
    try:
        df = ts.get_tick_data(s[0], s[1], retry_count=10)
    except TimeoutError:
        return s[0]+'Ea'+s[1]
    try:
        df['time'][5]
        #if df['time'][1] == 'window.close();':
            #return 1
    except KeyError:
        return s[0]+'Eb'+s[1]
    #df.to_sql(s[0]+'t'+s[1], engine)
    filename ='./tickdata/'+s[0]+'t'+s[1]+'.csv'
    try:
        df.to_csv(filename)
        #df.to_sql(s[0]+'t'+s[1], engine)
        return 0
    except IOError:
        return s[0]+'Ec'+s[1]

def get_ticks(C_file):
    codes = []
    file = open(C_file)
    for each in file:
        codes.append(each.strip())
    file.close()
    data = []
    dates = gd.get_date('1999-11-01', '2005-12-31')
    for a in codes:
        for b in dates:
            data.append([a,b])	
	
    p0 = time.perf_counter()
    pool = Pool(processes=cpu_count())
    gtlog = pool.map(get_tick, data)
    pool.close() 
    pool.join()
    #for each in data:
    #gtlog.append(get_tick(each))
    p1 = time.perf_counter()
    print(p1-p0)
    return gtlog

if __name__ == '__main__' :
    print(get_ticks('codes'))
	
