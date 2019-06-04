import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split

from src.generate_features import choose_features
from src.train_model import split_data
from src.score_model import score_model

def test_choose_features():
    # load sample test data
    data = pd.read_csv("test_data.csv")

    features = ['size_bytes', 'price', 'rating_count_tot', 'rating_count_ver',
    			'cont_rating','prime_genre','sup_devices_num', 'ipadSc_urls_num', 'lang_num', 'app_desc']

    # desired output dataframe
    output_df = data[['size_bytes', 'price', 'rating_count_tot', 'rating_count_ver', 'user_rating',
    			'cont_rating','prime_genre','sup_devices_num', 'ipadSc_urls_num', 'lang_num', 'app_desc']]
    
    # raise AssertionError if dataframes do not match
    assert output_df.equals(choose_features(df=data, features_to_use=features, target='user_rating'))

def test_split_data():
    # load sample test data
    data = pd.read_csv("test_data.csv")
    X_df = data.drop('user_rating',axis=1)
    y_df = data['user_rating']
    X_train, X_test, y_train, y_test = train_test_split(X_df, y_df, test_size=0.3, random_state=123)

    # split data using the function
    X, y = split_data(X_df, y_df, train_size=0.7, test_size=0.3, random_state=123)

    # raise AssertionError if keys do not match
    assert X_train.equals(X['train'])
    assert y_test.equals(y['test'])

def test_evaluate_model():
    # desired predcited score 
    score_output = np.array([4.225851, 4.238039, 4.077815, 1.704345])
    #test data input
    x_input = {'id':[1,2,3,4],
                'size_bytes': [41779200, 288161792, 217378816, 39596032],
                'price': [0.688134639, 0.688134639, 0, 0],
                'sup_devices_num': [43,43,38,37],
                'ipadSc_urls_num': [5,5,5,3],
                'lang_num': [0.693147181, 1.098612289, 0.693147181, 1.098612289],
                'rating_count_before': [5.093750201, 5.135798437, 2.397895273, 0],
                'isNotFree': [1,1,0,0],
                '12+': [0,0,0,0],
                '17+': [0,0,1,0],
                '4+': [1,1,0,1],
                'Education':[0,0,0,0],
                'Entertainment':[0,0,0,0],
                'Games': [1,1,1,1],
                'isGame':[1,1,0,1],
                'descLen':[7.529406458, 7.507690078, 6.989335266,5.117993812]}
    #label_input = {'user_rating':[4.5，3.5，4，0]}

    x_df = pd.DataFrame(x_input)

    #model predictions
    target_score = score_model(x_df, '../models/app-prediction.pkl')
    target_score = np.around(target_score, decimals=6)

    # raise AssertionError if dataframes do not match
    assert np.array_equal(score_output, target_score)




