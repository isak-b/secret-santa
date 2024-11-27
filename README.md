# Secret Santa picker

Automatically create a list of giver-receiver pairs and send them an e-mail.

Author: Isak Barbopoulos (isak@xaros.org)

## Install

`pip install -r requirements.txt`

## Setup

Open `secret-santa/config.yaml` and modify the settings to suit your event.

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
