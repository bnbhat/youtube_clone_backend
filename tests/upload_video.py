import os
import requests


# Endpoint URL
url = "http://localhost:8000/api/v1/videos/upload/"

# Data you want to send (title and description)
data = {
    'title': 'Sample Video',
    'description': 'This is a sample video description.'
}


# The video file you want to upload
files = {
    'file': ('sample.mp4', open("/workspaces/backend/tests/files/test.mp4", 'rb'))
}

response = requests.post(url, data=data, files=files)

print(response.status_code)
print(response.json())

