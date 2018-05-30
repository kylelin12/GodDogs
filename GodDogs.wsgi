#!/usr/bin/python
import sys
if not "/var/www/GodDogs" in sys.path:
    sys.path.insert(0, "/var/www/GodDogs/")
from GodDogs import app as application