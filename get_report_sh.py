import os
import pickle
import requests
from datetime import datetime, timedelta, date
import time
from multiprocessing import Pool, cpu_count
report_type = ('quarter3','semiannual','quarter1','annual')

def get_report(code, year, rt):
    url = 'http://www.sse.com.cn/disclosure/listedinfo/announcement/c/'
    if rt not in report_type:
        return None
    if rt == 'annual':
        start_mm = '01'
        start_dd = '10'
        end_mm = '04'
        end_dd = '30'
        sep = '_n'
        ssep = 'n'
    elif rt == 'quarter1':
        start_mm = '02'
        start_dd = '01'
        end_mm = '04'
        end_dd = '30'
        sep = '_1'
        ssep = 'f'
    elif rt =='semiannual':
        start_mm = '07'
        start_dd = '01'
        end_mm = '08'
        end_dd = '31'
        sep = '_z'
        ssep = 'z'
    elif rt =='quarter3':
        start_mm = '10'
        start_dd = '10'
        end_mm = '10'
        end_dd = '31'
        sep = '_3'
        ssep = 't'

    if rt == report_type[3]:
        filename = code + '_' + str(int(year)-1) + sep + '.pdf'
    else:
        filename = code + '_' + year + sep + '.pdf'
    savepath = '/Volumes/ST HDD/stock/report/sh/' + rt + '/' + year
    if not os.path.isdir(savepath):
        os.system('mkdir /Volumes/ST\ HDD/stock/report/sh/'+rt+'/'+year)
    start_date = date(int(year), int(start_mm), int(start_dd))
    end_date = date(int(year), int(end_mm), int(end_dd))
    while start_date <= end_date:
        if start_date >= date.today():
            return 'It is not report time'
        try:
            pdfurl = url + start_date.strftime('%Y-%m-%d') + '/' + filename
            getpdf = requests.get(pdfurl)
            if getpdf.status_code == 200:
                with open(savepath + '/' + code + '_' + start_date.strftime('%Y_%m_%d')+ssep+'.pdf', 'wb') as fpdf:
                    fpdf.write(getpdf.content)
                return code,  start_date.strftime('%Y-%m-%d'), rt
        except:
            pass
        
        start_date = start_date + timedelta(days = 1)
    return None

def get_reports(code):
    results =[]
    years = list(range(2010, 2013))
    years.sort(reverse = True)
    years = [str(year) for year in years]
    for year in years:
        for report_t in report_type:
            result = get_report(code, year, report_t)
            if result != None:
                results.append(result)
    return results
    

if __name__ == '__main__':
    
    codes = []
    cfile = open('codes')
    for each in cfile:
        codes.append(each.strip())
    cfile.close()
    pool = Pool(processes=cpu_count())
    results = pool.map(get_reports, codes)
    pool.close() 
    pool.join()
