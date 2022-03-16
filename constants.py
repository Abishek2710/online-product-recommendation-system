# required Directories for file and data
RAW_DATA_DIR = "Data/sample30.csv"
PROCESSED_DATA_DIR = 'picklefiles/TextProcessedData_20220316_1959.pkl'
RATING_FILE_DIR = 'picklefiles/user_final_rating_20220316_2036.pkl'
MODEL_DIR = 'picklefiles/SentimentAnalysisLogisticRegressionModel_20220316_2017.pkl'
FEATURES_DIR =  'picklefiles/VectorizerFeatures_20220316_1959.pkl'

# Final N value for filtering and display
PRODUCT_RECO_N = 20
FINAL_N = 5

# Final columns to be displayed
FINAL_COLUMNS_TO_BE_DISPLAYED = ['name', 'brand', 'pos_perc']