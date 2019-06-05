import argparse
import logging
import yaml
import pickle
import numpy as np

import sklearn
from sklearn import metrics
import pandas as pd

from src.load_data import load_data
from src.generate_features import choose_features, get_target
from src.train_model import split_data
from sklearn.ensemble import RandomForestRegressor



logger = logging.getLogger(__name__)

def evaluate_model(label_df, X_split, y_predicted, path_to_tmo, **kwargs):
	"""Evaluate the performance of the model   
	Args:
	    label_df (:py:class:`pandas.DataFrame`): Dataframe containing true y label
	    y_predicted (:py:class:`pandas.DataFrame`): Dataframe containing predicted probability and score
	Returns: 
	    confusion_df (:py:class:`pandas.DataFrame`): Dataframe reporting confusion matrix
	"""

	with open(path_to_tmo, "rb") as f:
		model = pickle.load(f)
	X_split = X_split.drop(X_split.columns[0], axis=1)
	
	y_true = label_df.iloc[:,0]
	label_df = label_df.drop(label_df.columns[0], axis=1)
	# calculate r2 and accuracy if specified
	if "r2" in kwargs["metrics"]:
		r2 = model.score(X_split,label_df)
		print('r2 on test: %0.3f' % r2)
	if "accuracy" in kwargs["metrics"]:
		errors = abs(y_predicted.iloc[:,0]-label_df.iloc[:,0])
		mad = np.mean(errors)
		accuracy = 1-mad/np.mean(label_df)
		print('Accuracy on test: %0.3f' % accuracy)

	metric_df = pd.DataFrame({"r2": r2, "accuracy":accuracy})

	return metric_df


def run_evaluation(args):
	"""Orchestrates the evaluation of the model."""

	with open(args.config, "r") as f:
		config = yaml.load(f)

	if args.input is not None:
		label_df = pd.read_csv(args.input)
	elif "train_model" in config and "split_data" in config["train_model"] and "save_split_prefix" in config["train_model"]["split_data"]:
		label_df = pd.read_csv(config["train_model"]["split_data"]["save_split_prefix"]+ "-test-targets.csv")
		logger.info("test target loaded")
	else:
		raise ValueError("Path to CSV for input data must be provided through --input or "
			"'train_model' configuration must exist in config file")

	if "train_model" in config and "split_data" in config["train_model"] and "save_split_prefix" in config["train_model"]["split_data"]:
		x_split = pd.read_csv(config["train_model"]["split_data"]["save_split_prefix"]+ "-test-features.csv")

	if "score_model" in config and "save_scores" in config["score_model"]:
		y_predicted = pd.read_csv(config["score_model"]["save_scores"])
		logger.info("Predicted score on test set loaded")
	else:
		raise ValueError("'score_model' configuration mush exist in config file")

	confusion_df = evaluate_model(label_df, x_split, y_predicted, **config["evaluate_model"])
	
	if args.output is not None:
		confusion_df.to_csv(args.output)
		logger.info("Model evaluation saved to %s", args.output)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Evaluate model")
	parser.add_argument('--config', help='path to yaml file with configurations')
	parser.add_argument('--input', default=None, help="Path to CSV for input to model scoring")
	parser.add_argument('--output', default=None, help="Path to CSV for output to confusion matrix")

	args = parser.parse_args()

	run_evaluation(args)