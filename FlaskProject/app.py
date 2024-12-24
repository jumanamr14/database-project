from flask import Flask, render_template, request, session, redirect
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)


# Database connection session
database_connection_session = psycopg2.connect(
    database="postgres",
    user="postgres",
    password="eng5534891",
    host="localhost",
    port="5432"
)
app.secret_key = 'your_secret_key'

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
    userdata = session.get('user')  # Get user data from session if it exists
    return render_template('docprofile.html', userdata=userdata)
    # message=None
    #
    # userdata = session.get('user')
    # ddata=session.get('d')
    # print("user:", userdata)
    # print("d:", ddata)
    # return render_template('docprofile.html', userdata=userdata, ddata=ddata)

@app.route('/patprofile', methods=['GET', 'POST'])
def patprofile():
    userdata = session.get('user')  # Get user data from session if it exists
    return render_template('patprofile.html', userdata=userdata)
@app.route('/homedoc', methods=['GET', 'POST'])
def homedoc():
    userdata = session.get('user')  # Get user data from session if it exists
    return render_template('homedoc.html', userdata=userdata)

@app.route('/loginpat', methods=['GET', 'POST'])
def loginpat():
    message = None
    if request.method == 'GET':
        return render_template('loginpat.html')

    elif request.method == 'POST':
        p_id = request.form.get('ID')
        email = request.form.get('email')
        password = request.form.get('password')

        cur = database_connection_session.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute('SELECT * FROM patient WHERE  p_id = %s ', (p_id, ))
        userdata = cur.fetchone()

        if userdata is None:
            message = 'Email or password incorrect'
            return render_template('loginpat.html', message=message)
        else:
            message = 'logged in successfully'
            session['user'] = userdata


        return render_template('loginpat.html', message=message)

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


        cur.execute('SELECT * FROM users WHERE email = %s', (email,))
        if cur.fetchone():
            message = 'User already registered'
        else:
            cur.execute('INSERT INTO patient(p_id, fname, mname, lname, age, gender, phone, address, condition)  VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                        (p_id,fname,mname,lname,age,gender,condition,phone,address))

            database_connection_session.commit()
            message = 'Registration successful! You can now log in.'
            cur.close()
            session['email']=email
            # return redirect('/patprofile')

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
            # return redirect('/patprofile')

    return render_template('docprofile.html', msg=message)


@app.route('/logout')
def logout():
    # Safely remove user from session
    session.pop('user', None)
    return redirect('/login')

if __name__ == "__main__":
    app.run(debug=True)