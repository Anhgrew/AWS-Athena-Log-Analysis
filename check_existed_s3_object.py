import sys
import csv
import boto3

s3_client = boto3.client('s3')

def check_existed_key(bucket_name, key_name):
    try:
        s3_client.head_object(Bucket=bucket_name, Key=key_name)
        print(f"Key {key_name} exists in bucket {bucket_name}")
        return True
    # except s3_client.exceptions.NoSuchKey:
    #     print(f"Key {key_name} does not exist in bucket {bucket_name}")
    #     return False
    except Exception as e:
        # print(f"Error checking key {key_name} in bucket {bucket_name}: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_csv_file>")
        sys.exit(1)

    csv_file_path = sys.argv[1]

    try:
        with open(csv_file_path, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            header = next(csvreader)  # skip the header row
            header.append("KeyExistent")
            rows = []
            for row in csvreader:
                if len(row) >= 5 and check_existed_key(str(row[4]), str(row[5])):
                    row.append("Existed")
                else:
                    row.append("None")
                    # raise ValueError(f"Invalid row: {row}")
                rows.append(row)

            with open("result.csv", 'w', newline='') as new_csvfile:
                csvwriter = csv.writer(new_csvfile)
                csvwriter.writerow(header)
                csvwriter.writerows(rows)

    except FileNotFoundError:
        print(f"Error: file {csv_file_path} not found.")
    except Exception as e:
        print(f"Error: {e}")

