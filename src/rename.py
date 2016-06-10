# coding: UTF-8
import sys
dic = {}

for s in open("../input/test.bib", "r"):
    s.strip()
    if s.find("@") != -1:
        if s.find("inproceedings") != -1:
            dic["type"] = "inproceedings"
            dic["type"].strip()
    elif s.find("{") != -1 and s.find("}") != -1:
        key = s[0:s.find("=")].strip()
        dic[key] = s[s.find("{")+1:s.find("}")]

if dic["booktitle"].find("Humanoid") != -1 and dic["booktitle"].find("Conference"):
    dic["booktitle"] = "Known:Humanoids" # あとでこれをキーにして色々な表現で出力

names = dic["author"].split("and");
for i in range(len(names)):
    names[i] = names[i].strip() # "Bolanowski Jr, Stanley J"は、論文の苗字として省略しないところとするところを明示しているので良い。日本人も同じく。
reference = ""
if names[0].find(",") != -1:
    index = names[0].find(",")
    reference += names[0][0:index]
reference += dic["year"];

title_ws = dic["title"].replace("-", "").replace(":", "").replace("\"", "").replace("\'", "").replace("!", "").replace("?", "").split(" ")
for i in range(len(title_ws)):
    reference += title_ws[i].strip().capitalize()
dic["reference"] = reference

# print
numbering = [
        "reference",
        "title",
        "author",
        "year",
        "journal",
        "volume",
        "number",
        "pages",
        "booktitle",
        "publisher",
        "organization",
        "url",
        "note"
]

sys.stdout.write("|")
for i in range(20):
    if (i < len(numbering)):
        a = dic.get(numbering[i])
        if a != None:
            print a,
    sys.stdout.write("|")
sys.stdout.write("\n")
