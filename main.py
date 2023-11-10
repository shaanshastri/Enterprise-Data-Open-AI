from flask import Flask, render_template, request
from nlp import convert_nlp_to_sql_poc
from tabulate import tabulate

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('chat.html')


@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    return get_Chat_response(msg)


@app.route('/call_model', methods=['POST'])
def get_Chat_response(txt):
    response, data = convert_nlp_to_sql_poc(txt)

    if data is None:
        return render_template('index_new.html', response=response)
    # Convert the DataFrame to a tabular format with borders
    table = tabulate(data, headers='keys', tablefmt='fancy_grid')
    # Print the tabular format
    print(table)
    return render_template('index.html', tables=[data.to_html(classes='data')], titles=data.columns.values,
                           response=response)


if __name__ == "__main__":
    app.run()
