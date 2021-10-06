from flask import *
import sqlite3
import hashlib
import os
from admin import add
from werkzeug.utils import secure_filename 
ad=Blueprint('admin',__name__,template_folder='templates')

@ad.route("/",methods=['GET','POST'])
def admin():
	try:
		admin_id=session['username']
		conn=sqlite3.connect('chatbot.db')
		cur=conn.cursor()
		cur.execute("SELECT sr_no from guest")
		row=cur.fetchall()
		m=len(row)
		cur.execute("SELECT query from new_question")
		row=cur.fetchall()
		n=len(row)
		cur.execute("SELECT query from invalid")
		row=cur.fetchall()
		i=len(row)
		return render_template('admin/admin.html',data=[m,n,i])
	except KeyError:
		return redirect('/login')

@ad.route("/addStudent",methods=['GET','POST'])
def addStudent():
	try:
		sid=session['username']
	except KeyError:
		return redirect('/login')
	if request.method=='POST':
		roll=request.form['roll']
		name=request.form['name']
		password=request.form['pass']
		hpass=hashlib.md5(password.encode())
		password=hpass.hexdigest()
		dob=request.form['dob']
		contact=request.form['contact']
		email=request.form['email']
		department=request.form['department']
		address=request.form['address']
		year=request.form['year']
		div=request.form['div']
		fee=request.form['fee']
		sem=request.form['sem']
		conn=sqlite3.connect('chatbot.db')
		cur=conn.cursor()
		try:
			cur.execute("INSERT into student(s_id,name,password,dob,contact,email,d_id,address,adm_year,division,fee_class,semester) values(?,?,?,?,?,?,?,?,?,?,?,?)" ,(roll,name,password,dob,contact,email,department,address,year,div,fee,sem))
			conn.commit()
			return render_template('admin/addStudent.html',data='details are succesfully saved')
		except sqlite3.IntegrityError:
			err='already exists'
			return render_template('admin/addStudent.html',data=err)
	return render_template('admin/addStudent.html')

@ad.route("/addFaculty",methods=['GET','POST'])
def addFaculty():
	try:
		sid=session['username']
	except KeyError:
		return redirect('/login')
	if request.method=='POST':
		fid=request.form['fid']
		name=request.form['name']
		password=request.form['password']
		hpass=hashlib.md5(password.encode())
		password=hpass.hexdigest()
		dob=request.form['dob']
		contact=request.form['contact']
		email=request.form['email']
		department=request.form['department']
		address=request.form['address']
		designation=request.form['designation']
		qual=request.form['qual']
		conn=sqlite3.connect('chatbot.db')
		cur=conn.cursor()
		try:
			cur.execute("INSERT into faculty(f_id,name,d_id,email,contact,dob,designation,password,qualification,address) values(?,?,?,?,?,?,?,?,?,?)" ,(fid,name,department,email,contact,dob,designation,password,qual,address))
			conn.commit()
			return render_template('admin/addFaculty.html',data='details are succesfully saved')
		except sqlite3.IntegrityError:
			err='already exists'
			return render_template('admin/addFaculty.html',data=err)
	return render_template('admin/addFaculty.html')

@ad.route("/addQuestion",methods=['GET','POST'])
def addQuestion():
	try:
		sid=session['username']
	except KeyError:
		return redirect('/login')
	if request.method=='POST':
		query=request.form['query']
		response=request.form['res']
		cat=request.form['Category']
		if cat=='informal':
			add.add('previous_chats.json',query,response)
		if cat=='guest':
			add.add('guest.json',query,response)
		if cat=='student':
			keyword=request.form['key']
			query=query+" "+keyword
			add.add('student.json',query,'student')
		return render_template('admin/addQuestion.html',qry='',msg='Question is added successfully')

	try:
		data=request.args['dt']
		return render_template('admin/addQuestion.html',qry=data,msg='')
	except KeyError:
		return render_template('admin/addQuestion.html')

@ad.route("/updateAnswer",methods=['GET','POST'])
def updateAnswer():
	try:
		sid=session['username']
	except KeyError:
		return redirect('/login')
	if request.method=='POST':
		query=request.form['query']
		response=request.form['response']
		cat=request.form['Category']
		if cat=='informal':
			add.add('previous_chats.json',query,response)
		else:
			add.update('guest.json',query,response)
		return render_template('admin/updateAnswer.html',data='',msg='Question is added successfully')
	try:
		q=request.args['q']
		return render_template('admin/updateAnswer.html',data=q,msg='')
	except KeyError:
		return render_template('admin/updateAnswer.html')

@ad.route("/addFile",methods=['GET','POST'])
def addFile():
	try:
		sid=session['username']
	except KeyError:
		return redirect('/login')
	if request.method == 'POST':
		f = request.files['file']
		f.save(secure_filename(f.filename))
		category=request.form['Category']
		subcat=request.form['cat']
		name=request.form['name']
		cwd=os.getcwd()
		if category=='image':
			if subcat=='timetable':
				fname=cwd+'/static/image/time-table/'+name
			else:
				fname=cwd+'/static/image/'+name
		else:
			if subcat=='result':
				fname=cwd+'/static/documents/results/'+name
			else:
				fname=cwd+'/static/documents/'+name
		os.rename(f.filename,fname)
		return render_template('admin/addFile.html',msg="file uploaded successfully")

	return render_template('admin/addFile.html')

@ad.route("/setting",methods=['GET','POST'])
def setting():
	try:
		sid=session['username']
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
		cur.execute("SELECT password from admin where id=?",(session['username'],))
		row=cur.fetchall()
		print(row[0][0])
		if str(row[0][0])==password and np==cfp:
			cur.execute("UPDATE admin set password=? where id=?",(npassword,session['username']))
			conn.commit()
			return render_template("admin/setting.html",msg='password is changed successfully')
		else:
			return render_template("admin/setting.html",err='password is not matched')
	return render_template('admin/setting.html')

@ad.route("/messages",methods=['GET','POST'])
def messages():
	try:
		sid=session['username']
	except KeyError:
		return redirect('/login')
	conn=sqlite3.connect('chatbot.db')
	cur=conn.cursor()
	if request.method=='POST':
		cid=request.form.getlist('del')
		for i in cid:
			cur.execute("DELETE FROM guest WHERE sr_no=?",(i))
		conn.commit()

	cur.execute("SELECT * from guest")
	row=cur.fetchall()
	return render_template('admin/messages.html',data=row)


@ad.route("/newQuestions",methods=['GET','POST'])
def newQuestions():
	try:
		sid=session['username']
	except KeyError:
		return redirect('/login')
	conn=sqlite3.connect('chatbot.db')
	cur=conn.cursor()
	if request.method=='POST':
		cid=request.form.getlist('del')
		for i in cid:
			cur.execute("DELETE FROM new_question WHERE query=?",(i,))
		conn.commit()
	cur.execute("SELECT * from new_question")
	row=cur.fetchall()
	return render_template('admin/newQuestions.html',data=row)

@ad.route("/invalidAnswers",methods=['GET','POST'])
def invalidAnswers():
	try:
		sid=session['username']
	except KeyError:
		return redirect('/login')
	conn=sqlite3.connect('chatbot.db')
	cur=conn.cursor()
	try:
		qry=request.args['dt']
		cur.execute("DELETE FROM invalid where query=?",(qry,))
		conn.commit()
	except KeyError:
		print('h')
	cur.execute("SELECT * from invalid")
	row=cur.fetchall()
	return render_template('admin/invalidAnswers.html',data=row)

@ad.route("/adlogout",methods=['GET', 'POST'])
def adlogout():
	session.pop('username')
	return redirect('/home')