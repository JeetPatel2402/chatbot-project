from flask import *
import bot
import sqlite3
import re
import os
import datetime
import hashlib
import string
import random
from admin.admin import ad
from student.student import sd
from faculty.faculty import fd
from flask_mail import Mail, Message

app=Flask(__name__)

app.register_blueprint(ad,url_prefix='/admin')
app.register_blueprint(sd,url_prefix='/student')
app.register_blueprint(fd,url_prefix='/faculty')
app.secret_key = '32153abfd564bc76i7t776r76vrc65ce6vr76tv67bt67g7bhbhycgrd'

UPLOAD_FOLDER ='/uploads/'
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'abhipatel056@gmail.com'
app.config['MAIL_PASSWORD'] = 'abhipatel29797'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

@app.route("/",methods=['GET', 'POST'])
@app.route("/home",methods=['GET', 'POST'])
def home():
	return render_template('home.html')

@app.route("/login",methods=['GET', 'POST'])
def login():
	conn=sqlite3.connect('chatbot.db')
	cur=conn.cursor()
	if request.method=='POST':
		username=request.form['username']
		passw=request.form['pass']
		hpass=hashlib.md5(passw.encode())
		password=hpass.hexdigest()
		category=request.form['category']
		if category=='admin':
			cur.execute("SELECT id from admin where id=? AND password=?",(username,password))
			row=cur.fetchall()
			if len(row)==1:
				session['username'] = request.form['username']
				return redirect('/admin')
			else:
				error='username or password is incorrect'
				return render_template('login.html',output=error)
		elif category=='student':
			cur.execute("SELECT s_id from student where s_id=? AND password=?",(username,password))
			row=cur.fetchall()
			if len(row)==1:
				session['id']=str(row[0][0])
				return redirect('/student')
			else:
				error='username or password is incorrect'
				return render_template('login.html',output=error)
		elif category=='faculty':
			cur.execute("SELECT f_id from faculty where f_id=? AND password=?",(username,password))
			row=cur.fetchall()
			if len(row)==1:
				session['fid']=str(row[0][0])
				return redirect('/faculty')
			else:
				error='username or password is incorrect'
				return render_template('login.html',output=error)
	else:
		return render_template('login.html')


@app.route("/forgot",methods=['GET', 'POST'])
def forgot():
	return render_template('password_reset.html')

@app.route("/reset",methods=['GET', 'POST'])
def reset():
	conn=sqlite3.connect('chatbot.db')
	cur=conn.cursor()
	username=request.form['username']
	email=request.form['email']
	category=request.form['category']
	def id_generator(size=32, chars=string.ascii_lowercase + string.digits):
		return ''.join(random.choice(chars) for _ in range(size))
	if category=='admin':
		cur.execute("SELECT email from admin where id=?",(username,))
		row=cur.fetchall()
		if row[0][0]==email:
			code=id_generator()
			msg = Message('Password Reset', sender = 'abhipatel056@gmail.com', recipients = [email])
			msg.body = '''Reset your password using this link 
http://localhost:5000/password_reset/'''+code+''','''+username
			mail.send(msg)
			cur.execute("INSERT into reset values(?,?,'admin')",(username,code))
			conn.commit()
			return render_template("password_reset.html",msg="Password reset link is sent to your mail")
		else:
			error='enter the correct details'
			return render_template('password_reset.html',output=error)
	elif category=='student':
		cur.execute("SELECT email from student where s_id=?",(username,))
		row=cur.fetchall()
		if row[0][0]==email:
			code=id_generator()
			msg = Message('Password Reset', sender = 'abhipatel056@gmail.com', recipients = [email])
			msg.body = '''Reset your password using this link 
http://localhost:5000/password_reset/'''+code+''','''+username
			mail.send(msg)
			cur.execute("INSERT into reset values(?,?,'student')",(username,code))
			conn.commit()
			return render_template("password_reset.html",msg="Password reset link is sent to your mail")
		else:
			error='enter the correct details'
			return render_template('password_reset.html',output=error)
	elif category=='faculty':
		cur.execute("SELECT f_id from faculty where f_id=? AND password=?",(username,password))
		row=cur.fetchall()
		if row[0][0]==email:
			code=id_generator()
			msg = Message('Password Reset', sender = 'abhipatel056@gmail.com', recipients = [email])
			msg.body = '''Reset your password using this link 
http://localhost:5000/password_reset/'''+code+''','''+username
			mail.send(msg)
			cur.execute("INSERT into reset values(?,?,'faculty')",(username,code))
			conn.commit()
			return render_template("password_reset.html",msg="Password reset link is sent to your mail")
		else:
			error='enter the correct details'
			return render_template('password_reset.html',output=error)

@app.route("/password_reset/<code>",methods=['GET', 'POST'])
def password_reset(code):
	lst=code.split(',')
	uname=lst[1]
	code=lst[0]
	conn=sqlite3.connect('chatbot.db')
	cur=conn.cursor()
	cur.execute("SELECT * from reset where user=? and reset=?",(uname,code))
	row=cur.fetchall()
	if(len(row)!=0):
		return render_template('reset.html',uname=uname,category=row[0][2])
	else:
		return render_template('error.html')

@app.route("/password_change",methods=['GET', 'POST'])
def password_change():
	conn=sqlite3.connect('chatbot.db')
	cur=conn.cursor()
	passw=request.form['pass']
	hpass=hashlib.md5(passw.encode())
	password=hpass.hexdigest()
	user=request.form['user']
	category=request.form['category']
	if category=='admin':
		cur.execute("UPDATE admin set password=? where id=?",(password,user))
		cur.execute("DELETE from reset where user=?",(user,))
		conn.commit()
		return render_template('reset.html',output="password changed successfully")
	elif category=='student':
		cur.execute("UPDATE student set password=? where s_id=?",(password,user))
		cur.execute("DELETE from reset where user=?",(user,))
		conn.commit()
		return render_template('reset.html',output="password changed successfully")
	elif category=='faculty':
		cur.execute("UPDATE faculty set password=? where f_id=?",(password,user))
		cur.execute("DELETE from reset where user=?",(user,))
		conn.commit()
		return render_template('reset.html',output="password changed successfully")

@app.route("/invalid",methods=['GET', 'POST'])
def invalid():
	conn=sqlite3.connect('chatbot.db')
	cur=conn.cursor()
	query=request.form['query']
	res=request.form['res']
	try:
		if session['id']:
			cat='student'
	except KeyError:
		cat='guest'
	resp=str(res)
	if resp=="sorry I can't understand what you want to say":
		try:
			cur.execute("INSERT INTO new_question VALUES (?,?)",(str(query),cat))
			conn.commit()
			return jsonify({'msg':'response is successfully added to invalid responses'})
		except:
			return jsonify({'msg':'please check your query or response is already is added as invalid'})
	else:
		try:
			cur.execute("INSERT INTO invalid VALUES (?,?,?)",(str(query),resp,cat))
			conn.commit()
			return jsonify({'msg':'response is successfully added to invalid responses'})
		except:
			return jsonify({'msg':'please check your query or response is already is added as invalid'})

@app.route("/contact",methods=['GET', 'POST'])
def contact():
	conn=sqlite3.connect('chatbot.db')
	cur=conn.cursor()
	if request.method=='POST':
		name=str(request.form['name'])
		email=str(request.form['email'])
		contact=str(request.form['contact'])
		city=str(request.form['city'])
		message=str(request.form['message'])
		today=datetime.date.today()
		date=str(today.strftime('%d, %b %Y'))
		cur.execute("INSERT INTO guest(name,email,contact,city,message,date) VALUES (?,?,?,?,?,?)",(name,email,contact,city,message,date))
		conn.commit()
		msg='your details are successfully sent'
		return render_template('contact.html',output=msg)
	else:
		return render_template('contact.html')


@app.route("/get",methods=['GET', 'POST'])
def get():
	conn=sqlite3.connect('chatbot.db')
	cur=conn.cursor()
	if request.method=='POST':
		query=request.form['query']
		if query:
			response = bot.previous_chats(query)
			if response=='student':
				try:
					if 'attendance' in query:
						response=""
						cur.execute("SELECT * from attendance where s_id=?",(session['id'],))
						row=cur.fetchall()
						cur.execute("SELECT d_id,semester from student where s_id=?",(session['id'],))
						row1=cur.fetchall()
						cur.execute("SELECT name from course where d_id=? AND semester=?",(row1[0]))
						row2=cur.fetchall()
						for j in range(len(row2)):
							response=response+str(row2[j][0])+':'+str(row[0][j+1])+'<br>'
					elif 'result' in query or 'scored' in query:
						cur.execute("SELECT * from result where s_id=?",(session['id'],))
						row=cur.fetchall()
						response=str(row[0][1])+' result<br>'
						cur.execute("SELECT d_id,semester from student where s_id=?",(session['id'],))
						row1=cur.fetchall()
						cur.execute("SELECT name from course where d_id=? AND semester=?",(row1[0]))
						row2=cur.fetchall()
						for j in range(len(row2)):
							response=response+str(row2[j][0])+':'+str(row[0][j+2])+'<br>'
					elif 'mid-sem exam' in query or 'viva' in query or 'submission' in query:
						cur.execute("SELECT d_id,semester from student where s_id=?",(session['id'],))
						row1=cur.fetchall()
						if 'mid-sem exam' in query:
							cur.execute("SELECT name,mid_date from course where d_id=? AND semester=?",(row1[0]))
							row2=cur.fetchall()
							response="mid-sem exam schedule:<br>"
						if 'viva' in query or 'submission' in  query:
							cur.execute("SELECT name,int_viva_date from course where d_id=? AND semester=?",(row1[0]))
							row2=cur.fetchall()
							response="mid-sem exam schedule:<br>"
						if  not row2[0][1]:
							response=response+'not available yet'
						else:
							for j in range(len(row2)):
								response=response+str(row2[j][0])+':'+str(row2[j][1])+'<br>'
					elif 'class time table' in query:
						cur.execute("SELECT d_id,division from student where s_id=?",(session['id'],))
						row1=cur.fetchall()
						cur.execute("SELECT d_name from department where d_id=?",(str(row1[0][0])))
						row2=cur.fetchall()
						department=str(row2[0][0])
						division=str(row1[0][1])
						response='''<img src="/static/image/time-table/'''+department+division+'''.jpg">'''
					else:
						response=bot.previous_chats(query,False)
				except KeyError:
					response="please login into your student portal first!"
			if 'link' in response:
				link=re.search('#(.+?)#',response).group(1)
				print(link)
				if 'image' in str(link):
					img=re.search('(.+?)[^\S]image',link).group(1)
					print(img)
					response='<a href="static/image/'+str(img)+'.jpg" target="_blank"><img src="static/image/'+str(img)+'.jpg"></a>'
				else:
					if link=='result':
						path=os.getcwd()
						path=path+'/static/documents/results/'
						response="results:"
						for file in os.listdir(path):
							filename=re.search('(.+?).pdf',str(file)).group(1)
							response=response+'<a href="static/documents/results/'+str(file)+'" target="_blank" style="color:red;">'+str(filename)+'</a><br>'
					else:
						res='<a href="static/documents/'+str(link)+'.pdf" target="_blank" style="color:red;">Click here to get information</a>'
						response=re.search('(.*?)#(.+?)#',response).group(1)+res
			return jsonify({'response':response})
		else:
			return jsonify({'error':'input needed'})

if __name__ == '__main__':
	app.run(debug=True)
