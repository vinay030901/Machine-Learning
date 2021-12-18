from flask import Flask, request,redirect,render_template,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random,string

import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///urls.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)
shorts=[]

data={}

@app.before_first_request
def create_tables():
    db.create_all()

class Text(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(2000),nullable=False)
    short = db.Column(db.String(1000),nullable=False)
    date_created  = db.Column(db.DateTime,default=datetime.utcnow)

    def __init__(self,text,short):
        self.text =text
        self.short = short
    
    def __repr__(self)->str:
        return f"{self.sno} - {self.title}"
    
def _create_frequency_table(text_string) -> dict:
    """
    we create a dictionary for the word frequency table.
    For this, we should only use the words that are not part of the stopWords array.
    Removing stop words and making frequency table
    Stemmer - an algorithm to bring words to its root word.
    :rtype: dict
    """
    stopWords = set(stopwords.words("english"))
    words = word_tokenize(text_string)
    ps = PorterStemmer()

    freqTable = dict()
    for word in words:
        word = ps.stem(word)
        if word in stopWords:
            continue
        if word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1

    return freqTable


def _score_sentences(sentences, freqTable) -> dict:
    """
    score a sentence by its words
    Basic algorithm: adding the frequency of every non-stop word in a sentence divided by total no of words in a sentence.
    :rtype: dict
    """

    sentenceValue = dict()

    for sentence in sentences:
        word_count_in_sentence = (len(word_tokenize(sentence)))
        word_count_in_sentence_except_stop_words = 0
        for wordValue in freqTable:
            if wordValue in sentence.lower():
                word_count_in_sentence_except_stop_words += 1
                if sentence[:10] in sentenceValue:
                    sentenceValue[sentence[:10]] += freqTable[wordValue]
                else:
                    sentenceValue[sentence[:10]] = freqTable[wordValue]

        if sentence[:10] in sentenceValue:
            sentenceValue[sentence[:10]] = sentenceValue[sentence[:10]] / word_count_in_sentence_except_stop_words

        '''
        Notice that a potential issue with our score algorithm is that long sentences will have an advantage over short sentences. 
        To solve this, we're dividing every sentence score by the number of words in the sentence.
        
        Note that here sentence[:10] is the first 10 character of any sentence, this is to save memory while saving keys of
        the dictionary.
        '''

    return sentenceValue


def _find_average_score(sentenceValue) -> int:
    """
    Find the average score from the sentence value dictionary
    :rtype: int
    """
    sumValues = 0
    for entry in sentenceValue:
        sumValues += sentenceValue[entry]

    """[summary]

    Returns:
        [type]: [description]
    """    # Average value of a sentence from original text
    average = (sumValues / len(sentenceValue))

    return average


def _generate_summary(sentences, sentenceValue, threshold):
    sentence_count = 0
    summary = ''

    for sentence in sentences:
        if sentence[:10] in sentenceValue and sentenceValue[sentence[:10]] >= (threshold):
            summary += " " + sentence
            sentence_count += 1

    return summary


def run_summarization(text):
    # 1 Create the word frequency table
    freq_table = _create_frequency_table(text)

    '''
    We already have a sentence tokenizer, so we just need 
    to run the sent_tokenize() method to create the array of sentences.
    '''

    # 2 Tokenize the sentences
    sentences = sent_tokenize(text)

    # 3 Important Algorithm: score the sentences
    sentence_scores = _score_sentences(sentences, freq_table)

    # 4 Find the threshold
    threshold = _find_average_score(sentence_scores)

    # 5 Important Algorithm: Generate the summary
    summary = _generate_summary(sentences, sentence_scores, 1.3 * threshold)

    return summary

@app.route('/',methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        text=request.form["text"]
        t = Text.query.filter_by(text=text).first()
        if t:
            return redirect(url_for("redirect_new_url",short=t.short))
        else:
            while(True):
               short=run_summarization(text)
               if short not in shorts:
                    break
            shorts.append(short)
            obj = Text(text=text,short=short)
            db.session.add(obj)
            db.session.commit()
            data[short]=text
            allurl = Text.query.all()
            return redirect(url_for('redirect_new_url',short=short))
    
    return render_template("index.html")

@app.route('/history')
def history():
    return render_template("history.html",allurl=Text.query.all())

@app.route('/display/<short>')
def redirect_new_url(short):
    return render_template('shorten.html',short_url=short)

@app.route('/delete/<int:sno>')
def delete(sno):
    url = Text.query.filter_by(sno=sno).first()
    db.session.delete(url)
    db.session.commit()
    return redirect("/history")

if __name__ == '__main__':
    app.run(debug=True)