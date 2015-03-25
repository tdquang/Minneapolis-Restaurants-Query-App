#!/usr/bin/python
# CS 257 WEProject
#

import cgi
import sys
import os
import os.path
from decimal import *
from dataSource import dataSource

def sanitizeUserInput(s):
    charsToRemove = ';\\/:\'"<>@'
    for ch in charsToRemove:
        s = s.replace(ch, '')
    return s

# get parameters from user input
def getCGIParameters():
    form = cgi.FieldStorage()
    parameters = {'keyword':'' , 'cuisine':'' , 'price':'' , 'neighbourhood':'' , 'showsource':'', 'submit':'', 'sort':''} 
    
    if 'keyword' in form:
        parameters['keyword'] = sanitizeUserInput(form['keyword'].value)
    if 'cuisine' in form:
        parameters['cuisine'] = form['cuisine'].value
    if 'price' in form:
        parameters['price'] = int(form['price'].value)
    if 'neighbourhood' in form:
        parameters['neighbourhood'] =  form['neighbourhood'].value
    if 'submit' in form:
        parameters['submit'] = "search"
    if 'sort' in form:
        parameters['sort'] = int(form['sort'].value)
    return parameters

# Takes the user input, if the user pressed "submit", go to query page. If not, print the main page. Uses the template to print pages.
def printMainPageAsHTML(keyword, cuisine, price, neighbourhood, submit, query, sort, templateFileName):
    if submit is 'search':
        printQueryPageAsHTML(keyword, cuisine, price, neighbourhood, query, sort, 'queryp.html')
    
    outputText = ''
    
    links = '<br><br><a href="showsource.py?source=index.py">index.py source</a><br>\n'
    links += '<a href="showsource.py?source=dataSource.py">dataSource.py source</a><br>\n'
    links += '<a href="showsource.py?source=%s">%s source</a><br>\n' % (templateFileName, templateFileName)
    links += '<a href="readme.html">README</a><br>\n'
    links += '<a href="showsource.py?source=showsource.py">the script we use for showing source</a>\n'
       
    try:
        f = open(templateFileName)

        templateText = f.read()

        f.close()
        outputText = templateText % (keyword, links)

    except Exception, e:
        outputText = 'Cannot read template file "%s".' % (templateFileName)

    
    print 'Content-type: text/html\r\n\r\n',
    print outputText

        
# Takes the user input and prints the query page accordingly. 
def printQueryPageAsHTML(keyword, cuisine, price, neighbourhood, query, sort, templateFileName):
    result = ''
    price2 = ''
    if price is not '':
        for i in range(price):
            price2 += '$'
    sortStr = ''
    if sort == 1:
        sortStr = 'price'
    else:
        sortStr = 'rating'
    report = '<p>You typed in %s to search in categories %s, %s, %s sorted by %s.</p>' % (keyword, cuisine, price2, neighbourhood, sortStr)
    for restaurant in query:
        result += '<div class="ex"><p>'
        result += '<h1 style="margin-bottom:0;">'
        result += restaurant[0]
        result += '</h1>'
        result += '<p class="info"><br>' + "Price: " + str(restaurant[7]) + '       Rating: ' + str(restaurant[8]) + '<br>' + restaurant[1] + '<br>' + 'Minneapolis, MN,'+ '&nbsp;' + str(restaurant[2])  #+ '</div>'
        result += '<br>' + str(restaurant[3])
        result += '<br>' + 'Deliver: ' + str(restaurant[9]) + '         Take-out: ' + str(restaurant[10])
        result += '<br>' + '<a href="' + str(restaurant[5]) + '" target="_blank">Go to Website</a>' 
        result += '</p></p></div>'
        

    links = '<br><br><a href="showsource.py?source=index.py">index.py source</a><br>\n'
    links += '<a href="showsource.py?source=dataSource.py">dataSource.py source</a><br>\n'
    links += '<a href="showsource.py?source=%s">%s source</a><br>\n' % (templateFileName, templateFileName)
    links += '<a href="showsource.py?source=readme.html">README</a><br>\n'
    links += '<a href="showsource.py?source=showsource.py">the script we use for showing source</a>\n'
    

    outputText = ''
    try:
        f = open(templateFileName)

        templateText = f.read()

        f.close()

        outputText = templateText % (report,len(query),result,links)

    except Exception, e:
        outputText = 'Cannot read template file "%s".' % (templateFileName)
        print e

    print 'Content-type: text/html\r\n\r\n',
    print outputText
    sys.exit(0)
    
#filter the restaurant according to the input and search for keyword in the filted list, return a list of matched restaurants' information
def filterSearch(parameters):
    list = dataSource()
    newList = []
    # If parameter sort is 1, get the list sorted by price. Else, gets the list sorted by rating(default).
    if parameters['sort'] == 1:
        newList = list.sortPrice()
    # Initialize all the lists passed to the filter functions to be the complete list sorted by certain order
    cuisine = list.getAll(newList)
    price = list.getAll(newList)
    nbh = list.getAll(newList)
    keyw = []
    # Gets the list sorted by rating 
    if len(newList) == 0:
        newList = list.getAll([])
    # Check if each input is empty or not, call the functions accordingly. Update the lists being passed to the next function(s).
    if parameters['cuisine'] is not "":
        cuisine = list.getResOfCuisine(parameters['cuisine'], newList)
        price = cuisine
        nbh = cuisine        
    if parameters['price'] is not "":
        price = list.getResOfPrice(parameters['price'], cuisine)
        nbh = price
    if parameters['neighbourhood'] is not "":
        nbh = list.getResOfNbh(parameters['neighbourhood'], price)
    if parameters['keyword'] is not "":
        keyw = list.splitKeyword(parameters['keyword'], nbh)
        return keyw
    else:
        return nbh
        

def main():
    parameters = getCGIParameters()
    query = filterSearch(parameters)
    printMainPageAsHTML(parameters['keyword'],parameters['cuisine'],parameters['price'],parameters['neighbourhood'],parameters['submit'], query, parameters['sort'], 'tinywebapp.html')
        
    
     
if __name__ == '__main__':
    main()
