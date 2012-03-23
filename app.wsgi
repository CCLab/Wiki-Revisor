import sys, os

sys.path = ['/var/www/wiki_rewizor/'] + sys.path
os.chdir(os.path.dirname(__file__))

import bottle, app

application = bottle.default_app()