#!/usr/bin/python
import sys, os
sys.path.insert(0, "/var/www/GodDogs/")

os.environ['DBENV'] = "./var/www/GodDogs/GodDogs/GodDog.db"
from GodDogs import app as application