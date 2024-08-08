from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import PIL.Image
import google.generativeai as genai
import io
import re
import base64
import json

# Initialize the model
genai.configure(api_key="AIzaSyCaSmIPJ5GabW5hwsDDBmPyUFFiz6hmSnE")
model = genai.GenerativeModel("gemini-1.5-flash")


@csrf_exempt
def get_artists_name_with_similar_work(request):
    if request.method == 'POST':
        try:
            # Parse the JSON body
            data = json.loads(request.body)
            base64_url = data.get('image_base64_url')
            
            if not base64_url:
                return JsonResponse({'error': 'No image_base64_url provided'}, status=400)

            # Extract the base64 string from the URL
            base64_string = base64_url.split(',')[1]

            # Decode the base64 string to binary data
            image_data = base64.b64decode(base64_string)

            # Save the binary data to a file
            with open("imageToSave.png", "wb") as fh:
                fh.write(image_data)

            # Open the saved image with PIL
            organ = PIL.Image.open("imageToSave.png")

            # Generate content using the image
            response = model.generate_content(["Give me artist names with similar artworks for this image", organ])
            response_text = response._result.candidates[0].content.parts[0].text

            # Extract artist names from the response using regex
            pattern = re.compile(r'\*\*([^\*]+?)\:\*\*')
            artists = pattern.findall(response_text)

            # Return extracted artist names as JSON
            return JsonResponse({'artists': artists})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)