import argparse
import logging
import pickle
import os
import subprocess
import re
import yaml

import numpy as np
import pandas as pd
import sklearn
from sklearn import model_selection
from sklearn import metrics
from sklearn.ensemble import RandomForestRegressor

from src.load_data import load_data
from src.generate_features import choose_features, get_target
from src.train_model import split_data

logging.basicConfig(level=logging.INFO, filename="logfile")
logger = logging.getLogger(__name__)

score_model_kwargs = ["predict"]

def score_model(X_split, path_to_tmo, save_scores=None, **kwargs):
	"""predict the value of target using the tarined model
	
	Args:
		X_split (:py:class:`pandas.DataFrame`): DataFrame containing the test and train data
		path_to_tmo (str): path to the training model. 
		save_scores (str, optional): If given, will save the predicted socre to the given path.
		**kwargs:
	Returns:
		X (:py:class:`pandas.DataFrame`): DataFrame containing extracted features (and target, it applicable)
	"""

	with open(path_to_tmo, "rb") as f:
		model = pickle.load(f)

	# if "get_target" in kwargs:
 #        y = get_target(df_feature, **kwargs["get_target"])
 #        df_feature = df_feature.drop(labels=[kwargs["get_target"]["target"]], axis=1)
 #    else:
 #        y = None

	# if "choose_features" in kwargs:
	# 	X = choose_features(df_feature, **kwargs["choose_features"])
	# else:
	# 	X = df

	# X, y = split_data(X, y, **kwargs["split_data"])
	X_split = X_split.drop(X_split.columns[0], axis=1)
	y_predicted = model.predict(X_split)

	if save_scores is not None:
		pd.DataFrame(y_predicted).to_csv(save_scores,  index=False)

	return y_predicted

def run_scoring(args):
	with open(args.config, "r") as f:
		config = yaml.load(f)

	if args.input is not None:
		x_split = pd.read_csv(args.input)
	elif "train_model" in config and "split_data" in config["train_model"] and "save_split_prefix" in config["train_model"]["split_data"]:
		x_split = pd.read_csv(config["train_model"]["split_data"]["save_split_prefix"]+ "-test-features.csv")
	else:
		raise ValueError("Path to CSV for input data must be provided through --input or "
			"'train_model' configuration must exist in config file")

	y_predicted = score_model(x_split, **config["score_model"])

	if args.output is not None:
		pd.DataFrame(y_predicted).to_csv(args.output, index=False)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Score Model")
	parser.add_argument('--config', help='path to yaml file')
	parser.add_argument('--input', help='path to dataset')
	parser.add_argument('--output', help='Path to where the dataset should be saved to')

	args = parser.parse_args()

	run_scoring(args)