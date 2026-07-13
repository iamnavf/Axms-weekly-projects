import sqlite3
from database.databse_tables import database

db = database()

class user_table:

#add user
    def add_user(self,name,email,password,role):
        cursor,con=db.connection()
        try:
            cursor.execute("""
                INSERT INTO users (name, email, password, role) 
                VALUES (?, ?, ?, ?)
            """, (name, email, password, role))
            con.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            con.close()

#verify the user      
    def verify_user(self, email):
        cursor, con = db.connection()
       
        user = cursor.execute("SELECT user_id, name, email, password, role FROM users WHERE email = ?", (email,)).fetchone()
        con.close()
        return user

#select the user by id 
    def user_by_id(self, id):
        cursor, con = db.connection()
        # Enable Row Factory to acces by col name
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        
        # Index layout:  0        1     2      3         4     5            6       7       8         9
        user = cursor.execute("""
            SELECT user_id, name, email, password, role, resume_file, profile_pic,skills,experience,company 
            FROM users 
            WHERE user_id = ?
        """, (id,)).fetchone()
        con.close()
        return user
    
#update the profile
    def update_profile(self, user_id, name, email, skills, experience, resume_file, profile_pic,company):
        cursor, con = db.connection()
        try:
            # We update the primary user details
            sql = "UPDATE users SET name = ?, email = ?"
            params = [name, email]
            
            # Only append the file string if a new file was actually uploaded
            if resume_file:
                sql += ", resume_file = ?"
                params.append(resume_file)
            if profile_pic:
                sql += ", profile_pic = ?"
                params.append(profile_pic)
            if skills:
                sql +=", skills = ?"
                params.append(skills)
            if skills:
                sql +=", experience = ?"
                params.append(experience)
            if company:
                sql +=", company = ?"
                params.append(company)
                
            sql += " WHERE user_id = ?"
            params.append(user_id)
            
            cursor.execute(sql, tuple(params))
            con.commit()
            return True
        except sqlite3.IntegrityError:
            return False 
        finally:
            con.close()

# Save a job 
    def save_job(self, user_id, job_id):
        cursor, con = db.connection()
        try:
            #check if the job details exist 
            job = cursor.execute("SELECT company_name, job_title, location FROM jobs WHERE job_id = ?", (job_id,)).fetchone()
            if not job:
                return False

            # Check if the candidate has already saved this job
            already_saved = cursor.execute(
                "SELECT 1 FROM save_job WHERE user_id = ? AND job_id = ?", (user_id, job_id)
            ).fetchone()

            if already_saved:
                return True  # Already saved,

            # Insert a new save table
            cursor.execute("""
                INSERT INTO save_job (user_id, job_id, company_name, job_title, location)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, job_id, job[0], job[1], job[2]))
            con.commit()
            return True
        except Exception as e:
            print(f"Database Error: {e}")
            return False
        finally:
            con.close()

# Get all saved jobs for a specific user
    def get_save_job(self, user_id):
        cursor, con = db.connection()
        try:
            query = """
                SELECT job_id, company_name, job_title, location 
                FROM save_job 
                WHERE user_id = ?
                ORDER BY save_id DESC
            """
            rows = cursor.execute(query, (user_id,)).fetchall()

            saved_jobs_list = []
            for row in rows:
                saved_jobs_list.append({
                    'job_id': row[0],
                    'company_name': row[1],
                    'job_title': row[2],
                    'location': row[3]
                })#setting up like dictionary
            return saved_jobs_list
        except Exception as e:
            return []
        
        finally:
            con.close()

#unsave job
    def unsave_job(self, user_id, job_id):
        cursor, con = db.connection()
        try:
            cursor.execute("DELETE FROM save_job WHERE user_id = ? AND job_id = ?", (user_id, job_id))
            con.commit()
            return True
        except Exception as e:
            return False
        
        finally:
            con.close()



