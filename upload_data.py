import boto3
import argparse




def upload_data(args):
	"""upload the data to the target s3 bucket
	Args:
		args (str): strings entered from the commend. 

	Returns:
		None
	"""
	s3 = boto3.client('s3', aws_access_key_id= args.acess_key,aws_secret_access_key= args.private_key)
	s3.upload_file(args.filename, args.bucket, args.savename)

if __name__ == "__main__":
	#upload data to S3 bucket
	parser = argparse.ArgumentParser(description="Upload data to S3")

	parser.add_argument("--acess_key", default = None, help="S3 acess_key")
	parser.add_argument("--private_key", default = None, help="S3 private_key")
	parser.add_argument("--filename", help="Target file want to upload")
	parser.add_argument("--bucket", help="Target S3 bucket name")
	parser.add_argument("--savename", help="Filename to be save in S3")

	args = parser.parse_args()
	upload_data(args)
