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

import tweepy, webbrowser, time, os, subprocess, random 

class StreamWatcher:

    def retweetStatus(self, api, status_id):
        api.retweet(status_id)

    def executeCommand(self, api, status, commandID, status_id):
        command = status.strip("@%s %s " %(api.me().screen_name, commandID))

        if command.startswith("\"") == True: 
            command = command.strip("\"")
            try:
                subprocess.Popen(command, shell=True)
                self.retweetStatus(api, status_id)
            except:
                pass
        else:
            print "No quotations"

    def watchMentions(self, api):
        f = open(".settings")
        info = f.read().strip().split(',')
        f.close()

        date = config.date()
        while True:
            try:
                os.system("clear")
                print "Watcher (Ctrl + C to quit)"
                
                status_list = []
                status_date = []
                status_id   = []

                #for status in tweepy.Cursor(api.mentions).items():
                   
                statuses = tweepy.Cursor(api.mentions).items()
                for status in statuses:
                    if status.author.screen_name == info[2]\
                    and status.text.startswith("@%s %s " %(\
                                            api.me().screen_name,\
                                            info[1])):
                        
                        status_list.append(status.text)
                        status_date.append(str(status.created_at))
                        status_id.append(status.id)

                status_list.reverse()
                status_date.reverse()
                status_id.reverse()

                counter = 0
                for status in status_list:
                    if status_date[counter] > date:
                        date = status_date[counter]

                        print "\t\n[%s] - %s\n" %(date, status)
                        time.sleep(2)

                        self.executeCommand(api, status, info[1], status_id[counter])
                    counter += 1

                time.sleep(int(info[0]))

            except KeyboardInterrupt:
                return False 
            except IndexError:
                pass

    def checker(self, api):
        os.system("clear")

        if os.path.exists(".settings") == False:
            print "You need to go to the settings menu before proceeding to this step."
            time.sleep(6)
    
        else:
            self.watchMentions(api)

class Config:
	
    def OAuth(self):
        if os.path.exists(".consumer"):
            f = open(".consumer", "r")
            info = f.read()
            f.close()

            info = info.split(",")

            consumer_key = info[0]
            consumer_secret = info[1]
            
        else:
            os.system("clear")

            print "Twiterminal requires a Twitter app to connect to this computer's Twitter account. Please provide Twiterminal with the required information."

            consumer_key = str(raw_input("Enter consumer key: "))
            consumer_secret = str(raw_input("Enter consumer secret: ")) 
            
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
            os.system("clear")
            print "Twiterminal needs to have access to the Twitter account of this computer."
            print "You will be directed to a web page where you can authorize access for Twiterminal."

            time.sleep(10)

            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            redirect_url = auth.get_authorization_url()
            webbrowser.open_new_tab(redirect_url)
    
            time.sleep(5)
    
            verifier = raw_input("Enter PIN: ")
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
        os.system("clear")

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
    api = config.OAuth()

    global streamWatcher
    streamWatcher = StreamWatcher()

    try:
        while True:
            os.system("clear")

            print "Twerminal"
            print "\n    1. Start"
            print "    2. Settings"
            print "    3. Commands list"
            print "    4. History"
            print "    5. Exit"

            user = int(raw_input("I choose: "))

            if user == 1:
                streamWatcher.checker(api) 
            elif user == 2:
                config.settings()
            elif user == 3:
                pass
            elif user == 4:
                pass
            elif user == 5:
                print "Good bye!"
                time.sleep(2)
                os.system("clear")
                return False
            else:
                print "Invalid input."
                time.sleep(2)
    except KeyboardInterrupt:
        print "\n"

if __name__ == "__main__":
    main()
