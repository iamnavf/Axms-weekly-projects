import sqlite3
from database.databse_tables import database

db = database()

class job_table:
#add new job
    def add_job(self, employer_id, company_name, job_title, location, 
                experience, salary, skills, description):
        cursor, con = db.connection()
        try:
            cursor.execute('''
                INSERT INTO jobs (employer_id, company_name, job_title, 
                location, experience, salary, skills, description)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (employer_id, company_name, job_title, location, 
                  experience, salary, skills, description))
            con.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            con.close()

#get all the job  
    def all_job(self):
        cursor, con = db.connection()
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        all_jobs = cursor.execute("SELECT * FROM jobs ORDER BY posted_date DESC").fetchall()
        con.close()
        return all_jobs
    
#  get the job posted by paticular employee 
    def job_by_employee(self, employer_id):
        cursor, con = db.connection()
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        data = cursor.execute("SELECT * FROM jobs WHERE employer_id = ? ORDER BY posted_date DESC",
                              (employer_id,)).fetchall()
        con.close()
        return data

# get the particular job 
    def job_by_jobid(self, job_id):
        cursor, con = db.connection()

        # Enable Row Factory to acess by col name
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        
        
        # Index:   0        1            2             3          4         5           6       7       8
        job = cursor.execute("""
            SELECT job_id, employer_id, company_name, job_title, location, experience, salary, skills, description 
            FROM jobs 
            WHERE job_id = ?
        """, (job_id,)).fetchone()
        
        con.close()
        return job
    
#update the job details   
    def update_job(self, job_id, employer_id, company_name, job_title,
                   location, experience, salary, skills, description):
        cursor, con = db.connection()
        try:
            cursor.execute('''
                UPDATE jobs 
                SET company_name = ?, job_title = ?, location = ?,
                experience = ?, salary = ?, skills = ?, description = ?
                WHERE job_id = ? AND employer_id = ?
            ''', (company_name, job_title, location, experience, salary,
                  skills, description, job_id, employer_id))
            con.commit()
            return True
        except Exception as e:
            print(f"Error updating job: {e}")
            return False
        finally:
            con.close()

#delete the job
    def delete_job(self, job_id, employer_id):
        cursor, con = db.connection()
        try:
            cursor.execute('DELETE FROM jobs WHERE job_id = ? AND employer_id = ?', 
                           (job_id, employer_id))
            con.commit()
            return True
        except Exception as e:
            print(f"Error removing job: {e}")
            return False
        finally:
            con.close()

#filter ou job   
    def filter_jobs(self, query=None, location=None, experience=None, max_salary=None):
        """Fetches jobs based on dynamic optional filters from the sidebar."""
        cursor, con = db.connection()
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        
        sql = "SELECT * FROM jobs WHERE 1=1"
        params = []
        
        if query:
            sql += " AND (job_title LIKE ? OR company_name LIKE ? OR skills LIKE ?)"
            search_filter = f"%{query}%"
            params.extend([search_filter, search_filter, search_filter])
            
        if location:
            sql += " AND location LIKE ?"
            params.append(f"%{location}%")
    
        if experience:
            sql += " AND experience LIKE ?"
            params.append(f"%{experience}%")
            
        if max_salary:
            sql += " AND salary LIKE ?"
            params.append(f"%{max_salary}%")
            
        sql += " ORDER BY posted_date DESC"
        
        results = cursor.execute(sql, tuple(params)).fetchall()
        con.close()
        return results