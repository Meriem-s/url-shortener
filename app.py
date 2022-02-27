from flask import Flask, jsonify, request, redirect, url_for
import sqlite3
from hashids import Hashids
from helper import  url_validator, extract_domain
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime    


app = Flask(__name__)
app.config.from_pyfile('flask_config.cfg')
db = SQLAlchemy(app)
from model import Urls


@app.before_first_request 
def create_tables():
    db.create_all()

#We need to specify a salt for the Hashids library; 
# this will ensure the hashes are unpredictable since every time the salt changes, the hashes also change.
hashids = Hashids(min_length=4, salt=app.config['SECRET_KEY'])
    

@app.route('/<id>')
def url_redirect(id):
    """
    This route takes the short hash that has been generated inside index() and decodes the hash into its integer value (the original URLs ID)
    At the end, users will be redirected to the original URL and the return a unique short-form URL .
    """    
    #decode hash into integer value
    id_orig = hashids.decode(id) 
    
    if id_orig:
        original_id = id_orig[0]       
        url_data = Urls.query.filter_by(id=original_id).first()         
        url_original = url_data.url_original
        url_short = url_data.url_short
        count_original = url_data.count_original       
        db.session.commit()
        return(redirect(url_original))
    
    else:
        return(jsonify(error='Invalid URL'))


@app.route('/shortenurl', methods=('GET', 'POST'))
def index():
    """
    return the shortened url upon POST requests and store it in DB 
    """    
    if request.method == 'POST':
        #Get raw long url         
        content= request.get_json(force=True)
        print(content)
        if not content:
            return(jsonify(status=400 ,error='Bad request'))
            
        url = content['url']
        
        if url_validator(url) == False : 
            return(jsonify(error='Wrong url format'))
        
        if not url:
            return redirect(url_for('index'))
        
        # if url_original exists than increment the count_original, if not then we add it to the DB
        found_short_url = Urls.query.filter_by(url_short=url).first()
        print('found_short_url',found_short_url)
        found_long_url = Urls.query.filter_by(url_original=url).first()
        print('found_long_url',found_long_url)
        if found_short_url: 
            #if url_original exists than increment the count_original in the DB
            db.session.query(Urls).filter_by(url_short= url).update({Urls.count_original: Urls.count_original+ 1})
            db.session.commit()
            print('original_url found then increment count')
            return(jsonify(url=found_short_url.url_original, sent_url_type='short'))
        
        elif not found_long_url:
            #create new model 
            url_record = Urls(url, '', datetime.now(), 0) 
            #save model
            db.session.add(url_record)
            db.session.commit()
        
        new_long_url = Urls.query.filter_by(url_original=url).first()       
        id_url =  new_long_url.id
        hash_id = hashids.encode(id_url)
        url_short = request.host_url + hash_id      
        db.session.query(Urls).filter_by(url_original= url).update({Urls.url_short: url_short })
        db.session.commit()       
        redirect(url_short)# url_redirect(id) function will be called 
        return(jsonify(url=url_short, count= new_long_url.count_original, sent_url_type='long'))

        

    return(jsonify(status=400 ,error='Bad request'))
    
    
if __name__ == '__main__':
    app.run(host="127.0.0.1:5000")