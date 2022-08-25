import PyPDF2
import fitz

class PDFData():
    def __init__(self, filename):
        self.text = ''
        self.img = None
        self.filename = filename
        
    def parse_pdf(self):
        # pdf_file = open(self.filename, 'rb')
        # read_pdf = PyPDF2.PdfFileReader(pdf_file)
        # number_of_pages = read_pdf.getNumPages()
        # page = read_pdf.getPage(0)
        # page_content = page.extractText()
        # print(page_content)
        pdf_file = fitz.open(self.filename)
        page = pdf_file[0]
        pix = page.get_pixmap()
        output = 'outfile.png'
        pix.save(output)
        
if __name__ == '__main__':
    filename = 'test2.pdf'
    pdfdata = PDFData(filename)
    pdfdata.parse_pdf()