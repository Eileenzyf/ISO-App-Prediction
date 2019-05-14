import boto3
s3 = boto3.client('s3')
s3.download_file('nw-eileenzhang-test', 'AppleStore.csv', 'AppStore.csv')
s3.download_file('nw-eileenzhang-test', 'appleStore_description.csv', 'appStore_description.csv')