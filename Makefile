.PHONY: venv model-evaluation test-score trained-model features dataset predictions test clean-tests app database clean-pyc clean-env


data/user_input.db: src/Create_database.py
	python src/Create_database.py 
database: data/user_input.db

data/app.csv: src/load_data.py config/model_config.yml 
	python src/load_data.py --config=config/model_config.yml --output=data/app.csv
dataset: data/app.csv

data/app_processed.csv: data/app.csv src/generate_features.py config/model_config.yml
	python  src/generate_features.py --config=config/model_config.yml --input=data/app.csv --output=data/app_processed.csv
features: data/app_processed.csv

models/app-prediction.pkl: data/app_processed.csv src/train_model.py config/model_config.yml
	python  src/train_model.py --config=config/model_config.yml --input=data/app_processed.csv --output=models/app-prediction.pkl
trained-model: models/app-prediction.pkl

models/app_test_scores.csv: models/app-prediction.pkl data/app-test-features.csv src/score_model.py config/model_config.yml
	python  src/score_model.py --config=config/model_config.yml --input=data/app-test-features.csv --output=models/app_test_scores.csv
test-score: models/app_test_scores.csv

models/evaluation.csv: data/app-test-targets.csv src/evaluate_model.py config/model_config.yml
	python  src/evaluate_model.py --config=config/model_config.yml --input=data/app-test-targets.csv --output=models/evaluation.csv
model-evaluation: models/evaluation.csv

predictions:
	python test/app_predict.py --config=config/model_config.yml --input=test/user_input_test.csv

# Create a virtual environment named avcproject
avcproject-env/bin/activate: requirements.txt
	test -d avcproject-env || virtualenv avcproject-env
	. avcproject-env/bin/activate; pip install -r requirements.txt
	#avcproject/bin/pip install -r requirements.txt
	touch avcproject-env/bin/activate

venv: avcproject-env/bin/activate
	

# Run the Flask application
app: app/app.py
	python app/app.py

test:
	py.test

clean-tests:
	rm -rf test/.pytest_cache
# 	mkdir test/model/test
# 	touch test/model/test/.gitkeep
	
clean-env:
	rm -r avcproject

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	rm -rf .pytest_cache


all: venv database dataset features trained-model test-score model-evaluation predictions test clean-tests app clean-env clean-pyc
