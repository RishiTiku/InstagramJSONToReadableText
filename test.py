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

def Feb(yy):
    if(yy%4==0):
        if(yy%100==0):
            if(yy%400==0):
                leap = 1
            else:
                leap = 0
        else:
            leap = 1
    else:
        leap = 0

    if(leap==0):
        feb = 28
    else:
        feb = 29

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


def createDir(dir_name):
    try:    
        os.mkdir(dir_name)
        return True
    except:
        return False

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

def Pre(A):
    if(A<10):
        A = "0"+str(A)
    else:
        A = str(A)
    return A

def DateTime(date):
    global tzhh
    global tzmm
    yy = int(date[0:4])
    mn = int(date[5:7])
    dd = int(date[8:10])
    hh = int(date[11:13])
    mm = int(date[14:16])
    ss = int(date[17:19])
    day31 = {1,3,5,7,8,10,12}
    
    daytime=((hh*3600)+(mm*60)+ss)
    if(tzhh<0):
        tz = ((tzhh*3600)-(tzmm*60))
    else:
        tz = ((tzhh*3600)+(tzmm*60))
    left = daytime + tz
    if((left%86400)<43200):
        st = 'AM'
    else:
        st = 'PM'

    if(tzhh<0):        
        if(left<0):
            if(dd<=1):
                if(mn<=1):
                    yy -= 1
                    mn = 12
                    dd = 31
                else:
                    mn -= 1
                    if(mn in day31):
                        dd = 31
                    elif(mn==2):
                        dd = Feb(yy)
                    else:
                        dd = 30
            else:
                dd-=1
            left = 86400 + left
            
    elif(tzhh>=0):
        day = int(left/86400)
        left = (left%86400)
        if(day==1):
            if(mn in day31):
                if(dd==31):
                    if(mn == 12):
                        yy += 1
                        mn = 1
                        dd = 1
                    else:       
                        mn+=1
                        dd = 1
                else:
                    dd+=1
            elif(mn==2):
                if(dd==Feb(yy)):
                     dd = 1
                     mn += 1
                else:
                    dd += 1                        
            else:
                if(dd==30):
                    dd = 1
                    mn+=1
                else:
                    dd+=1

    hh = int(left/3600)
    if(st=='PM'):
        hh = hh-12
    if(hh==0):
        hh = 12
        
    mm = int((left%3600)/60)
    ss = int(left%60)
        
    TimeStamp = Pre(hh)+':'+Pre(mm)+':'+Pre(ss)+' '+st+', '+Pre(dd)+'/'+Pre(mn)+'/'+Pre(yy)
    return(TimeStamp)

with codecs.open(filename, encoding = 'utf-8-sig', errors = 'ignore') as f:
    data = json.load(f)
    global date
    global ctr
    global count
    ctr = 1
    count = 1
    checked = False
    Name = False
    for participants in data:
        p = participants['participants']
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
                date = dtime[0:19]
                f.write(DateTime(date))
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
            f = open(os.path.join(username, "Group{}.txt".format(ctr)),"w", encoding='utf-8-sig')
            for i in p:
                f.write(i)
                if i != p[-1]:
                    f.write(" , ")
                else:
                    f.write("\n\n\n")
            for sender in reversed(participants['conversation']):
                dtime =  sender['created_at']
                date = dtime[0:19]
                f.write(DateTime(date))
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
            f = open(os.path.join(username, "AnonymousPerson{}.txt".format(count)),"w", encoding='utf-8-sig')
            for sender in reversed(participants['conversation']):
                dtime =  sender['created_at']
                date = dtime[0:19]
                f.write(DateTime(date))
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
    print('All Done Correctly. Enjoy!!!')
