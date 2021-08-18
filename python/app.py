import markov
import parse
import scrape
import os

from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

app = Flask(__name__, template_folder='../templates')

# don´t upload to github/glitch as plaintext
#need to change now woops.
app.config['SECRET_KEY'] = 'EtsnSkuUKV:>qx?T^*eahFwq+[c!5}'
Bootstrap(app)

class MarkovForm(FlaskForm):
    authors = StringField("Please enter your favorite authors, separated by ',' (no spaces pls)\n"
        + "If more than one author is entered, their works will be combined into a single markov chain)", validators=[DataRequired()])
    lang = StringField("Enter your language (sorry these instructions are only available in English)", validators=[DataRequired()])
    p_length = StringField('Phrase length? (numbers only) (3 works well): ', validators=[DataRequired()])
    punc = SelectField('Keep punctuation?', choices=['Yes', 'No'], validators=[DataRequired()])
    s_length = StringField("Sentence length? (numbers only): ", validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = MarkovForm()
    message = ""
    if form.validate_on_submit():
        authors = form.authors.data.split(',')
        lang = form.lang.data
        p_length = int(form.p_length.data)
        s_length = int(form.s_length.data)
        punc = form.punc.data
        directories = []
        for a in authors:
            directories.append(a.replace(" ", "_").title())
        form.authors.data = ""
        form.lang.data = ""
        form.p_length.data = ""
        form.s_length.data = ""
        os.chdir(os.pardir)
        if (not already_downloaded(directories, os.path.join(os.path.abspath(os.getcwd()), 'data'))):
            for a in authors:
                scrape.download(a,lang)
            for i in range(len(directories)):
                directories[i] = markov.author_freq(directories[i], p_length, punc)
            m = markov.merge_authors(directories)
            message = markov.chain(m, s_length, p_length)
        elif already_downloaded(directories, os.path.join(os.getcwd(), 'data')):
            for i in range(len(directories)):
                directories[i] = markov.author_freq(directories[i], p_length, punc)
            m = markov.merge_authors(directories)
            message = markov.chain(m, s_length, p_length)
        else:
            message = "That author is not in our database."
    return render_template('index.html', form=form, message=message)

def already_downloaded (folders, path):
    for f in folders:
        if (os.path.isdir(os.path.join(path, f))):
            return True
    return False