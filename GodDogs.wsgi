#!/usr/bin/python
import sys, os
sys.path.insert(0, "/var/www/dogechat/")

os.environ['DBENV'] = "./var/www/dogechat/GodDogs/GodDog.db"
from GodDogs import app as application
