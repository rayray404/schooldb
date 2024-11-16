
from mysql import connector
import json
import pickle

def verify_admin(form_data):
    with open("admin_id.bin", "rb") as adm_id_file:
        admin_cred=pickle.load(adm_id_file)
    print("a", form_data, admin_cred)
    if form_data==admin_cred:
        return True
    else:
        return False


with open("./misc/sql_access.json") as access_file:
    sql_access_dict = json.load(access_file)

conn = connector.connect(**sql_access_dict)

cursor=conn.cursor()

cursor.execute("USE test;")
# cursor.execute("CREATE TABLE students")
# cursor.execute(")")


print(cursor.fetchall())
conn.commit()
conn.close()
