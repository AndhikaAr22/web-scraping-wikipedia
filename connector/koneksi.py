import boto3


class Connection:
    def __init__(self, end_point, aws_access_key_id, aws_secret_access_key):
        self.end_point = end_point
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key

    def conn_minio(self):
        s3_client = boto3.client(
            's3',
            endpoint_url=self.end_point,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key
        )
        return s3_client