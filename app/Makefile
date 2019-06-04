.PHONY: venv clean clean-pyc clean-env model-evaluation test-score trained-model features dataset predictions app


data/app.csv: load_data.py ../config/model_config.yml 
	python load_data.py --config=../config/model_config.yml --output=../data/app.csv
dataset:data/app.csv

data/app_processed.csv: data/app.csv generate_features.py model_config.yml
	python  generate_features.py --config=model_config.yml --input=data/app.csv --output=data/app_processed.csv
features: data/app_processed.csv

models/app-prediction.pkl: data/app_processed.csv train_model.py model_config.yml
	python  train_model.py --config=model_config.yml --input=data/app_processed.csv --output=models/app-prediction.pkl
trained-model: models/app-prediction.pkl

models/app_test_scores.csv: models/app-prediction.pkl data/app-test-features.csv score_model.py model_config.yml
	python  score_model.py --config=model_config.yml --input=data/app-test-features.csv --output=models/app_test_scores.csv
test-score: models/app_test_scores.csv

models/evaluation.csv: data/app-test-targets.csv evaluate_model.py model_config.yml
	python  evaluate_model.py --config=model_config.yml --input=data/app-test-targets.csv --output=models/evaluation.csv
model-evaluation: models/evaluation.csv

predictions:
	python app_predict.py --config=config/model_config.yml --input=test/user_input_test.csv

# Create a virtual environment named avcproject
avcproject/bin/activate: requirements.txt
	test -d avcproject || virtualenv avcproject
	. avcproject/bin/activate; pip install -r requirements.txt
	touch avcproject/bin/activate

venv: avcproject/bin/activate
	

# Run the Flask application
app: app.py
	python app.py

test:
	py.test

clean-tests:
	rm -rf .pytest_cache
	rm -r test/model
# 	mkdir test/model/test
# 	touch test/model/test/.gitkeep
	
clean-env:
	rm -r avcproject

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	rm -rf .pytest_cache


all: venv dataset features trained-model test-score model-evaluation predictions app  clean-tests clean-env clean-pyc
