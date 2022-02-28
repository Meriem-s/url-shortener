
# URL Shortner using Flask ,SQLAlchemy and SQLite

## Problem

This Flask server application is an API that can:
1. Receive a URL and return a unique short-form URL for a domain.
2. Receive a short URL and return the original long URL. (For the sake of simplicity, this
does not have to be a redirect from the short URL to the long one. For the real thing, it
would work that way; here, just do whatever satisfies the requirement.)
3. Count the number of times each short URL was resolved back to the original, as per
point 3 above within the database.


## Getting started

For the standalone web service:

### Install Requirements 
only Flask, SQLite will be used for this installation. 
```shell
pip install -r requirements.txt
```

### Run Server 
```shell
python -m flask run
```

## Usage
To test the API,  json data is sent through POST requesand parsed. Below there are few examples of the usage.  

```
POST http://127.0.0.1:5000/shortenurl
```

REQUEST
A long url is sent.
```json
{
	"url": "https://about.tier.app/fr/sustainability/?_ga=2.85563857.939010014.1643906854-877565766.1641397042"
}
```
RESPONSE
```json
{
    "count": 10,
    "sent_url_type": "long",
    "url": "http://127.0.0.1:5000/jlAD"
}

```

- url: returned url, can be in short form or long form depending on the sent url
- count: is the number of times each short URL was resolved back to the original
- sent_url_type: type of the url to be transformed (long or short)
  
```
POST http://127.0.0.1:5000/shortenurl
```

REQUEST
A short url is sent.
```json
{ "url": "http://127.0.0.1:5000/jlAD" }
```
RESPONSE
the original long url will be sent back as follows:
```json
{
    "sent_url_type": "short",
    "url": "https://about.tier.app/fr/sustainability/?_ga=2.85563857.939010014.1643906854-877565766.1641397042"
}

