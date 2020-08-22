import sys
import os
from flask import Flask, render_template, Response, flash, request, redirect, url_for, send_from_directory, Markup,make_response,jsonify
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

test=None
students=None
student_scores=None
stu_scor_dict={}
stu_per_dict={}
# Score Card Analysis
def scorCard(reportcard):
	test=pd.read_excel(reportcard)
	students=test['Student No'].unique()
	student_scores=[]
	from scipy.stats import percentileofscore
	for student in students:
		student_scores.append(test[test['Student No']==student]['Your score'].sum())   

	for student in students:
		stu_scor_dict[student]=test[test['Student No']==student]['Your score'].sum()
		stu_per_dict[student]=percentileofscore(student_scores,stu_scor_dict[student],kind='strict')
		'''print(stu_scor_dict[student],' And ',stu_per_dict[student])
		'''
		fig=plt.figure()
		timebar=plt.bar(test[test['Student No']==student]['Question No.'], test[test['Student No']==student]['Time Spent on question (sec)'])
		plt.title('Time (sec)')
		plt.xlabel('Questions')
		plt.ylabel('Time')
		plt.legend([timebar],['Time'])
		plt.savefig('static/img/time/'+str(student)+'.png')
		plt.close(fig)

		fig=plt.figure()
		colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue','red']
		plt.pie(test[test['Student No']==student]['Time Spent on question (sec)'],labels=test[test['Student No']==student]['Question No.'], colors=colors,autopct='%1.1f%%', shadow=True, startangle=180)
		plt.title('Time Spent on question (sec)')
		plt.legend()
		plt.savefig('static/img/timespent/'+str(student)+'.png')
		plt.close(fig)

		fig=plt.figure()
		stu=test[test['Student No']==student]
		attempted=stu['Attempt status']=="Attempted"
		attempted=attempted.sum()
		Unattempted=stu['Attempt status']=="Unattempted"
		Unattempted=Unattempted.sum()
		attemotlist=[attempted,Unattempted]
		plt.pie(attemotlist,autopct='%1.1f%%', shadow=True, startangle=180)
		plt.title('Attempts')
		plt.legend(["Attempted","Unattempted"])
		plt.savefig('static/img/attempt/'+str(student)+'.png')
		plt.close(fig)

		fig=plt.figure()
		attempted=stu[stu['Attempt status']=="Attempted"]
		Correct=attempted['Outcome (Correct/Incorrect/Not Attempted)']=='Correct'
		Incorrect=attempted['Outcome (Correct/Incorrect/Not Attempted)']=='Incorrect'
		Correct=Correct.sum()
		Incorrect=Incorrect.sum()
		#print(Correct," ",Incorrect)
		correctionlist=[Correct,Incorrect]
		plt.pie(correctionlist,autopct='%1.1f%%', shadow=True, startangle=180)
		plt.title('Accuracy From Attempted Questions')
		plt.legend(["Correct","Incorrect"])
		plt.savefig('static/img/accuracy/'+str(student)+'.png')
		plt.close(fig)
		fig=plt.figure()

		outcome=stu['Outcome (Correct/Incorrect/Not Attempted)']
		Unattempted=outcome[:]=='Unattempted'
		Unattempted=Unattempted.sum()
		correctionlist=[Correct,Incorrect,Unattempted]
		plt.pie(correctionlist,autopct='%1.1f%%', shadow=True, startangle=180)
		plt.title('Overall performamnce against test')
		plt.legend(["Correct","Incorrect","Unattempted"])
		plt.savefig('static/img/performance/'+str(student)+'.png')
		plt.close(fig)





# initialize a flask object
app = Flask(__name__)
stulist=[]
count=0
excel=False
# root
@app.route("/",methods=['GET','POST'])
def test():
	global excel
	global questions
	global stu_scor_dict
	global stu_per_dict
	global stulist
	global count
	# Get Request of Next Page
	if request.method == 'POST':
		if request.values.get('count') !=None:
			if int(request.values.get('count'))<9:
				count=count+1
			else:
				count=0

		elif request.files['excel']!=None:
			report_file=request.files['excel']
			print(report_file)
			report_file.save(report_file.filename)
			scorCard(report_file.filename) 
			excel=True
			

	if excel:
		print(count)
		stulist=[0,1,2,3,4,5,6,7,8,9]
		picdir=os.listdir('static/Pics')
		accuracydir=os.listdir('static/img/accuracy')
		attemptdir=os.listdir('static/img/attempt')
		performancedir=os.listdir('static/img/performance')
		timedir=os.listdir('static/img/time')
		timespentdir=os.listdir('static/img/timespent')

		accuracy_imgs=[]
		attempt_imgs=[]
		performance_imgs=[]
		time_imgs=[]
		timespent_imgs=[]
		pics=[]

		# Get Images
		for img in picdir:
			if img.endswith(".jpg"):
				pics.append(img)
		checkname=os.path.splitext((pics[count])[0])
		'''print(checkname[0])'''
		stu_score=stu_scor_dict[int(checkname[0])]
		stu_per=stu_per_dict[int(checkname[0])]
		student_no=int(checkname[0])
		testread=pd.read_excel('Test_Report.xlsx')
		Name=testread[testread['Student No']==student_no]['Name of Candidate'].tolist()
		Grade=testread[testread['Student No']==student_no]['Grade'].tolist()
		school=testread[testread['Student No']==student_no]['Name of school'].tolist()
		City=testread[testread['Student No']==student_no]['City of Residence'].tolist()
		Country=testread[testread['Student No']==student_no]['Country of Residence'].tolist()
		Registration=testread[testread['Student No']==student_no]['Registration'].tolist()
		Gender=testread[testread['Student No']==student_no]['Gender'].tolist()
		Birth=testread[testread['Student No']==student_no]['Date of Birth'].tolist()
		testdate=testread[testread['Student No']==student_no]['Date and time of test'].tolist()
		assistance=testread[testread['Student No']==student_no]['Extra time assistance'].tolist()
		can_details=[Name,Grade,school,City,Country,Registration,Gender,Birth,testdate,assistance]

		questions=testread[testread['Student No']==student_no]['Question No.'].tolist()

		times=testread[testread['Student No']==student_no]['Time Spent on question (sec)'].tolist()
		cscores=testread[testread['Student No']==student_no]['Score if correct'].tolist()
		inscore=testread[testread['Student No']==student_no]['Score if incorrect'].tolist()
		astatus=testread[testread['Student No']==student_no]['Attempt status'].tolist()
		wmarked=testread[testread['Student No']==student_no]['What you marked'].tolist()
		canswer=testread[testread['Student No']==student_no]['Correct Answer'].tolist()
		outcia=testread[testread['Student No']==student_no]['Outcome (Correct/Incorrect/Not Attempted)'].tolist()
		yscore=testread[testread['Student No']==student_no]['Your score'].tolist()

		recorddetails=[times,cscores,inscore,astatus,wmarked,canswer,outcia,yscore]

		pdfrender= render_template('card.html',can_details=can_details,recorddetails=recorddetails,questions=questions,pics=pics,count=count,stu_score=stu_score,stu_per=stu_per,graphimg=checkname[0]+'.png',excel=excel)
		'''print(pics[count],':',accuracy_imgs[count])'''
		return pdfrender
	else:
		pdfrender= render_template('card.html',excel=excel)
		return pdfrender
		




if __name__=="__main__":
	app.run(port='8000', debug=True)