import os
import json

with open("./misc/sql_access.json") as access_file:
    sql_acc_dict = json.load(access_file)

with open("./misc/db_names.txt") as db_names_file:
    db_names = db_names_file.readlines()

def file_to_db(*db):
    os.system(f"mysql -u {sql_acc_dict["host"]} -p test < ./db/test.sql")
# file_to_db()


def db_to_file(*db):
    os.system(f"mysqldump -u {sql_acc_dict["host"]} -p test > ./db/test.sql")
# db_to_file()
