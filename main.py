from flask import Flask,request,render_template,jsonify,redirect,url_for
import json
import mysql.connector
app=Flask(__name__)
class workshopTree:
   def __init__(self,data):
      self.data=data
      self.children=[]
      self.parent=None

   def Add_child(self,child):
      child.parent=self
      self.children.append(child)

@app.route('/')
def home():
   return render_template("index.html")

db_config={
   'host':'localhost',
   'user':'root',
   'password':'krishna@2510',
   'database':'workshop'
}
 
con= mysql.connector.connect(**db_config)
cursor=con.cursor()

@app.route('/run',methods=['POST','GET'])
def run():
      root =workshopTree("workshop")
      
      select_workshop=request.form.get('selectworkshop')
      select_college=request.form.get('selectcollege')

      if select_workshop is not None and select_college is not None:
       select_branch=request.form.get('selectbranch')
       select_name=request.form.get('StudentName')

       workshop=workshopTree(select_workshop)
       college=workshopTree(select_college)
       branch=workshopTree(select_branch)
       name=workshopTree(select_name)

       root.Add_child(workshop)
       workshop.Add_child(college)
       college.Add_child(branch)
       branch.Add_child(name) 

      if request.method=='POST':
        workshop_name=request.form.get('selectworkshop')
        college_name=request.form.get('selectcollege')
        branch_name=request.form.get('selectbranch')
        Name=request.form.get('StudentName')

        cursor.execute("INSERT INTO Data (workshop,college,branch,name) VALUES (%s,%s,%s,%s)", (workshop_name,college_name,branch_name,Name))
        con.commit()
        
      return redirect(url_for('home'))
@app.route('/data',methods=['GET'])
def getdata():
   Data=[]
   with open('workshop.txt','r',encoding='ISO-8859-1') as file:
      for line in file:
         values=line.strip().split(':')
         if len(values)==4:
          workshop,college,branch,StudentName=values
          Data.append({
            'workshop':workshop,
            'college': college,
            'branch':branch,
            'StudentName':StudentName
          })
         else:
           print(f'skinping this line:{line}')
      

   return jsonify(Data=Data)
@app.route('/stat',methods=['POST','GET'])
def statforcollege():
   with open('workshop.txt','r',encoding='ISO-8859-1') as f:
    workshops={
       'photography':0,
       'ethical hacking':0,
       'robotic':0
     }
    for lines in f:
         values=lines.strip().split(':')
         if len(values)==4:
          workshop,college,branch,StudentName=values
          if workshop in workshops:
             workshops[workshop]+=1
      
          result=[{'workshop': workshop, 'noofstudent': count} for workshop, count in workshops.items()]  
    
   return jsonify(result) 

@app.route('/stat2',methods=['POST','GET'])   
def statforcollege2():
   with open('workshop.txt','r',encoding='ISO-8859-1')  as f:
      Data2={}
      for lines in f:
         value=lines.strip().split(':')
         if len(value)==4:
           workshop,college,branch,StudentName=value
           if workshop not in Data2:
             Data2[workshop]={}
           if college in Data2[workshop]:
               Data2[workshop][college]+=1
           else:
               Data2[workshop][college]=1
          
         
      return jsonify(Data2)
if __name__=='__main__':
   app.run(debug=True)