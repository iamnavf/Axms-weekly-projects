from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
from werkzeug.security import generate_password_hash, check_password_hash

from database.user_database import db
from database.user_database import user_table
from database.job_database import job_table
from database.application_database import application_table

us_db=user_table()#initializing object for the class
job_db=job_table()#initializing object for the class
app_db=application_table()#initializing object for the class


app = Flask(__name__)

app.secret_key = 'You_will_get_it'#secret key for session


app.config['UPLOAD_FOLDER'] = 'static/uploads'#stroes the uploaded files in dict


os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)#create folder
#home
@app.route("/")
def home():
    jobs = job_db.all_job()[:5]#fetch 5 jobs 
    
    cursor, con = db.connection()#collecting the stats 
    total_jobs = cursor.execute("SELECT COUNT(*) FROM jobs").fetchone()[0]
    total_companies = cursor.execute("SELECT COUNT(DISTINCT company_name) FROM jobs").fetchone()[0]
    total_candidates = cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'Candidate'").fetchone()[0]
    con.close()
    
    stats ={
        "jobs": total_jobs,
        "companies": total_companies,
        "candidates": total_candidates
    }
    
    return render_template("home.html",jobs=jobs,stats=stats)#rendr template with the 5jobs and stats
    

#login  
@app.route("/login",methods=["GET","POST"])
def login():
    
    if request.method == "POST":#if method is post
        email = request.form["email"]
        enter_pass =request.form["password"]
        
        user = us_db.verify_user(email)#get email and pass key from db
        
        if user and check_password_hash(user[3], enter_pass):#using the check_hash it hases and check
        #geting the required
            session["user_id"] = user[0]
            session["name"] = user[1]
            session["role"] = user[4]
            
            flash(f"welcome back,{user[1]}","success")
            return redirect(url_for("dashboard"))
#if hahesh doest match redirect to login   
        else:
            flash(f"invalid email or password","danger")
            return redirect(url_for("login"))
    return render_template("login.html")

#register
@app.route("/register",methods=["GET","POST"])
def register():
    if request.method == "POST":#if method is post
        name = request.form["name"]
        email = request.form["email"]
        raw_password = request.form["password"]
        role = request.form["role"]
        
        secure_password_hash = generate_password_hash(raw_password)#generate hashed pass
        
        if us_db.add_user(name,email,secure_password_hash,role):#insert it into table
            flash("Registration successful ! please log in.","success")
            return redirect(url_for("login"))
        else:#if user already exsited
            flash("this email is alrady exist","danger")
            return redirect(url_for("register"))
        
    return render_template("register.html")#if it is get

#all job
@app.route("/jobs")
def jobs_catalog():
    # Get search filter parameters
    search_query = request.args.get('search', '').strip()
    location_query = request.args.get('location', '').strip()
    experience_query = request.args.get('experience', '').strip()
    salary_query = request.args.get('salary', '').strip()
    
    # Page calculation
    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        page = 1

    PER_PAGE = 3  # 3 jobs per page

    # Fetch filtered jobs list from database
    all_filtered_jobs = job_db.filter_jobs(
        query=search_query,
        location=location_query,
        experience=experience_query,
        max_salary=salary_query
    )

    total_jobs = len(all_filtered_jobs)
    total_pages = (total_jobs + PER_PAGE - 1) // PER_PAGE if total_jobs > 0 else 1

    if page < 1:
        page = 1
    elif page > total_pages:
        page = total_pages

    # Slice jobs array
    start_idx = (page - 1) * PER_PAGE
    end_idx = start_idx + PER_PAGE
    paginated_jobs = all_filtered_jobs[start_idx:end_idx]

    # Build a clean dictionary containing ONLY non-empty active filters
    active_filters = {}
    if search_query:
        active_filters['search'] = search_query
    if location_query:
        active_filters['location'] = location_query
    if experience_query:
        active_filters['experience'] = experience_query
    if salary_query:
        active_filters['salary'] = salary_query

    return render_template('jobs.html',jobs=paginated_jobs,query=search_query,location=location_query,
        experience=experience_query,salary=salary_query,page=page,total_pages=total_pages,total_jobs=total_jobs,
        active_filters=active_filters)  # Pass clean active filters

#edit job
@app.route("/job/<int:job_id>", methods=["GET", "POST"])
def job_details(job_id):
    #getting the job 
    job = job_db.job_by_jobid(job_id)

    #if the job is not present
    if not job:
        flash("The requested job listing could not be found.", "danger")
        return redirect(url_for("jobs_catalog")) 

    # get the user candiadte resume to apply job default profile resume
    current_user_data = None
    if "user_id" in session:
        current_user_data = us_db.user_by_id(session["user_id"])

    if request.method == "POST":
        if "user_id" not in session:
            flash("Please sign in as a Candidate to submit an application.", "warning")
            return redirect(url_for("login"))
            
        if session.get("role") != "Candidate":
            flash("Employer profile access tokens are blocked from submitting applications.", "danger")
            return redirect(url_for("jobs_catalog")) 
       
        if app_db.check_existing_application(session["user_id"], job_id):
            flash("You have already submitted an application for this position.", "warning")
            return redirect(url_for("dashboard"))
       
        strategy = request.form.get("resume_strategy", "new")
        filename = None

        #using the profile resume
        #cheking whether the current user is in for of dict or tuple using hasattr
        if strategy == "profile" and current_user_data:
            filename = current_user_data['resume_file'] if hasattr(current_user_data, 'keys') else current_user_data[5]
           
        #if new file is inserted
        file = request.files.get("resume")
        if file and file.filename != "":
            filename = f"user_{session['user_id']}_{file.filename}"#merging the user id and file name
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))#saving the file in the folder
           
        #insert into apply table 
        if filename:
            success = app_db.apply_job(session["user_id"], job_id, filename)
            if success:
                flash("Your application and resume pack have been successfully submitted!", "success")
                return redirect(url_for("dashboard"))
            else:
                flash("An unexpected database connection error occurred.", "danger")
        else:
            flash("Please upload a resume file or save a default resume in your profile view layout.", "danger")

    applied_job_ids = []#getting the already appleid jobs
    if "user_id" in session and session.get("role") == "Candidate":#cheching whether the user is in session and he is candidate
        applied_job_ids = app_db.get_applied_job_ids_by_candidate(session["user_id"])

    return render_template("job_details.html", job=job, applied_job_ids=applied_job_ids, current_user=current_user_data)#render template

#dashboard
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:#checking there log in or not
        flash("Please log in to access your dashboard hub.", "danger")
        return redirect('/login')

    user_id = session['user_id']
    role = session.get('role')

    #employee updating the status and posting job
    if request.method == 'POST':
        action_type = request.form.get('action_type')

        #if checking the role and if  want to job post
        if action_type == 'create_job' and role == 'Employer':
            company_name = request.form.get('company_name')
            job_title = request.form.get('job_title')
            location = request.form.get('location')
            experience = request.form.get('experience')
            salary = request.form.get('salary')
            skills = request.form.get('skills')
            description = request.form.get('description')

            #add job
            if job_db.add_job(user_id, company_name, job_title, location, experience, salary, skills, description):
                flash("Corporate position row deployed successfully!", "success")
            else:
                flash("Failed to deploy vacancy row. Please try again.", "danger")
            return redirect('/dashboard')

        #if employee update candidate status
        elif action_type == 'update_status' and role == 'Employer':
            application_id = request.form.get('application_id')
            new_status = request.form.get('status')

            #override the status using update statement
            try:
                cursor, con = db.connection()
                con.execute("PRAGMA ignore_check_constraints = ON;")#creted table without the interview sheduled so turning off the check constarin
                cursor = con.cursor()
                cursor.execute("UPDATE applications SET status = ? WHERE application_id = ?", (new_status, application_id))
                con.commit()
                con.close()#updating the stauts 
                flash("Candidate application tracking status updated.", "success")
            except Exception as e:
                flash(f"An unexpected database error occurred: {e}", "danger")
                
            return redirect('/dashboard')


    if role == 'Employer':#dash board for emplyee
        jobs = job_db.job_by_employee(user_id)  # selected posted job
        applicants = app_db.get_applications_for_employer(user_id)#get the applicants
        cur,con =db.connection()
        result=cur.execute("SELECT company FROM users WHERE user_id =? ",(user_id,)).fetchone()#getiing company name
        company_name= result[0] if result else ""
        return render_template('dashboard.html', jobs=jobs, applicants=applicants,company_name=company_name)

    else:#candidate dash board
        #getting all the applied job
        applications = app_db.get_applications_by_candidate(user_id)

        #seting stats to display
        apps_submitted = len(applications)

        #chching te staus and and all the to give count
        apps_accepted = sum(1 for app in applications if app[2] in ['Accepted', 'Interview Scheduled'])
        apps_pending = sum(1 for app in applications if app[2] == 'Pending')
        
        stats = {
            'apps_submitted': apps_submitted,
            'apps_accepted': apps_accepted,
            'apps_pending': apps_pending
        }
        #saved job
        saved_jobs =us_db.get_save_job(user_id)

        #render template
        return render_template('dashboard.html', applications=applications, stats=stats,saved_jobs=saved_jobs)
    

#profile
@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "user_id" not in session:#check in session or not
        flash("Please log in to manage your profile configurations.", "warning")
        return redirect(url_for("login"))
        
    user_id = session["user_id"]
    
    if request.method == "POST":#getiing all the value 
        name = request.form.get("name")
        email = request.form.get("email")
        company = request.form.get("company")
        skills = request.form.get("skills", "")
        experience = request.form.get("experience", "")
        
        resume_file = request.files.get("resume")
        avatar_file = request.files.get("profile_pic")
        
        saved_resume_name = None
        saved_avatar_name = None

        #if avatar and resume updated
        if resume_file and resume_file.filename != "":
            saved_resume_name = f"resume_{user_id}_{resume_file.filename}"
            resume_file.save(os.path.join(app.config["UPLOAD_FOLDER"], saved_resume_name))

        if avatar_file and avatar_file.filename != "":
            saved_avatar_name = f"avatar_{user_id}_{avatar_file.filename}"
            avatar_file.save(os.path.join(app.config["UPLOAD_FOLDER"], saved_avatar_name))
            
        #update the profile 
        success = us_db.update_profile(
            user_id, name, email, skills, experience, saved_resume_name, saved_avatar_name,company)
        
        if success:#checking whaether the user profile updated or not
            session["name"] = name 
            flash("Profile updates saved successfully!", "success")
        else:
            flash("Failed to update profile details. Email might already be taken.", "danger")#if email already existed show error
            
        return redirect(url_for("profile"))

    current_user = us_db.user_by_id(user_id)#get the current user details to display
    return render_template("profile.html", user=current_user)

#job edit
@app.route("/job/edit/<int:job_id>", methods=["GET", "POST"])
def edit_job(job_id):
    #cheking the user in session or not
    if "user_id" not in session or session.get("role") != "Employer":
        flash("Unauthorized access blocked.", "danger")
        return redirect(url_for("login"))
        
    employer_id = session["user_id"]

    #if method is post get all the details to chnage
    if request.method == "POST":
        company_name = request.form["company_name"]
        job_title = request.form["job_title"]
        location = request.form["location"]
        experience = request.form["experience"]
        salary = request.form["salary"]
        skills = request.form["skills"]
        description = request.form["description"]
        
        #updating with new value
        success = job_db.update_job(
            job_id, employer_id, company_name, job_title,
            location, experience, salary, skills, description
        )
        
        if success:
            flash("Job modifications updated successfully!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Failed to update job vacancy parameters.", "danger")
            return redirect(url_for("dashboard"))

    #if job is not available
    job = job_db.job_by_jobid(job_id)
    if not job:
        flash("The requested job listing could not be found.", "danger")
        return redirect(url_for("dashboard"))
        
    #checking wheather the this employee post this job
    if job['employer_id'] != employer_id:
        flash("You do not have permission to modify this entry.", "danger")
        return redirect(url_for("dashboard"))

    return render_template("edit_job.html", job=job)

#delete job
@app.route("/job/delete/<int:job_id>", methods=["POST"])
def delete_job(job_id):
    if "user_id" not in session or session.get("role") != "Employer":
        flash("Unauthorized operational command blocked.", "danger")
        return redirect(url_for("login"))
        
    employer_id = session["user_id"]
    
    #deleting the job
    if job_db.delete_job(job_id, employer_id):
        flash("Job listing dropped permanently from routing systems.", "success")
    else:
        flash("Failed to remove the requested job entry.", "danger")
        
    return redirect(url_for("dashboard"))

# Save Job Route
@app.route("/save/<int:job_id>")
def save(job_id):
    if "user_id" not in session:
        flash("Please log in to save job openings.", "warning")
        return redirect(url_for("login"))
        
    if session.get("role") != "Candidate":
        flash("Employer accounts cannot save job listings.", "danger")
        return redirect(url_for("dashboard"))
        
    user_id = session["user_id"]
    
    save_result = us_db.save_job(user_id, job_id)

    if save_result:
        flash("Job saved to your watchlist!", "success")
    else:
        flash("Unable to save job listing.", "danger")
        
    return redirect(request.referrer or url_for("dashboard"))

# Unsave / Delete Saved Job Route
@app.route("/unsave/<int:job_id>")
def unsave(job_id):
    if "user_id" not in session or session.get("role") != "Candidate":
        flash("Unauthorized action.", "danger")
        return redirect(url_for("login"))
        
    user_id = session["user_id"]
    if us_db.unsave_job(user_id, job_id):
        flash("Job removed from saved watchlist.", "info")
    return redirect(url_for("dashboard"))

#logout
@app.route("/logout")
def logout():
    # Clear the session and log out
    session.clear()
    flash("You have been logged out successfully.", "success")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run()
    
        
    
                