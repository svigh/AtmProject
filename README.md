# AtmProject

Atm project with REST-ful elements

## `headquarters_backend.py`

    This is the HQ server, it contains admin operations to the master users database and manages each ATM transaction.

## `hqClient.py`

    This is the HQ client, which has admin privileges to modify the master database. This client needs to provide a theoretical password to have access.

## `atm_frontend.py`

    This is the ATM server interface with the user. it allows a client to access its account and do operations on their personal account.

## `atmClient.py`

    This is the ATM client which has to provide account info to acces its bank account.
