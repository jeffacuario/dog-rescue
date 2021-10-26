from flask import Blueprint, render_template
from flask import request
import requests

views = Blueprint('views', __name__)

# petfinder api access information

setup = 'https://api.petfinder.com/v2/oauth2/token'
dog_search = 'https://api.petfinder.com/v2/animals/'
rescue_search = 'https://api.petfinder.com/v2/organizations/'
breed_list = 'https://api.petfinder.com/v2/types/dog/breeds'
next_page1 = 'https://api.petfinder.com/'



# TODO hide this stuff
data = {
    'grant_type': 'client_credentials',
    'client_id': "5446CBgLfw9SuJlUBqkQ8Pxkd33ZC81Zzdf7monQvmZWbSK7DU",
    'client_secret': 'oGDRPbKFdFOzv3WVNToy7GgbHusPRHt7vMDogY1T'
}

r = requests.post(setup, data)
response = r.json()

headers={
    'Authorization': 'Bearer ' + response['access_token']
}

@views.route('/')
def home():
    return render_template("home.html")


@views.route('/rescues', methods=['POST'])
def results_rescues():
    if request.method == 'POST':
        if (request.form['distance']) == '':
            params = {
            "location" :int(request.form['location']),
            "distance" :0
            }
        else:
            params = {
                "location" :int(request.form['location']),
                "distance" :int(request.form['distance'])
            }
            

        r = requests.get(rescue_search, headers=headers, params=params)
        v = r.json()
        v['distance'] = params['distance']
        v['location'] = params['location']

        return render_template("results_rescues.html", data=v)
    else:
        return render_template("home.html")



@views.route('/dogs', methods=['POST'])
def results_dogs():
    if request.method == 'POST':
        params = {'type':'Dog'}

        for each in request.form:
            if request.form[each] != '':
                params[each] = request.form[each]

        r = requests.get(dog_search, headers=headers, params=params)
        v = r.json()

        return render_template("results_dogs.html", data=v)
    else:
        return render_template("home.html")


# get breed list
@views.route('/breeds', methods=['GET'])
def breeds():
    if request.method == 'GET':

        r = requests.get(breed_list, headers=headers)
        v = r.json()

        return render_template("breeds.html", data=v)