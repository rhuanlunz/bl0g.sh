from time import localtime, strftime
from os import path, listdir

from mistune import html
from werkzeug.exceptions import NotFound
from flask import Flask, render_template, redirect

ARTICLES_FOLDER = 'articles/'

app = Flask(__name__)
app.template_folder = 'views/pages'
app.static_folder = 'views/static'

def get_modification_time(file):
	return strftime('%d/%m/%Y às %Hh%Mmin', localtime(path.getmtime(ARTICLES_FOLDER + file)))

@app.route('/artigo/<article_name>', methods=['GET'])
def article(article_name=None):
	if not article_name or article_name == None:
		return redirect('/')

	article_path = ARTICLES_FOLDER + article_name
	if not path.exists(article_path):
		raise NotFound

	with open(article_path, 'r') as f:
		article_content = f.read()

	article_html = html(article_content)
	article_modification_time = get_modification_time(article_name)
	return render_template(
		'article.html', 
		article_html=article_html, 
		article_name=article_name, 
		article_modification_time=article_modification_time
	)

@app.route('/artigos', methods=['GET'])
def articles():
	files = listdir(ARTICLES_FOLDER)
	articles = []

	for file in files:
		articles.append({
			"name": file,
			"modification_time": get_modification_time(file)
		})

	return render_template('articles.html', article_list=articles)

# next version
# @app.route('/whoami', methods=['GET'])
# def whoami():
# 	return render_template('whoami.html')

@app.route('/', methods=['GET'])
def index():
	return render_template('index.html')

@app.errorhandler(NotFound)
def not_found(e):
	return render_template('404.html'), 404
