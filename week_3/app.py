from flask import Flask, render_template, redirect, url_for, request, flash, session
from datetime import datetime

from database import database

# Initialize database instance object
db = database()


app = Flask(__name__)
app.secret_key = 'super_secret_key_change_me_in_production' # super key to use session


@app.route("/")#home page route
def home():
    featured_courses = db.get_featured_courses()
    return render_template("home.html",featured=featured_courses)


@app.route('/courses')#all courses
def courses():
    search_query = request.args.get('search', '').strip()
    
    if "user_id" in session:#checking weather the user is in log in
        allready_enrolled = db.enroll_btn(session["user_id"])#to ckeck the course allready enrolled or not
    else:
        allready_enrolled =[]

    if search_query:# selecting the filered course
        all_courses = db.search_courses(search_query)
    else:
        all_courses = db.view_all_course()#if no filetr all course dispaly
    return render_template('courses.html', courses=all_courses, search_query=search_query,allready_enrolled=allready_enrolled)
#rendering all the course, search key word, allready endrolled course list

@app.route('/course/<int:course_id>')#course detail page
def course_details(course_id):
    course = db.get_course_by_id(course_id)#getting the specific course by that course id

    if "user_id" in session:#checking the user loged in or not
        allready_enrolled = db.enroll_btn(session["user_id"]) #checking already enrolled or not
    else:
        allready_enrolled =[]

    return render_template('course_details.html', course=course,allready_enrolled=allready_enrolled)

@app.route('/enroll/<int:course_id>', methods=['POST'])#enroll to the course
def enroll(course_id):
    if 'user_id' not in session:#checking user in log in or not
        flash("Please log in to enroll in courses.", "error")
        return redirect(url_for('login'))
        
    user_id = session['user_id']
    today_date = datetime.today().strftime('%d/%m/%y')
    
    #inserting data into the enrollemnt table
    success = db.inser_enrolmet(user_id, course_id, today_date)#return true / false
    
    if success:#cheking true / false and redirect
        flash("Successfully enrolled in the course!", "success")
        return redirect(url_for('dashboard'))
    else:
        flash("You are already enrolled in this course!", "warning")
        return redirect(url_for('courses'))

@app.route('/dashboard', methods=['GET', 'POST']) # course progress dashboard
def dashboard():
    if 'user_id' not in session: # checking user in the session or not
        flash("Please log in to access your dashboard.", "error")
        return redirect(url_for('login'))
        
    user_id = session['user_id']
    
    if request.method == 'POST':#cheching whether it is post oor not
        enrollment_id = request.form.get('enrollment_id')
    
        new_progress = request.form.get('progress', type=int)
        
        # cheing the progess between 0% and 100%
        if new_progress is not None and 0 <= new_progress <= 100:
            db.update_progress(enrollment_id, new_progress)
            
            if new_progress == 100:#pop up message
                flash("Successfully coure completed","success")
            else:
                flash("New progress successfully updated","success")
        else:
            flash("Enter the valid progress between 0 to 100")
            
        return redirect(url_for('dashboard'))
        
    my_coures = db.get_user_enrollments(user_id) # get the enrolled coures
    return render_template('dashboard.html', enrollments=my_coures)


@app.route('/login', methods=['GET', 'POST'])
def login(): #check the posted credential with the data in user database
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = db.get_user_by_email(email)
        
        # user[0]=UserID, user[1]=NAME, user[2]=EMAIL, user[3]=PASSWORD
        if user and user[3] == password:
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            flash(f"Welcome back, {user[1]}!", "success")
            return redirect(url_for('home'))
        else:
            flash("Invalid email credentials or matching password. Try again.", "error")
            return redirect(url_for('login'))
            
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register(): 
    if request.method == 'POST':#checking method is post
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        success = db.add_user(name, email, password)#add the fetched value to db
        if success:
            flash("Registration Successful! Please log in with your new credentials.", "success")
            return redirect(url_for('login'))
        else:
            flash("Error: That email identifier layout is already registered here!", "error")
            return redirect(url_for('register'))
            
    return render_template('register.html')#if method is get


@app.route('/logout')
def logout():
    session.clear() #clear the current session and return to home
    flash("You have successfully logged out.", "success")
    return redirect(url_for('home'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        flash("Please log in to manage your account profile.", "error")
        return redirect(url_for('login'))
        
    user_id = session['user_id']
    
    if request.method == 'POST':#update the profile with new mail and password
        new_name = request.form.get('name')
        new_email = request.form.get('email')
        new_password = request.form.get('password')

        success = db.update_user_profile(user_id, new_name, new_email, new_password)
         # send the data to db
        if success:#if succesfully added 
            session['user_name'] = new_name
            flash("Account profile updated successfully!", "success")
            return redirect(url_for('profile'))
        else:#if error passes
            flash("Error: That email address is already taken by another user.", "error")
            return redirect(url_for('profile'))
        
    return render_template('profile.html')#if method is get


if __name__ == "__main__":#check the we are running from main page
    app.run()