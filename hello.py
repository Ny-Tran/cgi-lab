#!/usr/bin/env python3
import os, sys
import json
import templates, secret

# print('Content-Type: application/json') # HTTP header, tells browser what file we're sending
# print() # new line to print and show up in curl in between the header & content 
# print(json.dumps(dict(os.environ), indent=2))

print('Content-Type: text/html')

show_login_page = True

# get all cookies and parse until we find the login cookie-key
cookie_data = os.environ.get("HTTP_COOKIE", 0)
if cookie_data:
    for cookies in cookie_data.split("; "):
        cookie_key = cookies.split("=")[0]
        if cookie_key == "login":
            print()
            print(templates.secret_page(secret.username, secret.password))
            show_login_page = False

# show login form if not currently logged in
if show_login_page:
    posted_bytes = os.environ.get("CONTENT_LENGTH", 0)
    if posted_bytes:
        posted = sys.stdin.read(int(posted_bytes)).split("&")
        print(posted)
        # SOURCE: https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies accessed on Jan.28.2021
        if posted[0].split("=")[1] == secret.username and posted[1].split("=")[1] == secret.password:
            print(f"Set-Cookie: login={secret.username}&{secret.password}")
            print()
            print("Successfully logged in: Please refresh page")
        else:
            print()
            print("Unsuccessful login: bad information")

    print("""
    <!doctype html>
    <html>
    <body>
    """)

    print(templates.login_page())

    print("<h1>HELLO I AM HTML</h1>")
    print(f"<p> QUERY_STRING={os.environ['QUERY_STRING']} </p>")
    print("<ul>") #sends string to browser
    if os.environ['QUERY_STRING']:
        for param in os.environ['QUERY_STRING'].split('&'):
            (name, value) = param.split('=')
            print(f"<li><em>{name}</em> = {value}</li>")
        print("</ul>")

    print("""
    </body>
    </html>
    """)