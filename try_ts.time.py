import time
from multiprocessing import Pool, cpu_count
import tushare as ts
def get_tick(code, date='2016-03-22'):
	try:
		return ts.get_tick_data(code, date, retry_count=10)
	except TimeoutError:
		return None

if __name__ == '__main__':
	print(time.clock())
	cs500 = ts.get_sz50s().code
	print(time.clock())
	t0 = time.clock()
	res = [get_tick(sc) for sc in cs500]
	t1 = time.clock()

	pool = Pool(processes=cpu_count()*3)
	res = pool.map(get_tick, cs500)
	pool.close()
	pool.join()
	t2 = time.clock()

	pool = Pool(processes=cpu_count()*3)
	res = pool.starmap(get_tick, zip(cs500,['2016-03-22']*50))
	pool.close()
	pool.join()
	t3 = time.clock()

	pool = Pool(processes=cpu_count()*4)
	res = pool.map(get_tick, cs500)
	pool.close()
	pool.join()
	t4 = time.clock()

	pool = Pool(processes=cpu_count()*4)
	res = pool.starmap(get_tick, zip(cs500,['2016-03-22']*50))
	pool.close()
	pool.join()
	t5 = time.clock()
	print('normal: %.2f second' %(t1-t0))
	print('multi-map8: %.2f second'%(t2-t1))
	print('multi-starmap8: %.2f second'%(t3-t2))
	print('multi-map32: %.2f second'%(t4-t3))
	print('multi-starmap32: %.2f second'%(t5-t4))
