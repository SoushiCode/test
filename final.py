import requests
from bs4 import BeautifulSoup
import re
import mysql.connector

#Connect to database
cnx = mysql.connector.connect(user='root', password='',
                              host='127.0.0.1',
                              database='learn')
cursor=cnx.cursor()

#Lists for inputs
model_list=[]
price_list=[]
miles_list=[]
city_list=[]
year_list=[]
#Get inputs from the website
name=input("Car brand: ").strip()
for i in range (1,27):
    r=requests.get("https://www.truecar.com/used-cars-for-sale/listings/%s/location-schenectady-ny/?page=%i" %(name,i))
    soup=BeautifulSoup(r.text,'html.parser')
    model=soup.find_all('span',attrs={'class':'vehicle-header-make-model text-truncate'})
    price=soup.find_all('div', attrs={'class':'heading-3 margin-y-1 font-weight-bold'})
    miles=soup.find_all('div',attrs={'data-test':'vehicleMileage'})
    city=soup.find_all('div',attrs={'data-test':'vehicleCardLocation'})
    year=soup.find_all('span',attrs={'class':'vehicle-card-year font-size-1'})
#Currect the types and put them in their lists
    for once in model:
        model_list.append(once.text)
    for second in price:
        temp=re.sub(r"\$", "", second.text).strip()
        temp=int(re.sub(r"\,", "", temp).strip())
        price_list.append(temp)
    for third in miles:
        temp2=re.sub(r"miles", "", third.text).strip()
        temp2=int(re.sub(r"\,", "", temp2).strip())
        miles_list.append(temp2)
    for fourth in city:
        city_list.append(fourth.text)
    for fifth in year:
        year_list.append(int(fifth.text))


#Send data to database
for i in range (0,500):
    cursor.execute('INSERT INTO truecar VALUES(id,\'%s\', \'%i\',\'%i\',\'%s\', \'%i\')' % (model_list[i],price_list[i],miles_list[i],city_list[i],year_list[i]))
    cnx.commit()
#Delete duplicate items
cursor.execute('DELETE t1 FROM truecar t1 INNER JOIN truecar t2 WHERE t1.id < t2.id AND t1.model = t2.model AND t1.price = t2.price AND t1.miles = t2.miles AND t1.city = t2.city AND t1.year = t2.year')
cnx.commit()


cnx.close()
