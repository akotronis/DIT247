

def main(params):
    _params = {
      "EventName": "s3:ObjectCreated:Put",
      "Key": "dit247/file-265.jpg",
      "Records": [
        {
          "eventVersion": "2.0",
          "eventSource": "minio:s3",
          "awsRegion": "",
          "eventTime": "2024-08-29T14:55:11.400Z",
          "eventName": "s3:ObjectCreated:Put",
          "userIdentity": {
            "principalId": "admin"
          },
          "requestParameters": {
            "principalId": "admin",
            "region": "",
            "sourceIPAddress": "172.18.0.4"
          },
          "responseElements": {
            "x-amz-id-2": "dd9025bab4ad464b049177c95eb6ebf374d3b3fd1af9251148b658df7ac2e3e8",
            "x-amz-request-id": "17F03ACD6F38F575",
            "x-minio-deployment-id": "330c02db-3fe3-4464-ae22-27f7e8da89b1",
            "x-minio-origin-endpoint": "http://172.18.0.5:9000"
          },
          "s3": {
            "s3SchemaVersion": "1.0",
            "configurationId": "Config",
            "bucket": {
              "name": "dit247",
              "ownerIdentity": {
                "principalId": "admin"
              },
              "arn": "arn:aws:s3:::dit247"
            },
            "object": {
              "key": "file-265.jpg",
              "size": 11,
              "eTag": "e4f750659742b67df44c2c633522acbe",
              "contentType": "binary/octet-stream",
              "userMetadata": {
                "content-type": "binary/octet-stream"
              },
              "sequencer": "17F03ACD72204E9D"
            },
            "source": {
              "host": "172.18.0.4",
              "port": "",
              "userAgent": "MinIO (linux; x64) minio-js/8.0.1"
            }
          }
        }
      ]
    }
    params = {'firstname':'Anastasios', 'lastname': 'Kotronis'}
    firstname, lastname = map(lambda x:params.get(x, 'stranger'), ['firstname', 'lastname'])
    greeting = f'Hello {firstname} - {lastname}'
    return {"greeting": greeting}