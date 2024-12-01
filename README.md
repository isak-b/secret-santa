# Secret Santa Picker

Automatically create a list of giver-receiver pairs and send an e-mail to each giver.

Author: Isak Barbopoulos (isak@xaros.org)

## Install

`pip install -r requirements.txt`

## Setup

1. Open `config.yaml` and modify the list of participants and the e-mail template to suit your event.

2. Create a SMTP token for your gmail account:

    [Google app passwords](https://myaccount.google.com/apppasswords)

3. Add your gmail address and the SMTP token to the environment in one of two ways:

    a. Export them using the terminal:

        export SENDER_EMAIL="your gmail account e-mail address
        export SMTP_TOKEN="your gmail token

    b. Create an .env file in the root of the project with the following content:
    
        SENDER_EMAIL="your gmail account e-mail address"
        SMTP_TOKEN="your gmail token"

## Usage

**NOTE**: 
- It is highly recommended that you try the program out before sending out any real e-mails (e.g., use your own e-mail address for all participants)
- I do not take any responsibility for any errors, mistakes or misuse on anyone's part including my own
- Run the script with the `-m` flag or the internal imports may break

### Dry run (removes the option to send e-mails)

`python -m santa --dry-run`

### Real run

`python -m santa`

## Run with a custom path to config.yaml

`python -m santa path/to/config.yaml`

## Unit tests

Install dev requirements:

`pip install -r requirements-dev.txt`

Run tests:

`pytest`
