def main(params):
    try:
        from io import BytesIO
        import os
        from minio import Minio
        from PIL import Image

        VMIP, BUCKET_FILE = params['vmip'], params['Key']
        MINIO_URL = f'{VMIP}:9990'
        ACCESS_KEY = 'admin'
        SECRET_KEY = 'password'
        SOURCE_BUCKET = 'dit247'
        DEST_BUCKET = 'dit247c'
            
        _, input_file = os.path.split(BUCKET_FILE)
        input_file_no_ext, input_file_ext = os.path.splitext(input_file)
        output_file = f'{input_file_no_ext}-c{input_file_ext}'
        
        # Resize Image func
        def resize_image(image_data):
            with Image.open(BytesIO(image_data)) as img:
                img = img.resize((100, 100))
                output = BytesIO()
                img.save(output, format='JPEG')
                return output.getvalue()

        # Initialize MinIO client
        client = Minio(MINIO_URL, access_key=ACCESS_KEY, secret_key=SECRET_KEY, secure=False)

        # Download the object from the source bucket
        response = client.get_object(SOURCE_BUCKET, input_file)
        image_data = response.read()

        # Resize the image
        resized_image_data = resize_image(image_data)

        # Make the bucket if it doesn't exist.
        found = client.bucket_exists(DEST_BUCKET)
        if not found:
            client.make_bucket(DEST_BUCKET)

        # Upload the resized image to the destination bucket
        client.put_object(
            DEST_BUCKET,
            output_file,
            data=BytesIO(resized_image_data),
            length=len(resized_image_data),
            content_type='image/jpeg'
        )
        msg = f'Successfully resized and uploaded {output_file} to {DEST_BUCKET}'
    except Exception as e:
        msg = f'Error occurred: {e}'
    return {
        'input-file': input_file,
        'output-file': output_file,
        'message': msg
    }