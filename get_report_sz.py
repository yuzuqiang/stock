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
            pdfLinks[each[:-1]] = results[each].get('href')
            getPdf = requests.get('http://disclosure.szse.cn/'+results[each].get('href'))
            if not os.path.isdir(savePath+'annual/'+each[0:4]):
                os.system('mkdir /Volumes/ST\ HDD/stock/report/sz/annual/'+each[0:4])
            fPdf = open(savePath+'annual/'+each[0:4]+'/'+stockCode+'_'+each[0:4]+'_'+each[5:7]+'_'+each[8:-1]+'n.pdf', 'wb')
            fPdf.write(getPdf.content)
        elif results[each].text.endswith('报告（已取消）'):
            pdfLinks[each[:-1]] = results[each].get('href')
            getPdf = requests.get('http://disclosure.szse.cn/'+results[each].get('href'))
            if not os.path.isdir(savePath+'annual/'+each[0:4]):
                os.system('mkdir /Volumes/ST\ HDD/stock/report/sz/annual/'+each[0:4])
            fPdf = open(savePath+'annual/'+each[0:4]+'/'+stockCode+'_'+each[0:4]+'_'+each[5:7]+'_'+each[8:-1]+'nc.pdf', 'wb')
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
        get_report_annual_sz(stockCode, '2010-01-01', '2014-12-31')

    pool = Pool(processes=cpu_count())
    gtlog = pool.map(get_reports_annual, szcodes)
    pool.close() 
    pool.join()
