from flask import Flask, render_template, request, url_for, redirect
from model import ProductRecommendationUserLevel

product_reco = ProductRecommendationUserLevel()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        name = request.form['Username']
        return redirect(url_for('submit', name=name))
    return render_template('homepage.html')

# Dynamic URLs based on user input
@app.route('/predict/<name>', methods=['GET', 'POST'])
def submit(name):
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