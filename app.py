import csv
from sklearn.preprocessing import LabelEncoder
from flask import Flask, render_template, request, flash, session
import numpy as np
import mysql.connector
import cv2, os
import pandas as pd
import pickle
import smtplib
import datetime
import time
import random
from PIL import Image
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import threading

mydb = mysql.connector.connect(host="localhost", user="root", passwd="", port=3307,database="face_biometric")
cursor = mydb.cursor()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'navya'


@app.route('/')
def index():
    return render_template('index.html')
@app.route('/adminlog')
def adminlog():
    return render_template('adminlog.html')

@app.route('/portfolio_details')
def portfolio_details():
    return render_template('portfolio-details.html')


@app.route('/register', methods=["POST"])
def register():
    print("*******************")
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        pwd = request.form['pwd']
        cpwd = request.form['cpwd']
        pno = request.form['pno']
        addr = request.form['addr']
        uname = request.form['uname']
        otp1 = random.randint(0000, 9999)
        ts = time.time()
        date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        sql = "select * from user_registration"
        result = pd.read_sql_query(sql, mydb)
        email1 = result['email'].values
        # print(email1)
        if email in email1:
            flash("Eamil already existed", "warning")
            return render_template('index.html')
        if pwd == cpwd:
            cam = cv2.VideoCapture(0)
            harcascadePath = r"haarcascade\haarcascade_frontalface_default.xml"
            detector = cv2.CascadeClassifier(harcascadePath)
            df = pd.read_csv("person_details/person_details.csv")
            val = df.email.values
            if email in str(val):
                # df.loc[df['Aadhar_no'] == aa, 'dose'] = 'Dose2'
                # writing into the file
                # df.to_csv("person_details/person_details.csv", index=False)
                flash("Id already exists", "danger")
                return render_template("index.html")

            sampleNum = 0
            while (True):
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    # incrementing sample number
                    sampleNum = sampleNum + 1
                    # saving the captured face in the dataset folder TrainingImage
                    cv2.imwrite("TrainingImage/ " + name + "." + str(otp1) + '.' + str(sampleNum) + ".jpg",
                                gray[y:y + h, x:x + w])
                    # display the frame

                else:
                    cv2.imshow('frame', img)
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
                elif sampleNum > 350:
                    break

            cam.release()
            cv2.destroyAllWindows()
            row = [otp1, name, email, pno]
            with open(r'person_details\person_details.csv', 'a+') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(row)
            csvFile.close()
            sql = "INSERT INTO user_registration (sid,name,email,uname,pwd,pno,addr,d1) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (otp1, name, email, uname, pwd, pno, addr, date)
            cursor.execute(sql, val)
            mydb.commit()
            msg = 'Your Exam Id is: '
            t = 'Regards,'
            t1 = 'Online Student Authentication and Proctoring System.'
            mail_content = 'Dear ' + name +','+'\n'+msg  + str(otp1) +'\n'+ '\n' + t + '\n' + t1
            sender_address = 'prasanthsai79@gmail.com'
            sender_pass = 'soxunjeybrvylqro'
            receiver_address = email
            message = MIMEMultipart()
            message['From'] = sender_address
            message['To'] = receiver_address
            message['Subject'] = 'Online Student Authentication and Proctoring System.'
            message.attach(MIMEText(mail_content, 'plain'))
            ses = smtplib.SMTP('smtp.gmail.com', 587)
            ses.starttls()
            ses.login(sender_address, sender_pass)
            text = message.as_string()
            ses.sendmail(sender_address, receiver_address, text)
            ses.quit()
            flash("Successfully Registered", "warning")
            return render_template('index.html')
        else:
            flash("password and confirm password not same", "warning")
            return render_template('index.html')

    return render_template('index.html')

@app.route('/adminlog1', methods=['POST','GET'])
def adminlog1():
    if request.method == 'POST':
        username = request.form['name']
        password1 = request.form['pwd']

        if username == 'admin' and password1 == 'admin':
            flash("Welcome Admin", "success")
            return render_template('adminhome.html')
        else:
            flash("Invalid Credentials Please Try Again", "warning")
            return render_template('adminlog.html')
    return render_template('index.html')
@app.route('/login', methods=['POST', 'GET'])
def login():
    recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
    recognizer.read(r"Trained_Model\Trainner.yml")
    harcascadePath = r"Haarcascade\haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath);
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    pkl_file = open('label_encoder.pkl', 'rb')
    le = pickle.load(pkl_file)
    pkl_file.close()
    flag = 0
    det = 0
    global tt
    tt = " "
    while True:
        ret, im = cam.read()
        flag += 1
        if flag == 200:
            flash(r"Unable to detect person", "info")
            cv2.destroyAllWindows()
            return render_template('index.html')
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
            Id, conf = recognizer.predict(gray[y:y + h, x:x + w])
            # print(conf)
            if (conf < 50):
                det += 1
                tt = le.inverse_transform([Id])
                tt = tt[0]
                print(tt)
                if det == 15:
                    sql = "select * from user_registration where sid='%s' " % (str(tt))
                    x = cursor.execute(sql)
                    results = cursor.fetchall()
                    session['sid'] = results[0][1]
                    session['name'] = results[0][2]
                    session['email'] = results[0][3]
                    flash("Welcome ", "success")
                    cam.release()
                    cv2.destroyAllWindows()
                    return render_template('studenthome.html', msg=results[0][2])
            cv2.putText(im, str(tt), (x, y + h), font, 1, (255, 255, 255), 2)
        cv2.imshow('im', im)

        if (cv2.waitKey(1) == ord('q')):
            break
    cam.release()
    cv2.destroyAllWindows()
    return render_template('index.html')


@app.route('/adminhome')
def adminhome():
    return render_template('adminhome.html')


@app.route('/view_registrations')
def view_registrations():
    sql = "select * from user_registration  "
    x = pd.read_sql_query(sql, mydb)
    x = x.drop(['pwd'], axis=1)

    return render_template('view_registrations.html', row_val=x.values.tolist())


@app.route('/training', methods=['POST', 'GET'])
def training():
    le = LabelEncoder()
    faces, Id = getImagesAndLabels("TrainingImage")
    Id = le.fit_transform(Id)
    output = open('label_encoder.pkl', 'wb')
    pickle.dump(le, output)
    output.close()
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(faces, np.array(Id))
    recognizer.save("Trained_Model/Trainner.yml")
    flash("Model Trained Successfully", "success")
    return render_template('adminhome.html')


def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faces = []
    Ids = []
    for imagePath in imagePaths:
        pilImage = Image.open(imagePath).convert('L')
        imageNp = np.array(pilImage, 'uint8')
        Id = str(os.path.split(imagePath)[-1].split(".")[1])
        faces.append(imageNp)
        Ids.append(Id)
    return faces, Ids


@app.route('/add_question')
def add_question():
    return render_template('add_question.html')


@app.route('/qsnback', methods=["POST"])
def qsnback():
    print("*******************")
    if request.method == 'POST':
        qsn = request.form['qsn']
        opt1 = request.form['opt1']
        opt2 = request.form['opt2']
        opt3 = request.form['opt3']
        opt4 = request.form['opt4']
        ans = request.form['ans']
        print("&&&&&&&&&")
        sql = "INSERT INTO qsn_ans(qsn,opt1,opt2,opt3,opt4,ans) VALUES (%s,%s,%s,%s,%s,%s)"
        val = (qsn, opt1, opt2, opt3, opt4, ans)
        cursor.execute(sql, val)
        mydb.commit()
        flash("Question added", "info")
        return render_template('add_question.html')
    return render_template('add_question.html')


@app.route('/view_questions')
def view_questions():
    # email=session.get('email')
    sql = "select * from qsn_ans "
    x = pd.read_sql_query(sql, mydb)
    x = x.drop(['id'], axis=1)
    return render_template('viewqsn.html', row_val=x.values.tolist())


@app.route('/create_exam')
def create_exam():
    return render_template('create_exam.html')


@app.route('/create_exam_back', methods=["POST"])
def create_exam_back():
    print("*******************")
    if request.method == 'POST':
        opt1 = request.form['opt1']
        opt2 = request.form['opt2']
        s = "select * from qsn_ans ORDER BY RAND()  LIMIT 10"
        x = pd.read_sql_query(s, mydb)
        # qsn=x.values['qsn']
        # id=x.values['id']
        # opt1=x.values['opt1']
        # opt2=x.values['opt2']
        # opt3=x.values['opt3']
        # opt4=x.values['opt4']
        # ans=x.values['ans']
        print(len(x))
        v = len(x)
        for i in range(0, v):
            sql = "INSERT INTO exam_paper(a,b,c,d,e,f,g,hh,i) VALUES ('" + str(x.values[i][0]) + "','" + x.values[i][
                1] + "','" + x.values[i][2] + "','" + x.values[i][3] + "','" + x.values[i][4] + "','" + x.values[i][
                      5] + "','" + x.values[i][6] + "','" + opt1 + "','" + opt2 + "')"
            # print(sql)
            # val = (qsn, opt1, opt2, opt3, opt4, ans)
            cursor.execute(sql, mydb)
            mydb.commit()

        flash("Exam paper created", "info")
        # return render_template('add_question.html')
    return render_template('create_exam.html')


@app.route('/studenthome')
def studenthome():
    return render_template('studenthome.html')


@app.route('/view_exam')
def view_exam():
    # email=session.get('email')
    sql = "select * from exam_paper where i>=CURRENT_DATE() GROUP BY hh"
    x = pd.read_sql_query(sql, mydb)
    x = x.drop(['a', 'b', 'c', 'd', 'e', 'f', 'g'], axis=1)
    return render_template('view_exam.html', row_val=x.values.tolist())

def TrackImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
    recognizer.read("Trained_Model\Trainner.yml")
    harcascadePath = "Haarcascade\haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath);
    global cam
    # df = pd.read_csv("person_details\person_details.csv")
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    font = cv2.FONT_HERSHEY_SIMPLEX
    pkl_file = open('label_encoder.pkl', 'rb')
    le = pickle.load(pkl_file)
    pkl_file.close()

    count = []
    flag = 0
    det = 0
    global val_data, global_stop
    global_stop=False


    print("hhhhhhhhhhhhhhhhhhhhhhh")
    while True:
        ret, im = cam.read()
        flag += 1
        if flag == 5:
            print(flag)
        print("rrrrrrrrrrrrrr")

        # print(flag)
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
            Id, conf = recognizer.predict(gray[y:y + h, x:x + w])
            print(conf)
            if (conf < 50):
                det += 1
                tt = le.inverse_transform([Id])
                tt = tt[0]
                print(tt)
                val_data="Real"

            else:
                Id = 'Unknown'
                flag += 1
                print("unknown")
                print(flag)
                tt = str(Id)
                print(tt)

                if flag > 100:
                    cam.release()
                    cv2.destroyAllWindows()
                    val_data='Fake'
                    return
            cv2.putText(im, str(tt), (x, y + h), font, 1, (255, 255, 255), 2)
        cv2.imshow('im', im)
        if (cv2.waitKey(1) == ord('q')):
            break
        if global_stop:
            break
        # return redirect(url_for('TrackImages'))
    cam.release()
    cv2.destroyAllWindows()
    # return redirect(url_for('TrackImages'))

@app.route('/take_test/<s>/<s1>/<s2>')
def take_test(s=0, s1="", s2=""):
    email=session.get("email")
    sid=session.get("sid")
    s="select count(*) from results where sid='"+str(sid)+"' and ename='"+str(s1)+"' and edate='"+str(s2)+"' "
    y=pd.read_sql_query(s,mydb)
    count=y.values[0][0]
    print("hhhhhhhhhhhhhhhhh")
    print(count)
    if count==0:
        sql = "select * from exam_paper where hh='" + s1 + "' and i='" + s2 + "'"
        x = pd.read_sql_query(sql, mydb)
        # print(x)
        ans = x['g']
        # x=x.drop(['id','a','hh','g','hh','i'],axis=1)
        row1 = len(x.values.tolist())
        print(type(row1))
        print(row1)
        # print(x)
        dd = row1
        global t1
        t1 = threading.Thread(target=TrackImages)
        t1.start()
        return render_template("take_test.html", s=s, s1=s1, s2=s2, row_val=x.values.tolist(), r1=row1, a=ans)
    else:
        flash("You have already attempted the exam","warning")
        return render_template("studenthome.html")

@app.route('/textback', methods=['GET','POST'])
def textback():
    if request.method=='POST':
        lenn=request.form['dpr']
        s1=request.form['s1']
        s2=request.form['s2']
        sid=session.get('sid')
        email=session.get('email')
        name=session.get('name')
        print(type(lenn))
        print(lenn)
        # print(type(int(lenn)))
        # lenn=int(lenn)
        print(s1)
        print(s2)
        for ss in range(0,int(lenn)):
            print(ss)
            sss="myans"+str(ss)
            ca="currans"+str(ss)

            ca1 = request.form[ca]
            sss1 = request.form[sss]

            sql="insert into results(sid,sname,semail,ename,edate,ca,ua,status)values('"+str(sid)+"','"+str(name)+"','"+str(email)+"','"+str(s1)+"','"+str(s2)+"','"+str(ca1)+"','"+str(sss1)+"','"+str(val_data)+"')"

            print(sql)
            cursor.execute(sql)
            mydb.commit()
        sql1="insert into finalresults(sid,semail,ename,edate,ca,ua,status) values ('"+str(sid)+"','"+str(email)+"','"+str(s1)+"','"+str(s2)+"',(select count(*) from results where ca=ua and sid='"+str(sid)+"' and ename='"+str(s1)+"' and edate='"+str(s2)+"') ,(select count(*) from results where sid='"+str(sid)+"' and ename='"+str(s1)+"' and edate='"+str(s2)+"'),'"+str(val_data)+"' )"
        print(sql1)
        cursor.execute(sql1)
        mydb.commit()
        # sq="select ca,ua from finalresults where umail='"+session['email']+"' and cid='"+ci+"'"
        # # sq="select ca,ua from finalresults where umail='"+email+"' and cid='"+ci+"'"
        # z=pd.read_sql_query(sq,mydb)
        # c1=z.values[0][0]
        # ua1=z.values[0][1]
        # msg=c1+' Our of '+ua1
        global_stop = True
        cam.release()
        cv2.destroyAllWindows()
        flash("Your answers submitted","warning")

    return render_template("view_exam.html")


@app.route('/exam_results')
def exam_results():
    # email=session.get('email')
    sql = "select * from exam_paper GROUP BY hh"
    x = pd.read_sql_query(sql, mydb)
    x = x.drop(['a', 'b', 'c', 'd', 'e', 'f', 'g'], axis=1)
    return render_template('exam_results.html', row_val=x.values.tolist())


@app.route('/exam_results_back/<s>/<s1>/<s2>')
def exam_results_back(s=0, s1="", s2=""):
    # sq="select results.sname,results.sid,results.semail,results.ename,results.edate,finalresults.ca, finalresults.ua,results.status from finalresults,results where finalresults.sid=results.sid and results.ename='" + s1 + "' and results.edate='" + s2 + "' LIMIT 1"
    sq = "select * from finalresults where ename='" + s1 + "' and edate='" + s2 + "'"
    x = pd.read_sql_query(sq, mydb)
    # print(x)
    # x = x.drop(['a', 'b', 'c', 'd', 'e', 'f', 'g'], axis=1)

    return render_template("exam_results1.html",row_val=x.values.tolist())

@app.route('/reply_mail/<s>/<s1>/<s2>/<s3>/<s4>')
def reply_mail(s=0, s1="", s2="",s3="",s4=""):
    if s4=="Fake":
        msg = 'Unknown person is authenticated so we are disconnecting you from exam terminal '
        t = 'Regards,'
        t1 = 'Online Student Authentication and Proctoring System.'
        mail_content = 'Dear student '  +','+'\n'+msg +'\n'+ '\n' + t + '\n' + t1
        sender_address = 'prasanthsai79@gmail.com'
        sender_pass = 'soxunjeybrvylqro'
        receiver_address = s2
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = 'Online Student Authentication System'
        message.attach(MIMEText(mail_content, 'plain'))
        ses = smtplib.SMTP('smtp.gmail.com', 587)
        ses.starttls()
        ses.login(sender_address, sender_pass)
        text = message.as_string()
        ses.sendmail(sender_address, receiver_address, text)
        ses.quit()
    else:
        msg = 'You are authenticated and you can view your results'
        t = 'Regards,'
        t1 = 'Online Student Authentication and Proctoring System.'
        mail_content = 'Dear ' + s + ',' + '\n' + msg + '\n' + '\n' + t + '\n' + t1
        sender_address = 'prasanthsai79@gmail.com'
        sender_pass = 'soxunjeybrvylqro'
        receiver_address = s2
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = 'Online Student Authentication System'
        message.attach(MIMEText(mail_content, 'plain'))
        ses = smtplib.SMTP('smtp.gmail.com', 587)
        ses.starttls()
        ses.login(sender_address, sender_pass)
        text = message.as_string()
        ses.sendmail(sender_address, receiver_address, text)
        ses.quit()
    return render_template("exam_results1.html")
@app.route('/view_result')
def view_result():
    sid=session.get('sid')

    # sq="select results.ename,results.edate,finalresults.ca, finalresults.ua from finalresults,results where finalresults.sid='"+str(sid)+"' and results.status='Real' LIMIT 1"
    sq = "select * from finalresults where sid='" + str(sid) + "'and  status='Real' "
    x = pd.read_sql_query(sq, mydb)
    # print(x)
    x = x.drop(['id', 'sid', 'semail', 'status'], axis=1)
    #
    return render_template("view_result.html", row_val=x.values.tolist())

if __name__ == '__main__':
    app.run(debug=True)
