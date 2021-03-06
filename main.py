from bs4 import BeautifulSoup
import requests
import re
import http.cookiejar
import time
import os
import re
import sys
import urllib.parse

print("Name, Email")

# Set headers
headers = requests.utils.default_headers()
headers.update(
    {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})
# cookies = http.cookiejar.MozillaCookieJar('cookies.txt')
# cookies.load()


def get_domain(url):
    a = urllib.parse.urlsplit(url)
    return str(a.scheme) + "://" + str(a.hostname)


def get_urls(root):
    urls = []

    req = requests.get(root, headers)  # , cookies=cookies)
    soup = BeautifulSoup(req.content, 'html.parser')
    main = soup.find(
        ['div', 'ul', 'section'],
        class_=re.compile(
            'msl_organisation_list|view-uclu-societies-directory|atoz-container|listsocieties|block-og-menu')
    )

    for a in main.find_all('a', href=True):
        url = a['href']
        if url.startswith("/"):
            urls.append(domain + url)

        if url.startswith("https://society.tedu.edu"):
            urls.append(url)

    urls = list(dict.fromkeys(urls))
    return urls


try:
    root = sys.argv[1].strip().strip("\"")
    domain = get_domain(root)
except:
    print("error in unis.yml file")

if "studentsunionucl" in root:
    urls = []
    for i in range(16):
        urls += get_urls(root + "?page=" + str(i))
        time.sleep(0.3)

    urls = list(dict.fromkeys(urls))

else:
    urls = get_urls(root)

for url in urls:  # [urls[i] for i in range(5)]:
    req = requests.get(url, headers)  # , cookies=cookies)
    soup = BeautifulSoup(req.content, 'html.parser')
    try:
        if "cusu.co.uk" in root:
            name = soup.find('h2').find('a').text.strip().lower()
        else:
            name = soup.find('title').text.strip().lower()
        try:
            email = soup.find('a', class_=re.compile(
                "msl_email|socemail"))['href'][7:]
            if "infooffice.su@coventry.ac" in email:
                raise ValueError("Oh no")
        except:
            email_regex = "[A-Za-z0-9]+[\.\-_]?[A-Za-z0-9]+[@]\w+([.]\w{2,8})+"
            email = soup.find(string=lambda s:
                              re.search(email_regex, s) and not
                              re.search("contact@hertfordshire.su", s) and not
                              re.search("union.reception@aston.ac", s) and not
                              re.search("ctivities@brunel.ac", s) and not
                              re.search("infooffice.su@coventry.ac", s) and not
                              re.search("societies.su@coventry.ac", s) and not
                              re.search("studentsunion@nottingham.ac", s) and not
                              re.search("studentsunion@cardiff.ac.uk", s) and not
                              re.search("union@imperial.ac.uk", s) and not
                              re.search("societies@roehampton.ac", s)
                              )
            reg = re.compile(
                "(" + email_regex + ")")
            email = str(reg.findall(email)[0][0])

        name = name.replace("&", " and ")
        name = name.replace(",", "")
        name = name.replace("  ", " ")
        name = name.replace("   ", " ")
        name = name.replace(" | hertfordshire students' union", "")
        name = name.replace(" | coventry university students' union", "")
        name = name.replace(" | clubs and societies | students' union ucl", "")
        name = name.replace(" | imperial college union", "")
        name = name.replace(" | ted üniversitesi", "")
        name = name.strip()
        name = name.title()

        print(name + ", " + email)

    except:  # Exception as e:
        # print(e)
        pass

    time.sleep(0.1)
