from itertools import count
from flask import Flask, jsonify, request, redirect, url_for
import sqlite3
from hashids import Hashids
from helper import  url_validator, extract_domain

app = Flask(__name__)
app.config.from_pyfile('flask_config.cfg')

#We need to specify a salt for the Hashids library; 
# this will ensure the hashes are unpredictable since every time the salt changes, the hashes also change.
hashids = Hashids(min_length=4, salt=app.config['SECRET_KEY'])



@app.route('/<id>')
def url_redirect(id):
    """
    This route takes the short hash that has been generated inside index() and decodes the hash into its integer value (the original URLs ID)
    At the end, users will be redirected to the original URL and the return a unique short-form URL .
    """
    
    #connect to DB
    con = sqlite3.connect('database.db')
    con.row_factory = sqlite3.Row
    
    #decode hash into integer value
    id_orig = hashids.decode(id) 
    
    if id_orig:
        original_id = id_orig[0]
        url_data = con.execute('SELECT url_original, url_short, count_original FROM urls'
                                ' WHERE id = (?)', (original_id,)
                                ).fetchone()
        
        url_original = url_data['url_original']
        url_short = url_data['url_short']
        count_original = url_data['count_original']       
        con.commit()
        con.close()
        return(redirect(url_original))
    
    else:
        return(jsonify(error='Invalid URL'))


@app.route('/shortenurl', methods=('GET', 'POST'))
def index():
    """
    return the shortened url upon POST requests and store it in DB 
    """
    
    #connect to DB
    con = sqlite3.connect('database.db')
    con.row_factory = sqlite3.Row
    
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
                
        check_long_url = con.execute('SELECT * FROM urls WHERE url_original = ?',(url,)).fetchone()
        check_short_url = con.execute('SELECT * FROM urls WHERE url_short = ?',(url,)).fetchone()

        #if short url found, return long url from db and increment count_original
        if check_short_url: 
            counter= check_short_url['count_original'] + 1
            con.execute("UPDATE urls SET count_original = ? , url_short = ? WHERE id = ?", (counter ,check_short_url['url_short'], check_short_url['id']))
            con.commit()
            con.close() 
            return(jsonify(url=check_short_url['url_original'], sent_url_type='short'))

        #if check_long_url not found
        if not check_long_url: 
            data =  con.execute("INSERT INTO urls(url_original) VALUES (?)",(url,))
    
        #get id of latest record 
        lastrecord = con.execute('SELECT * FROM urls  WHERE url_original = ?', (url,)).fetchone()
        id_url = lastrecord['id'] 
        hash_id = hashids.encode(id_url)
        url_short = request.host_url + hash_id 
        
        if not check_long_url: 
            data =  con.execute("UPDATE urls SET url_short = ? WHERE url_original =?",(url_short,url))
            
        con.commit()
        con.close() 
        
        redirect(url_short)# url_redirect(id) function will be called 
        return(jsonify(url=url_short, count= lastrecord['count_original'], sent_url_type='long'))

        

    return(jsonify(status=400 ,error='Bad request'))
    
    
if __name__ == '__main__':
    app.run(host="127.0.0.1:5000")