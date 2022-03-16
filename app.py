from flask import Flask, render_template, request, url_for
import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

app = Flask(__name__)

def valid_input_check(username):
	df = pd.read_csv("Data/sample30.csv")
	list_of_valid_username  = df.reviews_username.unique().tolist()
	return username in list_of_valid_username

pro = r'picklefiles\TextProcessedData_20220316_1221.pkl'
rating = r"picklefiles\user_final_rating_20220316_1224.pkl"
model = r'picklefiles\SentimentAnalysisLogisticRegressionModel_20220313_2054.pkl'
features = r'picklefiles\VectorizerFeatures_20220316_1232.pkl'

pro_data = pickle.load(open(pro,'rb'))
ratings = pickle.load(open(rating,'rb'))
model_pred = pickle.load(open(model,'rb'))
features = pickle.load(open(features, 'rb'))

def get_top20_prod_based_on_recommendation(name):
    name = name.lower()
    
    return (ratings
                .loc[name]
                .sort_values(ascending=False)
                [:20]
                .index
                .tolist()
               )
    
def get_top5_prod_based_on_sentiment_of_reviews(top_20_prod):
    reviews_top_20 = pro_data.loc[pro_data.id.isin(top_20_prod), ['id', 'name', 'review']]
    vectorizer = TfidfVectorizer(ngram_range=(1,2), vocabulary=features)
    temp = vectorizer.fit_transform(reviews_top_20['review'])
    # temp = vectorizer.transform(reviews_top_20['review'])
    reviews_top_20['pred'] = model_pred.predict(temp)
    a = (reviews_top_20
         .groupby('id',as_index=False)
         .agg({'name':'max', 'pred': ['count','sum']})
        )
    a.columns = ['id', 'name', 'pred_total', 'pred_pos']
    a = (a
         .assign(pos_perc=round(a.pred_pos*100/a.pred_total, 2))
         .sort_values('pos_perc', ascending=False)
         .reset_index(drop=True)
    )
    return a.loc[:4, ['name', 'pos_perc']]

def _get_recommendation_from_username_(name):
    
    top20 = get_top20_prod_based_on_recommendation(name)
    top5 = get_top5_prod_based_on_sentiment_of_reviews(top20)
    return top5

@app.route("/", methods=['POST', "GET"])
def home():
    return render_template('homepage.html')

@app.route("/submit", methods=['POST', "GET"])
def submit():
    name = request.form.get('Username')
    if valid_input_check(name):
        df = _get_recommendation_from_username_(name)
        return render_template('return.html', name=name, tables=[df.to_html(classes='data')], titles=df.columns.values)
    else:
        return render_template('returnfail.html', name=name)
if __name__ == '__main__':
    app.run()