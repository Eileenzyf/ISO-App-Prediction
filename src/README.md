# README
## Overview of the Src Files

 - load_data.py
	 - Py file that allows the user to download the data from online source. 
 - upload_data.py
	 - Py file that enables the user to upload the data from the local to s3 bucket. 
 - create_database.py 
	 - Py file that read the data directly from the s3 bucket to the RDS. Three databases will be created after running this file: Appstore, appstore_description and user_input. 

## Setup the Environment
- Create a virtual environment 
	- Type "`conda create --name <environment name>`" 
	- `conda activate <environment name>`
- Install requirement (in the same directory)
	- `pip install -r requirements.txt`

## Instruction of Running the Files

 -  For downloading the dataset, please run `load_data.py` with `python load_data.py --bucket nw-eileenzhang-test --filename AppleStore.csv --savename <filen_name_you_want_to_save>.csv`
 - For uploading the dataset, please run `upload_data.py` with `python upload_data.py --acess_key <user s3 acess key> --private key <user s3 private key> --filename AppleStore.csv --bucket <Target_bucket_name> --savename <filen_name_you_want_to_save>.csv`
 - For creating the database, please run `python create_database.py`


