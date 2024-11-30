# Secret Santa picker

Automatically create a list of giver-receiver pairs and send them an e-mail.

Author: Isak Barbopoulos (isak@xaros.org)

## Install

`pip install -r requirements.txt`

## Setup

1. Open `config.yaml` and modify the settings to suit your event.

2. Create a SMTP token for gmail:

    [Google app passwords](https://myaccount.google.com/apppasswords)

3. Add the SMTP token to the environment in one of two ways:

    a. `export SMTP_TOKEN="your token"`
    b. Create an .env file in the root of the project and `SMTP_TOKEN="your token"` 

## Usage

### Dry run (e-emails will be printed to terminal rather than sent)

`python -m santa --dry-run`

### Real run

NOTE: Not yet implemented

`python -m santa`


## Unit tests

Install dev requirements:

`pip install -r requirements-dev.txt`

Run tests:

`pytest`
