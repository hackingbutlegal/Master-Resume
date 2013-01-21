# master-resume.py - (http://www.github.com/jackiesingh/Master-Resume) - 1/2013
#!/usr/bin/env python

import Image
from glob import glob
import json
import oauth2 as oauth
import os
import urllib
import subprocess
import pystache

# grab JSON-formatted profile data fron LinkedIn API
def get_lnkdn_json():

    # load api creds from JSON
    api_auth_conf = open('api-creds.json')
    api_auth_data = json.load(api_auth_conf)
    api_auth_conf.close()

    consumer_key = api_auth_data['consumer_key']
    consumer_secret = api_auth_data['consumer_secret']
    user_token = api_auth_data['user_token']
    user_secret = api_auth_data['user_secret']

    # authenticate to oauth
    consumer = oauth.Consumer(consumer_key, consumer_secret)
    access_token = oauth.Token(key=user_token, secret=user_secret)
 
    # instantiate oauth client object
    client = oauth.Client(consumer, access_token)

    # get a JSON set of the data we're interested in
    resp,content = client.request("http://api.linkedin.com/v1/people/~:(location:(name),public-profile-url,picture-url,first-name,maiden-name,last-name,email-address,phone-numbers,main-address,headline,summary,positions,certifications:(name,start-date,end-date,authority:(name)),educations,courses,skills,honors,languages)?format=json")
    content = content.replace('\\\\', '{\\\\textbackslash}')
    content = content.replace('\\n', '\\\\\\\\')
    profile_txt_json = json.loads(content)

    profile_data = {'profile' : profile_txt_json}

    # get JSON of url to profile picture (original size)
    resp,content = client.request("http://api.linkedin.com/v1/people/~/picture-urls::(original)?format=json")
    profile_img_json = json.loads(content)
    
    # join JSON sets
    profile_data['photo'] = profile_img_json
    profile_json = json.dumps(profile_data, sort_keys=True, indent=4)
 
    # print profile_json # (uncomment this for easier testing)

    # return full profile JSON set
    return profile_data

def render_lnkdn(profile):

    renderer = pystache.Renderer()

    # apply profile JSON set to resume template
    # this section determines the order of each group of data in the tex file
    resume = renderer.render_path('mustache/header.mustache', profile)
    resume += renderer.render_path('mustache/summary.mustache', profile)

    resume += renderer.render_path('mustache/languages.mustache', profile)
    for connection in profile['profile']['languages']['values']:
        connid = connection['language']
        resume += renderer.render_path('mustache/languages_style.mustache', connection)

    resume += renderer.render_path('mustache/educations.mustache', profile)
    for connection in profile['profile']['educations']['values']:
        connid = connection['schoolName']
        resume += renderer.render_path('mustache/educations_style.mustache', connection)

    resume += renderer.render_path('mustache/certifications.mustache', profile)
    for connection in profile['profile']['certifications']['values']:
        connid = connection['authority']
        resume += renderer.render_path('mustache/certifications_style.mustache', connection)

    resume += renderer.render_path('mustache/courses.mustache', profile)
    for connection in profile['profile']['courses']['values']:
        connid = connection['name']
        resume += renderer.render_path('mustache/courses_style.mustache', connection)

    resume += renderer.render_path('mustache/experience.mustache', profile)
    for connection in profile['profile']['positions']['values']:
        connid = connection['company']
        resume += renderer.render_path('mustache/positions_style.mustache', connection)

    resume += renderer.render_path('mustache/footer.mustache', profile)

    return resume

profile = get_lnkdn_json()
photourl = profile['photo']['values'][0]
headshot = open('headshot.jpg','wb')
headshot.write(urllib.urlopen(photourl).read())
headshot.close()
u = 'headshot.jpg'
# converting to a png for handling with XeLaTeX
out = u.replace('jpg','png')
img=Image.open(u)
img.save(out)
resume = render_lnkdn(profile)

# cleaning up some HTML-related ugliness, add new lines as necesarry to process out the ugly
resume = resume.replace("&amp;", "\&")
resume = resume.replace("quot;", " ")

# output contents of variable to resume.tex file in UTF-8
f = open( './resume.tex', 'w' )
f.write(resume.encode('utf-8'))
f.close()

# generate PDF from resume.tex
subprocess.call(["xelatex", "-interaction=nonstopmode", "./resume.tex"])
