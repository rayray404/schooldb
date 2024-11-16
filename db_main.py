
from mysql import connector
import json


with open("./misc/sql_access.json") as access_file:
    sql_access_dict = json.load(access_file)

conn = connector.connect(**sql_access_dict)

cursor=conn.cursor()

cursor.execute("USE  test;")
cursor.execute("CREATE TABLE students")
# cursor.execute(")")


print(cursor.fetchall())
conn.commit()
conn.close()
