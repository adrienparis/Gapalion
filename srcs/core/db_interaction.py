import os
import sqlite3
import config

rsrcs_path = config.read("resources_path")
db_schema_path = os.path.join(rsrcs_path, "database", "schema.db")
db_bond_path = os.path.join(rsrcs_path, "database", "bond.db")

tables_shema = ['''CREATE TABLE IF NOT EXISTS Users (id SERIAL NOT NULL PRIMARY KEY, name text NOT NULL, email text, login text, promotion text)''', 
                '''CREATE TABLE IF NOT EXISTS Projects (id SERIAL NOT NULL PRIMARY KEY, name text NOT NULL, path text NOT NULL)''',
                '''CREATE TABLE IF NOT EXISTS Exams (name text NOT NULL, project integer NOT NULL)''',
                '''CREATE TABLE IF NOT EXISTS Trials (name text NOT NULL, soft text NOT NULL, command text NOT NULL)''',
                '''CREATE TABLE IF NOT EXISTS Events (name text NOT NULL)''',
                '''CREATE TABLE IF NOT EXISTS Themes (name text NOT NULL)''',
                ]

tables_bond = ['''CREATE TABLE IF NOT EXISTS Job (name text, user_id integer NOT NULL, project_id integer NOT NULL, owner INTEGER)''', #link between user and projects
                '''CREATE TABLE IF NOT EXISTS Drafting (name text, exam_id integer NOT NULL, project_id integer NOT NULL)''',
              ]



exit()
con_ = sqlite3.connect(db_schema_path)

cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS users
               (name text, email text, login text, promotion text)''')


for p in people:
    if "cs_mentor" in p.group:
        promotion = "mentor"
    elif [x for x in p.group if x.startswith("cs_promo")]:
        promotion = "student" + str(p.group[0][-3:])
    else:
        continue

    p.print()
    cur.execute('''INSERT INTO users VALUES ("''' + p.name + '''","''' + p.email + '''","''' + p.login + '''", "''' + promotion + '''")''')
con.commit()

con.close()
