from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO

import os

def set_interpreter():
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    return { 'retstr': retstr, 'device': device, 'interpreter': interpreter }

def convert_pdf_to_txt(path):
    fp = file(path, 'rb')
    si = set_interpreter()
    retstr = si['retstr']
    device = si['device']
    interpreter = si['interpreter']
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()
    page_counter = 0

    for pageNumber, page in enumerate(PDFPage.get_pages(fp, pagenos, maxpages=maxpages,password=password,caching=caching, check_extractable=True)):
        interpreter.process_page(page)
        fpp = file('pagetext_%d.txt' % page_counter, 'w+')
        fpp.write(retstr.getvalue())
        fpp.close()
        page_counter += 1
        si = set_interpreter()
        retstr = si['retstr']
        device = si['device']
        interpreter = si['interpreter']

    fp.close()
    device.close()
    retstr.close()
    return text

print (convert_pdf_to_txt(os.path.dirname(os.path.realpath('filename.pdf')) + "/filename.pdf"))

