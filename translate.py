import os
from flask import Flask
from flask_restful import Api, Resource, reqparse
import six
from google.cloud import translate_v2 as translate


credential_key_location = r"C:\Users\jeffr\Desktop\future-snowfall-331116-58db091ef5fb.json"

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_key_location

app = Flask(__name__)
api = Api(app)

translateArgs = reqparse.RequestParser()
translateArgs.add_argument("input_text", type=str, help="Required: Text to be translated", required=True)
translateArgs.add_argument("text_language", type=str, help="Required: Language of the text", required=True)
translateArgs.add_argument("translated_language", type=str, help="Required: Language to translate to", required=True)


def translate_text(target, text):
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """


    translate_client = translate.Client()

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.

    all_languages = translate_client.get_languages()
    # print(target)
    for each_lang in all_languages:
        # print(each_lang)
        if target == each_lang['name']:
            target = each_lang['language']
        else:
            print("Language not found")
            return 400

    # print(all_languages)

    result = translate_client.translate(text, target_language=target)


    return result['translatedText']

class TranslateService(Resource):

    def post(self):
        args = translateArgs.parse_args()
        data = {
            "input_text" : args.input_text,
            "text_language" : args.text_language,
            "translated_language" : args.translated_language
        }
        # print(data)
        return translate_text(data['translated_language'], data['input_text'])

api.add_resource(TranslateService, "/translate")


if __name__ == '__main__':
    app.run(debug=True)