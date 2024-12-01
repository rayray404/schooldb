import sqlite3



with sqlite3.connect("school.db") as conn:
    cursor = conn.cursor()
    # cursor.execute("""
    #                 drop table announcements            
    #                 """)
    cursor.execute("""
                    ALTER TABLE student ADD COLUMN class TEXT""")
    print(cursor.fetchall())




# import pickle

# with open("./misc/admin_id.bin", "wb") as f:
#     pickle.dump({"id":"admin", "password": "admin"}, f)