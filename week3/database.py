import sqlite3

class database:

    def get_connection(self): #creating connection as method
        con = sqlite3.connect("courses.db")
        return con

    def create_user_table(self): #creating user table
        con = self.get_connection()
        cursor = con.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS USERS (
                            UserID INTEGER PRIMARY KEY AUTOINCREMENT,
                            NAME TEXT NOT NULL,
                            EMAIL TEXT UNIQUE NOT NULL,
                            PASSWORD TEXT NOT NULL)""")
        con.commit()
        con.close()

    def create_course_table(self): #course table
        con = self.get_connection()
        cursor = con.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS COURSES (
                            CourseID INTEGER PRIMARY KEY AUTOINCREMENT,
                            COURSE_NAME TEXT NOT NULL,
                            CATEGORY TEXT NOT NULL,
                            DURATION TEXT NOT NULL,
                            DESCRIPTION TEXT NOT NULL)""")
        con.commit()
        con.close()

    def create_enrolment_table(self): # enrollement table
        con = self.get_connection()
        cursor = con.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS ENROLEMENT (
                            enrollmentID INTEGER PRIMARY KEY AUTOINCREMENT,
                            UserID INTEGER,
                            CourseID INTEGER,
                            progress INTEGER DEFAULT 0,
                            enrollment_date TEXT,
                            FOREIGN KEY (UserID) REFERENCES USERS(UserID),
                            FOREIGN KEY (CourseID) REFERENCES COURSES(CourseID),
                            UNIQUE(UserID, CourseID))""")
        con.commit()
        con.close()

#enrollment methods
    def inser_enrolmet(self, user_id, course_id, date_str): # enroll to course
        con = self.get_connection()
        cursor = con.cursor()
        try:
            cursor.execute("INSERT INTO ENROLEMENT (UserID, CourseID, enrollment_date) VALUES (?, ?, ?)", 
                           (user_id, course_id, date_str))
            con.commit()
            return True #Added enrollment succeeded
        except sqlite3.IntegrityError:
            print("User already enrolled in this course!")
            return False # already enrolled 
        finally:
            con.close()
            
    
    def update_progress(self, enrollment_id, new_progress): #Updates the progress percentage for a specific enrollment.
        con = self.get_connection()
        cursor = con.cursor()
        cursor.execute("UPDATE ENROLEMENT SET progress = ? WHERE enrollmentID = ?", 
                       (new_progress, enrollment_id))
        con.commit()
        con.close()

    def enroll_btn(self,user_id): #cheching already enrolled or not
        con = self.get_connection()
        cursor = con.cursor()
        alreay_enrolred= cursor.execute("SELECT CourseID FROM ENROLEMENT WHERE UserID= ?",
                                        (user_id,)).fetchall() #list of tuple
        con.commit()
        con.close()
        return [ i[0] for i in alreay_enrolred] # returning as list

        
#course methods
    def view_all_course(self): # select all courses 
        con = self.get_connection()
        ALL_COURSE = con.execute("SELECT * FROM COURSES").fetchall()
        con.close()
        return ALL_COURSE
    
    def add_course(self, course_name, category, time, description): # add courses
        con = self.get_connection()
        cursor = con.cursor()
        try:
            cursor.execute("INSERT INTO COURSES (COURSE_NAME, CATEGORY, DURATION, DESCRIPTION) VALUES (?,?,?,?)", 
                           (course_name, category, time, description))
            con.commit()
        except sqlite3.IntegrityError:
            print("Course already exists!")
        finally:
            con.close()
            
    def delete_course(self, course_name): # delete course
        con = self.get_connection()
        cursor = con.cursor()  
        cursor.execute("DELETE FROM COURSES WHERE COURSE_NAME = ?", (course_name,))
        con.commit()
        con.close()
        
    def get_course_by_id(self, course_id): #select one course for course details
        con = self.get_connection()
        course = con.execute("SELECT * FROM COURSES WHERE CourseID = ?", (course_id,)).fetchone()
        con.close()
        return course # return particular course
    
    def search_courses(self, search_term): #filter course based on tile or deccription
        con = self.get_connection()
        query = "SELECT * FROM COURSES WHERE COURSE_NAME LIKE ? OR DESCRIPTION LIKE ?"
        result = f"%{search_term}%"
        filtered_courses = con.execute(query, (result, result)).fetchall()
        con.close()
        return filtered_courses # return filtered course
    
    def get_featured_courses(self):#featurred course
        con = self.get_connection()
        featured = con.execute("SELECT * FROM COURSES LIMIT 5").fetchall()
        con.close()
        return featured #return 5 course to show in home page
#user       
    def add_user(self, name, email, password): #add user
        con = self.get_connection()
        cursor = con.cursor()
        try:
            cursor.execute("INSERT INTO USERS (NAME, EMAIL, PASSWORD) VALUES (?, ?, ?)", 
                           (name, email, password))
            con.commit()
            return True
        except sqlite3.IntegrityError:#prevent duplicate user
            return False  
        finally:
            con.close()

    def get_user_by_email(self, email): #gives user mail password name userid
        con = self.get_connection()
        user = con.execute("SELECT * FROM USERS WHERE EMAIL = ?", (email,)).fetchone()
        con.close()
        return user
    
#course dashboard
    def get_user_enrollments(self, user_id):#using join to merge two table get
        con = self.get_connection()
        query = """
            SELECT e.enrollmentID, c.COURSE_NAME, c.CATEGORY, e.progress, e.enrollment_date
            FROM ENROLEMENT e
            JOIN COURSES c ON e.CourseID = c.CourseID
            WHERE e.UserID = ?
        """
        enrollments = con.execute(query, (user_id,)).fetchall()
        con.close()
        return enrollments
    
#profile update
    def update_user_profile(self, user_id, name, email, password):
        con = self.get_connection()
        cursor = con.cursor()
        try:
            cursor.execute("""UPDATE USERS SET NAME = ?, EMAIL = ?, PASSWORD = ? WHERE UserID = ?""", 
                           (name, email, password, user_id))
            con.commit()
            return True
        except sqlite3.IntegrityError:# error raised if they repeat 
            return False
        finally:
            con.close()

