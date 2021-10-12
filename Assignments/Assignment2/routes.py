from flask import Blueprint, json, render_template, request
import string
from random import choices, randint
import datetime

from flask.wrappers import Response

bitly = Blueprint('short',__name__)
links=[]
links.append({
    "long_url": "www.verylongurl.com",
    "domain": "bit.ly",
    "group_guid" : "bsadjkbjdns",
    "title" : "Bitly API",
    "short_link":"bit.ly/jMbU",
    "no_of_clicks": 0,
    "created_at": "Wed, 06 Oct 2021 23:14:26 GMT",
    "id": 48,
})


@bitly.route('/shorten', methods=['POST'])
def shorten_link():
    link_json = request.get_json()
    if 'long_url' in link_json:
        domain = link_json['domain'] if 'domain' in link_json else 'bit.ly'  
        link_data={
            "long_url": link_json['long_url'],
            "domain":  domain,
            "group_guid" : link_json['group_guid'] if 'group_guid' in link_json else 'qwerty',
            "title" : "Bitly API",
            "short_link":domain+'/'+short_url(),
            "noOfClicks": randint(1,100),
            "created_at": datetime.datetime.now(),
            "id": randint(1,100),
        }
        links.append(link_data)
        return json.dumps(link_data)
    else:
        return bad_request()

def short_url():
    characters = string.digits + string.ascii_letters
    short_url = ''.join(choices(characters, k=4))
    return short_url



@bitly.route('/create_bitlinks', methods=['POST'])
def create_shortlink():
    link_json = request.get_json()   
    if 'long_url' in link_json: 
        domain = link_json['domain'] if 'domain' in link_json else 'bit.ly'  
        link_data={
            "long_url": link_json['long_url'],
            "domain": domain,
            "group_guid" : link_json['group_guid'] if 'group_guid' in link_json else 'qwerty',
            "title" : link_json['title'],
            "short_link":domain+'/'+short_url(),
            "no_of_clicks": randint(1,100),
            "created_at": datetime.datetime.now(),
            "id": randint(1,100),
            }

        links.append(link_data)
        return json.dumps(link_data)
    else:
        bad_request()



@bitly.route('/update_shortlink/<domain>/<short_link>', methods=['PATCH'])
def update_shortlink(domain,short_link):
        new_link=request.get_json()
        print(new_link)
        for link in links:
            if link['short_link']==domain+'/'+short_link:
                for key in new_link:
                    link[key] = new_link[key]
                return link
        return page_not_found()


@bitly.route('/retrieve_shortlink/<domain>/<short_link>')
def retrieve_shortlink(domain,short_link):
    for link in links:
        if link['short_link']== domain+'/'+short_link:
            return json.dumps(link) 
    
    return page_not_found()



@bitly.route('/getClicks/<domain>/<short_link>/clicks')
def getClicks(domain,short_link):
    unit = request.args.get('unit')
    units = request.args.get('units')
    unit_reference =request.args.get('unit_reference')

    for link in links:
        if link['short_link']== domain+'/'+short_link:
            res = {
                "link_clicks":[
                    {
                        "clicks": link['no_of_clicks'],
                        "date": datetime.datetime.now()
                    }                
                ],
                "unit": unit,
                "units": units,
                "unit_reference": unit_reference if unit_reference is not None else datetime.datetime.now()
            }
            return json.dumps(res)
    return page_not_found()


@bitly.route('/<domain>/<short_link>')
def redirect_to_link(domain,short_link):
    
    for link in links:
        if link['short_link']==domain+'/'+short_link:
            link['no_of_clicks']+=1
            return link['long_url']
    return page_not_found()      

@bitly.route('/')
def index():
    return render_template('index.html', links=links)


@bitly.errorhandler(404)
def page_not_found():
    response = {
    "message": "Link not found",
    "description": "Link not found. Create a new link",
    }
    return json.dumps(response), 404


@bitly.errorhandler(400)
def bad_request():
    response = {
     "message": "Please provide long url",
    "description": "Long url is not present in the request",   
    }
    return json.dumps(response), 400