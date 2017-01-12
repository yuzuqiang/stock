import os
from multiprocessing import Pool, cpu_count
import requests
from bs4 import BeautifulSoup
import pickle

savePath = '/Volumes/ST HDD/stock/report/sz/'
def get_pdfTag_sz(stockCode,noticeType,startTime,endTime):
    params = {'stockCode': stockCode,
            'noticeType':noticeType,
            'startTime':startTime,
            'endTime':endTime}
    try:
        rhtml = requests.post("http://disclosure.szse.cn/m/search0425.jsp",
            data=params)
        bshtml = BeautifulSoup(rhtml.text)
        pdfTags = bshtml.tbody.findAll('a', href = True)
        timesTags = bshtml.tbody.findAll('span')
        timesList = list(timesTags)
        pdfTime = [(each.get_text())[1:-1] for each in timesList]
        i=0
        pdfTimes = []
        for each in pdfTime:
            pdfTimes.append(each+str(i))
            i=i+1
        return dict(zip(pdfTimes,pdfTags))
    except:
        print(stockCode)
        return None

def get_report_annual_sz(stockCode, startTime, endTime):
    results = get_pdfTag_sz(stockCode, '010301', startTime, endTime)
    pdfLinks = dict()
    for each in results:
        if results[each].text.endswith('报告') or results[each].text.endswith('报告（更新后）') or results[each].text.endswith('报告（调整后）'):
            pdfLinks[each[:10]] = results[each].get('href')
            getPdf = requests.get('http://disclosure.szse.cn/'+results[each].get('href'))
            if not os.path.isdir(savePath+'annual/'+each[0:4]):
                os.system('mkdir /Volumes/ST\ HDD/stock/report/sz/annual/'+each[0:4])
            fPdf = open(savePath+'annual/'+each[0:4]+'/'+stockCode+'_'+each[0:4]+'_'+each[5:7]+'_'+each[8:10]+'n.pdf', 'wb')
            fPdf.write(getPdf.content)
        elif results[each].text.endswith('报告（已取消）'):
            pdfLinks[each[:10]] = results[each].get('href')
            getPdf = requests.get('http://disclosure.szse.cn/'+results[each].get('href'))
            if not os.path.isdir(savePath+'annual/'+each[0:4]):
                os.system('mkdir /Volumes/ST\ HDD/stock/report/sz/annual/'+each[0:4])
            fPdf = open(savePath+'annual/'+each[0:4]+'/'+stockCode+'_'+each[0:4]+'_'+each[5:7]+'_'+each[8:10]+'nc.pdf', 'wb')
            fPdf.write(getPdf.content)
    return pdfLinks

def get_report_semiannual_sz(stockCode, startTime, endTime):
    results = get_pdfTag_sz(stockCode, '010303', startTime, endTime)
    pdfLinks = dict()
    for each in results:
        if results[each].text.endswith('报告') or results[each].text.endswith('报告（更新后）') or results[each].text.endswith('报告（调整后）')or results[each].text.endswith('报告（更正后）') or results[each].text.endswith('报告（全文）') :
            pdfLinks[each[:10]] = results[each].get('href')
            getPdf = requests.get('http://disclosure.szse.cn/'+results[each].get('href'))
            if not os.path.isdir(savePath+'semiannual/'+each[0:4]):
                os.system('mkdir /Volumes/ST\ HDD/stock/report/sz/semiannual/'+each[0:4])
            fPdf = open(savePath+'semiannual/'+each[0:4]+'/'+stockCode+'_'+each[0:4]+'_'+each[5:7]+'_'+each[8:10]+'z.pdf', 'wb')
            fPdf.write(getPdf.content)
        elif results[each].text.endswith('报告（已取消）'):
            pdfLinks[each[:10]] = results[each].get('href')
            getPdf = requests.get('http://disclosure.szse.cn/'+results[each].get('href'))
            if not os.path.isdir(savePath+'semiannual/'+each[0:4]):
                os.system('mkdir /Volumes/ST\ HDD/stock/report/sz/semiannual/'+each[0:4])
            fPdf = open(savePath+'semiannual/'+each[0:4]+'/'+stockCode+'_'+each[0:4]+'_'+each[5:7]+'_'+each[8:10]+'zc.pdf', 'wb')
            fPdf.write(getPdf.content)
    return pdfLinks

def get_report_quarter1_sz(stockCode, startTime, endTime):
    results = get_pdfTag_sz(stockCode, '010305', startTime, endTime)
    pdfLinks = dict()
    for each in results:
        if results[each].text.endswith('报告') or results[each].text.endswith('报告（更新后）') or results[each].text.endswith('报告（调整后）')or results[each].text.endswith('报告（更正后）') or results[each].text.endswith('报告（全文）') or results[each].text.endswith('全文（更新后）')or results[each].text.endswith('报告全文'):
            pdfLinks[each[:10]] = results[each].get('href')
            getPdf = requests.get('http://disclosure.szse.cn/'+results[each].get('href'))
            if not os.path.isdir(savePath+'quarter1/'+each[0:4]):
                os.system('mkdir /Volumes/ST\ HDD/stock/report/sz/quarter1/'+each[0:4])
            fPdf = open(savePath+'quarter1/'+each[0:4]+'/'+stockCode+'_'+each[0:4]+'_'+each[5:7]+'_'+each[8:10]+'f.pdf', 'wb')
            fPdf.write(getPdf.content)
        elif results[each].text.endswith('报告（已取消）') or results[each].text.endswith('全文（已取消）'):
            pdfLinks[each[:10]] = results[each].get('href')
            getPdf = requests.get('http://disclosure.szse.cn/'+results[each].get('href'))
            if not os.path.isdir(savePath+'quarter1/'+each[0:4]):
                os.system('mkdir /Volumes/ST\ HDD/stock/report/sz/quarter1/'+each[0:4])
            fPdf = open(savePath+'quarter1/'+each[0:4]+'/'+stockCode+'_'+each[0:4]+'_'+each[5:7]+'_'+each[8:10]+'fc.pdf', 'wb')
            fPdf.write(getPdf.content)
    return pdfLinks

def get_report_quarter3_sz(stockCode, startTime, endTime):
    results = get_pdfTag_sz(stockCode, '010307', startTime, endTime)
    pdfLinks = dict()
    for each in results:
        if results[each].text.endswith('报告') or results[each].text.endswith('报告（更新后）') or results[each].text.endswith('报告（调整后）')or results[each].text.endswith('报告（更正后）') or results[each].text.endswith('报告（全文）') or results[each].text.endswith('全文（更新后）')or results[each].text.endswith('报告全文'):
            pdfLinks[each[:10]] = results[each].get('href')
            getPdf = requests.get('http://disclosure.szse.cn/'+results[each].get('href'))
            if not os.path.isdir(savePath+'quarter3/'+each[0:4]):
                os.system('mkdir /Volumes/ST\ HDD/stock/report/sz/quarter3/'+each[0:4])
            fPdf = open(savePath+'quarter3/'+each[0:4]+'/'+stockCode+'_'+each[0:4]+'_'+each[5:7]+'_'+each[8:10]+'t.pdf', 'wb')
            fPdf.write(getPdf.content)
        elif results[each].text.endswith('报告（已取消）') or results[each].text.endswith('全文（已取消）'):
            pdfLinks[each[:10]] = results[each].get('href')
            getPdf = requests.get('http://disclosure.szse.cn/'+results[each].get('href'))
            if not os.path.isdir(savePath+'quarter3/'+each[0:4]):
                os.system('mkdir /Volumes/ST\ HDD/stock/report/sz/quarter3/'+each[0:4])
            fPdf = open(savePath+'quarter3/'+each[0:4]+'/'+stockCode+'_'+each[0:4]+'_'+each[5:7]+'_'+each[8:10]+'tc.pdf', 'wb')
            fPdf.write(getPdf.content)
    return pdfLinks

if __name__ == '__main__':
    szcodes = []
    for line in open('szcode.csv', 'r'):
        szcodes.append(line.strip())
    #lostcodes = []
    #with open('sz2016lost.pickle','rb') as fp:
        #lostcodes = pickle.load(fp)
    def get_reports_annual(stockCode):
        get_report_annual_sz(stockCode, '2016-01-01', '2016-12-31')

    def get_reports_semiannual(stockCode):
        get_report_semiannual_sz(stockCode, '2016-01-01', '2016-12-31')

    def get_reports_quarter1(stockCode):
        get_report_quarter1_sz(stockCode, '2001-01-01', '2006-12-31')
        
    def get_reports_quarter3(stockCode):
        get_report_quarter3_sz(stockCode, '2001-01-01', '2009-12-31')
    pool = Pool(processes=cpu_count())
    gtlog = pool.map(get_reports_quarter3, szcodes)
    pool.close() 
    pool.join()
