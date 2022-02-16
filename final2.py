import mysql.connector
from sklearn import tree

#Get info from user
name=input('Enter your car model: ').strip()
mi=int(input('Enter your car mileage: ').strip())
ye=int(input('Enter the year of manufacture of your car: ').strip())

#2 list for info from database
x=[]
y=[]
#Connect to database
cnx = mysql.connector.connect(user='root', password='',
                              host='127.0.0.1',
                              database='learn')
cursor = cnx.cursor()
#Get the information you want from database
query='SELECT * FROM truecar WHERE model=\'%s\';'%name
cursor.execute(query)

#Add data to lists
for (id,model,price,miles,city,year) in cursor:
    x.append([miles,year])
    y.append(price)
#Machine learning
clf= tree.DecisionTreeClassifier()
clf=clf.fit(x,y)
new_data=[[mi,ye]]
answer=clf.predict(new_data)
print(answer[0])
