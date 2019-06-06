import logging
import argparse
import yaml
import os
import subprocess
import re
import pandas as pd
import numpy as np

from src.load_data import load_data

logging.basicConfig(level=logging.INFO, filename="logfile")
logger = logging.getLogger(__name__)


def choose_features(df, features_to_use=None, target=None,save_path=None, **kwargs):
	"""Reduces the dataset to the features_to_use. Will keep the target if provided.
	Args:
		df (:py:class:`pandas.DataFrame`): DataFrame containing the features
		features_to_use (:obj:`list`): List of columnms to extract from the dataset to be features
		target (str, optional): If given, will include the target column in the output dataset as well.
		save_path (str, optional): If given, will save the feature set (and target, if applicable) to the given path.
		**kwargs:
	Returns:
		X (:py:class:`pandas.DataFrame`): DataFrame containing extracted features (and target, it applicable)
	"""

	logger.debug("Choosing features")

	if features_to_use is not None:
		features = []
		for column in df.columns:
			# Identifies if this column is in the features to use 
			if column in features_to_use or column == target:
				features.append(column)

		logger.debug(features)
		X = df[features]
	else:
		logger.debug("features_to_use is None, df being returned")
		X = df
	
	if save_path is not None:
		X.to_csv(save_path, **kwargs)


	return X


def get_target(df, target, save_path=None, **kwargs):
	"""set the target column of the dataset"""

	y = df[target]

	if save_path is not None:
		y.to_csv(save_path, **kwargs)

	return y.values


def generate_features(df, save_features=None, **kwargs):
	"""Add transformed features into original dataframe.
	Args:
		df (:py:class:`pandas.DataFrame`): DataFrame containing the data to be transformed into features.
		save_features (str, optional): If given, the feature set will be saved to this path.
	Returns:
	df (:py:class:`pandas.DataFrame`): DataFrame containing original features and transformed features.

	"""

	df= choose_features(df, **kwargs["choose_features"])

	# generate new features
	#create 'rating_count_before' vairable
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
	genre_dum = pd.get_dummies(df.genre)
	df= df.join(genre_dum)
	df.loc[:, 'isGame'] = df['app_desc'].apply(lambda x: 1 if 'game' in x.lower() else 0)
	df.loc[:, 'descLen'] = df['app_desc'].apply(lambda x: len(x.lower()))
	df['descLen'] = np.log(df['descLen'])

	if save_features is not None:
		df.to_csv(save_features,index=False)

	return df
	
def run_features(args):
	"""Orchestrates the generating of features from commandline arguments."""
	with open(args.config, "r") as f:
		config = yaml.load(f)

	if args.input is not None:
		df = pd.read_csv(args.input, index_col=0)
	elif "load_data" in config:
		df = load_data(config["load_data"])
	else:
		raise ValueError("Path to CSV for input data must be provided through --csv or "
						"'load_data' configuration must exist in config file")

	df_feature = generate_features(df, **config["generate_features"])

	if args.output is not None:
		df_feature.to_csv(args.output, index=False)
		logger.info("Features saved to %s", args.output)

	return df

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Generate Features")
	parser.add_argument('--config', help='path to yaml file')
	parser.add_argument('--input', help='path to dataset')
	parser.add_argument('--output', help='Path to where the dataset should be saved to')

	args = parser.parse_args()

	run_features(args)
