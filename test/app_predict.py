import logging
import argparse
import sys
sys.path.insert(0, 'src')

import yaml
import pandas as pd
import pickle

import generate_features as gf

logging.basicConfig(level=logging.INFO, filename="logfile")
logger = logging.getLogger(__name__)


class AppPredict:
    def __init__(self, model_config, debug=False):

        # Set up logger and put in debug mode if debug = True
        self.logger = logging.getLogger("app_predict-score")
        if debug:
            self.logger.setLevel("DEBUG")
        self.logger.debug("Logger is in debug model")

        # Load model configuration fle
        with open(model_config, 'r') as f:
            config = yaml.load(f)

        self.logger.info("Configuration file loaded from %s", model_config)
        self.config = config

        # Load in configurations for generating features
        self.choose_original = config["generate_features"]["choose_features"]
        self.generate_features = config["generate_features"]
        self.choose_features = config["score_model"]["choose_features"]

        # Load trained model object
        path_to_tmo = config["score_model"]["path_to_tmo"]
        with open(path_to_tmo, "rb") as f:
            self.tmo = pickle.load(f)

        self.logger.info("Trained model object loaded from %s", path_to_tmo)

        # Load in prediction parameters
        self.predict = {} if "predict" not in config["score_model"] else config["score_model"]["predict"]

    def run(self, data):
        """Predicts song popularity for the input data

        Args:
            data (:py:class:`pandas.DataFrame`): DataFrame containing the data inputs for scoring

        Returns:
            results (:py:class:`numpy.Array`): Array of predictions of song popularity

        """

        # Generate features
        data = gf.choose_features(data, **self.choose_original)
        data = gf.generate_features(data, **self.generate_features)
        self.logger.info("Features generated")

        # Choose which features to use
        features = gf.choose_features(data, **self.choose_features)
        self.logger.info("Features being used are: %s", ",".join(features.columns.tolist()))


        # Make predictions
        results = self.tmo.predict(features, **self.predict)
        self.logger.info(dict(predictions=results))

        return results


def run_apppredict(args):
    #run the predcition 
    data_df = pd.read_csv(args.input)

    apppredict_instance = AppPredict(args.config, args.debug)
    
    #predicted result
    results = apppredict_instance.run(data_df)

    if args.output is not None:
        pd.DataFrame(results).to_csv(args.output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict app rating")
    parser.add_argument("--config", "-c", default="config/model_config.yml",
                        help="Path to the configuration file")
    parser.add_argument("--input", "-i", default="test/user_input_test.csv",
                        help="Path to input data for scoring")
    parser.add_argument("--output", "-o",  default="test/prediction_test.csv",
                        help="Path to where to save output predictions")
    parser.add_argument("--debug", default=False, action="store_true",
                        help="If given, logger will be put in debug mode")
    args = parser.parse_args()

    run_apppredict(args)