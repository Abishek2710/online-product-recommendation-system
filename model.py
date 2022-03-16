import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from constants import *

class ProductRecommendationUserLevel():
    """
    Class for calculate the product recommendation at a User level
    """
    def __init(self):
        self

    def valid_input_check(self, name):
        """
        Function to check if the input value from the user is valid or not.
        Defintion of valid: Should be present in our input data list (based on assumption that no new user will be included)
        """
        df = pd.read_csv(RAW_DATA_DIR)
        list_of_valid_username  = df.reviews_username.unique().tolist()
        return name in list_of_valid_username
    

    def get_top20_prod_based_on_recommendation(self, name):
        """
        Function to return top N (default=20) products based on user-user matrix
        input: name: username from the user
        output: list: List of top N products using user-user matrix
        """
        name = name.lower()

        # Load user user matrix file
        ratings = pickle.load(open(RATING_FILE_DIR,'rb'))
        return (ratings
                    .loc[name]
                    .sort_values(ascending=False)
                    [:PRODUCT_RECO_N]
                    .index
                    .tolist()
                )
        
    def get_top5_prod_based_on_sentiment_of_reviews(self, top_20_prod):
        """
        Function to return the top N (default=5) products based on the positive % of reviews
        input: top_20_prod: List of Top N products from USER USER matrix
        output: dataframe contains the product details
        """
        # Load necessary files
        processed_data = pickle.load(open(PROCESSED_DATA_DIR,'rb'))
        features = pickle.load(open(FEATURES_DIR, 'rb'))
        model_pred = pickle.load(open(MODEL_DIR,'rb'))

        # Filter reviews only for required number of products
        reviews_top_20 = processed_data.loc[processed_data.id.isin(top_20_prod), ['id', 'name', 'review']]
        
        # Vectorize the input reviews 
        vectorizer = TfidfVectorizer(ngram_range=(1,2), vocabulary=features)
        vectorized_input = vectorizer.fit_transform(reviews_top_20['review'])

        # Predicts from the class for reviews
        reviews_top_20['pred'] = model_pred.predict(vectorized_input)

        # Aggregate the predictions and calculate the positive percentage of reviews
        df = (reviews_top_20
              .groupby('id',as_index=False)
              .agg({'name':'max', 'pred': ['count','sum']})
              )
        df.columns = ['id', 'name', 'pred_total', 'pred_pos']
        
        # Calculate the positve percentage of reviews 
        df = (df
              .assign(pos_perc=round(df.pred_pos*100/df.pred_total, 2))
              .sort_values('pos_perc', ascending=False)
              .reset_index(drop=True)
              )

        return df.loc[:(FINAL_N-1), FINAL_COLUMNS_TO_BE_DISPLAYED]

    def _get_recommendation_from_username_(self, name):
        """
        Function to return the TOP N recommended products from the username shared by the user
        """
        product_reco = ProductRecommendationUserLevel()
        top20_users = product_reco.get_top20_prod_based_on_recommendation(name)
        top5_products = product_reco.get_top5_prod_based_on_sentiment_of_reviews(top20_users)
        return top5_products
