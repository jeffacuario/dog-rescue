params = {}

# string = '/v2/animals?distance=10&location=94513&type=Dog&page=2'
string = '/v2/animals?distance=10&location=94513&page=1&type=Dog'


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

print(params)