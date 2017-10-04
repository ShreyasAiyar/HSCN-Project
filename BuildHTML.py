import socket
import os

def getHTML():
    cwd = os.getcwd()

    list1 = os.listdir(cwd + '/Files')
    print(list1)
    str2 = ""
    for i in list1:
        str2 += '<p><a>' +i + '</a></p>'

    str1 = """
    <!DOCTYPE html>
    <html>
        <head>
            <style>
                h1{ text-align: center; font-size: 50px;}
                p{ text-align: center; font-size: 25px;}
                a{ text-align: center; font-size: 25px;}
                </style>
            <title>File Server</title>
        </head>
        <body>
            <h1>File Server Application</h1>
            """  + str(str2) + """ 
        </body>
    </html>"""
    return str1

print(getHTML())
