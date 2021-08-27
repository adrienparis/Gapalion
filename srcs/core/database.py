import os
import sqlite3
import config

db_path = os.path.join(config.read("resources_path"), "database", "gapalion.db")
con = sqlite3.connect(db_path)

cur = con.cursor()
