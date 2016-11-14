
# coding: utf-8

# In[17]:
#Data of top 100 movies from imdb website is scrapped using selenium 
#and added to the sql database using python sql connector
import requests
from selenium import webdriver
from sets import Set
import mysql.connector

#Link for the top 100 movies on imdb.com
resp = requests.get('http://www.imdb.com/list/ls055592025/')
jj= resp.text.split('class="image"')


# In[18]:

ll =[]
for each in jj:
	ll.append(each.split('/title/')[1].split('/')[0])
#from urllib.request import urlopen
cast=[]
movies=[]
m_director=[]
m_location=[]
m_language=[]
m_country=[]
persons=Set()
country=Set()

#function for retreiving data for a movie from the webpage
def getdata(url,movieID):	
	mov={}
	mov['MID']=movieID
	driver = webdriver.Chrome("/home/rj/Documents/chromedriver")
	driver.get(url)
	elements = driver.find_elements_by_class_name("title_wrapper")
	rows = elements[0].find_elements_by_tag_name("h1")[0].text;
	mov['genre'] = elements[0].find_elements_by_class_name("itemprop")[0].text
	mov['time'] = elements[0].find_elements_by_tag_name('time')[0].text
	mov['name']=rows
	year = rows.split('(')[1].split(')')[0]
	mov['year']=year
	rating1 = driver.find_elements_by_class_name("ratingValue")[0].find_elements_by_css_selector("strong")[0].get_attribute("title")
	rat = rating1.split(' ')[0]
	votes = rating1.split(' ')[3]
	mov['rating']=rat
	mov['votes']=votes
	mdir=driver.find_elements_by_class_name("plot_summary_wrapper")[0].find_elements_by_class_name("credit_summary_item")[0].find_elements_by_tag_name("a")[0].text
	m_director.append([movieID,mdir])
	cast1 = driver.find_elements_by_class_name("cast_list")[0].find_elements_by_css_selector("a")
	for each in cast1:
		x = each.get_attribute("href")
		v = x.split('/')[4]
		if v[0]=='c':
			continue
		persons.add(v)
		cast.append([movieID,v])

	details = driver.find_elements_by_id("titleDetails")[0].find_elements_by_class_name("txt-block")
	ab = {}
	for each in details:
		try :
			hw = each.find_elements_by_tag_name("h4")[0].text
			val = each.find_elements_by_tag_name("a")[0].text
			ab[hw] = val
		except :
			break
	m_country.append([movieID,ab['Country:']])
	m_location.append([movieID,ab['Filming Locations:']])
	m_language.append([movieID,ab['Language:']])
	movies.append(mov)
	driver.close()


try:
    #Retreiving data for top 100 movies
    for (i,each) in enumerate(ll):
        getdata('http://www.imdb.com/title/'+each,each)
except:
    print "hello"


cnx = mysql.connector.connect(host='localhost',database='myimdb',user='root',password='random1234')




# In[33]:

cnx = mysql.connector.connect(host='localhost',database='myimdb',user='root',password='random1234')
cursor = cnx.cursor()


# In[21]:
#Filling up movie entity into database 
for each in movies:
   
   add_session = ("INSERT INTO Movie "
                          "(MID,title,year,rating,num_votes) "
                          "VALUES(%s, %s, %s, %s, %s) ")
   session_data = (each['MID'],each['name'],each['year'],each['rating'],each['votes'])
           
   try:
      # Execute the SQL command
      cursor.execute(add_session,session_data)
      # Commit your changes in the database
      cnx.commit()
   except Exception as e:
       print("Error in Session Insert",e)
       # Rollback in case there is any error
       cnx.rollback()


# In[30]:
#Filling up m_director and director entity into database 
dd = {}
for i,each in enumerate(m_director):
    index =0
    if each[1] in dd:
        index = dd[each[1]]
    else :
        x = int(1000000)+int(i)
        s1 = "nm"+str(x)

        add_session = ("INSERT INTO Person "
                               "(PID,Name,DOB,Gender) "
                               "VALUES(%s, %s, %s, %s) ")
        session_data = (s1,each[1],"1968-01-01","male")
        try:
            # Execute the SQL command
            cursor.execute(add_session,session_data)
            index = s1
            dd[each[1]]= s1
            # Commit your changes in the database
            cnx.commit()
        except Exception as e:
            print("Error in Session Insert",e)
            # Rollback in case there is any error
            cnx.rollback()
            index = -1
    if index ==-1 :
        continue
    add_session = ("INSERT INTO M_Director "
                               "(ID,MID,PID) "
                               "VALUES(%s, %s, %s) ")
    session_data = (i+1,each[0],index)
    try:
        # Execute the SQL command
        cursor.execute(add_session,session_data)
        # Commit your changes in the database
        cnx.commit()
    except Exception as e:
        print("Error in Session Insert",e)
        # Rollback in case there is any error
        cnx.rollback()
    


# In[35]:
#Filling up m_location and location entity into database 

dd = {}
for i,each in enumerate(m_location):
    index =0
    if each[1] in dd:
        index = dd[each[1]]
    else :
        x = int(1000000)+int(i)
        s1 = x

        add_session = ("INSERT INTO Location"
                               "(LID,Name) "
                               "VALUES(%s, %s) ")
        session_data = (s1,each[1])
        try:
            # Execute the SQL command
            cursor.execute(add_session,session_data)
            index = s1
            dd[each[1]]= s1
            # Commit your changes in the database
            cnx.commit()
        except Exception as e:
            print("Error in Session Insert",e)
            # Rollback in case there is any error
            cnx.rollback()
            index = -1
    if index ==-1 :
        continue
    add_session = ("INSERT INTO M_Location "
                               "(ID,MID,LID) "
                               "VALUES(%s, %s, %s) ")
    session_data = (i+1,each[0],index)
    try:
        # Execute the SQL command
        cursor.execute(add_session,session_data)
        # Commit your changes in the database
        cnx.commit()
    except Exception as e:
        print("Error in Session Insert",e)
        # Rollback in case there is any error
        cnx.rollback()
    


# In[38]:
#Filling up m_genre and genre entity into database 

dd = {}
for i,each in enumerate(movies):
    index =0
    if each['genre'] in dd:
        index = dd[each['genre']]
    else :
        x = int(1000000)+int(i)
        s1 = x

        add_session = ("INSERT INTO Genre"
                               "(GID,Name) "
                               "VALUES(%s, %s) ")
        session_data = (s1,each['genre'])
        try:
            # Execute the SQL command
            cursor.execute(add_session,session_data)
            index = s1
            dd[each['genre']]= s1
            # Commit your changes in the database
            cnx.commit()
        except Exception as e:
            print("Error in Session Insert",e)
            # Rollback in case there is any error
            cnx.rollback()
            index = -1
    if index ==-1 :
        continue
    add_session = ("INSERT INTO M_Genre "
                               "(ID,MID,GID) "
                               "VALUES(%s, %s, %s) ")
    session_data = (i+1,each['MID'],index)
    try:
        # Execute the SQL command
        cursor.execute(add_session,session_data)
        # Commit your changes in the database
        cnx.commit()
    except Exception as e:
        print("Error in Session Insert",e)
        # Rollback in case there is any error
        cnx.rollback()
    


# In[42]:
#Filling up m_cast into database 

for i,each in enumerate(cast):
    add_session = ("INSERT INTO M_Cast"
                               "(ID,MID,PID) "
                               "VALUES(%s, %s, %s) ")
    session_data = (i+1,each[0],each[1])
    try:
        # Execute the SQL command
        cursor.execute(add_session,session_data)
        
        # Commit your changes in the database
        cnx.commit()
    except Exception as e:
        print("Error in Session Insert",e)
        # Rollback in case there is any error
        cnx.rollback()



# In[43]:
#Filling up m_language and language entity into database 

dd = {}
for i,each in enumerate(m_language):
    index =0
    if each[1] in dd:
        index = dd[each[1]]
    else :
        x = int(1000000)+int(i)
        s1 = x

        add_session = ("INSERT INTO Language"
                               "(LAID,Name) "
                               "VALUES(%s, %s) ")
        session_data = (s1,each[1])
        try:
            # Execute the SQL command
            cursor.execute(add_session,session_data)
            index = s1
            dd[each[1]]= s1
            # Commit your changes in the database
            cnx.commit()
        except Exception as e:
            print("Error in Session Insert",e)
            # Rollback in case there is any error
            cnx.rollback()
            index = -1
    if index ==-1 :
        continue
    add_session = ("INSERT INTO M_Language "
                               "(ID,MID,LAID) "
                               "VALUES(%s, %s, %s) ")
    session_data = (i+1,each[0],index)
    try:
        # Execute the SQL command
        cursor.execute(add_session,session_data)
        # Commit your changes in the database
        cnx.commit()
    except Exception as e:
        print("Error in Session Insert",e)
        # Rollback in case there is any error
        cnx.rollback()
    


# In[46]:
#Filling up m_country and country into database 

dd = {}
for i,each in enumerate(m_country):
    index =0
    if each[1] in dd:
        index = dd[each[1]]
    else :
        x = int(1000000)+int(i)
        s1 = x

        add_session = ("INSERT INTO Country"
                               "(CID,Name) "
                               "VALUES(%s, %s) ")
        session_data = (s1,each[1])
        try:
            # Execute the SQL command
            cursor.execute(add_session,session_data)
            index = s1
            dd[each[1]]= s1
            # Commit your changes in the database
            cnx.commit()
        except Exception as e:
            print("Error in Session Insert",e)
            # Rollback in case there is any error
            cnx.rollback()
            index = -1
    if index ==-1 :
        continue
    add_session = ("INSERT INTO M_Country "
                               "(ID,MID,CID) "
                               "VALUES(%s, %s, %s) ")
    session_data = (i+1,each[0],index)
    try:
        # Execute the SQL command
        cursor.execute(add_session,session_data)
        # Commit your changes in the database
        cnx.commit()
    except Exception as e:
        print("Error in Session Insert",e)
        # Rollback in case there is any error
        cnx.rollback()


# In[48]:
#Retreiving and filling up person entity into database 

person_data=[]
def get_person_data(url,PID):
    try:
        urlname = url
        data = {}
        resp = requests.get(urlname)
        sitedata = resp.text
        data['PID'] = each
        data['name'] = sitedata.split('<h1 class="header"> <span class="itemprop" itemprop="name">')[1].split('<')[0]
        if '#actress' in sitedata:
            data['gender'] = 'female'
        if '#actor' in sitedata:
            data['gender'] = 'male'
        data['dob'] = sitedata.split('datetime="')[1].split('"')[0]
        person_data.append(data)
        add_session = ("INSERT INTO Person "
                           "(PID,Name,DOB,Gender) "
                           "VALUES(%s, %s, %s, %s) ")
        session_data = (PID,data['name'],data['dob'],data['gender'])
        try:
           # Execute the SQL command
           cursor.execute(add_session,session_data)
           # Commit your changes in the database
           cnx.commit()
        except Exception as e:
            print("Error in Session Insert",e)
            # Rollback in case there is any error
            cnx.rollback()
    except:
        return
try:
    for i,each in enumerate(persons):
        get_person_data('http://www.imdb.com/name/'+each,each)
        
except:
    print "hello2"

