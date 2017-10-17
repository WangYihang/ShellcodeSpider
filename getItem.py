#!/usr/bin/env python
# encoding:utf-8

import requests
import bs4
import time
import sys
import os

def getType(soup):
    result = ""
    return result

def getCode(soup):
    result = soup.find("pre").text
    return result

def getAuthor(soup):
    result = soup.findAll(attrs={"name":"author"})[0]["content"]
    return result

def getDescribe(soup):
    result = soup.findAll(attrs={"name":"description"})[0]["content"]
    return result

def getTitle(soup):
    result = soup.title.string
    return result

def save(path, content):
    codefile = open(path, 'w')
    codefile.write(content.encode("UTF-8"))
    codefile.close()

def formate(filename):
    filename = filename.replace(" ","_")
    filename = filename.replace("[","_")
    filename = filename.replace("]","_")
    filename = filename.replace("(","_")
    filename = filename.replace(")","_")
    filename = filename.replace("/","_")
    filename = filename.replace("\\","_")
    filename = filename.replace("{","_")
    filename = filename.replace("}","_")
    filename = filename.replace(".","_")
    filename = filename.replace("\"","_")
    filename = filename.replace(">","_")
    filename = filename.replace("<","_")
    filename = filename.replace("'","_")
    if filename.endswith("_"):
        filename = filename[:-1]
    return filename

def compile(path):
    command = "gcc -g -fno-stack-protector -z execstack " + path + " -o " + path[:-2] + ".out"
    os.system(command)

def commit(comment):
    command = "git add ."
    os.system(command)
    command = "git commit -m \"" + comment + "\""
    print command
    os.system(command)

def run(url, pages_type):
    headers = {
            "Host" : "www.exploit-db.com",
            "User-Agent" : "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0",
            "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language" : "en-US,en;q=0.5",
            "Accept-Encoding" : "gzip, deflate, br",
            "Connection" : "keep-alive",
            "Upgrade-Insecure-Requests" : "1",
            "Pragma" : "no-cache",
            "Cache-Control" : "no-cache"
    }

    response = requests.get(url, headers=headers)
    content = response.text.encode("UTF-8")
    soup = bs4.BeautifulSoup(content, "html.parser")

    dirname = getDescribe(soup)
    dirname = formate(dirname)
    dirname = pages_type + "/" + dirname
    file_content = getCode(soup)
    # print "Making dir : %s" % (dirname)
    try:
        os.makedirs(dirname)
    except Exception as e:
        print e
    filename = "shellcode.c"
    path = dirname + "/" + filename
    save(path, file_content)
    comment = getDescribe(soup).replace("\"","")
    # print "Comment : %s" % (comment)
    commit(comment)
    # print "Compiling..."
    # compile(dirname + "/" + filename)

def main():
    url = "https://www.exploit-db.com/exploits/39617/"
    pages_type = "Lin_x86" # 指定类型 主要为了确定要将文件保存在哪儿
    # url = sys.argv[1] # 第一个参数指定 url
    # pages_type = sys.argv[2] # 指定类型 主要为了确定要将文件保存在哪儿
    run(url, pages_type)

if __name__ == "__main__":
    main()
