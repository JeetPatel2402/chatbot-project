from flask import *
import sqlite3
import hashlib
import os
from werkzeug.utils import secure_filename
sd=Blueprint('student',__name__,template_folder='templates')

@sd.route("/",methods=['GET','POST'])
def student():
	try:
		sid=session['id']
		conn=sqlite3.connect('chatbot.db')
		cur=conn.cursor()
		cur.execute("SELECT * from student where s_id=?",(session['id'],))
		row=cur.fetchall()
		cur.execute("SELECT d_name from department where d_id=?",(str(row[0][6])))
		row1=cur.fetchone()
		rw=list(row[0])
		rw[6]=row1[0]
		del rw[2]
		return render_template('student/student.html',data=rw)
	except KeyError:
		return redirect('/login')

@sd.route("/changePass",methods=['GET','POST'])
def changePass():
	try:
		sid=session['id']
	except KeyError:
		return redirect('/login')
	if request.method=='POST':
		cp=str(request.form['cp'])
		hpass=hashlib.md5(cp.encode())
		password=hpass.hexdigest()
		np=str(request.form['np'])
		hpass=hashlib.md5(np.encode())
		npassword=hpass.hexdigest()
		cfp=str(request.form['cfp'])
		conn=sqlite3.connect('chatbot.db')
		cur=conn.cursor()
		cur.execute("SELECT password from student where s_id=?",(session['id'],))
		row=cur.fetchall()
		print(row[0][0])
		if str(row[0][0])==password and np==cfp:
			cur.execute("UPDATE student set password=? where s_id=?",(npassword,session['id']))
			conn.commit()
			return render_template("student/changePass.html",msg='password is changed successfully')
		else:
			return render_template("student/changePass.html",err='password is not matched')
	return render_template("student/changePass.html")

@sd.route("/query",methods=['GET','POST'])
def query():
	try:
		sid=session['id']
	except KeyError:
		return redirect('/login')
	return render_template("student/query.html",data=session['id'])

@sd.route("/update",methods=['GET','POST'])
def update():
	try:
		sid=session['id']
	except KeyError:
		return redirect('/login')
	conn=sqlite3.connect('chatbot.db')
	cur=conn.cursor()
	data=[]*5
	if request.method=='POST':
		contact=request.form['contact']
		email=request.form['email']
		address=request.form['address']
		division=request.form['division']
		semester=request.form['sem']
		cur.execute("UPDATE student set contact=?,email=?,address=?,division=?,semester=? where s_id=?",(contact,email,address,division,semester,session['id']))
		conn.commit()
		try:
			f=request.files['file']
			f.save(secure_filename(f.filename))
			cwd=os.getcwd()
			fname=cwd+'/static/image/student/'+session['id']+'.jpg'
			if os.path.exists(fname):
				os.remove(fname)
			os.rename(f.filename,fname)
			return render_template("student/updateDetail.html",msg="Details updated successfully",data=data)
		except KeyError:
			return render_template("student/updateDetail.html",msg="Details updated successfully",data=data)
	cur.execute("SELECT contact,email,address,division,semester from student where s_id=?",(session['id'],))
	row=cur.fetchall()
	lst=list()
	for i in row[0]:
		lst.append(i)
	return render_template("student/updateDetail.html",data=lst)

@sd.route("/stdlogout",methods=['GET', 'POST'])
def stdlogout():
	session.pop('id')
	return redirect('/home')