"""MIT License
Copyright (c) 2019 Rishi Tiku
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights 
to use the Software only, subject to the following conditions:
1. The code shall not be redistributed commercially by anyone other than the Copyright owner.
2. The user shall not copy/paste or modify the code and publish it him/herself in any way 
   without the prior permission of the Copyright holder.
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""

import json
import codecs
import sys
import os

print("""Enter the time zone of your country here.
Example: For INDIA time is +05:30 hours ahead of GMT.
         Check the time zone of your country with the +/- sign included.\n\t\t\t*****\n""")
tzhh = int(input('Enter the HOURS part of YOUR Time Zone in hh format.\nPlease include the +/- sign.\nExample: For +05:30(+hh:mm) as for INDIA, Enter \"+05\" here.\n\t>>>'))
tzmm = int(input('Enter the MINUTES part YOUR Time Zone in mm format.\nExample: For +05:30(+hh:mm) as for INDIA, Enter \"30\" here.\n\t>>>'))
#tzhh = +05
#tzmm = 30

username = str(input('Enter Your Instagram Username here!!! Please enter correctly.\n\t>>>')) #gets your Instagram username here in string format
#username = 'rishi.tiku' #My username, if you wish to, replace your username here, remove the '#' in front of this line and put a '#' in front of previous line. 


filename = "messages.json" #if editing this, specify either the full file location here or just keep the file in the same folder as this script.

def st(t):
    if int(t)<10:
        string = "0"+str(t)
        return string
    else:
        return str(t)

def createDir(dir_name):
    try:    
        os.mkdir(dir_name)
        return True;
    except:
        return False

def folderExists(dir_name):
    ct=0
    while(True):
            if(os.path.exists(dir_name)):
                break
            else:
                check = createDir(username)
                if(check):
                    break
                else:
                    if(ct==3):
                        print('Unable to Create Folder')
                        sys.exit()
                    ct+=1

def fileExists(string):
    counter = 0
    while(1):
                try:
                    if(counter == 0):    
                        f = open(os.path.join(username, "{}.txt".format(string)), 'r', encoding = 'utf-8-sig')
                    else:
                        f = open(os.path.join(username, "{} - {}.txt".format(string,counter)), 'r', encoding = 'utf-8-sig')
                    f.close()
                except FileNotFoundError:
                    return counter
                counter+=1

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
    previous=""
    current=""
    checked = False
    Name = False
    for participants in data:
        p = participants['participants']
        previous=''
        if(not(checked)):
            for i in p:
                if(i==username):
                    Name = True
            checked = True
            if(Name):
                createDir(username)
            else:
                print('The Instagram username you entered is incorrect. Please try again!')
                sys.exit()
            folderExists(username)
        if(len(p)==2):
            if(p[0]==username):
                value = 1
            elif(p[1] == username):
                value = 0
            else:
                print('The instagram username you entered is wrong. Try again or maybe change the username argument in source code.')
                sys.exit()
            result = fileExists(p[value])
            if(result == 0):
                f = open(os.path.join(username, "{}.txt".format(p[value])), 'w', encoding = 'utf-8-sig')
            elif(result>=1):
                f = open(os.path.join(username, "{} - {}.txt".format(p[value],result)), 'w', encoding = 'utf-8-sig')
            for sender in reversed(participants['conversation']):
                dtime =  sender['created_at']
                date = dtime[0:10].replace("-" , "/")
                time = dtime[11:19]
                Time()
                if(sender['sender']!= None):
                    current = sender['sender']
                else:
                    current = 'Anonymous'
                if(previous!=current and previous!=''):
                    f.write('\n')
                previous=current
                f.write(date)
                f.write(", ")
                f.write(time)
                f.write(" - ")
                f.write(current)
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
            f = open(os.path.join(username, "Group{}.txt".format(ctr)),"w", encoding='utf-8-sig')
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
                if(sender['sender']!= None):
                    current = sender['sender']
                else:
                    current = 'Anonymous'
                if(previous!=current and previous!=''):
                    f.write('\n')
                previous=current
                f.write(date)
                f.write(", ")
                f.write(time)
                f.write(" - ")
                f.write(current)
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
                if(previous!=current):
                    f.write('\n')
                previous=current

            ctr = ctr + 1
        else:
            f = open(os.path.join(username, "AnonymousPerson{}.txt".format(count)),"w", encoding='utf-8-sig')
            for sender in reversed(participants['conversation']):
                dtime =  sender['created_at']
                date = dtime[0:10].replace("-" , "/")
                time = dtime[11:19]
                Time()
                if(sender['sender']!= None):
                    current = sender['sender']
                else:
                    current = 'Anonymous'
                if(previous!=current and previous!=''):
                    f.write('\n')
                previous=current
                f.write(date)
                f.write(", ")
                f.write(time)
                f.write(" - ")
                f.write(current)
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
                if(previous!=current):
                    f.write('\n')
                previous=current
                count += 1
        f.close()
    print('All Done Correctly. Enjoy!!!')
