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

from load_data import load_data
from generate_features import choose_features, get_target
from train_model import split_data

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
		y_predcited (:py:class:`pandas.DataFrame`): DataFrame containing the predicted value for the target 
	"""

	#load the model
	try:
		with open(path_to_tmo, "rb") as f:
			model = pickle.load(f)
		#drop the index column
		X_split = X_split.drop(X_split.columns[0], axis=1)

		#predict the y value
		y_predicted = model.predict(X_split)

		if save_scores is not None:
			pd.DataFrame(y_predicted).to_csv(save_scores,  index=False)

		return y_predicted
	except:
		logger.warning("Incorrect model path.")


def run_scoring(args):
	"""Loads config and executes load data set
    Args:
        args: From argparse, should contain args.config, args.input and args.ouput
            args.config (str): Path to yaml file with load_data as a top level key containing relevant configurations
            args.input (str): input file path
            args.output (str): output file path
    Returns: None
    """
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