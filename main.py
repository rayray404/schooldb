from mysql import connector
import json

with open("sql_access.json") as access_file:
    sql_access_dict = json.load(access_file)
    