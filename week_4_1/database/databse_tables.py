import sqlite3

class database:
    def connection(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        return cursor,conn
    
    def user_table(self): # 1. Users Table
        cursor,conn = self.connection()
        cursor.execute('''
            CREATE TABLE users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('Employer', 'Candidate'))
            )
        ''')
        conn.commit()
        conn.close()
        
    def job_table(self): # 2. Jobs Table
       
        cursor,conn = self.connection()
        cursor.execute('''
            CREATE TABLE jobs (
                job_id INTEGER PRIMARY KEY AUTOINCREMENT,
                employer_id INTEGER,
                company_name TEXT NOT NULL,
                job_title TEXT NOT NULL,
                location TEXT NOT NULL,
                experience TEXT,
                salary TEXT,
                skills TEXT,
                description TEXT,
                posted_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (employer_id) REFERENCES users (user_id)
            )
        ''')
        conn.commit()
        conn.close()
        
    def application_table(self):    # 3. Applications Table
    
        cursor,conn = self.connection()
        cursor.execute('''
            CREATE TABLE applications (
                application_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                job_id INTEGER,
                resume_file TEXT,
                applied_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'Pending' CHECK(status IN ('Pending', 'Reviewed', 'Accepted', 'Rejected')),
                FOREIGN KEY (user_id) REFERENCES users (user_id),
                FOREIGN KEY (job_id) REFERENCES jobs (job_id)
            )
        ''')
        conn.commit()
        conn.close()
    
    def save_table(self):

        cursor,conn = self.connection()
        cursor.execute('''
            CREATE TABLE save_job (
                save_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                job_id INTEGER,
                company_name TEXT NOT NULL,
                job_title TEXT NOT NULL,
                location TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (user_id),
                FOREIGN KEY (job_id) REFERENCES jobs (job_id)
            )
        ''')

        conn.commit()
        conn.close()
        
 



