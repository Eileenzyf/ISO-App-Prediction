import boto3
import argparse

s3 = boto3.client('s3')


def upload_data(args):
	"""upload the data to the target s3 bucket
	Args:
		args (str): strings entered from the commend. 

	Returns:
		None
	"""
	s3.upload_file(args.filename, args.bucket, args.savename)

if __name__ == "__main__":
	#upload data to S3 bucket
	parser = argparse.ArgumentParser(description="Upload data to S3")

	parser.add_argument("--filename", help="Target file want to upload")
	parser.add_argument("--bucket", help="Target S3 bucket name")
	parser.add_argument("--savename", help="Filename to be save in S3")

	args = parser.parse_args()
	upload_data(args)
