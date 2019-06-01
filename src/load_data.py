import boto3
import argparse
import pandas as pd
import numpy as np
import logging
import glob
import yaml

logging.basicConfig(level=logging.INFO, filename="logfile")
logger = logging.getLogger(__name__)

def load_from_s3(s3_bucket, filename, columns_1, columns_2):
	s3 = boto3.client('s3')
	for file in filename:
		s3.download_file(s3_bucket,file,"data/"+file)

	#import data
	data1 = pd.read_csv('data/AppleStore.csv', index_col = 0)
	data2 = pd.read_csv('data/appleStore_description.csv')

	#select dolumns
	data1 = data1[columns_1]
	data2 = data2[columns_2]

	#merge two datasets
	df = pd.merge(data1, data2,on = "id")
	df.drop(columns = "id", inplace = True)
	df=df.rename(columns = {'sup_devices.num':'sup_devices_num', 'ipadSc_urls.num': 'ipadSc_urls_num',
		'lang.num':'lang_num'})

	#get rid of outliers
	df = df.drop(index = [115,1479])
	df = df.drop(index = [7,16,519,707,755,1346]) ##total rating >1000000
	df = df.drop(index = [498,690,4467]) ##current version rating >100000

	df = df.reset_index()
	df.drop(columns = 'index', inplace=True)

	return df

def load_data(**kwargs):
	"""Loads the data to a dataframe from a online resource
	"""

	how = kwargs['how'].lower()

	if how == "load_from_s3":
		if "load_from_s3" not in kwargs:
			raise ValueError("'how' given as 'load_from_s3' but 'load_from_s3' not in configuration")
		else:
			df = load_from_s3(kwargs["load_from_s3"]['s3_bucket'], kwargs["load_from_s3"]['filename'], kwargs["load_from_s3"]['columns_1'], kwargs["load_from_s3"]['columns_2'])

	else:
		raise ValueError("Option for 'how' is 'load_from_s3' but %s was given" % how)

	#save data
	if "save_data" in kwargs and kwargs["save_data"] is not None:
		df.to_csv(kwargs["save_data"],index=False)
	else:
		raise ValueError("'save_data' need to specify a path")
     
	return df

def run_loading(args):
    """Loads config and executes load data set
    Args:
        args: From argparse, should contain args.config and optionally, args.save
            args.config (str): Path to yaml file with load_data as a top level key containing relevant configurations
            args.save (str): Optional. If given, resulting dataframe will be saved to this location.
    Returns: None
    """
    with open(args.config, "r") as f:
        config = yaml.load(f)

    df = load_data(**config["load_data"])

    if args.output is not None:
        df.to_csv(args.output)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Load Data")
	parser.add_argument('--config', help='path to yaml file')
	parser.add_argument('--output', default=None, help='Path to where the dataset should be saved to (optional)')

	args = parser.parse_args()

	run_loading(args)


