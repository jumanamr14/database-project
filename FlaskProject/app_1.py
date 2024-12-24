from flask import Flask, render_template, request, session, redirect
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database connection session
database_connection_session = psycopg2.connect(
    database="postgres",
    user="postgres",
    password="eng5534891",
    host="localhost",
    port="5432"
)


# @app.route('/dochome', methods=['GET', 'POST'])
# def homedoc():
#     userdata = session.get('user')  # Get user data from session if it exists
#     return render_template('homedoc.html', userdata=userdata)


@app.route('/', methods=['GET', 'POST'])
def home():
    userdata=session.get('user')
    pdata=session.get('p')

    return render_template('index.html', userdata=userdata,pdata=pdata)


@app.route('/homepat', methods=['GET', 'POST'])
def homepat():
    userdata = session.get('user')  # Get user data from session if it exists
    return render_template('homepat.html', userdata=userdata)

@app.route('/docprofile', methods=['GET', 'POST'])
def docprofile():
    userdata = session.get('user')
    ddata = session.get('d')
    print("user:", userdata)
    print("d:", ddata)
    # Get user data from session if it exists
    return render_template('docprofile.html', userdata=userdata, ddata=ddata)



@app.route('/loginpat', methods=['GET', 'POST'])
def loginpat():
    message = None

    # Handle GET request: render the login page
    if request.method == 'GET':
        return render_template('loginpat.html')

    # Handle POST request: process login form submission
    elif request.method == 'POST':

        u_id = request.form.get('u_id')
        p_id = request.form.get('p_id')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        password = request.form.get('password')

        # Create a database cursor
        cur = database_connection_session.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Query to check user exists in both 'users' and 'patient' tables
        cur.execute('SELECT * FROM patient WHERE p_id = %s AND fname = %s', (p_id, firstname))
        userdata = cur.fetchone()
        pdata =cur.fetchone()
        ddata = cur.fetchone()
        if userdata is None:
            message='User not found'
            print("No user found with the given p_id and firstname.")
        else:

            print("User found:", userdata)
            # message='login successful'
            session['userdata'] = userdata
            session['doc'] = ddata
            session['patient'] = pdata

            # print(f"Query result: {userdata}")
        return render_template('patprofile.html',userdata=userdata, ddata=ddata,pdata=pdata,message=message)
    else:
         message = 'User not found'
         return render_template('loginpat.html', message=message)


@app.route('/patprofile', methods=['GET', 'POST'])
def patprofile():
    userdata = session.get('userdata')
    ddata = session.get('doc')
    pdata = session.get('patient')

    print("userdata:", userdata)
    print("ddata:", ddata)
    print("pdata:", pdata)

    return render_template('patprofile.html', userdata=userdata, ddata=ddata, pdata=pdata)

@app.route('/logindoc', methods=['GET', 'POST'])
def logindoc():
    message = None
    if request.method == 'GET':
        return render_template('logindoc.html')

    elif request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        cur = database_connection_session.cursor()
        cur.execute('SELECT * FROM doctor WHERE dr_id=%s'),(password,)
        userdata = cur.fetchone()
        cur.close()

        if userdata is None:
            message = 'Email or password incorrect'
            return render_template('logindoc.html', message=message)
        else:
            # Optional: Convert userdata tuple to a dictionary if needed
            session['user'] = {'id': userdata[0], 'email': userdata[1]}  # Example fields
            return redirect('/')

@app.route('/registerpat', methods=['GET', 'POST'])
def registerpat():
    message = None
    if request.method == 'GET':
        return render_template('registerpat.html')

    if request.method == 'POST':
        p_id=request.form.get('id')
        fname = request.form.get('firstname')
        mname=request.form.get('middlename')
        lname = request.form.get('lastname')
        age = request.form.get('age')
        gender=request.form.get('gender')
        phone=request.form.get('phone')
        address=request.form.get('address')
        condition=request.form.get('condition')
        email = request.form.get('email')
        password = request.form.get('password')
        confirmpassword = request.form.get('confirmpassword')


        if password == confirmpassword:
            cur = database_connection_session.cursor()
        else:
            message = 'Passwords do not match'
            return render_template('registerpat.html', msg=message)

        # Check if the email is already registered
        cur.execute('SELECT * FROM users WHERE email = %s', (email,))
        if cur.fetchone():
            message = 'User already registered'
        else:
            # Insert the user first
            cur.execute(
                'INSERT INTO users(u_id, firstname, lastname, email, password) VALUES (%s,%s,%s,%s,%s)',
                (p_id, fname, lname, email, password)
            )

            # After inserting, you can now use the same p_id as u_id for the patient
            cur.execute(
                'INSERT INTO patient(p_id, fname, mname, lname, age, gender, phone, address, condition, u_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s, %s)',
                (p_id, fname, mname, lname, age, gender, phone, address, condition, p_id)  # Use p_id as u_id
            )

            # Commit the transaction
            database_connection_session.commit()

            message = 'Registration successful! You can now log in.'
            cur.close()
            session['email'] = email

    return render_template('registerpat.html', msg=message)

@app.route('/registerdoc', methods=['GET', 'POST'])
def registerdoc():
    message = None
    if request.method == 'GET':
        return render_template('registerdoc.html')

    if request.method == 'POST':
        dr_id = request.form.get('ID')
        pat_id = request.form.get('p_id')
        fname = request.form.get('firstname')
        lname = request.form.get('lastname')
        gender = request.form.get('gender')
        phone = request.form.get('phone')
        speciality = request.form.get('speciality')
        address = request.form.get('address')
        cond=request.form.get('condition')

        email = request.form.get('email')
        password = request.form.get('password')
        confirmpassword = request.form.get('confirmpassword')

        if password != confirmpassword:
            message = 'Passwords do not match'
            return render_template('registerdoc.html', msg=message)


        cur = database_connection_session.cursor()


        cur.execute('SELECT * FROM users WHERE email = %s', (email,))
        if cur.fetchone():
            cur.close()
            message = 'User already registered'
            render_template('registerdoc.html', msg=message)
        else:
            cur.execute(
                'INSERT INTO doctor(dr_id, pat_id, fname, lname, gender, dr_phone, speciality, address, cond)   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                (dr_id,pat_id, fname, lname, gender,phone,speciality,address ,cond))

            database_connection_session.commit()
            message = 'Registration successful! You can now log in.'
            cur.close()
            session['email'] = email


    return render_template('docprofile.html', msg=message)


@app.route('/logout')
def logout():
    # Safely remove user from session
    session.pop('user', None)
    return redirect('/login')

if __name__ == "__main__":
    app.run(debug=True)