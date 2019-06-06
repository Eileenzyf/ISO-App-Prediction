"""Enables the command line execution of multiple modules within src/
This module combines the argparsing of each module within src/ and enables the execution of the corresponding scripts
so that all module imports can be absolute with respect to the main project directory.
To understand different arguments, run `python run.py --help`
"""
import argparse
import logging.config
from app.app import app

# Define LOGGING_CONFIG in config.py - path to config file for setting up the logger (e.g. config/logging/local.conf)
logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logger = logging.getLogger("run-iso-app")
logger.debug('Test log')

from Create_database import create_db, user_input, get_engine_string
from load_data import run_loading
from generate_features import run_features
from train_model import run_training
from score_model import run_scoring

def run_app(args):
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Run components of the model source code")
    subparsers = parser.add_subparsers()

    # Sub-parser for creating a database
    sb_create = subparsers.add_parser("create", description="Create database")
    sb_create.add_argument("--size_bytes", default = 28899, help="Size of the application")
    sb_create.add_argument("--price", default = 3.99, help="Price of the app")
    sb_create.add_argument("--rating_count_tot", default = 355, help="Total ratings received so far")
    sb_create.add_argument("--rating_count_ver", default = 10, help="Ratings received for the lastest version")
    sb_create.add_argument("--cont_rating", default = "4+", help="Content rating")
    sb_create.add_argument("--prime_genre", default = "Games", help="Genre of the app")
    sb_create.add_argument("--sup_devices_num", default=1, help="Number of supported device")
    sb_create.add_argument("--ipadSc_urls_num", default=0, help="Number of screenshots displayed")
    sb_create.add_argument("--lang_num", default=1, help="Number of support languages")
    sb_create.add_argument("--app_desc", default = 'Games are fun', help="Application descriptions")

    sb_create.add_argument("--engine_string", default=get_engine_string(RDS=True),
                           help="SQLAlchemy connection URI for database")
    sb_create.set_defaults(func=create_db)

    # # Sub-parser for ingesting new data
    # sb_ingest = subparsers.add_parser("ingest", description="Add data to database")
    # sb_ingest.add_argument("--size_bytes", help="Size of the application")
    # sb_ingest.add_argument("--price", help="Price of the app")
    # sb_ingest.add_argument("--rating_count_tot", help="Total ratings received so far")
    # sb_ingest.add_argument("--rating_count_ver", help="Ratings received for the lastest version")
    # sb_ingest.add_argument("--cont_rating", help="Content rating")
    # sb_ingest.add_argument("--prime_genre", help="Genre of the app")
    # sb_ingest.add_argument("--sup_devices_num", default=1, help="Number of supported device")
    # sb_ingest.add_argument("--ipadSc_urls_num", default=0, help="Number of screenshots displayed")
    # sb_ingest.add_argument("--lang_num", default=1, help="Number of support languages")
    # sb_ingest.add_argument("--app_desc", help="Application descriptions")
    # sb_ingest.add_argument("--engine_string", default='sqlite:///../data/user_input.db',
    #                        help="SQLAlchemy connection URI for database")
    # sb_ingest.set_defaults(func=user_input)

    sb_load = subparsers.add_parser("load_data", description="Load data into a dataframe")
    sb_load.add_argument('--config', help='path to yaml file with configurations')
    sb_load.add_argument('--output', default=None, help='Path to where the dataset should be saved to (optional')
    sb_load.set_defaults(func=run_loading)

    # FEATURE subparser
    sb_features = subparsers.add_parser("generate_features", description="Generate features")
    sb_features.add_argument('--config', help='path to yaml file with configurations')
    sb_features.add_argument('--input', default=None, help="Path to CSV for input to model scoreing")
    sb_features.add_argument('--output', default=None, help='Path to where the dataset should be saved to (optional')
    sb_features.set_defaults(func=run_features)

    # TRAIN subparser
    sb_train = subparsers.add_parser("train_model", description="Train model")
    sb_train.add_argument('--config', help='path to yaml file with configurations')
    sb_train.add_argument('--input', default=None, help="Path to CSV for input to model training")
    sb_train.add_argument('--output', default=None, help='Path to where the dataset should be saved to (optional')
    sb_train.set_defaults(func=run_training)

    # SCORE subparser
    sb_score = subparsers.add_parser("score_model", description="Score model")
    sb_score.add_argument('--config', help='path to yaml file with configurations')
    sb_score.add_argument('--input', default=None, help="Path to CSV for input to model scoring")
    sb_score.add_argument('--output', default=None, help='Path to where the dataset should be saved to (optional')
    sb_score.set_defaults(func=run_scoring)

    sb_run = subparsers.add_parser("app", description="Run Flask app")
    sb_run.set_defaults(func=run_app)

    args = parser.parse_args()
    args.func(args)
