'''
Resume parser to give information to be evaluated in reviewer.py
'''
from docx import Document
import win32com.client as win32
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

import os


class Resume:
    '''
    Loads a resume Word document and parses it to automate some basic resume reviewing tasks
    '''

    def __init__(self, file_path):
        self.PATH = file_path
        
        self.document = Document(self.PATH) # load word document

        paragraph_list = self.document.paragraphs # find paragraphs in text
        self.content = []

        # add each paragraph to content list
        for paragraph in paragraph_list:
            self.content.append(paragraph.text)
    
    def page_count(self):
        '''
        Return the number of pages in the document/resume
        '''
        try:
            # open word document
            word = win32.gencache.EnsureDispatch('Word.Application')
            word.Visible = False
            doc_path = os.getcwd() + self.PATH
            doc = word.Documents.Open(doc_path)
            
            # get number of sheets
            doc.Repaginate()
            pages = doc.ComputeStatistics(2)

            # close word
            doc.Close()
            word.Quit()

            return pages
        
        # if error while loading document or getting page count
        except:
            print('[ERROR] Error Checking Page Count. Make sure document is not in Protected View Mode.')
        
        return None
    
    def get_text(self):
        '''
        Parses the content list to refine the analyzable text
        '''
        # Remove short words and phrases that aren't narrative
        for c in reversed(self.content):
            if len(c) < 5 or len(c.strip().split(' ')) < 5:
                self.content.remove(c)
        
        # Delete escape characters
        self.text = []
        for c in self.content:
            self.text.append(c.replace('\t', ''))
        
        return self.text
    
    def text_sentiment(self):
        '''
        Returns the calculated max sentiment of the narrative text
        '''
        nltk_sentiment = SentimentIntensityAnalyzer()

        # Make sure self.text actually has text in it
        try:
            self.text += ''
        except AttributeError:
            self.get_text()

        # Get sentiment values for each sentence
        neg, neu, pos, count = (0, 0, 0, 0)
        for paragraph in self.text:
            for sentence in paragraph.split('.'):
                sentiment_results = nltk_sentiment.polarity_scores(sentence.strip()) # get sentiment values for sentence
                count += 1
                neg += sentiment_results['neg']
                neu += sentiment_results['neu']
                pos += sentiment_results['pos']
        
        # Find maximum sentiment value
        sentiment_list = {'negative': neg/count, 'neutral': neu/count, 'positive': pos/count}
        maximum = max([neg/count, neu/count, pos/count])

        for _type, value in sentiment_list.items():
            if value == maximum:
                sentiment = (_type, value)

        return sentiment


if __name__ == "__main__":
    resume = Resume('./test_data/resume_template.docx')
    resume.get_text()
    print(f'Detected {resume.page_count()} pages in resume')
    sentiment = resume.text_sentiment()
    print(f'Detected tone of resume is {sentiment[0]} of value {sentiment[1]}')