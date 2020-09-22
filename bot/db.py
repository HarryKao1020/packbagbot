import sqlite3


def setTname(data):
 	connection = sqlite3.connect('db/test.db')
 	c = connection.cursor()
 	c.execute('insert into User(UserID, Tname) values (?,?)', data)
 	connection.commit()

def setCOUNTY(data):
	connection = sqlite3.connect('db/test.db')
	c = connection.cursor()
	c.execute('UPDATE User SET COUNTY = ? WHERE UserID LIKE? AND Tname LIKE?', data)
	connection.commit()

def setTYPE_one(data):
	print(type(data))
	connection = sqlite3.connect('db/test.db')
	c = connection.cursor()
	c.execute("UPDATE User SET TYPE_one = ? WHERE UserID LIKE? AND Tname LIKE?",data)
	connection.commit()

def setTYPE_two(data):
	connection = sqlite3.connect('db/test.db')
	c = connection.cursor()
	c.execute("UPDATE User SET TYPE_two = ? WHERE UserID LIKE? AND Tname LIKE?",data)
	connection.commit()

def setTYPE_three(data):
	connection = sqlite3.connect('db/test.db')
	
	c = connection.cursor()
	c.execute("UPDATE User SET TYPE_three = ? WHERE UserID LIKE?  AND Tname LIKE?",data)
	connection.commit()

def setPlace(times,data): #data= [Place, UserID, Tname]
	connection = sqlite3.connect('db/test.db')
	c = connection.cursor()

	if times == 1:
		c.execute("UPDATE User SET Place = ? WHERE UserID LIKE?  AND Tname LIKE?",data)
		connection.commit()
	else:

		place = data.pop(0)

		c.execute("SELECT Place FROM User WHERE UserID LIKE? AND Tname LIKE?",data)
		places = c.fetchone()
		places = list(places)
		places = places [0]
		places = places + '$' + place
		data.insert(0,places)
		c.execute("UPDATE User SET Place = ? WHERE UserID LIKE?  AND Tname LIKE?",data)

	connection.commit()

def setPlacedetail(data):
	connection = sqlite3.connect('db/test.db')
	c = connection.cursor()
	c.execute('insert into Place(PlaceName, Address, Rating, Phone, Time) values (?,?,?,?,?)',data)
	connection.commit()




def getTYPE(data): #input list tsype
	connection = sqlite3.connect('db/test.db')
	c = connection.cursor()
	c.execute("SELECT TYPE_one, TYPE_two, TYPE_three FROM User WHERE UserID LIKE? AND Tname LIKE?",data)
	types = c.fetchone()
	return types #return is tunple type


def getCOUNTY(data):
	connection = sqlite3.connect('db/test.db')
	c = connection.cursor()
	c.execute("SELECT COUNTY FROM User WHERE UserID LIKE? AND Tname LIKE?",data)
	county = c.fetchone()
	return county

def getPLACE(data):
	connection = sqlite3.connect('db/test.db')
	c = connection.cursor()
	c.execute("SELECT Place FROM User WHERE UserID LIKE? AND Tname LIKE?",data)
	place = c.fetchone()
	place = place[0]
	places = place.split('$')
	return places


def getPlaceDetail(data):
	connection = sqlite3.connect('db/test.db')
	c = connection.cursor()
	c.execute("SELECT Address, Rating, Phone, Time FROM Place WHERE PlaceName LIKE? ",data)
	PlaceDetail = c.fetchone()

	return PlaceDetail

def getTnames(data):
	connection = sqlite3.connect('db/test.db')
	c = connection.cursor()
	c.execute("SELECT Tname FROM User WHERE UserID LIKE? ",data)
	Tnames = c.fetchall()

	return Tnames



def Deleterecord(ID):
	connection = sqlite3.connect('db/test.db')
	c = connection.cursor()
	c.execute("DELETE FROM User WHERE UserID LIKE? ",ID)
	connection.commit()

data = ['永康商圈']
detail = getPlaceDetail(data)
for a in detail:
	print(a)