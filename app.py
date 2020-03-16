from flask import Flask, render_template, redirect, request, url_for, abort, session, jsonify
import json
import os.path

app = Flask(__name__)
app.secret_key = "itssecretkey"


@app.route('/')
def home():
    return render_template('index.html', codes=session.keys())


@app.route('/result/done', methods=['GET', 'POST'])
def result():
    mapping = {}
    if request.method == 'POST':
        url = request.form['url']
        code = request.form['code']
        if os.path.exists('data.json'):
            with open('data.json') as datafile:
                mapping = json.load(datafile)
        if code in mapping.keys():
            return redirect(url_for('home'))
        mapping[code] = {'url': url}
        with open('data.json', 'w') as database:
            json.dump(mapping, database)
            session[code] = True
            return " "
    else:
        return redirect(url_for('home'))


@app.route('/<string:code>')
def map_route(code):
    if os.path.exists('data.json'):
        with open('data.json') as datafile:
            mapping = json.load(datafile)
    if code in mapping.keys():
        if 'url' in mapping[code].keys():
            return redirect(mapping[code]['url'])
    return abort(404)


@app.errorhandler(404)
def error_function(error):
    return "error bro"


@app.route('/api')
def session_api():
    return jsonify(list(session.keys()))


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
