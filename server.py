from flask import Flask, url_for, render_template, request, send_from_directory
import bball_ref

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', stuff=[])

@app.route('/query')
def query_results():
    query = request.values.get("query_form")
    rows = bball_ref.getRows(query)
    return rows

if __name__ == '__main__':
    app.run(debug=True)