# Dog Rescue Webapp

A dog rescue application that allows users search for dogs based on selected parameters. The app would look for a match and allow the user to read more about the dog allowing them to decide if they want to move forward with adoption. App also allows users to search for rescues based on the location provided.

![](dog-rescue.gif)
## Cloning Repository

```bash
git clone https://github.com/jeffacuario/dog-rescue.git
```

## Python Virtual Environment (Optional but Recommended)

Open terminal, navigate to the root of your project folder (the top level of your repo folder):

```bash
# On your machine:
pip3 install virtualenv
```

We then want to run the command

```bash
# Linux and Mac
python3 -m virtualenv ./venv

# Windows Command Prompt
python -m virtualenv venv
```

This will create a virtual environment in your project root. It will be in the folder `venv` located in the project root.

To activate the virtual environment:

```bash
# Linux and Mac
source ./venv/bin/activate

# Windows Command Prompt
/venv/Scripts/activate
```

If you ever want to leave the virtual environment

```bash
deactivate
```

## Install Dependencies

In the terminal, change directory to the dog-rescue folder and make sure the virtual environment is activated, then run the command:

```bash
pip3 install -r requirements.txt
```

## Get Petfinder API Key

Go to [Petfinder](https://www.petfinder.com/developers/v2/docs/) and click Sign Up.

Under the Developer Settings you will find your API key and Secret.

## Create credentials.json

Create `credentials.json` in the same level as `main.py` with the format

```
{
  "grant_type": "client_credentials",
  "pf_client_id": "Enter API Key here",
  "client_secret": "Enter Secret Key here"
}
```

## Running application

After all of the setup you can run the command:

```bash
python3 .\main.py
```
