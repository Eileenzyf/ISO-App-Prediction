import boto3
s3 = boto3.client('s3')
s3.upload_file('Appstore.csv', 'nw-eileenzhang-test', 'Appstore.csv')
s3.upload_file('appStore_description.csv', 'nw-eileenzhang-test', 'appStore_description.csv')