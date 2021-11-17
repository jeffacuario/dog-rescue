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
    v = breeds()
    # print(v)
    return render_template("home.html", data=v)


@views.route('/rescues', methods=['POST'])
def results_rescues():
    if request.method == 'POST':
        try:
            return pagination_check(rescue_search, "results_rescues.html.html")
        except:
            pass


        if request.form['distance'] == '':
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
        v['breeds'] = breeds()['breeds']

        return render_template("results_rescues.html", data=v)
    else:
        return render_template("home.html")

# TODO testing dog sidebar
@views.route('/dogs', methods=['POST'])
def results_dogs():
    if request.method == 'POST':
        # handle sort
        try:
            # recent, -recent, distance (clostest), -distance (furthest), random (default: recent)
            if request.form['sortSelection']:
                print("*******",request.form['sortSelection'])
                newParams = {}
                jsonParams = eval(request.form['params'])
                for p in jsonParams:
                    newParams[p] = jsonParams[p]


                if request.form['sortSelection'] == 'Newest':
                    newParams['sort'] = 'recent'
                if request.form['sortSelection'] == 'Oldest':
                    newParams['sort'] = '-recent'
                elif request.form['sortSelection'] == 'Nearest':
                    newParams['sort'] = 'distance'
                elif request.form['sortSelection'] == 'Furthest':
                    newParams['sort'] = '-distance'
                elif request.form['sortSelection'] == 'Random':
                    newParams['sort'] = 'random'

                # newParams['sorted'] = request.form['sortSelection']
                print(newParams)
                
                
            r = requests.get(dog_search, headers=headers, params=newParams)
            v = r.json()
            v['location'] = newParams['location']
            v['distance'] = newParams['distance']
            # v['primaryBreeds'] = primaryBreeds
            # v['secondaryBreeds'] = secondaryBreeds
            v['params'] = newParams
            v['sorted'] = request.form['sortSelection']
        
            # for breed in v['animals']:
            #     prim = breed['breeds']['primary']
            #     sec = breed['breeds']['secondary']
            #     if prim not in primaryBreeds:
            #         primaryBreeds.append(prim)
            #     if sec not in secondaryBreeds:
            #         secondaryBreeds.append(sec)
            return render_template("results_dogs.html", data=v)
        except:
            pass

        # print(request.form['sortSelection'])
        # print(request.form['params'])


        primaryBreeds = []
        secondaryBreeds = []
        params = {'type':'Dog'}

        try:
            return pagination_check(dog_search, "results_dogs.html")
        except:
            pass

        for each in request.form:
            if request.form[each] != '':
                params[each] = request.form[each]

        if request.form['distance'] == '':
            params["distance"] = 0
            
        print(params)
        r = requests.get(dog_search, headers=headers, params=params)
        v = r.json()
        v['location'] = params['location']
        v['distance'] = params['distance']
        v['primaryBreeds'] = primaryBreeds
        v['secondaryBreeds'] = secondaryBreeds
        v['params'] = params
        v['breeds'] = breeds()['breeds']
    
        for breed in v['animals']:
            prim = breed['breeds']['primary']
            sec = breed['breeds']['secondary']
            if prim not in primaryBreeds:
                primaryBreeds.append(prim)
            if sec not in secondaryBreeds:
                secondaryBreeds.append(sec)

        return render_template("results_dogs.html", data=v)
    else:
        return render_template("home.html")


# get breed list
def breeds():
    # if request.method == 'GET':
    r = requests.get(breed_list, headers=headers)
    v = r.json()
    return v



# TODO delete later
@views.route('/filter', methods=['GET'])
def filter():
    return render_template("filter.html")


# TODO delete later
@views.route('/sidebar', methods=['GET'])
def sidebar():
    return render_template("sidebar.html")

# TODO delete later
@views.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        print(request.form)
        print(request.form['sortSelection'])
        print(request.form['params'])

        return render_template("result.html")



def pagination_check(type_search, template):
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

        r = requests.get(type_search, headers=headers, params=params)
        v = r.json()
        v['location'] = params['location']
        v['distance'] = params['distance']

        return render_template(template, data=v)
