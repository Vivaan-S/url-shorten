import flask, requests, replitdb

db = replitdb.Client()

app = flask.Flask(__name__)

@app.route('/')
def main():
	return flask.render_template('index.html', url=None)

@app.route('/Invalid URL')
def invalid():
	return flask.redirect('/')

@app.route('/', methods=['POST'])
def add():	
	newURL = flask.request.form['add']
	valid = False
	allURLs = db.view('allURLs')
	
	try:
		requests.get(newURL)
		valid = True
	except:
		url = 'Invalid URL'
	if valid:
		lastNum = int(allURLs[-1], base=16)
		newNum = str(hex(lastNum + 1))[2:]
		allURLs.append(newNum)
		db.set(allURLs=allURLs)
		db.set_dict({newNum:newURL})
		url = 'https://url.vivaansa.repl.co' + newNum
	return flask.render_template('index.html', url=url, valid=valid)

@app.route('/<num>')
def url(num):
	url = db.view(num)
	if url != None:
		return flask.redirect(url)
	else:
		return flask.render_template('index.html')

@app.route('/favicon.ico')
def favicon():
	return flask.send_file('favicon.ico')


app.run('0.0.0.0')
