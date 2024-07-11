from datetime import datetime                                                   
from random import sample  
from os import path
from time import time                                                           
import os

from jinja2 import Template
SCRIPT_DIR = path.abspath(path.join(path.dirname(__file__)))


def jinja(args):

    # start timing
    name = args.get('username')
    size = args.get('random_len')
    cur_time = datetime.now()
    random_numbers = sample(range(0, 1000000), size)
    template = Template( open('/app/JinjaTemplate.html', 'r').read())
    html = template.render(username = name, cur_time = cur_time, random_numbers = random_numbers)

    if (html): 
        result =  {
            "status" : f" Sucess. HTML sucessfully create with name **{name}** ",
            "output" : html
            }

    return (result)
    

biblio = { 'jinja' : jinja}

# Define the main function
def main(args):
    if "username" in args:
        username = args["username"]
    else: username = "default"
    if "random_len" in args:
        random_len = args["random_len"]
    else: random_len = 1
    result = biblio['jinja']({"username" : username, "random_len" : random_len})
    
    return {'staus': result["status"]}

 

