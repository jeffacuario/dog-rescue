from flask import request
from flask import Blueprint, render_template
import requests
import json

views = Blueprint('views', __name__)

# petfinder api access information
setup = 'https://api.petfinder.com/v2/oauth2/token'
dogSearch = 'https://api.petfinder.com/v2/animals/'
rescueSearch = 'https://api.petfinder.com/v2/organizations/'
breedList = 'https://api.petfinder.com/v2/types/dog/breeds'


def setupAPI():
    """
    Initial Setup of PetFinder API 
    Returns headers needed to make calls for other functions
    """
    # load credentials from file
    with open('credentials.json') as configFile:
        config = json.load(configFile)

    data = {
        'grant_type': config['grant_type'],
        'client_id': config['pf_client_id'],
        'client_secret': config['client_secret']
    }
    req = requests.post(setup, data)
    response = req.json()

    headers = {
        'Authorization': 'Bearer ' + response['access_token']
    }
    return headers


headers = setupAPI()


@views.route('/')
def home():
    """
    Render Home Page
    """
    values = breeds()
    return render_template("home.html", data=values)


@views.route('/rescues', methods=['POST'])
def results_rescues():
    """
    Render List of Rescues based on user input
    """
    if request.method == 'POST':
        # handle sort
        if 'sortSelection' in request.form:
            values = rescueSort(request)
            return render_template("results_rescues.html", data=values)

        # handle pagination
        if 'next' in request.form:
            values = pagination_check(rescueSearch, request, 'rescue')
            return render_template("results_rescues.html", data=values)

        if request.form['distance'] == '':
            params = {
                "location": int(request.form['location']),
                "distance": 0
            }
        else:
            params = {
                "location": int(request.form['location']),
                "distance": int(request.form['distance'])
            }

        req = requests.get(rescueSearch, headers=headers, params=params)
        values = rescueParams(req.json(), params)

        return render_template("results_rescues.html", data=values)
    else:
        return render_template("home.html")


@views.route('/dogs', methods=['POST'])
def results_dogs():
    """
    Render List of Dogs based on user input
    """
    if request.method == 'POST':
        # handle sort
        if 'sortSelection' in request.form:
            values = dogSort(request)
            return render_template("results_dogs.html", data=values)

        # handle pagination
        if 'next' in request.form:
            values = pagination_check(dogSearch, request, 'dog')
            return render_template("results_dogs.html", data=values)

        params = {'type': 'Dog'}

        if request.form['distance'] == '':
            params["distance"] = 0

        for each in request.form:
            if request.form[each] != '':
                params[each] = request.form[each]

        req = requests.get(dogSearch, headers=headers, params=params)
        values = dogParams(req.json(), params)

        return render_template("results_dogs.html", data=values)
    else:
        return render_template("home.html")


def breeds():
    """
    Makes API call returning list of all available dog breeds
    """
    req = requests.get(breedList, headers=headers)
    values = req.json()
    return values


def pagination_check(type_search, request, flag):
    """
    Handle pagination links 
    Returns the parameters used in the search
    """
    string = request.form['next']

    params = {}

    values = string.find("?")
    y = string.find('=')

    first = string[values+1:y]
    values = string.find("&")
    first_value = string[y+1:values]
    params[first] = first_value

    string = string[values+1:]
    while values != -1 and y != -1:
        y = string.find("=")
        values = string.find("&")
        word = string[:y]
        value = string[y+1:values]
        params[word] = value

        string = string[values+1:]

    if value != string[y+1:]:
        params[word] = string[y+1:]

    req = requests.get(type_search, headers=headers, params=params)

    if flag == 'dog':
        values = dogParams(req.json(), params)
    else:
        values = rescueParams(req.json(), params)

    return values


def dogSort(request):
    """
    Handles the sort API call for dogs
    """
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

    req = requests.get(dogSearch, headers=headers, params=newParams)
    values = dogParams(req.json(), newParams)
    values['sorted'] = request.form['sortSelection']

    return values


def rescueSort(request):
    """
    Handles the sort API call for rescues
    """
    newParams = {}
    jsonParams = eval(request.form['params'])
    for p in jsonParams:
        newParams[p] = jsonParams[p]

    if request.form['sortSelection'] == 'Nearest':
        newParams['sort'] = 'distance'
    elif request.form['sortSelection'] == 'Furthest':
        newParams['sort'] = '-distance'
    elif request.form['sortSelection'] == 'A-Z':
        newParams['sort'] = 'name'
    elif request.form['sortSelection'] == 'Z-A':
        newParams['sort'] = '-name'

    req = requests.get(rescueSearch, headers=headers, params=newParams)
    values = rescueParams(req.json(), newParams)
    values['sorted'] = request.form['sortSelection']

    return values


def dogParams(values, params):
    """
    Returns dictionary of the params for dogs
    """
    primaryBreeds = []
    secondaryBreeds = []
    ages = []
    sizes = []
    genders = []

    values['location'] = params['location']
    values['distance'] = params['distance']
    values['primaryBreeds'] = primaryBreeds
    values['secondaryBreeds'] = secondaryBreeds
    values['age'] = ages
    values['size'] = sizes
    values['gender'] = genders
    values['params'] = params
    values['breeds'] = breeds()['breeds']

    for attrib in values['animals']:
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

    return values


def rescueParams(values, params):
    """
    Returns dictionary of the params for rescues
    """
    zipCodes = []

    values['location'] = params['location']
    values['distance'] = params['distance']
    values['breeds'] = breeds()['breeds']
    values['params'] = params
    values['zipCodes'] = zipCodes

    for attrib in values['organizations']:
        zip = attrib['address']['postcode']

        if zip not in zipCodes:
            zipCodes.append(zip)
    return values
