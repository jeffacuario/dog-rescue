import requests

BASE = "https://mighty-wave-93567.herokuapp.com/"
BASE2 = "https://mighty-wave-93567.herokuapp.com/translate"

# BASE2 = "http://localhost:5000/translate"

# response = requests.get(BASE)
# print(response.text)

# response_2 = requests.get(BASE2)
# print(response_2.text)

response_3 = requests.post(BASE2, {"input_text": "Hello, my name is Jeffrey", "text_language": "Spanish", "translated_language":"Spanish"})
# print(response_3)


print(response_3.json())