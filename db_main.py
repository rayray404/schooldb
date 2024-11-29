import sqlite3



with sqlite3.connect("school.db") as conn:
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS attendance_12a 
                   (
                    s_id INTEGER,
                    
                    present BOOL,
                   FOREIGN KEY(s_id) REFERENCES student(s_id)
                   )""")




