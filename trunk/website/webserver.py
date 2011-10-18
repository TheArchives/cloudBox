# Arc is copyright 2009-2011 the Arc team and other contributors.
# Arc is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSING" file in the "docs" folder of the Arc Package.

import web
import os
import sys

BASE_DIR = os.path.dirname(__file__)
sys.path.insert(0, BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = "settings"

from django.conf import settings
    
import django.template
import django.template.loader
import backend

def render(name, params={}):
    ctx = django.template.Context(params)
    t = django.template.loader.get_template(name)
    return t.render(ctx)

BACKEND_HOST = "127.0.0.1"
BACKEND_PORT = 50012
BACKEND_PASSWORD = "muchphooey"

urls = (
    '/', 'index',
    '/status/', 'status',
)
app = web.application(urls, globals())

class index:        
    def GET(self):
        return render("index.html", {})

class status:        
    def GET(self):
        bs = backend.BackendSocket(BACKEND_HOST, BACKEND_PORT, BACKEND_PASSWORD)
        worlds = sorted(bs.query("userworlds")['worlds'])
        users = bs.query("users")['users']
        return render("status.html", {"users": users, "worlds": worlds})

application = app.wsgifunc()
if __name__ == "__main__":
    app.run()
