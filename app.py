from flask import Flask,render_template,request,redirect,url_for,flash,jsonify,session
from flask import abort
from flask_mysqldb import MySQL
import json, random
from forms import LoginForm,RegisterForm
import yaml
import numpy as np
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hello'

db = yaml.load(open('db.yaml'))

app.config['MYSQL_HOST']=  db['mysql_host']
app.config['MYSQL_USER']= db['mysql_user']
app.config['MYSQL_PASSWORD']= db['mysql_password']
app.config['MYSQL_DB']= db['mysql_db']
mysql=MySQL(app)

quantity= [35,45.4,45.65,36.04,23.76,20.12]

tones = []
track_of_crops = []
arr = ['Sugarcane','Rice','Maize']
arr1 = ['wheat','Barley','pulses']
dict1 = {'Sugarcane':1,'Rice':2,'Maize':3,'wheat':1,'Barley':2,'pulses':3}

crops = []


ls = []


value = dict1.keys()
q = []

for i in value:
    q.append(i)
def calculate(val,name):
    w2 = name
    q = int(val)
    # print(q)
    if name in arr:
        if w2==arr[0]:
            q=q*60
                
                

        elif w2==arr[1]:
            q=q*3
               

        else :

            q=q*3
                
        
    else:
            if w2==arr1[0]:

                q=q*40


            elif w2==arr1[1]:

                q=q*6
                    

            else:
                q=q*3
        
    return q     


def qua_change(n, acre):
    acre = int(acre)
    if n in arr:
        if n == arr[0]:

            q = acre * 60 * 100 / 6000
            quantity[dict1[n] - 1] = q + quantity[dict1[n] - 1]
        elif n == arr[1]:

            q = acre * 3 * 100 / 10000
            quantity[dict1[n] - 1] = q + quantity[dict1[n] - 1]
        elif n == arr[2]:
            q = acre * 3 * 100 / 2000
            # print(2)
            quantity[dict1[n]-1]=q+quantity[dict1[n]-1]

    else:
        if n == arr1[0]:
            q = acre * 40 * 100 / 3000
            quantity[dict1[n] + 2] = q + quantity[dict1[n] + 2]
        elif n == arr1[1]:
            q = acre * 6 * 100 / 2500
            quantity[dict1[n] + 2] = q + quantity[dict1[n] + 2]
        elif n==arr1[2]:
            q = acre * 3 * 100 / 1500
            quantity[dict1[n]+2]=q+quantity[dict1[n]+2]
            # print('----------------',quantity,'--------------')

def prev_calc(name,n):
    n = int(n)
    if name in arr:
        if name==arr[0]:
            n=n/6000*100
            quantity[dict1[name]-1] = quantity[dict1[name]-1]-n
                    
        elif name ==arr[1]:
            n=n/10000*100
            quantity[dict1[name]-1] = quantity[dict1[name]-1]-n
            
        else:
            n=n/2000*100
            quantity[dict1[name]-1] = quantity[dict1[name]-1]-n
    else:
        if name==arr1[0]:
            n=n/3000*100
            quantity[dict1[name]+2] = quantity[dict1[name]+2]-n
                    
        elif name==arr1[1]:
            n=n/2500*100
            quantity[dict1[name]+2] = quantity[dict1[name]+2]-n
                    
        else:
            n=n/1500*100
            quantity[dict1[name]+2] = quantity[dict1[name]+2]-n

from functools import wraps
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_admin' in session:
            return f(*args, *kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

def is_logged_out(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_admin' not in session:
            return f(*args, *kwargs)
            return redirect(url_for('login'))
        else:
            flash('You are Already logged in !', 'success')
            return redirect(url_for('admin_graph'))
           
    return wrap









pre_arr = []




@app.route('/home',methods=['POST','GET'])
def home():
    
    
    return render_template('home.html',quantity ={'results':quantity})
    


@app.route('/admin_graph')
@is_logged_in
def admin_graph():
    
    return render_template('admin_graph.html',quantity ={'results':quantity})




@app.route('/register',methods=['POST','GET'])
@is_logged_in
def register():
    form = RegisterForm()
    cur = mysql.connection.cursor()
    if request.method == 'POST' and form.validate_on_submit():
        
        print(form.username.data)
        print(form.soil.data) 
        print(form.phoneno.data)
        print(form.number.data)
        cur.execute("insert into register(username,rtc,phone,soil) values(%s,%s,%s,%s)",(form.username.data,form.number.data,form.phoneno.data,form.soil.data))
        cur.connection.commit()
        
        return redirect(url_for('loginuser'))
        
    else:
        flash('Please enter details','danger')
    cur.close()
    return render_template('register.html',form=form)


@app.route('/previous',defaults = {'crops':False},methods=['POST','GET'])
@app.route('/previous/<string:crops>' ,methods=['POST','GET'])
def previous(crops):
    cur = mysql.connection.cursor()
    res = 0
    crops = False
    res = cur.execute("select crop from crops where rtc = %s",[session['rtc']])
    
    
    if res>0:
        crops = cur.fetchall()
        crops = np.unique(crops)
        ls = crops
        
    else:
        flash('Sorry no previous crops ','warning')       
    
    print("ls-",ls)    
    print("Enetred")
    print(crops)
    
    # ls = ['vvv','nnn','bbb']
    # print('--------------',request.form["quantity")
    if request.method == 'POST':
        for crop in crops:
            if request.form.get(crop):
                prev_calc(crop,request.form[crop])
            else:
                flash(f'Please enter the amount of quantity of {crop} ','info')
                return redirect(url_for('previous'))
        # qua_change(pre_arr[0],pre_arr[1])
        # print('--------------',request.form["quantity"])
        # print('------------',request.form['gridRadios'],'-----------------------')
        # pre_arr.insert(0,crops)
        # pre_arr.insert(1,request.form['quantity'])
        # print('----------previous',pre_arr)
        
        cur.execute("delete from crops where rtc = %s",[session['rtc']])
        cur.connection.commit()
        cur.close()
        return redirect(url_for('add_details',crops=False))
    return render_template('previous.html',crops= crops)

@app.route('/add_details',defaults = {'crops':False},methods=['POST','GET'])
@app.route('/add_details/<string:crops>',methods=['POST','GET'])
@is_logged_in
def add_details(crops):
    
    cur = mysql.connection.cursor()
    # print(crops)
    
    if request.method == 'POST':
        
        try:
            
            if request.method=='POST' and request.form['gridRadios3'] and request.form['amount']:
                
                # print(request.form['gridRadios1'])
                # ls = 0
                # v = str(request.form['gridRadios1'])
                
                # print(ls)
                # print(request.form['gridRadios1'])
                # if v in ls:
                #     v=ls.pop()
                #     flash(f' ----**----Caution you are using same crops {v} ----**----!! ','danger')
                    
                    
                # ls.append(request.form['gridRadios1'])
                # print(ls)
                
                
                qua_change(request.form['gridRadios1'], request.form['amount'])
                # print('excurted')
                track_of_crops.append(request.form['gridRadios1'])
                # print('redirect ')
                return redirect(url_for('graph'))
            else:
                flash('Please enter the amount','danger')
        except:
            if request.form.get('amount'):
                print(request.form['amount'])
                flash('Click on radio button to confirm !!','success')
            else:
                flash('Please enter the amount','danger')            
                
        # print('-----------------',request.form['gridRadios1'],'------------')
        
            # return render_template('add_details.html' ,val = val,crop = request.form['gridRadios1'],arr = arr)
    res = cur.execute("select crop from crops where rtc = %s",[session['rtc']])
    cur.close()
    if session['soil'] == 'Red':
        return render_template('add_details.html' ,arr=arr,crops=res)
    else:
        return render_template('add_details.html' ,arr=arr1,crops = res)
    
        

@app.route('/loginuser',methods=['POST','GET'])
@is_logged_in
def loginuser():
    cur = mysql.connection.cursor()
    global n
    if request.method == 'POST':
        res = cur.execute('select soil,rtc,username from register where rtc = %s',[request.form['name']])
        if res>0:
            soil=cur.fetchone()
            print(soil[0])
            session['soil'] = soil[0]
            session['rtc'] = soil[1]
            session['username'] = soil[2]

            nn = cur.execute("select  crop from crops where rtc = %s ",[session['rtc']])
            if nn>0:
                new_arr = cur.fetchall()
                n = new_arr[len(new_arr)-1][0]
            else:
                n = 0
            cur.close()
            flash('Logged in successfully','success')
            return redirect(url_for('add_details',crops=False))
        else:
            flash('Invalid rtc number please enter a valid one','danger')
            return render_template('loginuser.html')

    
    return render_template('loginuser.html')



@app.route('/display')
def display():
    return jsonify({'results' : quantity,'pre' : n})
 


@app.route('/login',methods=['POST','GET'])
@is_logged_out
def login():
    form = LoginForm()
    
    if request.method == 'POST' :
        print()
        # userdetails = request.form
        email = request.form.get('email')
        password = request.form.get('pass')
        if email == 'ark2000@gmail.com' and password == 'ark':
            flash('Login successfull','success')
            session['logged_admin'] = True
            return redirect(url_for('admin_graph'))
        else:
            flash('Please enter valid email address and password','danger')
            return render_template('login.html',form=form)
    return render_template('login.html',form=form)

    


@app.route('/logoutuser')
@is_logged_in
def logoutuser():
    cur = mysql.connection.cursor()
    c = 0
    if 'soil' in session:
        for _ in range(len(track_of_crops)):
            v = track_of_crops.pop(c)
            cur.execute("insert into crops(crop,rtc) values(%s,%s) ",(v,session['rtc']))
            cur.connection.commit()
        cur.close()
        session.pop('soil',None)
        session.pop('username',None)
        session.pop('rtc',None)
        flash('Logged out successfully','success')
        return redirect(url_for('loginuser'))
    else:
        return redirect(url_for('loginuser'))


@app.route('/logout')
@is_logged_in
def logout():
    if 'logged_admin' in session:
        # Create cursor
        session.pop('soil',None)
        session.pop('logged_admin',None)
        session.clear()
        flash('You are logged out', 'success')
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

@app.route('/graph')
@is_logged_in
def graph():
    crops = list(zip(quantity,q))
    
    return render_template('graph.html',quantity = quantity,crops= crops)

if __name__ == '__main__':
    app.run(debug=True)

