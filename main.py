from flask_mail import Mail,Message
from random import random,randrange
from flask import Flask,redirect,request,render_template,session,url_for
import os,time
from werkzeug.utils import secure_filename
from mylib import check_photo
import pymysql
app=Flask(__name__)
app.secret_key='super secret key'
app.config['UPLOAD_FLODER']='./static/photos'
mail=Mail(app)
app.secret_key='super user key'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'shulabhdixit143@gmail.com'
app.config['MAIL_PASSWORD'] = 'ankita968026'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route('/login')
def home():
    return render_template('login.html')
@app.route('/forget')
def forget():
    return render_template('forgetpass.html')
@app.route('/logout')
def logout():
    if 'usertype' in session:
        session.pop('usertype',None)
        session.pop('usertype',None)
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))
@app.route('/autherror')
def autherror():
    return render_template('autherror.html')
@app.route('/adminhome')
def adminhome():
    if 'usertype' in session:
        ut=session['usertype']
        if ut=='admin':
            return render_template('admintemplete.html')
    else:
        return redirect(url_for('autherror'))
@app.route('/hospitalhome')
def hospitaladmin():
    if 'usertype' in session:
        ut=session['usertype']
        if ut=='hospital':
            return render_template('hospitaltemplete1.html')
    else:
        return redirect(url_for('autherror'))
@app.route('/changepass')
def changepass():
    return render_template('changepassword.html')
@app.route('/changepassword',methods=['GET','POST'])
def changepassword():
    if 'usertype' in session:
        utype=session['usertype']
        e1=session['email']
        if utype=='admin':
            if request.method=='POST':
                oldpass=request.form['oldpassword']
                newpass=request.form['newpassword']
                if oldpass==newpass:
                    conn = pymysql.connect(
                        host='localhost',
                        port=3306,
                        user='root',
                        passwd='',
                        db='test',
                        autocommit=True
                    )
                    cur = conn.cursor()
                    sql="update logindata set password='"+newpass+"'where  email='"+e1+"'"
                    cur.execute(sql)
                    n=cur.rowcount
                    if n==1:
                        return render_template('changesave.html',msg='password is successfully change')
                else:
                    return render_template('changesave.html',msg='password is not changed')
            else:
                return redirect(url_for('changepass'))
        elif utype=='hospital':
            if request.method=='POST':
                oldpass=request.form['oldpassword']
                newpass=request.form['newpassword']
                if oldpass==newpass:
                    conn = pymysql.connect(
                        host='localhost',
                        port=3306,
                        user='root',
                        passwd='',
                        db='test',
                        autocommit=True
                    )
                    cur = conn.cursor()
                    sql="update logindata set password='"+newpass+"' where password='"+oldpass+"' and email='"+e1+"'"
                    cur.execute(sql)
                    n=cur.rowcount
                    if n==1:
                        return render_template('changesave.html',msg='password is saved')
                else:
                    return render_template('changesave.html',msg='password is not saved')
            else:
                return redirect(url_for('changepass'))
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))
@app.route('/profile')
def adminprofile():
    if 'usertype' in session:
        utype=session['usertype']
        e1=session['email']
        if utype=='admin':
            conn = pymysql.connect(
                host='localhost',
                port=3306,
                user='root',
                passwd='',
                db='test',
                autocommit=True
            )
            cur = conn.cursor()
            sql="select *from admindata where email='"+e1+"'"
            cur.execute(sql)
            n=cur.rowcount
            if n==1:
                data=cur.fetchone()
                photo=check_photo(e1)
                return render_template('adminprofile.html',data=data,photo=photo)
            else:
                return render_template('adminprofile.html',msg='data not find')
        elif utype=='hospital':
            conn = pymysql.connect(
                host='localhost',
                port=3306,
                user='root',
                passwd='',
                db='test',
                autocommit=True
            )
            cur = conn.cursor()
            sql="select *from hospital_data where email='"+e1+"'"
            cur.execute(sql)
            n=cur.rowcount
            if n==1:
                data=cur.fetchone()
                return render_template('hospitalprofile.html',data=data)
            else:
                return render_template('hospitalprofile.html',msg='data is not found')
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        conn = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='',
            db='test',
            autocommit=True
        )
        cur = conn.cursor()
        sql="select *from logindata where email='"+email+"' and password='"+password+"'"
        cur.execute(sql)
        n=cur.rowcount
        if n==1:
            data=cur.fetchone()
            utype=data[2]
            session['usertype']=utype
            session['email']=email
            if utype=='admin':
                return redirect(url_for('adminhome'))
            elif utype=='hospital':
                return render_template('hospitaltemplete1.html')
        else:
            return render_template('login.html',msg='email or password incorrect')
    else:
        return redirect(url_for('login'))
@app.route('/adminreg',methods=['GET','POST'])
def adminreg():
    if 'usertype' in session:
        utype=session['usertype']
        if utype=='admin':
            if request.method=='POST':
                name=request.form['name']
                ad=request.form['address']
                con=request.form['contact']
                email=request.form['email']
                password=request.form['password']
                usertype='admin'
                conn = pymysql.connect(
                    host='localhost',
                    port=3306,
                    user='root',
                    passwd='',
                    db='test',
                    autocommit=True
                )
                cur = conn.cursor()
                sql1="insert into admindata values('"+name+"','"+ad+"','"+con+"','"+email+"')"
                sql2="insert into logindata values('"+email+"','"+password+"','"+usertype+"')"
                cur.execute(sql1)
                cur.execute(sql2)
                n=cur.rowcount
                if n==1:
                    return render_template('changesave.html',msg='data is saved')
                else:
                    return render_template('changesave.html',msg='data is not saved')
            else:
                return render_template('adminreg.html')
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))
@app.route('/showadmins')
def showadmis():
    if 'usertype' in session:
        ut=session['usertype']
        if ut=='admin':
            conn = pymysql.connect(
                host='localhost',
                port=3306,
                user='root',
                passwd='',
                db='test',
                autocommit=True
            )
            cur = conn.cursor()
            sql="select *from admindata"
            cur.execute(sql)
            n=cur.rowcount
            if n>0:
                data=cur.fetchall()
                return render_template('showadmins.html',data=data)
        else:
            return redirect(url_for('autherror'))
@app.route('/hospitalreg',methods=['GET','POST'])
def hospitalreg():
    if 'usertype' in session:
        utype=session['usertype']
        if utype=='admin':
            if request.method=='POST':
                name=request.form['name']
                sp=request.form['specility']
                ad=request.form['address']
                con=request.form['contact']
                acb=request.form['acbeds']
                nacb=request.form['nonacbeds']
                email=request.form['email']
                password=request.form['password']
                usertype='hospital'
                conn = pymysql.connect(
                    host='localhost',
                    port=3306,
                    user='root',
                    passwd='',
                    db='test',
                    autocommit=True
                )
                cur = conn.cursor()
                sql1="insert into hospital_data values('"+name+"','"+sp+"','"+ad+"','"+con+"','"+acb+"','"+nacb+"','"+email+"')"
                sql2="insert into logindata values('"+email+"','"+password+"','"+usertype+"')"
                cur.execute(sql1)
                cur.execute(sql2)
                n=cur.rowcount
                if n==1:
                    return render_template('changesave.html',msg='data is saved')
                else:
                    return render_template('changesave.html',msg='data is not saved')
            else:
                return render_template('hospitalreg.html')
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))
@app.route('/showhospitals')
def showhospitals():
    if 'usertype' in session:
        ut=session['usertype']
        if ut=='admin':
            conn = pymysql.connect(
                host='localhost',
                port=3306,
                user='root',
                passwd='',
                db='test',
                autocommit=True
            )
            cur = conn.cursor()
            sql="select *from hospital_data"
            cur.execute(sql)
            n=cur.rowcount
            if n>0:
                data=cur.fetchall()
                return render_template('showhospital.html',data=data)
            else:
                return render_template('showhospital.html',msg='no hospital found')
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))
@app.route('/deletehospital',methods=['GET','POST'])
def deletehospital():
    if 'usertype' in session:
        ut=session['usertype']
        if ut=='admin':
            if request.method=='POST':
                email=request.form['email']
                conn = pymysql.connect(
                    host='localhost',
                    port=3306,
                    user='root',
                    passwd='',
                    db='test',
                    autocommit=True
                )
                cur = conn.cursor()
                sql="delete from hospital_data where email='"+email+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    return render_template('deletehospital.html',msg='rocord is delete')
                else:
                    return render_template('deletehospital.html',msg='record is not delete')
            else:
                return redirect(url_for('deletehos'))
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))
@app.route('/deletehos')
def deletehos():
    return render_template('deletehospital.html')
@app.route('/edithospital',methods=['GET','POST'])
def edithospital():
    if 'usertype' in session:
        ut=session['usertype']
        if ut=='admin':
            if request.method=='POST':
                email=request.form['email']
                conn = pymysql.connect(
                    host='localhost',
                    port=3306,
                    user='root',
                    passwd='',
                    db='test',
                    autocommit=True
                )
                cur = conn.cursor()
                sql="select *from hospital_data where email='"+email+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    data=cur.fetchone()
                    return render_template('edithospital.html',data=data)
                else:
                    return render_template('edithospital.html',msg='record not found')
            else:
                return redirect(url_for('edithos'))
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))
@app.route('/edithos')
def edithos():
    return render_template('edithos.html')
@app.route('/edithospital1',methods=['GET','POST'])
def edithospital1():
    if 'usertype' in session:
        ut=session['usertype']
        if ut=='admin':
            if request.method=='POST':
                name = request.form['name']
                sp = request.form['specility']
                ad = request.form['address']
                con = request.form['contact']
                acb = request.form['acbeds']
                nacb = request.form['nonacbeds']
                email = request.form['email']
                conn = pymysql.connect(
                    host='localhost',
                    port=3306,
                    user='root',
                    passwd='',
                    db='test',
                    autocommit=True
                )
                cur = conn.cursor()
                sql="update hospital_data set Name='"+name+"',specility='"+sp+"',address='"+ad+"',Contact='"+con+"',ac_beds='"+acb+"',non_ac_beds='"+nacb+"' where email='"+email+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    return render_template('changesave.html',msg='data is changed')
                else:
                    return render_template('changesave.html',msg='data is not changed')
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))
@app.route('/doctorreg',methods=['GET','POST'])
def doctorreg():
    if 'usertype' in session:
        utype=session['usertype']
        if utype=='hospital':
            if request.method=='POST':
                name=request.form['name']
                sp=request.form['specility']
                time=request.form['time']
                exp=request.form['exprience']
                days=request.form['days']
                email=request.form['email']
                conn = pymysql.connect(
                    host='localhost',
                    port=3306,
                    user='root',
                    passwd='',
                    db='test',
                    autocommit=True
                )
                cur = conn.cursor()
                sql="insert into doctordata values('"+name+"','"+sp+"','"+time+"','"+exp+"','"+days+"','"+email+"')"
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    return render_template('changesave1.html',msg='data is inserted')
                else:
                    return render_template('changesave1',msg='data is not inserted')
            else:
                return render_template('doctorreg.html')
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))
@app.route('/showdoctors')
def showdoctors():
    if 'usertype' in session:
        ut=session['usertype']
        if ut=='hospital':
            conn = pymysql.connect(
                host='localhost',
                port=3306,
                user='root',
                passwd='',
                db='test',
                autocommit=True
            )
            cur = conn.cursor()
            sql="select *from doctordata"
            cur.execute(sql)
            n=cur.rowcount
            if n>0:
                data=cur.fetchall()
                return render_template('showdoctors.html',data=data)
            else:
                return render_template('showdoctors.html',msg='data is not found')
        else:
             return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))
@app.route('/deletedoctor', methods=['GET', 'POST'])
def deletedoctor():
    if 'usertype' in session:
        ut = session['usertype']
        if ut == 'hospital':
            if request.method == 'POST':
                email = request.form['D1']
                conn = pymysql.connect(
                    host='localhost',
                    port=3306,
                    user='root',
                    passwd='',
                    db='test',
                    autocommit=True
                )
                cur = conn.cursor()
                sql = "delete from doctordata where email='" + email + "'"
                cur.execute(sql)
                n = cur.rowcount
                if n == 1:
                    return render_template('changesave1.html',msg='Record is delete')
                else:
                    return render_template('changesave1.html',msg='record is not delete')
            else:
                return render_template('deletedoctor.html')
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))
@app.route('/editdoctor',methods=['GET','POST'])
def editdoctor():
    if 'usertype' in session:
        ut=session['usertype']
        if ut=='hospital':
            if request.method=='POST':
                email=request.form['E1']
                conn = pymysql.connect(
                    host='localhost',
                    port=3306,
                    user='root',
                    passwd='',
                    db='test',
                    autocommit=True
                )
                cur = conn.cursor()
                sql="select *from doctordata where email='"+email+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    data=cur.fetchone()
                    return render_template('editdoctor.html',data=data)
                else:
                    return render_template('editdoctor.html',msg='record not found')
            else:
                return redirect(url_for('editdoc'))
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))
@app.route('/editdoc')
def editdoc():
    return render_template('editdoc.html')
@app.route('/editdoctor1',methods=['GET','POST'])
def editdoctor1():
    if 'usertype' in session:
        ut=session['usertype']
        if ut=='hospital':
            if request.method=='POST':
                name = request.form['name']
                sp = request.form['specility']
                time= request.form['time']
                exp= request.form['exprience']
                days= request.form['days']
                email = request.form['email']
                conn = pymysql.connect(
                    host='localhost',
                    port=3306,
                    user='root',
                    passwd='',
                    db='test',
                    autocommit=True
                )
                cur = conn.cursor()
                sql="update doctordata set name='"+name+"',specility='"+sp+"',time='"+time+"',exprience='"+exp+"',days='"+days+"' where email='"+email+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    return render_template('changesave1.html',msg='data is changed')
                else:
                    return render_template('changesave1.html',msg='data is not changed')
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))
@app.route('/patientreg', methods=['GET', 'POST'])
def patientreg():
    if 'usertype' in session:
        utype = session['usertype']
        if utype == 'hospital':
            if request.method == 'POST':
                name = request.form['name']
                bed = request.form['bedallot']
                doctor = request.form['doctorassign']
                deceise = request.form['deceise']
                address = request.form['address']
                contact = request.form['contact']
                date=request.form['date']
                hname=request.form['hospitalname']
                conn = pymysql.connect(
                    host='localhost',
                    port=3306,
                    user='root',
                    passwd='',
                    db='test',
                    autocommit=True
                )
                cur = conn.cursor()
                sql = "insert into patientdata values('" + name + "','" + bed + "','" + doctor + "','" + deceise + "','" + address + "','" + contact + "','"+date+"','"+hname+"')"
                cur.execute(sql)
                n = cur.rowcount
                if n == 1:
                    return render_template('changesave1.html', msg='data is inserted')
                else:
                    return render_template('changesave1.html', msg='data is not inserted')
            else:
                return render_template('patientform.html')
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))
@app.route('/adminphoto1',methods=['GET','POST'])
def adminphoto1():
    if 'usertype' in session:
        ut=session['usertype']
        e1=session['email']
        if ut=='admin':
            if request.method=='POST':
                file=request.files['f1']
                if file:
                    path=os.path.basename(file.filename)
                    file_ext=os.path.splitext(path)[1][1:]
                    filename=str(int(time.time()))+'.'+file_ext
                    filename=secure_filename(filename)
                    conn = pymysql.connect(
                        host='localhost',
                        port=3306,
                        user='root',
                        passwd='',
                        db='test',
                        autocommit=True
                    )
                    cur = conn.cursor()
                    sql="insert into photo values('"+e1+"','"+filename+"')"
                    try:
                        cur.execute(sql)
                        n=cur.rowcount
                        if n==1:
                            file.save(os.path.join(app.config['UPLOAD_FLODER'],filename))
                            return render_template('photoupload_admin1.html',result="success")
                        else:
                            return render_template('photoupload_admin1.html',result="failure")
                    except:
                        return render_template('photoupload_admin1.html',result="duplicate")
                else:
                    return render_template('photoupload_admin.html')
            else:
                return render_template('photoupload_admin.html')
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))


@app.route('/adminphoto')
def adminphoto():
    return render_template('photoupload_admin.html')
@app.route('/change_adminphoto')
def change_adminphoto():
    if 'usertype' in session:
        usertype=session['usertype']
        email=session['email']
        if usertype=='admin':
            photo = check_photo(email)
            conn = pymysql.connect(
                user='root',
                passwd='',
                port=3306,
                host='localhost',
                db='test',
                autocommit=True

            )
            cur = conn.cursor()
            sql="delete from photo where email='"+email+"'"
            cur.execute(sql)
            n=cur.rowcount
            if n>0:
                os.remove("./static/photos/"+photo)
                return render_template('change_adminphoto.html',data="success")
            else:
                return render_template('change_adminphoto.html', data="failure")
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))
@app.route('/medicalreg')
def medicalreg():
    return render_template('medicaltemplate.html')




@app.route('/forgetpass',methods=['get','post'])
def forgetpass():
    if request.method=='POST':
        email=request.form['email']
        msg = Message('OTP', sender='shulabhdixit143@gmail.com', recipients=[email])
        otp=randrange(100000,999999)
        msg.body ="OTP::"+str(otp)
        mail.send(msg)
        return render_template('passwordgen.html')

@app.route('/passwordgenerator/otp/email',methods=['GET','POST'])
def passwordgenerator():
    if  request.method=='POST':
        npassword=request.form['npassword']
        cpassword=request.form['cpassword']
        email="shulabhdixit143@gmail.com"
        if npassword==cpassword:
            otp=request.form['otp']
            if otp==forgetpass.otp:
                conn = pymysql.connect(
                    host='localhost',
                    port=3306,
                    user='root',
                    passwd='',
                    db='test',
                    autocommit=True
                )
                cur = conn.cursor()
                sql="update logindata set password='"+cpassword+"' where email='"+email+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    return render_template('forgetpass.html',msg="password sucessfully change")
                else:
                    return render_template('forgetpass.html',msg="password not change")
            else:
                return render_template('forgetpass.html',msg='otp is not matching')
        else:
            return render_template('forgetpass.html',msg='password not match')
    else:
        return render_template('passwordgen.html')


if __name__=="__main__":
    app.run(debug=True)
