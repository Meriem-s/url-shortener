from urllib.parse import urlparse

def url_validator(url):
    """Helper function to validate url format"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc, result.path])
    except:
        return False

def extract_domain(url):
    domain = urlparse(url).netloc
    domain_sp = domain.split('.')
    domain = domain_sp[len(domain_sp) - 2] + '.' + domain_sp[-1] 
    print(domain)
    return domain