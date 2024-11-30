import sqlite3



with sqlite3.connect("school.db") as conn:
    cursor = conn.cursor()
    # cursor.execute("""
    #                 drop table announcements            
    #                 """)
    cursor.execute("""
                    CREATE TABLE announcements (announcement_id int auto_increment primary key,
                   announcement_title text default "",
                   announcement_text text default "",
                   announcer text default "Principal",
                   announce_date date default current_date)                
                    """)
    print(cursor.fetchall())




# import pickle

# with open("./misc/admin_id.bin", "wb") as f:
#     pickle.dump({"id":"admin", "password": "admin"}, f)