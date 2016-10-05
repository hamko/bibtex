# coding: UTF-8
import sys
import os
import re
import glob
import common

def constructCSVLine(dic):
    ret = ""
    ret += "|"
    for i in range(20):
        if (i < len(common.numbering)):
            a = dic.get(common.numbering[i])
            if a != None:
                ret += a
        ret += "|"
    ret += "\n"
    return ret

def stripTitle(title):
    prohibit = ["+","#","$","%","&","^","@","(",")","-",":","|","\"","\'","!","?","/",",",".","―","'","’",",","\t","\n"]
#    print title
    for c in prohibit:
        title = title.replace(c, "")
#    print title
    title_ws = title.split(" ")
    reference = ""
    for i in range(len(title_ws)):
        reference += title_ws[i].strip().capitalize()
#    print reference
    return reference


fnames = []
fnames += glob.glob("../input/*.bib")
fnames += glob.glob("../input/*.txt")
fnames.sort()
f = open("bibtex.csv","w")
for fname in fnames:
    dic = {}
    basename = fname[fname.rfind("/")+1:fname.rfind(".")]
    if basename.isdigit():
        dic["id"] = basename
    else:
        i = 0
        dic["id"] = ""
        while basename[i].isdigit():
            dic["id"] += basename[i]
            i = i + 1
        if dic["id"] == "":
            print "skipped, wrong file name:\n    "+fname
            continue;
            
        
    for s in open(fname, "r"):
        s.strip()
        if len(s) == 1:
            continue;
        if s.find("@") != -1:
            if re.compile("inproceedings",re.IGNORECASE).search(s) != None:
                dic["type"] = "inproceedings"
            elif re.compile("article",re.IGNORECASE).search(s) != None:
                dic["type"] = "article"
            elif re.compile("book",re.IGNORECASE).search(s) != None:
                dic["type"] = "book"
            elif re.compile("techreport",re.IGNORECASE).search(s) != None:
                ref = dic["id"] + s[s.find("{")+1:s.find(",")].strip()
                os.rename(fname, "../input/"+ref+".bib")
                dic["type"] = "techreport"
            elif re.compile("misc",re.IGNORECASE).search(s) != None:
                ref = dic["id"] + s[s.find("{")+1:s.find(",")].strip()
                os.rename(fname, "../input/"+ref+".bib")
                dic["type"] = "misc"
        else:
            if s.find("{{") != -1 and s.rfind("}}") != -1:
                key = s[0:s.find("=")].strip().lower()
                dic[key] = s[s.find("{{")+2:s.rfind("}}")]
            elif s.find("{") != -1 and s.rfind("}") != -1:
                key = s[0:s.find("=")].strip().lower()
                dic[key] = s[s.find("{")+1:s.rfind("}")]
            elif s.find("\"") != -1:
                key = s[0:s.find("=")].strip().lower()
                dic[key] = s[s.find("\"")+1:s.rfind("\"")]
            elif s.find("=") != -1: # 区切りなしで最後に,
                key = s[0:s.find("=")].strip().lower()
                dic[key] = s[s.find("=")+1:s.find(",")].strip()
            elif s.strip().find("}") != -1:
                pass
            else:
                print s
                print "Unknown syntax:\n    "+fname
                sys.exit(1)


    if not dic.has_key("type"):
        print "Unknown type:\n    "+fname
        continue

    if dic["type"] == "misc":
        dic["reference"] = dic["id"] + stripTitle(dic["title"])
        f.write(constructCSVLine(dic))
        continue;
    if dic["type"] == "techreport":
        dic["reference"] = dic["id"] + stripTitle(dic["title"])
        f.write(constructCSVLine(dic))
        continue;
    elif dic["type"] == "article":
        needed = ["id", "title", "year", "pages", "journal"] # , "volume"
        NG = 0
        for key in needed:
            if not dic.has_key(key):
                print "Lacking for "+ key +":\n    "+fname
                NG = 1
                break
        if NG:
            continue;
    elif dic["type"] == "proceedings":
        needed = ["id", "title", "year", "pages", "booktitle"]
        NG = 0
        for key in needed:
            if not dic.has_key(key):
                print "Lacking for "+ key +":\n    "+fname
                NG = 1
                break
        if NG:
            continue;
    elif dic["type"] == "book":
        needed = ["id", "title", "year", "publisher"]
        NG = 0
        for key in needed:
            if not dic.has_key(key):
                print "Lacking for "+ key +":\n    "+fname
                NG = 1
                break
        if NG:
            continue;

#    print "OK:\n    "+fname


    # Knownの自動検出
    if dic["type"] == "proceedings":
        if dic["booktitle"].find("Humanoid") != -1 and dic["booktitle"].find("Conference") != -1 and dic["booktitle"].find("International") != -1:
            dic["booktitle"] = "Known:Humanoids" # あとでこれをキーにして色々な表現で出力
#    elif dic["type"] == "article":
#        if dic["journal"].find("") != -1 and dic["journal"].find("Conference"):
#            dic["journal"] = "Known:Humanoids" # あとでこれをキーにして色々な表現で出力

    names = dic["author"].split("and");
    for i in range(len(names)):
        names[i] = names[i].strip() # "Bolanowski Jr, Stanley J"は、論文の苗字として省略しないところとするところを明示しているので良い。日本人も同じく。
    reference = dic["id"]
    commaname = names[0].split(",")
    toshow = commaname[0]
    toshow = toshow.strip().replace(" ", "").replace("\t", "").replace("\n", "").replace("\r", "");

    reference += toshow
    reference += dic["year"].strip();
    
    reference += stripTitle(dic["title"])
    dic["reference"] = reference

    os.rename(fname, "../input/"+reference+".bib")

    f.write(constructCSVLine(dic))

f.close()

