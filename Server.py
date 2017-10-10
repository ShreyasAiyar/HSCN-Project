# coding=utf-8
import socket
import httplib
import urllib
import os

# Returns The MimeType Of the Given Request File. Mime Type indicates whether file is image or text etc. This is used by the browser
def getMimeType(requesting_file):
    filename,file_extension = os.path.splitext(requesting_file)
    filename.lstrip('/')
    if (requesting_file.endswith('png')):
        print(filename+"."+file_extension[1:])
        return filename+"."+file_extension[1:]
    else:
        return 'text/html'


# Returns The Content Of The Given File
def getContent(requesting_file):
    requesting_file = requesting_file.lstrip('/')
    if requesting_file == '':
        return html
    else:
        file1 = open(requesting_file,'r')
        return file1.read()

# This Will Get The HTML Dynamically
def getHTML():
    cwd = os.getcwd()
    list1 = os.listdir(cwd)
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


# Main Function In Python
if __name__ == '__main__':

    #file1 = open('Main.html','rb')
    #html = file1.read()

    cwd = os.getcwd()
    os.chdir(cwd + '/Files')

    server_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 8080
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((host,port))
    server_sock.listen(5)
    print("Listening For Connection .../")


    while True:
        html = getHTML()
        client_sock, client_addr = server_sock.accept()
        pid = os.fork()
        if(pid == 0):
            print("Got Connection From ", client_addr)
            browser_info = client_sock.recv(1024).decode('utf-8')
            string_list = browser_info.split(' ')
            requesting_file = string_list[1]
            print("Client Requesting File " + requesting_file) 
            mimeType = getMimeType(requesting_file)
            content = getContent(requesting_file)
            header = "HTTP/1.1 200 OK\n"
            client_sock.send(header.encode('utf-8') + 'Content-Type:' + mimeType + '\n\n' + content)
            client_sock.close()
        else:
            print
