import csv
import sys
import boto3


s3_client = boto3.client('s3')
def check_existed_key(bucket, key):
    try:
        s3_client.head_object(
            Bucket=bucket,
            Key=key
        )
        return True
    except s3_client.exceptions.NoSuchKey:
        return False

# response = s3_client.list_buckets()

# # Output the bucket names
# print('Existing buckets:')
# for bucket in response['Buckets']:
#     print(f'  {bucket["Name"]}')

with open(str(sys.argv[1]), 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)
    for row in csvreader:
        if len(row) >= 5:
            check_existed_key(str(row[4]), str(row[5]))
        else:
            print(row)

