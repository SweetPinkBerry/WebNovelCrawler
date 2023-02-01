#!/urs/bin/env python

import sys
import os
import requests as req
from bs4 import BeautifulSoup
import re
from unidecode import unidecode
import pathlib

def main(args):
    get_chapters(args[1], args[2])


def get_chapters(url, filename):
    r = req.Session()
    r.headers.update({"User-Agent":"Mozilla/5.0"})
    chapters = get_chapter_links(url, r)

    if ".txt" in filename:
        create_textfile(url, chapters, r, filename)

    elif ".html" in filename:
        create_html_folder(filename, r, chapters)

    else:
        print("Needs: link to fastnovel.net front page and filename.txt or .html")


def get_chapter_links(url, session):
    r = session.get(url)
    assert r.status_code==200

    chapter_links = []

    soup = BeautifulSoup(r.text, "html.parser")
    chapters = soup.find("div",{"id":"list-chapters"})
    chapters = chapters.find_all("li")
    for ch in chapters:
        ch = ch.find("a")
        regex_url = re.findall(r'(https:\/\/[^\/]*)', url)
        ch_url = regex_url[0] + ch["href"]
        chapter_links.append(ch_url)
    return chapter_links


def create_textfile(url, filename, r, chapters):
    f = open(filename, "a+")
    f.write("Link: " + url + "\n\n\n")
    f.close()
    for ch in chapters:
        get_chapter_content(ch, r, filename, "text")


def write_to_txt(file, title, lines):
    f = open(file, "a+")
    f.write(unidecode(title.text) + "\n\n\n")
    for p in lines:
        f.write(unidecode(p.text) + "\n\n")
    f.write("\n_________________________________________________________________________\n\n\n\n")
    f.close()


def get_chapter_content(url, session, file, form, ch_num=None, directory=None):
    r = session.get(url)
    assert r.status_code==200

    soup = BeautifulSoup(r.content, "html.parser")
    title = soup.find("h1",{"class":"episode-name"})
    body = soup.find("div",{"id":"chapter-body"})
    lines = body.find_all("p")

    if form == "text":
        write_to_txt(file, title, lines)
    if form == "html":
        create_html_chapter(ch_num, directory, title, lines)

    return unidecode(title.text)


def create_html_folder(filename, r, chapters):
    name = filename.split(".")
    sub_dir = name[0] + "/chapters/"
    try:
        os.makedirs(sub_dir)
    except OSError:
        print("Creation of directories failed:", sub_dir)
        print("Could it already exist?")
        exit()

    write_to_folder(sub_dir, name[0], filename, r, chapters)


def write_to_folder(sub_dir, name, filename, r, chapters):
    file_path = name + "/index.html"

    f = open(file_path, "a+")
    f.write("<!DOCTYPE html>")
    f.write("<html><head><title>" + name[0] + " - index" + "</title>")

    #f.write(<link href="stylesheet.css" noe mer her>)

    f.write("</head><body>") #Lager index fil her, så hvert kapittel kan legge til seg
    
    f.close()

    add_chapters_to_folder(file_path, chapters, r, filename, sub_dir)

    f = open(file_path, "a")
    f.write("</body></html>") #Avslutter ikke filen før alt har blitt lagt til
    f.close()


def add_chapters_to_folder(index, chapters, r, filename, sub_dir):
    titles = []

    for i in range(len(chapters)): #0-3126 iirc
        titles.append(get_chapter_content(chapters[i], r, filename, "html", (i+1), sub_dir))

        ch = sub_dir + str(i+1) + ".html"
        prev = str(i) + ".html"
        nex = str(i+2) + ".html"
        x = open(ch, "a")
        if i > 0:
            x.write("<a href=" + prev + ">Previous</a>")
        if i < (len(chapters) - 1):
            x.write("<a href=" + nex + ">Next</a>")
        x.close()

        #add_chapters_to_dropdown(index, i, ch_i, len(chapters))

        if i == 9:
            break #test med bare første kapittelet

    for t in titles:
        print(t)


def create_css():
    pass


def add_chapters_to_dropdown(index, ch_len):
    pass
    


def create_html_chapter(ch_num, directory, title, lines):
    filename = directory + str(ch_num) + ".html"
    f = open(filename, "a+")

    f.write("<!DOCTYPE html>")
    f.write("<html><head><title>" + unidecode(title.text) + "</title></head><body>")

    f.write(unidecode(str(title)))
    for p in lines:
        f.write(unidecode(str(p)))

    f.write("</body></html>")
    f.close()
    
    #adds link to index file, remove after making add:chapters work, since I get the titles
    dir_i = directory.split("/")
    index_file = dir_i[0] + "/index.html"
    f = open(index_file, "a")
    f.write("<li><a href=chapters/" + str(ch_num) + ".html>" + unidecode(title.text) + "</a></li>")
    f.close()


if __name__ == "__main__":
    main(sys.argv)