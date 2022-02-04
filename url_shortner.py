
def shorten_url(url):
    """ shorten given url 
    
    Parameters
    ----------
    url : str
    url is a short version of irl
        
    
    1 long -> short url
    2- short url -> long url
    
    
    if I send  long url, i will go to the db and check 
    
    does the long url already exist? if yes will sned a new version of the DB. 
    
    
    
    *handle failed cases
     
     
     
    Shortening Logic:
There are different ways to go about this, I found a simplest way which is hashing. 
We will feed the long URL into the hashing function that will return us a string of a fixed length.
Multiple hashing functions are available, but we chose MD5 (128-bit hash value) for its popularity.


Md5 Hash -> Base62 Encoding -> Random Swap and pick 7 random caracters - > Generate short URL -> Store short URL into the DB
    """
    
    
    if url.find('tier.app')!=-1:
        url = url[url.find('.')+1:]
        
        
    return url 
    
    return('www.app.com')