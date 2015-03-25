import psycopg2
import getpass

class dataSource:
    #Initialize the object to be a full list of the data in database in descending order of rating
    def __init__(self):
        self.list = []
        try:
            connection = psycopg2.connect(database="gux", user="gux", password="purr789propane")
        except Exception, e:
            print 'Connection error: ', e
            exit()
        cursor = connection.cursor()
        query = 'SELECT name, address, postcode, tel, neighborhood, website, cuisine, price, rating, deliver, takeout  FROM minneapolisrestaurant WHERE postcode > 0 ORDER BY rating DESC'
        cursor.execute(query)
        for row in cursor.fetchall():
           self.list.append(row)

        connection.close()

    #Return a full list of all the restaurants
    def getAll(self, resList):
        allRes = []
        if len(resList) == 0:           
            for row in self.list:
                allRes.append(row)
        else:
            for row in resList:
                allRes.append(row)
        return allRes

    #Return a list of all the restaurants in descending order of price
    def sortPrice(self):
        list = []
        try:
            connection = psycopg2.connect(database="gux", user="gux", password="purr789propane")
        except Exception, e:
            print 'Connection error: ', e
            exit()
        cursor = connection.cursor()
        query1 = 'SELECT name, address, postcode, tel, neighborhood, website, cuisine, price, rating, deliver, takeout  FROM minneapolisrestaurant WHERE postcode > 0 ORDER BY price ASC'
        cursor.execute(query1)
        for row in cursor.fetchall():
           list.append(row)
        connection.close()
        return list

    #Search in self.list for restaurants with the given cuisine category and return a list of all such restaurants' information
    def getResOfCuisine(self, category,listRes):
        list = []
        for row in listRes:
            for item in row[6].split(","):
                if category in item:
                    list.append(row)
                    continue
        return list

    #Search in the given list for restaurants with certain price and return a list of all such restaurants' information
    def getResOfPrice(self, category,listRes):
        list = []
        for row in listRes:
            if category == row[7]:
                list.append(row)
                continue
        return list

    #Search in the given list for restaurants in one neighbourhood and return a list of all such restaurants' information
    def getResOfNbh(self, category,listRes):
        list = []
        for row in listRes:
            if category in row[4]:
                list.append(row)
            continue
        return list

    #split the keyword into single words and call the searchKeyword function recursively
    def splitKeyword(self, keyword,listRes):
        list = listRes
        bestRes = False
        keys = keyword.split(",")
        for key in keys:
            if "best" in key:
                bestRes = True
            else:
                list = self.searchKeyword(key, list)
        if bestRes == True:
            list = self.getBest(list)
        return list

    #search one keyword in a given list and return a list of restaurants that contain the keywords in their information
    def searchKeyword(self, keyword,listRes):
        list = []
        for row in listRes:
            for item in row:
                try:
                    if keyword in item:                       
                        list.append(row)
                    elif keyword in item.split(","):
                        list.append(row)
                except Exception, e: #when item is a number
                    if keyword == item:
                        list.append(row)
        return list

    #return a list of no more than 10 restaurants which are the top rating ones in the given list
    def getBest(self, listRes):
        list = listRes
        if len(list) < 10:
            return list
        else:
            return list[:10]

    
