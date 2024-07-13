
from datetime import datetime
import json
from connector.koneksi import Connection
from dotenv import load_dotenv
import os

load_dotenv()
# credential minio
end_point = os.getenv('end_point')
aws_access_key_id = os.getenv('aws_access_key_id')
aws_secret_access_key = os.getenv('aws_secret_access_key')

class Minio:
    def __init__(self):
        self.conn = Connection(
            end_point=end_point,
            aws_access_key_id = aws_access_key_id,
            aws_secret_access_key =aws_secret_access_key
        )
        self.client_minio = self.conn.conn_minio()
        
    def upload_data_minio(self, data):  
        credential = self.client_minio

        # buat bucket
        bucket_name = 'stadiondata'
        try:
            credential.head_bucket(Bucket=bucket_name)
            print(f'bucket {bucket_name} sudah ada')
        except credential.exceptions.ClientError as e:
            if e.response['Error']['Code'] == '404':
                credential.create_bucket(Bucket=bucket_name)
                print(f'Bucket {bucket_name} berhasil dibuat.')
            else:
                print(f'Error: {str(e)}')
        
        # buat path untuk diminio
        current_date = datetime.now()
        formatted_date = current_date.strftime("%Y%m%d")
        path = f'{bucket_name}/project/{current_date.year}/{current_date.month}/{current_date.day}/stadion_data{formatted_date}.json'

        # upload data ke minio
        try:
            json_data = json.dumps(data)
            credential.put_object(Bucket=bucket_name, Key=path, Body=json_data.encode('utf-8'))
            response = credential.list_objects(Bucket=bucket_name)
            for obj in response.get('Contents', []):
                print(obj['Key'])
            print(f'sukses upload data ke MinIO: {path}')
            return path
        except Exception as e:
            print(f'Error upload ke MinIO: {str(e)}')
            return None
        
    def get_data_minio(self, path_param):
        credential = self.client_minio
        bucket_name = 'stadiondata'
        try:
            response = credential.get_object(Bucket=bucket_name, Key=path_param)
            data_minio = response['Body'].read().decode('utf-8')
            data = json.loads(data_minio)
            print("data sudah didapatkan")
            return data
        except credential.exceptions.NoSuchKey as e:
                print(f'Objek dengan kunci {path_param} tidak ditemukan di bucket {bucket_name}')
        except Exception as e:
            print(f'Terjadi kesalahan saat mengambil objek: {str(e)}')

        

