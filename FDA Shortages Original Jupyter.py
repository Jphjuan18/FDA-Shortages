from bs4 import BeautifulSoup as bs
import requests as req
import pandas as pd
import re
 
res = req.get('https://www.accessdata.fda.gov/scripts/drugshortages/')

B_URL = 'https://www.accessdata.fda.gov/scripts/drugshortages/'

soup = bs(res.content)
divs = soup.find_all(['tbody'])
divs = divs[0].find_all('tr')
print(type(soup))
print(type(divs))
print(len(divs))

status_l = []
count = 0
while count < len(divs):
    for i in divs[count].find_all('strong'):
        status_l.append(i)
        count += 1
       # print('------------')
        #print(i)
        #print(test)
        #print('-----------')
        #print(type(i))

status_f = []
for i in status_l:
    w = i.string.strip()
    #print(i)
    status_f.append(w)

href_l = []
title_l = []
count = 0
subcount = 0
while count < len(divs):
    for i in divs[count].find_all('a'):
            i.find_all('a')
            href = i.get('href')
            href_l.append(href)
            title = i.get('title')
            title_l.append(title)
            subcount +=1
    if subcount == 2:
            subcount = 0
            count += 1

href_f = []
for i in range(1,len(divs)*2,2):
    words = href_l[i].split(' ')
    wordsjoin = '%20'.join(words)
    href_f.append(wordsjoin)
    #print(wordsjoin)
    #print(i)

S_URL = 'https://www.accessdata.fda.gov/scripts/drugshortages/'
 
href_link = []
for i in href_f: 
    href_link.append(S_URL + i)

title_f = []
for i in range(1,len(divs)*2,2):
    q = title_l[i]
    w = q.replace(' detail', '')
    title_f.append(re.sub('Link to ', '', w))   

subs = {'Drug': [], 'Link':[],'Status':[]}    
#Create a new dataframe
sub_df = pd.DataFrame(subs, columns=['Drug','Link','Status'])

######## Importing to MySQL ########
import pymysql

# Connect to the database
cnx = pymysql.connect(host='localhost',
                         user='root',
                         password='01181999',
                         db='fda')
# create cursor
cursor=cnx.cursor()
#cnx.close()

db_Info = cnx.get_server_info()
print(db_Info)
#cursor.execute("CREATE TABLE shortages (Drug VARCHAR(255), Link VARCHAR(255), Status VARCHAR(255))")
#cursor.execute("ALTER TABLE shortages ADD PRIMARY KEY (Drug)")

#cursor.execute('DESCRIBE shortages')
#for x in cursor:
#   print(x)

# creating column list for insertion
cols = "`,`".join([str(i) for i in sub_df[0:21].columns.tolist()])

# Insert DataFrame recrds one by one.
for i,row in sub_df[0:21].iterrows():
    sql = "INSERT INTO `shortages` (`" +cols + "`) VALUES (" + "%s,"*(len(row)-1) + "%s)"
    cursor.execute(sql, tuple(row))
    #print(sql)
    #print(row)

    # the connection is not autocommitted by default, so we must commit to save our changes
    cnx.commit()

cnx.close()
#cursor.execute("SELECT * FROM shortages WHERE Status = 'resolved'")
#for x in cursor:
#    print(x)

#cursor.execute("DELETE FROM shortages WHERE Status = 'Resolved'")
#cnx.commit()