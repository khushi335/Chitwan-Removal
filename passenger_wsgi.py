import os
import sys

# Add the project directory to the Python path
project_home = "/home1/studiori/chitwanremoval.com.au/chitwan_removal"
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Activate the virtual environment
activate_env = "/home1/studiori/virtualenv/chitwanremoval.com.au/chitwan_removal/3.10/bin/activate_this.py"
with open(activate_env) as file_:
    exec(file_.read(), {"__file__": activate_env})

# Set the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chitwan_removal.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()