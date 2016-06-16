# coding: UTF-8
 
import common
import sys
import re
 
f = "bibtex.csv"

# formal
outFile = open("bibtex_formal.bib","w")
for line in open(f, "r"):
    tmp = line.split("|")
    outFile.write("@"+tmp[2]+"{"+tmp[3]+",\n")
    # author
    i = 4
    word = common.numbering[i] 
    if word != "":
        outFile.write("    " + word + "={" + tmp[i+1] + "},\n")

    # journal
    i = 6
    word = common.numbering[i] 
    if word != "":
        outFile.write("    " + word + "={" + tmp[i+1] + "},\n")

    # booktitle
    i = 10
    word = common.numbering[i] 
    if word != "":
        outFile.write("    " + word + "={" + tmp[i+1] + "},\n")

    # others
    for i in range(len(common.numbering)):
        if tmp[i+1] == "":
            continue
        word = common.numbering[i] 
        if word == "volume" or word == "number" or word == "pages" or word == "year" or word == "url" or word == "organization" or word == "title":
            outFile.write("    " + word + "={" + tmp[i+1] + "},\n")
    outFile.write("}\n\n")
outFile.close()


# formal
knownConferenceShort = {
        "Known:ICRA" : "ICRA",
        "Known:ICAR" : "ICAR",
        "Known:IROS" : "IROS",
        "Known:Humanoids" : "HUMANOIDS",
}
knownConferenceFormal = {
        "Known:ICRA" : "International Conference on Robotics and Automation",
        "Known:ICAR" : "International Conference on Advanced Robotics",
        "Known:IROS" : "International Conference on Intelligent Robots and Systems",
        "Known:Humanoids" : "International Conference on Humanoid Robots",
}



knownConference = knownConferenceFormal
outFile = open("bibtex_formal.bib","w")
for line in open(f, "r"):
    tmp = line.split("|")
    outFile.write("@"+tmp[2]+"{"+tmp[3]+",\n")
    # author
    i = 4
    word = common.numbering[i] 
    if tmp[i+1] != "":
        outFile.write("    " + word + "={" + tmp[i+1] + "},\n")

    # journal
    i = 6
    word = common.numbering[i] 
    if tmp[i+1] != "":
        outFile.write("    " + word + "={" + tmp[i+1] + "},\n")

    # booktitle
    i = 10
    word = common.numbering[i] 
    if tmp[i+1] != "":
        if knownConference.has_key(tmp[i+1]):
            outFile.write("    " + word + "={" + knownConference[tmp[i+1]] + "},\n")
        else:
            outFile.write("    " + word + "={" + tmp[i+1] + "},\n")

    # others
    for i in range(len(common.numbering)):
        if tmp[i+1] == "":
            continue
        word = common.numbering[i] 
        if word == "volume" or word == "number" or word == "pages" or word == "year" or word == "url" or word == "organization" or word == "title":
            outFile.write("    " + word + "={" + tmp[i+1] + "},\n")
    outFile.write("}\n\n")
outFile.close()




knownConference = knownConferenceShort
outFile = open("bibtex_short.bib","w")
for line in open(f, "r"):
    tmp = line.split("|")
    outFile.write("@"+tmp[2]+"{"+tmp[3]+",\n")
    # author
    i = 4
    word = common.numbering[i] 
    if tmp[i+1] != "":
        outFile.write("    " + word + "={" + tmp[i+1] + "},\n")

    # journal
    i = 6
    word = common.numbering[i] 
    if tmp[i+1] != "":
        outFile.write("    " + word + "={" + tmp[i+1] + "},\n")

    # booktitle
    i = 10
    word = common.numbering[i] 
    if tmp[i+1] != "":
        if knownConference.has_key(tmp[i+1]):
            outFile.write("    " + word + "={" + knownConference[tmp[i+1]] + "},\n")
        else:
            outFile.write("    " + word + "={" + tmp[i+1] + "},\n")

    # others
    for i in range(len(common.numbering)):
        if tmp[i+1] == "":
            continue
        word = common.numbering[i] 
        if word == "volume" or word == "number" or word == "pages" or word == "year" or word == "url" or word == "organization" or word == "title":
            outFile.write("    " + word + "={" + tmp[i+1] + "},\n")
    outFile.write("}\n\n")
outFile.close()
