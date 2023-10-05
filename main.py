from flask import Flask, render_template, request
from nlp import convert_nlp_to_sql_poc

app = Flask(__name__)


@app.route("/")
def homepage():
    return render_template('index.html')


@app.route('/call_model', methods=['POST'])
def call_model():
    # call your Python function here
    usr_ip = request.form.to_dict()
    txt = usr_ip["question"]
    response = convert_nlp_to_sql_poc(txt)
    return render_template('result.html', response=response)


if __name__ == "__main__":
    app.run(debug=True)
