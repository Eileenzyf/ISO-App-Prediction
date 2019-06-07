# IOS App Store Project Repository

<!-- toc -->

- [Project Charter & Backlog](#project-charter--backlog)
- [Repo structure](#repo-structure)
- [Documentation](#documentation)
- [Running the application](#running-the-application)
  * [1. Set up environment](#1-set-up-environment)
    + [With `virtualenv` and `pip`](#with-virtualenv-and-pip)
    + [With `conda`](#with-conda)
  * [2. Configure Flask app](#2-configure-flask-app)
  * [3. Initialize the database](#3-initialize-the-database)
  * [4. Run the application](#4-run-the-application)
- [Testing](#testing)

<!-- tocstop -->

## Project Charter & Backlog

### Project Charter

 - **Vision**: The ever-changing mobile landscape is a challenging space to navigate. While the number of mobile apps has been increasing over the past few years, the competition has became more and more intense. Therefore, it is crucial for software developers to improve their competitive advantage and understand the existing strategy to drive growth. This project will allow the users to predict the their apps' potential ratings and popularity based on its current features and therefore help developers to improve their apps.
 - **Mission**: The "IOS App Store" project will use two data sets that contains attributes of 10k ios apps. The project enables users to input the features of their IOS apps and predict number of reviews and rating that specific app will receive, which indicates its popularity.
 - **Success criteria**: 
   - Model performance: R square. The final model is expected to improve R squared by 20% compared to the initial simple linear regression model.
   - Business sense: Ask the user to rate the app (thumbs up or thumbs down) and calculate the ratio. Potentially increase users' revenue. 

### Project Planning

 - **Develop Themes:** Help target users (software developers) to predict number of of reviews and ratings of their apps and therefore gauge potential popularity of their apps. Users can improve and make adjustment to their current version based on the results and potentially increase revenue.
 - **Epics**
	-  **Epic 1:** Exploratory Data Analysis to explore the relationship between variables and determine which subset of variable to use. (user input related)
		-	**Story 1:** Merge two data sets
		-	**Story 2:** Data cleaning, check NA values and duplicates. 
		-	**Story 3:** Distribution of each variables, check multicollinearity and outliners 
	- **Epic 2:** Feature Engineering
		-	**Story 1:** Variable transformation 
	- **Epic 3:** Model Building to predict the number of reviews and ratings using a set of attributes.
		-  **Story 1:** Split the data set to training and test set 
		-	**Story 2:** Run a simple linear regression model to use its R square as the naive baseline. Check variable importance and residual plot to determine what advanced model to use. 
		-	**Story 3:** Run Neural Network, Random Forest Model to predict the number of reviews and ratings. Making sure the model hit the performance metrics. 
		-	**Story 4:** If models above don’t perform well as expected, try more such as gradient boosting, GAM, etc.
		-	**Story 5:** Text analysis or sentiment analysis of app descriptions to see the correlation between certain words and popularity of the apps.
	-  **Epic 4:** Build Pipeline
		 -	**Story 1:** Set up the environment 
		 -	**Story 2:** Move algorithm from local to AWS 
		 -	**Story 3:** Run and save the trained model 
		 -	**Story 4:** Set up the data pipeline (e.g. RDS)
	- **Epic 5:** Web App Development to build interactive features that allow users to enter their data to get predictions.
		-	**Story 1:** Writing the backend using Flask app. 
		-	**Story 2:** Web page design, basic layout 
		-	**Story 3:** Create interactive page allow the user to enter the attributes of their apps, attributes should be corresponds to the parameters used in the models. (8 points)
		-	**Story 4:** For certain attributes, enable users to click on instead of simple text entry for diverse user experience. 
		-	**Story 5:** Predict and show the number of reviews and ratings for the specific file on the same page in 20 seconds. 
		-	**Story 6:** Aesthetic design, color palette, font, format details.
	 - **Epic 6:** Running the application
		 -	**Story 1:** Test run the app to evaluate the performance.
- **Backlog**
	- Epic 1 story 1 (1 point) --planned in 2 weeks
	- Epic 1 story 2 (1 point) --planned in 2 weeks
	- Epic 1 story 3 (1 point) --planned in 2 weeks
	- Epic 2 story 1 (1 point) --planned in 2 weeks
	- Epic 3 story 1 (1 point) --planned in 2 weeks
	- Epic 3 story 2 (2 points) --planned in 2 weeks
	- Epic 3 story 3 (4 points) --planned in 2 weeks
	- Epic 4 story 1 (1 point)
	- Epic 4 story 3 (2 points)
	- Epic 5 story 2 (1 point)
	- Epic 5 story 3 (8 points)
	- Epic 5 story 4 (2 points)
	- Epic 5 story 5 (2 points)
	- Epic 5 story 5 (4 points)
 - **Icebox**
	 1. Epic 3 story 4
	 2. Epic 3 story 5
	 3. Epic 4 story 2
	 4. Epic 4 story 4
	 5. Epic 5 story 1 
	 6. Epic 6

## Repo structure 

```
├── README.md                         <- You are here
│
├── app
│   ├── static/                       <- CSS, JS files that remain static 
│   ├── templates/                    <- HTML (or other code) that is templated and changes based on a set of inputs
│   ├── app.py                         <- Flask wrapper for running the model 
│   ├── __init__.py                   <- Initializes the Flask as ae for nneion
│
├── config                            <- Directory for yaml configuration files for model training, scoring, etc
│├──                  <- Configuration files for python loggers
│   ├── flask_config.py              <- Configurations that oel to local database or RDS
│   ├── model_config.yml              <- YAML file that contains the pipline of the entire mat l th as ato al t sample/ subdirectories are tracked by git. 

│
├── docs                              <- A default Sphinx project; see sphinx-doc.org for details.
│
├── figures                           <- Generated graphics and figures to be used in reporting.
│
├── models                            <- Trained model objects (TMOs), model predictions, and/or model summaries
│
├── notebooks
│   ├── develop                       <- Current notebooks being used in development.
│   ├── deliver                       <- Notebooks shared with others. 
│   ├── archive                       <- Develop notebooks no longer being used.
│   ├── template.ipynb                <- Template notebook for analysis with useful imports and helper functions. 
│
├── src                               <- Source data for the project 
│   ├── helpers/                      <- Helper scripts used in main src files 
│   ├── sql/                          <- SQL source code
│   ├── Create_database.py             <- Script for creating a (temporary) MySQL database and adding new user input to it 
│   ├── load_data.py                  <- Script for downloading data from 
│   ├── upload_data.py                  <- Script for uploading data from S3to a desinated S3 bucket if needed
│   ├── generate_features.py          <- Script for cleaning and transforming data and generating features used for use in training and scoring.
│   ├── train_model.py                <- Script for training machine learning model(s)
│   ├── score_model.py                <- Script for scoring new predictions using a trained model.
│   ├── evaluate_model.py             <- Script for evaluating model performance 
│
├── test                 <- Fipnecessary for running model tests (see documentation below) 
│   ├── test_helpers.py               <- Script for unit testing functions in the src scripts
│   ├── test_data.csv                 <- Dataframe for unit testing
│   ├── app_predict.py                <- Script for testing if the prediction works
│   ├── user-input_test.csv           <- Dataframe for app_predict.py

├── requirements.txtun.py                            <-    
├── MakefileSimplifiest ution n the src scripts ├── a.                 <- MakeFile to run the entire applicationarae for uning   ├── c.py                          urin fe for app
├── r                  <- Python package dependencies 
```
This project structure was partially influenced by the [Cookiecutter Data Science project](https://drivendata.github.io/cookiecutter-data-science/).

## Documentation
 
* Open up `docs/build/html/index.html` to see Sphinx documentation docs. 
* See `docs/README.md` for keeping docs up to date with additions to the repository.

## Running the application 
### 1. Set up environment 

The `requirements.txt` file contains the packages required to run the model code. An environment can be set up in two ways. See bottom of README for exploratory data analysis environment setup. 

#### With `virtualenv`

```bash
pip install virtualenv

virtualenv pennylane

source pennylane/bin/activate

pip install -r requirements.txt

```
#### With `conda`

```bash
conda create -n pennylane python=3.7
conda activate pennylane
pip install -r requirements.txt

```

### 2. Configure Flask app 

`config.py` holds the configurations for the Flask app. It includes the following configurations:

```python
DEBUG = True  # Keep True for debugging, change to False when moving to production 
LOGGING_CONFIG = "config/logging/local.conf"  # Path to file that configures Python logger
PORT = 3002  # What port to expose app on 
SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/tracks.db'  # URI for database that contains tracks

```


### 3. Initialize the database 

To create the database in the location configured in `config.py` with one initial song, run: 

`python run.py create --artist=<ARTIST> --title=<TITLE> --album=<ALBUM>`

To add additional songs:

`python run.py ingest --artist=<ARTIST> --title=<TITLE> --album=<ALBUM>`


### 4. Run the application 
 
 ```bash
 python app.py 
 ```

### 5. Interact with the application 

Go to [http://127.0.0.1:3000/]( http://127.0.0.1:3000/) to interact with the current version of hte app. 

## Testing 

Run `pytest` from the command line in the main project repository. 


Tests exist in `test/test_helpers.py`
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTIxNDMwOTUxNDQsLTE3Mjk2MDI1MDksLT
E4MzcxMjE1NDQsLTg3NjI3NTU0MywtMTg0NzMyNTQ4NiwyMDUz
NTkyNjU1LDIwMTYwMDk1MjUsMzgxMjg2MDQ2LC0xNTQ5MzY2Mj
kyLC0xOTQzMTg4NDU1LC0xOTM2NDg0MDgwLDEwMTA0NDIzODcs
NjA1Mzk2NjI3LDE3MTY4ODI5NjMsMTQwOTM4MjAzNiwxNTY1MT
gxNjU1LC0xMDI2MzAzNDczLDE1Njg5MTI2ODQsMTEwNzI3OTkx
MywtNDAwNjEzMzU2XX0=
-->