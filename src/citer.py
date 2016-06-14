# coding: UTF-8
 
import sys
import re
 
argvs = sys.argv  # コマンドライン引数を格納したリストの取得
argc = len(argvs) # 引数の個数
# デバッグプリント
if (argc != 2):   # 引数が足りない場合は、その旨を表示
    print 'Usage: # python %s input.tex' % argvs[0]
    quit()         # プログラムの終了


idtoref = {}
 

f = "bibtex.csv"
for line in open(f, "r"):
    tmp = line.split("|")
    id_ = tmp[1]
    ref_ = tmp[3]
    idtoref[id_] = ref_

outFile = open("out.tex","w")
linenum = 0
for s in open(argvs[1], "r"):
    linenum += 1
    l = 0
    while True: 
        l_ = s[l:len(s)-1].find("[") 
        r_ = s[l:len(s)-1].find("]") 
        if l_ == -1 or r_ == -1:
            break
        l = r_ + 1
        cites = s[l_+1:r_]
        if re.match("[a-zA-Z]", cites) != None:
            continue

        cites_array = cites.split(",")
        for i in range(len(cites_array)):
            cites_array[i] = cites_array[i].strip()

        error_not_yet_added_citation_number = 0
        for i in range(len(cites_array)):
            tef = 0
            for key, value in idtoref.iteritems():
                if cites_array[i] == key:
                    tef = 1;
            if tef == 0:
                error_not_yet_added_citation_number = 1
                sys.stderr.write("Citation number not found (line "+str(linenum)+"): "+cites_array[i]+"\n")
                break
        if error_not_yet_added_citation_number == 1:
            continue

        newcites = "\\cite{"
        for i in range(len(cites_array)):
            for key, value in idtoref.iteritems():
                if cites_array[i] == key:
                    newcites += value
                    if i != len(cites_array)-1:
                        newcites += ", "
                    break
        newcites += "}"

        s = s.replace(s[l_:r_+1], newcites)
    outFile.write(s)

outFile.close()
