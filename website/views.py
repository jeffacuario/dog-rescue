from flask import request
from flask import Blueprint, render_template

import requests
import json

views = Blueprint('views', __name__)

# petfinder api access information

setup = 'https://api.petfinder.com/v2/oauth2/token'
dog_search = 'https://api.petfinder.com/v2/animals/'
rescue_search = 'https://api.petfinder.com/v2/organizations/'
breed_list = 'https://api.petfinder.com/v2/types/dog/breeds'


with open('credentials.json') as config_file:
    config = json.load(config_file)

data = {
    'grant_type': config['grant_type'],
    'client_id': config['pf_client_id'],
    'client_secret': config['client_secret']
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
        try:
            if request.form['next']:
                string = request.form['next']

                params = {}

                v = string.find("?")
                y = string.find('=')

                first = string[v+1:y]
                v = string.find("&")
                first_value = string[y+1:v]
                params[first] = first_value


                string = string[v+1:]
                while v != -1 and y != -1:
                    y = string.find("=")
                    v = string.find("&")
                    word = string[:y]
                    value = string[y+1:v]
                    params[word] = value
                    
                    string = string[v+1:]

                if value != string[y+1:]:
                    params[word] = string[y+1:]

                r = requests.get(rescue_search, headers=headers, params=params)
                v = r.json()
                v['location'] = params['location']
                v['distance'] = params['distance']

                return render_template("results_rescues.html", data=v)
        except:
            pass



        if (request.form['distance']) == '':
            params = {
            "location" : int(request.form['location']),
            "distance" : 0
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

        try:
            if request.form['next']:
                string = request.form['next']

                params = {}

                v = string.find("?")
                y = string.find('=')

                first = string[v+1:y]
                v = string.find("&")
                first_value = string[y+1:v]
                params[first] = first_value


                string = string[v+1:]
                while v != -1 and y != -1:
                    y = string.find("=")
                    v = string.find("&")
                    word = string[:y]
                    value = string[y+1:v]
                    params[word] = value
                    
                    string = string[v+1:]

                if value != string[y+1:]:
                    params[word] = string[y+1:]

                r = requests.get(dog_search, headers=headers, params=params)
                v = r.json()
                v['location'] = params['location']
                v['distance'] = params['distance']

                return render_template("results_dogs.html", data=v)
        except:
            pass

        for each in request.form:
            if request.form[each] != '':
                params[each] = request.form[each]

        if (request.form['distance']) == '':
            params["distance"] = 0
            
        r = requests.get(dog_search, headers=headers, params=params)
        v = r.json()
        v['location'] = params['location']
        v['distance'] = params['distance']
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



# # get breed list
# @views.route('/https://dogs-service-cs361.herokuapp.com/', methods=['POST'])
# def breeds():
#     if request.method == 'GET':

#         r = requests.get(breed_list, headers=headers)
#         v = r.json()

#         return render_template("breeds.html", data=v)




