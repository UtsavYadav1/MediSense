# This file contains the WSGI configuration required to serve your application on PythonAnywhere.
# You needs to copy the contents of this file into the WSGI configuration file linked 
# in the "Code" section of your PythonAnywhere Web Tab.

import sys
import os

# 1. Set the project path
# REPLACE 'your_username' with your actual PythonAnywhere username!
path = '/home/your_username/WellSure'
if path not in sys.path:
    sys.path.append(path)

# 2. Load Environment Variables manually
# PythonAnywhere doesn't load .env automatically in WSGI
from dotenv import load_dotenv
project_folder = os.path.expanduser(path)  # adjust as appropriate
load_dotenv(os.path.join(project_folder, '.env'))

# 3. Import the Flask app
# Main file is 'main.py' and the flask object is 'app'
from main import app as application
