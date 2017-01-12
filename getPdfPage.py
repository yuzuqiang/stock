from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine
from PyPDF2 import PdfFileWriter, PdfFileReader
from multiprocessing import Pool, cpu_count
import os
def get_pageNum(pdffile):
    fp = open(pdffile, 'rb')
    parser = PDFParser(fp)
    doc = PDFDocument()
    parser.set_document(doc)
    doc.set_parser(parser)
    doc.initialize('')
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    pageNum = 0
    for page in doc.get_pages():
        pageNum = pageNum+1
        interpreter.process_page(page)
        layout = device.get_result()
        for lt_obj in layout:
            if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                if ('无限售条件股东' or '流通股股东') in lt_obj.get_text():
                    return 'ok', pageNum
    return 'no', pdffile
def getMyPdfPage(pdffile):
    pageNum = get_pageNum(pdffile)
    if pageNum[0] == 'no':
        return pageNum[1]
    output = PdfFileWriter()
    ipdf = PdfFileReader(open(pdffile, 'rb'))
    try:
        for i in [pageNum[1]-1, pageNum[1]]:
            page = ipdf.getPage(i)
            output.addPage(page)
        wpath = '/Volumes/ST HDD/stock/report/szscrap/annual/2016/'
        with open(wpath+pdffile[-22:-4]+'S.pdf', 'wb') as f:
            output.write(f)
    except: 
        return pageNum[1]
    return None

if __name__ == '__main__':
    rpath = '/Volumes/ST HDD/stock/report/sz/annual/2016/'
    data = os.listdir(rpath)
    data.remove('.DS_Store')
    results = []
    for each in data:
        result = getMyPdfPage(rpath+each)
        if result != None:
            results.append(result)
    print(results)
