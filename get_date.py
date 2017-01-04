import tushare as ts

def get_date(Sdate='2016-12-01', Edate='2016-12-29'):
	df = ts.get_k_data('000001', index=True, start=Sdate, end=Edate)
	return df['date'].tolist()

if __name__ == '__main__' :
	print(get_date('2016-12-01', '2016-12-29'))
