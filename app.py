from flask import Flask
from flask import request
import boto3
from botocore.exceptions import ClientError
app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello, World!"
    
@app.route('/list-objects')
def s3_listobjects():
    session = boto3.session.Session()
    s3_client = session.client('s3')
    s3_bucket = request.args.get('s3_bucket')
    try:
        response = s3_client.list_objects(Bucket=s3_bucket)
        objects = []
        for obj in response['Contents']:
            objects += {obj["Key"]}
    except ClientError:
        print("Couldn't get list of objects!")
        raise
    else:
        return objects
    
    return "Couldn't get list of objects!"
       
@app.route('/list-buckets')
def s3_list():
    session = boto3.session.Session()
    s3_client = session.client('s3')
    try:
        response = s3_client.list_buckets()
        buckets =[]
        for bucket in response['Buckets']:
            buckets += {bucket["Name"]}
    except ClientError:
        print("Couldn't get list of buckets!")
        raise
    else:
        return buckets
    
    return "Couldn't get list of buckets!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
