'''
'''

from docx import Document
import win32com.client as win32
import os


class Resume:

    def __init__(self, path):
        self.PATH = path # set resume path
        
        self.document = Document(self.PATH) # load word document

        paragraph_list = self.document.paragraphs # find paragraphs in text
        self.content = []

        # add each paragraph to content list
        for paragraph in paragraph_list:
            self.content.append(paragraph.text)

    def get_content(self):
        return self.content
    
    def get_page_count(self):
        try:
            # open word document
            word = win32.gencache.EnsureDispatch('Word.Application')
            word.Visible = False
            doc_path = os.getcwd() + self.PATH
            doc = word.Documents.Open(doc_path)
            
            # get number of sheets
            doc.Repaginate()
            self.pages = doc.ComputeStatistics(2)

            # close word
            doc.Close()
            word.Quit()

            return self.pages
        
        # if error while loading document or getting page count
        except:
            print('[ERROR] Error Checking Page Count. Make sure document is not in Protected View Mode.')
        
        return None

    
if __name__ == "__main__":
    resume = Resume('./test_data/resume_template.docx')
    # resume.print_content()
    print(f'Detected {resume.get_page_count()} pages in resume')