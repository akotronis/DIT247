def main(params):
	########## PARAMS ##########
	params = {
		"EventName": "s3:ObjectCreated:Put",
		"Key": "dit247/file-121.jpg",
		"Records": [
			{
					# Record details
			}
		]
	}
    #############################
	


	########## IMPORTS ##########
	from io import BytesIO
	import os
	from minio import Minio
	from PIL import Image

	########## MinIO configuration ##########
	MINIO_URL = '127.0.0.1:9990'
	ACCESS_KEY = 'admin'
	SECRET_KEY = 'password'
	SOURCE_BUCKET = 'dit247'
	DEST_BUCKET = 'dit247c'
	# Initialize MinIO client
	client = Minio(MINIO_URL, access_key=ACCESS_KEY, secret_key=SECRET_KEY, secure=False)

	########## RESIZE IMAGE ##########
	def resize_image(image_data):
		with Image.open(BytesIO(image_data)) as img:
			img = img.resize((100, 100))  # Resize the image to 100x100 pixels
			output = BytesIO()
			img.save(output, format='JPEG')
			return output.getvalue()

	########## PROCESS EVENT ##########
	try:
		_, input_file = os.path.split(params['Key'])
		input_file_no_ext, input_file_ext = os.path.splitext(input_file)
		output_file = f'{input_file_no_ext}-c{input_file_ext}'
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
		response = f'Successfully resized and uploaded {output_file} to {DEST_BUCKET}'
	except Exception as e:
		response = f'Error occurred: {e}'
	return {'response': response}


# if __name__ == "__main__":
# 	from pdb import set_trace as bp; bp()
# 	params = {
# 		"EventName": "s3:ObjectCreated:Put",
# 		"Key": "dit247/file-121.jpg",
# 		"Records": [
# 			{
# 					# Record details
# 			}
# 		]
# 	}
# 	main(params)