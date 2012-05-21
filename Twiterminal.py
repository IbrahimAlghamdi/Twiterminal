#!/usr/bin/env python
#
# Programmed By Ibrahim Alghamdi
#   Twitter @IbrahimAlghamdi
#   Github  www.github.com/IbrahimAlghamdi
#
# Control your pc without the need for an internet
# connection using your twitter account.
#
# Copyright (C) 2012

import tweepy, webbrowser, time, os, subprocess, random, sys

class Functions:
    
    def __init__(self):
        f = open(".settings", "r")
        info = f.read().strip().split(",")
        f.close()

        if sys.platform.startswith("linux")\
            or sys.platform.startswith("darwin")\
            or sys.platform.startswith("freebsd"):

            self.OS = "unix"

        elif sys.platform.startswith("win32"):
            self.OS = "windows"

    def shutdown(self):
        if self.OS == "unix":
            process = subprocess.Popen("sudo shutdown -h now", shell=True)
            process.wait()

        elif self.OS == "windows":
            pass
        
        else:
            print "Operating system is not supported." 

    def restart(self):
        if self.OS == "unix":
            process = subprocess.Popen("sudo shutdown -r now", shell=True)
            process.wait()

        elif self.OS == "windows":
            pass
        
        else:
            print "Operating system is not supported." 


    def sleep(self):
        if self.OS == "unix":
            process = subprocess.Popen("sudo pm-suspend", shell=True)
            process.wait()

        elif self.OS == "windows":
            pass
        
        else:
            print "Operating system is not supported." 

    def hibernate(self):
        if self.OS == "unix":
            process = subprocess.Popen("sudo pm-hibernate", shell=True)
            process.wait()

        elif self.OS == "windows":
            pass
        
        else:
            print "Operating system is not supported." 

    def logoff(self):
        if self.OS == "unix":
            process = subprocess.Popen("logout", shell=True)
            process.wait()

        elif self.OS == "windows":
            pass
        
        else:
            print "Operating system is not supported." 

    def status(self):
        if self.OS == "unix":
            pass #subprocess.Popen("", shell=True)
            
        elif self.OS == "windows":
            pass
             
        else:
            print "Operating system is not supported." 

    def customCommand(self, command):
        if self.OS == "unix":
            process = subprocess.Popen(command, shell=True)
            process.wait()
            return process

        elif self.OS == "windows":
            process = subprocess.Popen(command, shell=True)
            process.wait()
            return process

        else:
            print "Operating system is not supported." 

class Stream:

    def __init__(self):
        
        f = open(".settings", "r")
        info = f.read().strip().split(",")
        f.close()

        self.timeout  = info[0]
        self.command  = info[1]
        self.username = info[2]

        self.api    = config.OAuth()
        self.userID = self.api.get_user(screen_name=self.username).id
        self.me     = self.api.me().screen_name

    def replyTweet(self, tweet, statusID):
        
        self.api.update_status("@%s %s %d" %(self.username, tweet, config.randomNumber()), in_reply_to_status_id = statusID)

    def findCommand(self, status, statusID):
        
        command = status.strip("@%s %s " %(self.me, self.command))

        if command.startswith("\"") == True: 
            command = command.split("\"")
   
            process = functions.customCommand(command[1])
    
            if process.poll() != 0:
                self.replyTweet("I'm sorry, sir, the command hasn't been successfully executed.", statusID)
                
            else:
                self.replyTweet("Command has been successfully executed, sir.", statusID)
            
        else:
            if "shutdown" in command.lower():
                functions.shutdown()
          
            elif "restart" in command.lower():
                functions.restart()
            
            elif "sleep" in command.lower():
                functions.sleep()
           
            elif "hibernate" in command.lower():
                functions.hibernate()
          
            elif "logoff" in command.lower():
                functions.logoff()
            
            elif "status" in command.lower():
                functions.status()
            
            else:
                self.replyTweet("Command not found.", statusID)
                print "Command not found."
        
    def streamMentions(self):
       
        self.date = config.date()
        
        while True:
            try:
                config.clearScreen()
                print "Watcher (Ctrl + C to quit)"
                
                status_list = []
                status_date = []
                status_id   = []
                
                statuses = tweepy.Cursor(self.api.mentions).items()
                for status in statuses:

                    if str(status.created_at) > self.date\
                        and status.author.id == self.userID\
                        and status.text.startswith("@%s %s" %\
                                (self.me, self.command)):

                        status_list.append(status.text)
                        status_date.append(str(status.created_at))
                        status_id.append(status.id)
                
                status_list.reverse()
                status_date.reverse()
                status_id.reverse()

                counter = 0
                while counter < len(status_list):

                    print "\t\n[%s] - %s\n" %(status_date[counter],\
                                              status_list[counter])
                    time.sleep(2)

                    self.findCommand(status_list[counter],\
                                      status_id[counter])
                    
                    time.sleep(2)
                    
                    counter += 1

                self.date = status_date[-1]

                time.sleep(int(self.timeout))

            except KeyboardInterrupt:
                return False 
            except IndexError:
                pass 

class Config:

    def checker(self):
       
        config.clearScreen()

        if os.path.exists(".settings") == False:
            print "You need to go to the settings menu before proceeding to this step."
            time.sleep(6)
    
        else:
            stream.streamMentions()

    def clearScreen(self):
        
        if sys.platform.startswith("linux")\
            or sys.platform.startswith("darwin"):
            os.system("clear")

        elif sys.platform.startswith("win32"):
	        os.system("clrscr")

    def OAuth(self):
        
        if os.path.exists(".consumer"):
            f = open(".consumer", "r")
            info = f.read()
            f.close()

            info = info.split(",")

            consumer_key = info[0]
            consumer_secret = info[1]
            
        else:
            self.clearScreen()

            print "Twiterminal requires a Twitter app to connect to this computer's Twitter account. Please provide Twiterminal with the required information."

            consumer_key = str(raw_input("Enter consumer key: ")).strip()
            consumer_secret = str(raw_input("Enter consumer secret: ")).strip()
            
            f = open(".consumer", "w")
            f.writelines(consumer_key + "," + consumer_secret)
            f.close()
        
        if os.path.exists(".access"):
            f = open(".access", "r")
            info = f.read()
            f.close()

            info = info.split(",")

            access_key    = info[0]
            access_secret = info[1]

        else:
            self.clearScreen()
            print "Twiterminal needs to have access to the Twitter account of this computer."
            print "You will be directed to a web page where you can authorize access for Twiterminal."

            time.sleep(10)

            global auth
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            redirect_url = auth.get_authorization_url()
            webbrowser.open_new_tab(redirect_url)
    
            time.sleep(5)
    
            verifier = str(raw_input("Enter PIN: ")).strip()
            auth.get_access_token(verifier)
    
            access_key = auth.access_token.key
            access_secret = auth.access_token.secret

            f = open(".access", "w")
            f.writelines(access_key + "," + access_secret)
            f.close()

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        api = tweepy.API(auth)
        return api

    def date(self):
        
        gmttime = time.asctime(time.gmtime(time.time()))
        gmttime = gmttime.split(" ")

        months = {"Jan" : "01",\
                  "Feb" : "02",\
                  "Mar" : "03",\
                  "Apr" : "04",\
                  "May" : "05",\
                  "Jun" : "06",\
                  "Jul" : "07",\
                  "Aug" : "08",\
                  "Sept": "09",\
                  "Oct" : "10",\
                  "Nov" : "11",\
                  "Dec" : "12"}

        gmttime[1] = months[gmttime[1]]
        return "%s-%s-%s %s" %(gmttime[4],\
                               gmttime[1],\
                               gmttime[2],\
                               gmttime[3])

    def randomNumber(self):
        
        num = int(random.random() * pow(10,6)) 
        return num

    def settings(self):
        
        self.clearScreen()

        if os.path.exists(".settings") == False:
            info = ["30","DO","user"]
            f = open(".settings", "w")
            info = ",".join(info)
            f.write(info)
            f.close()
    
        f = open(".settings")
        info = f.read().strip().split(',')
        f.close()

        print "Settings"
        print "\nChange values:"
        print "    [1] Timeout(s) : %s" %info[0]
        print "    [2]  Command   : %s" %info[1]
        print "    [3]  Username  : %s" %info[2]
        print "\nDelete settings:"
        print "    [4] Settings."
        print "    [5] Login information."
        print "    [6] Default settings."

        user = raw_input("\nWhat do you want to change (-1 to quit)? ")

        if user == "1":
            user = int(raw_input("Enter a value: ").strip())
            info.pop(0)
            info.insert(0, str(user))
        
        elif user == "2":
            user = str(raw_input("Enter a starting command: ").strip())
            info.pop(1)
            info.insert(1, user)
        
        elif user == "3":
            user = str(raw_input("Enter a username: ").strip().strip("@"))
            info.pop(2)
            info.insert(2, user)
        
        elif user == "4":
            num = self.randomNumber()
            user = str(raw_input("Please enter %s to delete settings (Enter anything to keep them):" %num))
           
            if user == str(num):
                try:
                    os.remove(".settings")
                    print "Settings have been successfully removed."
                    time.sleep(3)
                except:
                    print "Unexpected error."
                    time.sleep(3)
            else:
                print "Nothing has been changed."
                time.sleep(3)

        elif user == "5":
            num = self.randomNumber()
            user = str(raw_input("Please enter %s to reset login information (Enter anything to keep them):" %num))
           
            if user == str(num):
                try:
                    os.remove(".consumer")
                    os.remove(".access")
                    print "Login information have been successfully reset."
                    time.sleep(3)
                except:
                    print "Unexpected error."
                    time.sleep(3)
            else:
                print "Nothing has been changed."
                time.sleep(3)

        elif user == "6":
            num = self.randomNumber()
            user = str(raw_input("Please enter %s to reset all settings (Enter anything to keep everything):" %num))
           
            if user == str(num):
                try:
                    os.remove(".settings")
                    os.remove(".consumer")
                    os.remove(".access")
                    print "All settings have been successfully removed."
                    time.sleep(3)
                except:
                    print "Unexpected error."
                    time.sleep(3)
            else:
                print "Nothing has been changed."
                time.sleep(3)

        elif user == "-1":
            pass 
        
        else:
            print "Invalid input"
            time.sleep(2)

        if os.path.exists(".settings"):
            info = ','.join(info)
            os.remove(".settings")
            f = open(".settings", "w")
            f.write(info)
            f.close()

def main():
    
    global config
    config = Config()

    global stream
    stream = Stream()

    global functions
    functions = Functions()

    try:
        while True:
            config.clearScreen()

            print "Twerminal"
            print "\n    1. Start"
            print "    2. Settings"
            print "    3. Commands list"
            print "    4. History"
            print "    5. Exit"

            user = int(raw_input("I choose: "))

            if user == 1:
                config.checker() 
            elif user == 2:
                config.settings()
            elif user == 3:
                pass
            elif user == 4:
                pass
            elif user == 5:
                print "Good bye!"
                time.sleep(2)
                config.clearScreen()
                return False
            else:
                print "Invalid input."
                time.sleep(2)
    except KeyboardInterrupt:
        print "\n"

if __name__ == "__main__":
    main()
