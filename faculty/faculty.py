from flask import * 
import sqlite3 
fd=Blueprint('faculty',__name__,template_folder='templates')

@fd.route("/",methods=['GET','POST'])
def faculty():
	try:
		sid=session['fid']
		conn=sqlite3.connect('chatbot.db')
		cur=conn.cursor()
		cur.execute("SELECT * from faculty where f_id=?",(session['fid'],))
		row=cur.fetchall()
		cur.execute("SELECT d_name from department where d_id=?",(str(row[0][2])))
		row1=cur.fetchone()
		rw=list(row[0])
		rw[2]=row1[0]
		del rw[7]
		print(rw)
		return render_template('faculty/faculty.html',data=rw)
	except KeyError:
		return redirect('/login')

@fd.route("/attendance",methods=['GET','POST'])
def attendance():
	try:
		sid=session['fid']
	except KeyError:
		return redirect('/login')
	conn=sqlite3.connect('chatbot.db')
	cur=conn.cursor()
	if request.method=='POST':
		sid=request.form['roll']
		sub=request.form['subject']
		att=request.form['attendance']
		sub='sub'+sub[-1:]
		print(sub)
		query="UPDATE attendance set "+sub+"=? where s_id=?"
		cur.execute(query,(att,sid))
		conn.commit()
		return render_template("faculty/attendance.html",data=[()],msg='successfully updated')
	else:
		try:
			cur.execute("SELECT c_id from faculty_course where f_id=?",(session['fid'],))
			row=cur.fetchall()
			sid=request.args['roll']
			course=[(sid,)]
			cur.execute("SELECT d_id,semester from student where s_id=?",(sid,))
			row1=cur.fetchall()
			for c in row:
				cid=c[0]
				cur.execute("SELECT name from course where c_id=? and d_id=? and semester=?",(cid,row1[0][0],row1[0][1]))
				cc=cur.fetchall()
				course.append((cid,cc[0][0]))
			return render_template("faculty/attendance.html",data=course,msg="")
		except KeyError:
			return render_template("faculty/attendance.html",data=[()],msg="")

@fd.route("/result",methods=['GET','POST'])
def result():
	try:
		sid=session['fid']
	except KeyError:
		return redirect('/login')
	conn=sqlite3.connect('chatbot.db')
	cur=conn.cursor()
	if request.method=='POST':
		sid=request.form['roll']
		sub=request.form['subject']
		marks=request.form['marks']
		exam=request.form['exam']
		sub='sub'+sub[-1:]
		try:
			cur.execute("INSERT into result(s_id,exam) values(?,?)",(sid,exam))
			conn.commit()
		except sqlite3.IntegrityError:
			print(sub)
		query="UPDATE result set "+sub+"=? where s_id=? and exam=?"
		cur.execute(query,(marks,sid,exam))
		conn.commit()
		return render_template("faculty/result.html",data=[()],msg='successfully updated')
	else:
		try:
			cur.execute("SELECT c_id from faculty_course where f_id=?",(session['fid'],))
			row=cur.fetchall()
			sid=request.args['roll']
			course=[(sid,)]
			cur.execute("SELECT d_id,semester from student where s_id=?",(sid,))
			row1=cur.fetchall()
			for c in row:
				cid=c[0]
				cur.execute("SELECT name from course where c_id=? and d_id=? and semester=?",(cid,row1[0][0],row1[0][1]))
				cc=cur.fetchall()
				course.append((cid,cc[0][0]))
			return render_template("faculty/result.html",data=course,msg="")
		except KeyError:
			return render_template("faculty/result.html",data=[()],msg="")
@fd.route("/schedule",methods=['GET','POST'])
def schedule():
	try:
		sid=session['fid']
	except KeyError:
		return redirect('/login')
	conn=sqlite3.connect('chatbot.db')
	cur=conn.cursor()
	if request.method=='POST':
		subject=request.form['subject']
		exam=request.form['exam']
		date=request.form['date']
		if exam=='mid-sem-1':
			cur.execute("UPDATE course set mid1_date=? where c_id=?",(date,subject))
		if exam=='mid-sem-2':
			cur.execute("UPDATE course set mid2_date=? where c_id=?",(date,subject))
		if exam=='internal':
			cur.execute("UPDATE course set int_viva_date=? where c_id=?",(date,subject))
		conn.commit()
	cur.execute("SELECT c_id from faculty_course where f_id=?",(session['fid'],))
	row=cur.fetchall()
	course=[]
	for c in row:
		cid=c[0]
		cur.execute("SELECT name from course where c_id=?",(cid,))
		cc=cur.fetchall()
		course.append((cid,cc[0][0]))
	return render_template("faculty/schedule.html",data=course,msg='successfully updated')
			

@fd.route("/fchangePass",methods=['GET','POST'])
def changePass():
	try:
		sid=session['fid']
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
		cur.execute("SELECT password from faculty where f_id=?",(session['fid'],))
		row=cur.fetchall()
		print(row[0][0])
		if str(row[0][0])==password and np==cfp:
			cur.execute("UPDATE faculty set password=? where f_id=?",(npassword,session['fid']))
			conn.commit()
			return render_template("faculty/changePass.html",msg='password is changed successfully')
		else:
			return render_template("faculty/changePass.html",err='password is not matched')
	return render_template("faculty/changePass.html")

@fd.route("/ftlogout",methods=['GET', 'POST'])
def ftlogout():
	session.pop('fid')
	return redirect('/home')