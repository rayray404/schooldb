import sqlite3



with sqlite3.connect("school.db") as conn:
    cursor = conn.cursor()
    # cursor.execute("""
    #                 drop table announcements            
    #                 """)
    cursor.execute(""" delete from marks""")
    print(cursor.fetchall())




# import pickle

# with open("./misc/admin_id.bin", "wb") as f:
#     pickle.dump({"id":"admin", "password": "admin"}, f)