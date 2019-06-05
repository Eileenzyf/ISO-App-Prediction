import traceback
import pickle
import sklearn
import pandas as pd
import os
import sys
sys.path.insert(0, 'src')
from sklearn.ensemble import RandomForestRegressor
from flask import render_template, request, redirect, url_for
import logging.config
#from app import app
# from app.models import Tracks
import numpy as np
from flask import Flask
from Create_database import user_input
from flask_sqlalchemy import SQLAlchemy
from os import path


# Initialize the Flask application
app = Flask(__name__)

# Configure flask app from flask_config.py
app.config.from_pyfile('../config/flask_config.py')

# Define LOGGING_CONFIG in flask_config.py - path to config file for setting
# up the logger (e.g. config/logging/local.conf)
logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logger = logging.getLogger("IOS-app")
logger.debug('Test log')
# Initialize the database
db = SQLAlchemy(app)


@app.route('/')
def index():
    """Main view that depplays the homepage and allow the user to start rating. 
    Returns: rendered html template
    """
    #return the homepage
    try:
        return render_template('app.html')
    except:
        logger.warning("Not able to display homepage, error page returned")
        return render_template('error.html')


@app.route('/add', methods=['POST','GET'])
def add_entry():
    """View that process a POST with new user_input
    :return: direct to prediction page
    """

    #downlaod the data from the web
    try:
        logger.info("start retrieving!")
        size_bytes=request.form['size_bytes']
        price=request.form['price']
        rating_count_tot=request.form['rating_count_tot']
        rating_count_ver=request.form['rating_count_ver']
        cont_rating=request.form['cont_rating']
        prime_genre=request.form['prime_genre']
        sup_devices_num=request.form['sup_devices_num']
        ipadSc_urls_num=request.form['ipadSc_urls_num']
        lang_num=request.form['lang_num']
        app_desc = request.form['app_desc']
        logger.info("all inputs retrieved!")


        # load trained model
        path_to_tmo = app.config["PATH_TO_MODEL"]
        with open(path_to_tmo, "rb") as f:
            model = pickle.load(f)
        logger.info("model loaded!")

        #create a dataframe to store inputs for prediction
        df = pd.DataFrame(columns=["size_bytes", "price", "rating_count_tot", "rating_count_ver",
                      "cont_rating","prime_genre","sup_devices_num", "ipadSc_urls_num", "lang_num", "app_desc"])

        df.loc[0] = [size_bytes, price, rating_count_tot, rating_count_ver, cont_rating, prime_genre, sup_devices_num, ipadSc_urls_num, lang_num, app_desc]

        #change the datatype to predict later
        df.size_bytes = df.size_bytes.astype("float")
        df.price = df.price.astype("float")
        df.rating_count_tot = df.rating_count_tot.astype("float")
        df.rating_count_ver = df.rating_count_ver.astype("float")
        df.sup_devices_num = df.sup_devices_num.astype("int")
        df.ipadSc_urls_num = df.ipadSc_urls_num.astype("int")
        df.lang_num = df.lang_num.astype("int")

        #generate necessary features for the model
        df['rating_count_before'] = df['rating_count_tot'] - df['rating_count_ver']
        ##create 'isnotfree' variables
        df['isNotFree'] = df['price'].apply(lambda x: 1 if x > 0 else 0)
        df['price'] = np.log(df['price']+1)
        df['rating_count_tot'] = np.log(df['rating_count_tot']+1)
        df['rating_count_ver'] = np.log(df['rating_count_ver']+1)
        df['lang_num'] = np.log(df['lang_num']+1)
        df['rating_count_before'] = np.log(df['rating_count_before']+1)
        cont_rat_dum=pd.get_dummies(df.cont_rating)
        df= df.join(cont_rat_dum)
        df['genre'] = df['prime_genre'].apply(lambda x: x if x =="Games" or x== "Entertainment" or x=="Education" else "Other")
        genre_dum = pd.get_dummies(df['genre'])
        df= df.join(genre_dum)
        genre_list = ['Games', 'Entertainment','Education','Other']
        for g in genre_list:
            if g not in df.columns:
                df[g] = 0
        cont_list = ["4+", "7+", "9+", "12+"]
        for c in cont_list:
            if c not in df.columns:
                df[c] = 0
        df.loc[:, 'isGame'] = df['app_desc'].apply(lambda x: 1 if 'game' in x.lower() else 0)
        df.loc[:, 'descLen'] = df['app_desc'].apply(lambda x: len(x.lower()))
        df['descLen'] = np.log(df['descLen'])

        #drop the uneecessary column to match the model features
        df = df.drop(["cont_rating","genre","prime_genre", "app_desc", "rating_count_tot", "rating_count_ver", "Other","12+"], axis = 1)
        df['4+'] = df['4+'].astype('float')


        #predic the rating            
        rating = model.predict(df)
        logger.info('prediction made: %0.3f' % rating)

        #add user input entry to user_input database
        user1 = user_input(size_bytes=float(size_bytes),price=float(price),rating_count_tot=int(rating_count_tot),
            rating_count_ver=int(rating_count_ver), cont_rating=str(cont_rating), prime_genre=str(prime_genre),
            sup_devices_num= int(sup_devices_num), ipadSc_urls_num=int(ipadSc_urls_num), lang_num=int(lang_num),
            app_desc = str(app_desc), prediction  = float(rating))

        db.session.add(user1)
        db.session.commit()
        logger.info("New entry added")

        result = '%0.1f' % rating

        print(db)

        #direct to the prediction page
        return render_template('prediction.html', result=result)

    except:
        traceback.print_exc()
        logger.warning("Not able to display prediction, error page returned")
        return render_template('error.html')

if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])
