from flask import Flask, render_template, request, url_for
from model import ProductRecommendationUserLevel

product_reco = ProductRecommendationUserLevel()

app = Flask(__name__)

@app.route("/", methods=['POST', "GET"])
def home():
    return render_template('homepage.html')

@app.route("/submit", methods=['POST', "GET"])
def submit():
    name = request.form.get('Username')
    if product_reco.valid_input_check(name):
        df = product_reco._get_recommendation_from_username_(name)
        return render_template('return.html',
                               name=name,
                               tables=[df.to_html(classes='data')],
                               titles=df.columns.values
                               )
    else:
        return render_template('returnfail.html', name=name)

if __name__ == '__main__':
    app.run()