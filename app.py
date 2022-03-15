from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

def valid_input_check(username):
	df = pd.read_csv(r"Data\sample30.csv")
	list_of_valid_username  = df.reviews_username.unique().tolist()
	return username in list_of_valid_username

@app.route("/", methods=['POST', "GET"])
def home():
    return render_template('homepage.html')

@app.route("/submit", methods=['POST', "GET"])
def submit():
    name = request.form.get('Username')
    return render_template('return.html', check=valid_input_check(name), name=name)

if __name__ == '__main__':
    app.run()