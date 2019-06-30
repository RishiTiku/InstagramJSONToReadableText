import json
import codecs
import sys

'''Put the hour part of the time zone of your country (with sign +/-) in tzhh and minute part in tzmm.
(eg for +5:30, put +5 in tzhh and 30 in tzmm)'''
tzhh = +5
tzmm = 30

username = str(print('Enter Your Instagram Username here!!! Please enter correctly.')) #gets your Instagram username here in string format
filename = "messages.json" #if editing this, specify either the full file location here or just keep the file in the same folder as this script.

def st(t):
    if int(t)<10:
        string = "0"+str(t)
        return string
    else:
        return str(t)

    

def Date():
    global date
    yy = int(date[0:4])
    mm = int(date[5:7])
    dd = int(date[8:10])
    dd = dd + 1
    day31 = {1,3,5,7,8,10,12}
    if mm in day31:
        if(int(dd/31)==1):
            mm = mm + 1
            dd = dd%31
    elif(mm == 2):
        if(yy%4==0):
            if(yy%100==0):
                if(yy%400==0):
                    feb = 29
                else:
                    feb = 28
            else:
                feb = 29
        else:
            feb = 28
        if(int(dd/feb)==1):
            mm = mm + 1
            dd = dd%feb
    else:
        if(int(dd/30)==1):
            mm = mm + 1
            dd = dd%30
    if(int(mm%12)==1):
        yy = yy+1
        mm = mm%12
            
    test = st(dd)+"/"+ st(mm)+"/"+ st(yy)
    date = test



def Time():
    global time
    hh = int(time[0:2])
    mm = int(time[3:5])
    ss = int(time[6:8])
    hh = hh + tzhh
    mm = mm + tzmm
    string = " "
    if mm/60>=1:
        hh += 1
        mm = mm%60
    if(int(hh/24)==1):
        Date()
        hh = hh%24
        string = "AM"
    elif(int(hh/12)==1):
        hh = hh%12
        string = "PM"
    elif(int(hh/12)==0):
        string = "AM"
    test = st(hh)+":"+st(mm)+":"+st(ss)+string
    time = test



with codecs.open(filename, encoding = 'utf-8-sig', errors = 'ignore') as f:
    data = json.load(f)
    global date
    global time
    global ctr
    global count
    ctr = 1
    count = 1
    for participants in data:
        p = participants['participants']
        if(len(p)==2):
            if(p[0]==username):
                value = 1
            elif(p[1] == username):
                value = 0
            else:
                print('The instagram username you entered is wrong. Try again or maybe change the username argument in source code.')
                sys.exit()
            f = open("{}.txt".format(p[value]),"w", encoding = 'utf-8-sig')
            for sender in reversed(participants['conversation']):
                dtime =  sender['created_at']
                date = dtime[0:10].replace("-" , "/")
                time = dtime[11:19]
                Time()
                f.write(date)
                f.write(", ")
                f.write(time)
                f.write(" - ")
                if(sender['sender']!= None):
                    f.write(sender['sender'])    
                else:
                    f.write("Anonymous")
                f.write(": ")
                if('story_share' in sender):
                    f.write("<replied to story>")
                if('text' in sender):
                    if(sender['text']!= None):
                        f.write(sender['text'])
                elif('heart' in sender):
                    f.write('<Heart omitted>')
                else:
                    f.write("<Media omitted>")
                    if('media_share_url' in sender):
                        f.write('<link = ')
                        f.write(sender['media_share_url'])
                        f.write('>')
                f.write('\n')
        elif(len(p)>2):
            f = open("Group{}.txt".format(ctr),"w", encoding='utf-8-sig')
            for i in p:
                f.write(i)
                if i != p[-1]:
                    f.write(" , ")
                else:
                    f.write("\n\n\n")
            for sender in reversed(participants['conversation']):
                dtime =  sender['created_at']
                date = dtime[0:10].replace("-" , "/")
                time = dtime[11:19]
                Time()
                f.write(date)
                f.write(", ")
                f.write(time)
                f.write(" - ")
                if(sender['sender']!= None):
                    f.write(sender['sender'])    
                else:
                    f.write("Anonymous")
                f.write(": ")
                if('story_share' in sender):
                    f.write("<replied to story>")
                if('text' in sender):
                    if(sender['text']!= None):
                        f.write(sender['text'])
                elif('heart' in sender):
                    f.write('<Heart omitted>')
                else:
                    f.write("<Media omitted>")
                    if('media_share_url' in sender):
                        f.write('<link = ')
                        f.write(sender['media_share_url'])
                        f.write('>')
                f.write('\n')

            ctr = ctr + 1
        else:
            f = open("AnonymousPerson{}.txt".format(count),"w", encoding='utf-8-sig')
            for sender in reversed(participants['conversation']):
                dtime =  sender['created_at']
                date = dtime[0:10].replace("-" , "/")
                time = dtime[11:19]
                Time()
                f.write(date)
                f.write(", ")
                f.write(time)
                f.write(" - ")
                if(sender['sender']!= None):
                    f.write(sender['sender'])    
                else:
                    f.write("Anonymous")
                f.write(": ")
                if('story_share' in sender):
                    f.write("<replied to story>")
                if('text' in sender):
                    if(sender['text']!= None):
                        f.write(sender['text'])
                elif('heart' in sender):
                    f.write('<Heart omitted>')
                else:
                    f.write("<Media omitted>")
                    if('media_share_url' in sender):
                        f.write('<link = ')
                        f.write(sender['media_share_url'])
                        f.write('>')
                f.write('\n')
                count += 1
        f.close()
