from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import PIL.Image
import google.generativeai as genai
import io
import re
import base64
import json
from decouple import config


GEMINI_API_KEY = config('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)

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

            # Create a BytesIO object from the binary data
            image_io = io.BytesIO(image_data)

            # Open the image with PIL from the BytesIO object
            img = PIL.Image.open(image_io)

            # Generate content using the image
            response = model.generate_content(["Give me artist names with similar artworks for this image", img])
            response_text = response._result.candidates[0].content.parts[0].text

            # Extract artist names and descriptions
            artists = response_text.replace("*","").split("\n")
            # Return extracted artist names as JSON
            return JsonResponse({'artists': artists})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)