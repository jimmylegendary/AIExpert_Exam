import fitz
import json
import os

ans_keyword = [
    '정답',
    '(답)',
    'Answer',
    '답:',
    '답변:',
]

ans_block = []
i = 0
class PDFData():
    def __init__(self, filename):
        self.text = ''
        self.img = None
        self.filename = filename
        
    def parse_pdf(self):
        global i
        pdf_file = fitz.open(self.filename)
        for page in pdf_file:
            pix = page.get_pixmap()
            json_data = page.get_text('json')
            data = json.loads(json_data)
            for block in data['blocks']:
                if block['type'] != 0: continue
                for line in block['lines']:
                    for span in line['spans']:
                        text = span['text']
                        is_ans = False
                        for keyword in ans_keyword:
                            if keyword in text:
                                is_ans = True
                        if is_ans:
                            # print(text)
                            ans_block.append((page,block))
                            mat = fitz.Matrix(2, 2)  # zoom factor 2 in each direction
                            bbox = block['bbox']
                            clip = fitz.Rect(bbox)  # the area we want
                            pix = page.get_pixmap(matrix=mat, clip=clip)
                            pix.save(f'{i}.png','png')
                            i += 1
                        
        # output = 'outfile.png'
        # pix.save(output)
        
if __name__ == '__main__':
    filename = 'test2.pdf'
    root_dir = '문제은행'
    for (root, dirs, files) in os.walk(root_dir):
        if len(files) > 0:
            for file_name in files:
                if 'pdf' in file_name:
                    pdfdata = PDFData(f'{root}/{file_name}')
                    pdfdata.parse_pdf()
    
    # for i, (page, block) in enumerate(ans_block):
    #     mat = fitz.Matrix(2, 2)  # zoom factor 2 in each direction
    #     bbox = block['bbox']
    #     clip = fitz.Rect(bbox)  # the area we want
    #     pix = page.get_pixmap(matrix=mat, clip=clip)
    #     pix.save(f'{i}.png','png')
        # for line in block['lines']:
        #     for span in line['spans']:
        #         text = span['text']
        #         print(text.strip('\n'))