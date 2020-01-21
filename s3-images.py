#! venv/bin/python
from functions import get_state
import re
import requests
import os
import boto3

state = get_state()


modules = []
for topic in state['topics']:
	for module in topic['modules']:
		modules.append({
			'readme': f'{module["gitUri"]}/README.md',
			'resourceName': module['resourceName']
		})

def download_images(images, image_directory):
	downloaded = []
	for module_images in images:
			for index, image in enumerate(module_images):
					print(f'downloading: {image["link"]} to: {image_directory}')
					response = requests.get(image["link"])
					content_type = response.headers.get('Content-Type')
					image['contentType'] = content_type
					if content_type.startswith('image'):
						image_base_directory = f'{image_directory}{image["resourceName"]}'
						if not os.path.exists(image_base_directory):
							os.makedirs(image_base_directory)
						download = f'{image_base_directory}/{str(index).zfill(3)}.{content_type.split("/")[-1]}'
						print(f'downloaded: {download}')
						with open(download, 'wb') as file:
							file.write(response.content)
						image['download'] = download
						downloaded.append(image)
					else:
						print(f'the content type is wrong for the link: {image["link"]}\n\tit should be image/*, not {content_type}')
	return downloaded


images = []

markdown_image_pattern = re.compile('\!\[.*\]\((.+)\)')
bucket_name = os.getenv('AWS_BUCKET_NAME')
region = os.getenv('AWS_REGION')


for module in modules:
	image_count = 0
	with open(module['readme'], 'r') as module_content:
		lines = module_content.read().split('\n')
	module_images = []
	s3_migration = False
	for index, line in enumerate(lines):
		match = markdown_image_pattern.search(line)
		if match:
			module_images.append({'resourceName': module['resourceName'], 'readme': module['readme'], 'line_index': index, 'link': match.group(1)})
			if bucket_name not in match.group(1):
				s3_migration = True
	if s3_migration:
		images.append(module_images)

download_prefix = '/tmp/images/'
downloaded = download_images(images, download_prefix)

for image in downloaded:
	s3_key = image['download'].replace(download_prefix, '')
	s3 = boto3.resource('s3')
	s3.meta.client.upload_file(image['download'], bucket_name, s3_key, ExtraArgs={'ContentType': image['contentType']})
	s3_url = f"https://{bucket_name}.s3.{region}.amazonaws.com/{s3_key}"
	print(f'replacing {image["link"]} for {s3_url}')
	with open(image['readme'], 'r') as readme:
		lines = readme.read().split('\n')
	lines[image['line_index']] = lines[image['line_index']].replace(image['link'], s3_url)
	with open(image['readme'], 'w') as readme:
		readme.write('\n'.join(lines))