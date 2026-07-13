import sqlite3

from database.databse_tables import database

db = database()

class application_table:
    #adding the applicant
    def apply_job(self, user_id, job_id, resume_file):
        cursor, con = db.connection()#getting connection
        try:
            cursor.execute('''
                INSERT INTO applications (user_id, job_id, resume)
                VALUES (?, ?, ?)
            ''', (user_id, job_id, resume_file))
            con.commit()
            return True
        except Exception as e: 
            # This line will print the exact reason for the failure in your terminal window
            print(f"Database Error: {e}")
            return False
        finally:
            con.close()

    def get_applications_by_candidate(self, user_id):#application satus to diplay in dash board
        cursor, con = db.connection()
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        applications = cursor.execute('''
            SELECT a.application_id, a.applied_date, a.status, a.resume,
                   j.job_title, j.company_name, j.location
            FROM applications a
            JOIN jobs j ON a.job_id = j.job_id
            WHERE a.user_id = ?
            ORDER BY a.applied_date DESC 
        ''', (user_id,)).fetchall() #using joins to join app table and job table
        con.close()
        return applications

    def get_applications_for_employer(self, employer_id):
        cursor, con = db.connection()
        con.row_factory = sqlite3.Row #to acess them by col name we use row factory
        cursor = con.cursor()
        applicants = cursor.execute('''
            SELECT a.application_id, a.applied_date, a.status, a.resume,
                   u.name AS candidate_name, u.email AS candidate_email,
                   j.job_title
            FROM applications a
            JOIN users u ON a.user_id = u.user_id
            JOIN jobs j ON a.job_id = j.job_id
            WHERE j.employer_id = ?
            ORDER BY a.applied_date DESC
        ''', (employer_id,)).fetchall() #using join get job name from job table user name from user table resume from app table
        con.close()
        return applicants
    

#update the application satus
    def update_application_status(self, application_id, new_status):
        cursor, con = db.connection()
        try:
            cursor.execute('''
                UPDATE applications 
                SET status = ? 
                WHERE application_id = ?
            ''', (new_status, application_id))
            con.commit()
            return True
        except Exception:
            return False
        finally:
            con.close()

#get job id to check they allready applied or not            
    def get_applied_job_ids_by_candidate(self, user_id):
        cursor, con = db.connection()
        try:
            rows = cursor.execute('''
                SELECT job_id FROM applications WHERE user_id = ?
            ''', (user_id,)).fetchall()
            return [row[0] for row in rows]
        except Exception:
            return []
        finally:
            con.close()


    def check_existing_application(self, user_id, job_id):
        cursor, con = db.connection()
        try:
            existing = cursor.execute("""
                SELECT 1 FROM applications 
                WHERE user_id = ? AND job_id = ?
            """, (user_id, job_id)).fetchone()
            return existing is not None
        except Exception:
            return False
        finally:
            con.close()