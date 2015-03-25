#!/usr/bin/python


import cgi

def printFileAsPlainText(fileName):
    ''' Prints to standard output the contents of the specified file, preceded
        by a "Content-type: text/plain" HTTP header.
    '''
    text = ''
    try:
        f = open(fileName)
        text = f.read()
        f.close()
    except Exception, e:
        pass

    print 'Content-type: text/plain\r\n\r\n',
    print text

if __name__ == '__main__':
    # Not going to allow people to view just anything.
    allowedFiles = (
        'showsource.py',
        'dataSource.py',
        'index.py',
        'queryp.html',
        'tinywebapp.html',
        'createtable.sql'
        'readme.html',
        'ajax-sample.py',
        'jqplot-sample.py',
        'json-sample.py',
        'cookies.py',
    )

    # Really. Don't trust the user.
    form = cgi.FieldStorage()
    sourceFileName = 'showsource.py'
    if 'source' in form:
        sourceFileName = form['source'].value
    if sourceFileName not in allowedFiles:
        sourceFileName = 'showsource.py'

    # Print the file in question.
    printFileAsPlainText(sourceFileName)


