import requests

BASE = "http://127.0.0.1:5000/"


# response = requests.post(BASE + "translate", {"input_text": "Me gustan los tacos", "text_language": "Spanish", "translated_language":"English"})
response = requests.post(BASE + "translate", {"input_text": "I like tacos", "text_language": "Spanish", "translated_language":"Spanish"})
print(response.json())