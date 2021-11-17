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
        print(r.url)
        v = r.json()

        v['distance'] = params['distance']
        v['location'] = params['location']
        v['breeds'] = breeds()['breeds']

        return render_template("results_rescues.html", data=v)
    else:
        return render_template("home.html")


@views.route('/dogs', methods=['POST'])
def results_dogs():
    if request.method == 'POST':
        # handle sort
        if 'sortSelection' in request.form:
            v = dogSort(request)
            return render_template("results_dogs.html", data=v)

        # handle pagination
        if 'next' in request.form:
            v = pagination_check(dog_search, request)
            return render_template("results_dogs.html", data=v)


        params = {'type':'Dog'}

        for each in request.form:
            if request.form[each] != '':
                params[each] = request.form[each]

        if request.form['distance'] == '':
            params["distance"] = 0
            
        r = requests.get(dog_search, headers=headers, params=params)
        v = dicParams(r.json(), params)

        return render_template("results_dogs.html", data=v)
    else:
        return render_template("home.html")


# get breed list
def breeds():
    r = requests.get(breed_list, headers=headers)
    print(r.url)
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


def pagination_check(type_search, request):
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
    v = dicParams(r.json(), params)

    return v

def dogSort(request):
    print("This is the request:", request)
    print("Request list:", request.form)
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

    print(newParams)
    r = requests.get(dog_search, headers=headers, params=newParams)

    v = dicParams(r.json(), newParams)
    v['sorted'] = request.form['sortSelection']

    return v

def dicParams(v, params):
    primaryBreeds = []
    secondaryBreeds = []
    ages = []
    sizes = []
    genders = []

    v['location'] = params['location']
    v['distance'] = params['distance']
    v['primaryBreeds'] = primaryBreeds
    v['secondaryBreeds'] = secondaryBreeds
    v['age'] = ages
    v['size'] = sizes
    v['gender'] = genders
    v['params'] = params
    v['breeds'] = breeds()['breeds']

    for attrib in v['animals']:
        prim = attrib['breeds']['primary']
        sec = attrib['breeds']['secondary']
        age = attrib['age']
        size = attrib['size']
        gender = attrib['gender']
        
        if prim not in primaryBreeds:
            primaryBreeds.append(prim)
        if sec not in secondaryBreeds:
            secondaryBreeds.append(sec)
        if age not in ages:
            ages.append(age)
        if size not in sizes:
            sizes.append(size)
        if gender not in genders:
            genders.append(gender)

    return v
