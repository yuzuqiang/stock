import pdfminer
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import HTMLConverter
from pdfminer.layout import LAParams
from io import StringIO
from io import open

def readPDF(pdfFile):
    rsrcmgr = PDFResourceManager()
    retstr = open('test.html','w')
    laparams = LAParams()
    device = HTMLConverter(rsrcmgr, retstr, laparams = laparams)

    process_pdf(rsrcmgr, device, pdfFile)
    device.close()

    content = retstr.getvalue()
    retstr.close()
    return content

if __name__ == '__main__':
    pdfFile = open('000004_2015_05_04n.pdf','rb')
    outputString = readPDF(pdfFile)
    print(outputString)
    pdfFile.close()
