# coding=utf-8
import socket
import httplib
import urllib
import os
import sys

HOST = '127.0.0.1'
PORT = 8080


def getMimeType(requesting_file):
    " Returns The MimeType Of the Given Request File. Mime Type indicates whether file is image or text etc. This is used by the browser to detect the content type "
    #filename,file_extension = os.path.splitext(requesting_file)
    # filename.lstrip('/') # We Remove the Slash in order to extract the file name
    if (requesting_file.endswith('png')):
        return 'image/png'
    elif(requesting_file.endswith('jpg')):
        return 'image/jpg'
    elif(requesting_file.endswith('mp4')):
        return 'video/mp4'
    else:
        return 'text/html'


def getContent(requesting_file):
    "Returns The Content Of The Given File. A text File would return text"
    requesting_file = requesting_file.lstrip('127.0.0.1:8080/')
    if requesting_file == '':
        return html
    else:
        file1 = open(requesting_file, 'r')
        return file1.read()


def getHTML():
    file_list = os.listdir(os.getcwd())
    file_list_html = ""

    for i in file_list:
        file_list_html += '<p><a href="/' + i + '"' + '>' + i + '</a></p>'

    return """
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
            """ + str(file_list_html) + """
        </body>
    </html>"""


def run_server():
    os.chdir(os.getcwd() + 'files')

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((HOST, PORT))
    server_sock.listen(5)
    print("Listening for connections on port {1}".format(PORT))

    while True:
        client_sock, client_addr = server_sock.accept()
        pid = os.fork()
        if pid == 0:
            html = getHTML()
            browser_info = client_sock.recv(1024).decode('utf-8')
            string_list = browser_info.split(' ')
            requesting_file = string_list[1]
            mimeType = getMimeType(requesting_file)
            content = getContent(requesting_file)
            header = "HTTP/1.1 200 OK\n"
            size_of_content = sys.getsizeof(content)
            if sys.getsizeof(content) > 1024:
                # Sendall is a socket send function which continously sends
                client_sock.sendall(header.encode(
                    'utf-8') + 'Content-Type:' + mimeType + '\n\n' + content)
            else:
                client_sock.send(header.encode('utf-8') +
                                 'Content-Type:' + mimeType + '\n\n' + content)
            client_sock.close()
        else:
            print


if __name__ == '__main__':
    run_server()
