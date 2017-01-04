import os
import pickle
import requests
from datetime import datetime, timedelta, date
import time
from multiprocessing import Pool, cpu_count
report_type = ('annual', 'quarterly3','semi_annual','quarterly1')

def get_report(code, year, rt):
    url = 'http://www.sse.com.cn/disclosure/listedinfo/announcement/c/'
    if rt not in report_type:
        return None
    if rt == 'quarterly1':
        start_mm = '02'
        start_dd = '01'
        end_mm = '04'
        end_dd = '30'
        sep = '_1'
    elif rt =='semi_annual':
        start_mm = '07'
        start_dd = '01'
        end_mm = '08'
        end_dd = '31'
        sep = '_z'
    elif rt =='quarterly3':
        start_mm = '10'
        start_dd = '10'
        end_mm = '10'
        end_dd = '31'
        sep = '_3'
    else:
        start_mm = '01'
        start_dd = '10'
        end_mm = '04'
        end_dd = '30'
        sep = '_n'

    filename = code + '_' + year + sep + '.pdf'
    savepath = '/Volumes/ST HDD/stock/report/' + year
    if not os.path.isdir(savepath):
        os.system('mkdir /Volumes/ST\ HDD/stock/report/'+year)
    if rt == report_type[0]:
        start_date = date(int(year)+1, int(start_mm), int(start_dd))
        end_date = date(int(year)+1, int(end_mm), int(end_dd))
    else:
        start_date = date(int(year), int(start_mm), int(start_dd))
        end_date = date(int(year), int(end_mm), int(end_dd))
    while start_date <= end_date:
        if start_date >= date.today():
            return 'It is not report time'
        pdfurl = url + start_date.strftime('%Y-%m-%d') + '/' + filename
            
        getpdf = requests.get(pdfurl)
        if getpdf.status_code == 200:
            with open(savepath + '/' + filename, 'wb') as fpdf:
                fpdf.write(getpdf.content)
            return code,  start_date.strftime('%Y-%m-%d'), rt
        else:
            start_date = start_date + timedelta(days = 1)
    return None

def get_reports(code):
    results =[]
    years = list(range(2002, 2017))
    years.sort(reverse = True)
    years = [str(year) for year in years]
    for year in years:
        for report_t in report_type:
            result = get_report(code, year, report_t)
            if result == None:
                return results
            results.append(result)
            if year=='2002' and report_t==report_type[2]:
                break

    url = 'http://www.sse.com.cn/disclosure/listedinfo/announcement/c/'
    pdfurl = url + code + '_2002' + '_1.pdf' 
    savepath = '/Volumes/ST HDD/stock/report/2002' 
    result = requests.get(pdfurl)
    if result.status_code == 200:
        with open(savepath + '/' + code + '_2002_1.pdf', 'wb') as fpdf:
            fpdf.write(result.content)
        results.append((code, '2002', 'quarterly1'))
        """years = list(range(1999,2002))
        years.sort(reverse = True)
        for year in years:
            pdfurl = url + code + '_' + year + '_0.pdf'
            result = requests.get(pdfurl)
            if result.status_code == 200:
                with open(savepath + '/' + code + '_' + year + '_n.pdf', 'wb') as fpdf:
                    fpdf.write(getpdf.content)
                results.appdnd((code, year, 'annual'))
                
                pdfurl = url + code + '_' + year + '_1.pdf'
                result = requests.get(pdfurl)
                if result.status_code == 200:
                    with open(savepath + '/' + code + '_' + year + '_z.pdf', 'wb') as fpdf:
                        fpdf.write(getpdf.content)
                    results.appdnd((code, year, 'semi_annual'))
                else:
                    return results
            else:
                return results"""
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
    for result in results:
        with open('/Volumes/ST HDD/stock/report/'+result[0][0]+'.log', 'wb') as fpickle:
            pickle.dump(result, fpickle)
