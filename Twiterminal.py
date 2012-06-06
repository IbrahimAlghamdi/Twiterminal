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

# Contains all the system commands.
class Functions:

    # Initial method.
    def __init__(self):

        # Determines if the program is running on
        # a *NIX or windows machine.
        if sys.platform.startswith("linux")\
            or sys.platform.startswith("darwin")\
            or sys.platform.startswith("freebsd"):

            self.OS = "unix"

        elif sys.platform.startswith("win32"):
            self.OS = "windows"

    # Shutdown method.
    def shutdown(self):

        # Runs the appropriate command for each supported OS.
        # Unix OS's:
        if self.OS == "unix":
            # Shutdown command.
            process = subprocess.Popen("sudo shutdown -h now", shell=True)
            # Makes subprocess wait until command finishes.
            process.wait()

        # Windows OS:
        elif self.OS == "windows":
            process = subprocess.Popen("shutdown -s", shell=True)
            process.wait()

        # Unsupported OS's:
        else:
            print "Operating system is not supported."

    # Restart method.
    def restart(self):

        if self.OS == "unix":
            process = subprocess.Popen("sudo shutdown -s now", shell=True)
            process.wait()

        elif self.OS == "windows":
            process = subprocess.Popen("sudo shutdown -r", shell=True)
            process.wait()

        else:
            print "Operating system is not supported."

    # Sleep/Suspend method.
    def sleep(self):

        if self.OS == "unix":
            process = subprocess.Popen("sudo pm-suspend", shell=True)
            process.wait()

        elif self.OS == "windows":
            process = subprocess.Popen("rundll32.exe powrprof.dll,SetSuspendState 0,1,0", shell=True)
            process.wait()
#pass

        else:
            print "Operating system is not supported."

    # Hibernate method.
    def hibernate(self):

        if self.OS == "unix":
            process = subprocess.Popen("sudo pm-hibernate", shell=True)
            process.wait()

        elif self.OS == "windows":
            process = subprocess.Popen("rundll32.exe powrprof.dll,SetSuspendState", shell=True)
            process.wait()
#pass

        else:
            print "Operating system is not supported."

    # Logoff method.
    def logoff(self):

        if self.OS == "unix":
            process = subprocess.Popen("logout", shell=True)
            process.wait()

        elif self.OS == "windows":
            pass

        else:
            print "Operating system is not supported."

    # System information method.
    def status(self):

        if self.OS == "unix":
            pass #subprocess.Popen("", shell=True)

        elif self.OS == "windows":
            pass

        else:
            print "Operating system is not supported."

    # Custom command method.
    def customCommand(self, command):

        if self.OS == "unix":
            # Executes a custom command and return 0 if
            # successfully done.
            process = subprocess.Popen(command, shell=True)
            process.wait()
            return process

        elif self.OS == "windows":
            process = subprocess.Popen(command, shell=True)
            process.wait()
            return process

        else:
            print "Operating system is not supported."

# Contains all the Twitter functions.
class Stream:

    # Initial method.
    def __init__(self):

        # Imports settings.
        f = open(".settings", "r")
        info = f.read().strip().split(",")
        f.close()

        # Sets settings to variables.
        self.timeout  = info[0] # Timeout variable.
        self.command  = info[1] # Command variable.
        self.username = info[2] # Username variable.

        # Sets account information to variables.
        self.api    = config.OAuth() # API
        self.userID = self.api.get_user(screen_name=self.username).id # Admin's Twitter ID
        self.me     = self.api.me().screen_name # Client's screen name (username)

    # Reply method.
    def replyTweet(self, tweet, statusID):

        # Replies to a specific tweet using its status id.
        self.api.update_status("@%s %s %d" %(self.username,\
                                           tweet,\
                                           config.randomNumber()),\
                                           in_reply_to_status_id = statusID)

    # Find command method. Finds the command
    # within a tweet.
    def findCommand(self, status, statusID):

        # Strips away the client's accound name and command.
        command = status.strip("@%s %s " %(self.me, self.command))

        # Determines whether it's a custom command
        # or a pre-made command.
        # If a custom command:
        if command.startswith("\"") == True:

            # Splits ".
            command = command.split("\"")

            # Runs the custom command method and sets
            # its output to a variable <process>.
            process = functions.customCommand(command[1])

            # If output doesn't equal 0, it will
            # reply with "No, sir!":
            if process.poll() != 0:
                self.replyTweet("No, sir!", statusID)

            # Otherwise reply with "Yes, sir!":
            else:
                self.replyTweet("Yes, sir!", statusID)

            # Adds command to history.
            config.addHistory(command[1])

        #If a pre-made command:
        else:
            # Find the command in the status and
            # run the appropriate function:
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

            # Replies with "Command not found, sir!" when
            # command is not found:
            else:
                self.replyTweet("Command not found, sir!", statusID)
                print "Command not found."

            # Adds command to history.
            config.addHistory(command)

    # Import mentions method.
    def streamMentions(self):

        # Sets GMT time to a variable.
        self.date = config.date()

        # While-loop.
        while True:
            try:

                # Displays remaining_hits
                rem = self.api.rate_limit_status()
                rem = rem['remaining_hits']

                # Clears screen.
                config.clearScreen()
                print "Watcher (Ctrl + C to quit) - Remaining requests: %d" %rem

                # Initiates lists.
                status_list = [] # Contains statuses.
                status_date = [] # Contains statuses dates.
                status_id   = [] # Contains statuses ID's.

                # Imports mentions and sets them to a variable.
                statuses = tweepy.Cursor(self.api.mentions).items()

                # For-loop. For each status in statuses variable.
                for status in statuses:

                    # Only works for statuses that are newer than
                    # the initial date, have the same author's name
                    # as in settings, and starts with @<username> <command>:
                    if str(status.created_at) > self.date\
                        and status.author.id == self.userID\
                        and status.text.startswith("@%s %s" %\
                                (self.me, self.command)):

                        # Adds status, status date, and author ID
                        # to the lists initiated above.
                        status_list.append(status.text) # Statuses.
                        status_date.append(str(status.created_at)) # Statuses dates.
                        status_id.append(status.id) # Statuses ID's.

                # Reverses lists to be from older to newer.
                status_list.reverse() # Statuses.
                status_date.reverse() # Statuses dates.
                status_id.reverse() # Statuses ID's.

                # Only works if status_list is not empty.
                if len(status_list) > 0:

                    # Counter variable.
                    counter = 0

                    # While-loop. While counter is less than
                    # the length of status_list:
                    while counter < len(status_list):

                        # Prints status and status date/time.
                        print "\t\n[%s] - %s\n" %(status_date[counter],\
                                                  status_list[counter])

                        # Sleeps for 2 seconds.
                        time.sleep(2)

                        # Passes status and status ID to findCommand method.
                        self.findCommand(status_list[counter],\
                                         status_id[counter])

                        # Sleeps for 2 seconds.
                        time.sleep(2)

                        # Adds 1 to counter.
                        counter += 1

                        # Important command. This sets the date variable
                        # equal to the last executed command's status so
                        # the program will ignore that status and
                        # statuses before that one.
                        self.date = status_date[-1]

            # Closes when user presses <Ctrl + C>.
            except KeyboardInterrupt:
                return False

            # Keeps program running.
            except:
                time.sleep(int(self.timeout))

            # Makes computer sleep for a
            # number of seconds.
            else:
                time.sleep(int(self.timeout))

# Contains all the settings and access information.
class Config:

    # Clear screen method.
    def clearScreen(self):

        # If OS is Linux, Mac, or BSD:
        if sys.platform.startswith("linux")\
            or sys.platform.startswith("darwin")\
            or sys.platform.startswith("freebsd"):

            # Executes <clear>.
            os.system("clear")

        # If OS is Windows:
        elif sys.platform.startswith("win32"):

            # Executes <clrscr>.
            os.system("clrscr")

    # File checking method.
    def fileCheck(self):

        # If ".settings" doesn't exist:
        if os.path.exists(".settings") == False:

            # Creates it by using the default values.
            info = ["65","DO","user"]
            f = open(".settings", "w")
            os.chmod(".settings", 0600)
            info = ",".join(info)
            f.write(info)
            f.close()

        # If ".history" doesn't exist:
        if os.path.exists(".history") == False:

            # Creates .history if it doesn't exist.
            f = open(".history", "w")
            os.chmod(".history", 0600)
            f.close()

        # If ".consumer" and ".access"
        # don't exist.
        if os.path.exists(".consumer") == False or\
           os.path.exists(".access") == False:

            self.OAuth()

    # OAuth method.
    def OAuth(self):

        # If ".consumer" file exists:
        if os.path.exists(".consumer"):

            # Opens file and import information.
            f = open(".consumer", "r")
            info = f.read()
            f.close()

            # Splits information seperated by ','.
            info = info.split(",")

            # Sets data to variables.
            consumer_key = info[0] # Consumer Key.
            consumer_secret = info[1] # Consumer Secret.

        # If ".consumer" doesn't exist:
        else:

            # Clears screen.
            self.clearScreen()

            # Prints a message.
            print "Twiterminal requires a Twitter app to connect to this computer's Twitter account. Please provide Twiterminal with the required information."

            # Prompts user for Consumer Key and Consumer Secret.
            consumer_key = str(raw_input("\nEnter consumer key: ")).strip()
            consumer_secret = str(raw_input("Enter consumer secret: ")).strip()

            # Writes Consumer Key and Consumer Secret
            # to a file for later use.
            f = open(".consumer", "w")
            os.chmod(".consumer", 0600)
            f.writelines(consumer_key + "," + consumer_secret)
            f.close()

            time.sleep(2)

        # If ".access" file exists:
        if os.path.exists(".access"):

            # Opens file and imports information.
            f = open(".access", "r")
            info = f.read()
            f.close()

            # Splits information seperated by ','.
            info = info.split(",")

            # Sets Access Key and Access Secret to variables.
            access_key    = info[0] # Access Key
            access_secret = info[1] # Access Secret

        # If ".access" file doesn't exist:
        else:

            # Clears screen.
            self.clearScreen()

            # Prints messages.
            print "Twiterminal needs to have access to the Twitter account for this computer."

            user = raw_input("\n[1] PIN.\n[2] Access key/secret\nI choose: ")

            # If user chooses 1.
            if user == '1':

                print "\nYou will be directed to a web page where you can authorize access for Twiterminal."

                # Sleeps for 10 seconds.
                time.sleep(10)

                # Connects to the Twitter app, and redirects
                # the user to a web page to authorize the app
                # and returns a PIN.
                global auth
                auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
                redirect_url = auth.get_authorization_url()
                webbrowser.open_new_tab(redirect_url)

                # Sleep for 5 seconds.
                time.sleep(5)

                # Prompts the user for PIN to have access to the
                # client's Twitter account.
                verifier = str(raw_input("\nEnter PIN: ")).strip()
                auth.get_access_token(verifier)

                # Sets Access Key and Access Secret to variables.
                access_key    = auth.access_token.key
                access_secret = auth.access_token.secret

                time.sleep(2)

            # If user chooses 2.
            else:

                access_key    = raw_input("\nAccess Key: ")
                access_secret = raw_input("Access Secret: ")

                time.sleep(2)

            # Writes information to a file for later use.
            f = open(".access", "w")
            os.chmod(".access", 0600)
            f.writelines(access_key + "," + access_secret)
            f.close()

        # Connects to Twitter and returns API.
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        api = tweepy.API(auth)
        return api

    # Date method. Returns GMT time in the same
    # format as Twitter.
    def date(self):

        # Gets GMT time.
        gmttime = time.asctime(time.gmtime(time.time()))

        # Splits information seperated by " ".
        gmttime = gmttime.split()

        # Dictionary of months.
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

        # Changes month from words to numbers.
        gmttime[1] = months[gmttime[1]]

        if int(gmttime[2]) < 10:
            gmttime[2] = "0%s" %gmttime[2]

        # Returns date in the same format as Twitter.
        return "%s-%s-%s %s" %(gmttime[4],\
                               gmttime[1],\
                               gmttime[2],\
                               gmttime[3])

    # Random number generator method. Used for
    # avoiding double tweets and for user confirmation.
    def randomNumber(self):

        # Generates a random number and returns it.
        num = int(random.random() * pow(10,6))
        return num

    # Settings method. This is where settings will
    # be made and edited by the user.
    def settings(self):

        # Clears screen.
        self.clearScreen()

        # Opens ".settings" and imports information.
        f = open(".settings", "r")
        info = f.read().strip().split(',')
        f.close()

        # Displays the settings menu.
        print "Settings"
        print "\nChange values:"
        print "    [1] Timeout(s) : %s" %info[0] # Timeout.
        print "    [2]  Command   : %s" %info[1] # Command.
        print "    [3]  Username  : %s" %info[2] # Username.
        print "\nDelete settings:"
        print "    [4] Settings."
        print "    [5] History."
        print "    [6] Login information."
        print "    [7] Default settings."

        # Prompts user for an option.
        user = raw_input("\nWhat do you want to change (-1 to quit)? ")

        # If user chooses 1 OR 2 OR 3:
        # 1 - Timeout.
        # 2 - Command.
        # 3 - Username.
        if user == "1":
            # Prompts user for input and changes the settings value.
            user = int(raw_input("Enter a value: ").strip())

            # Only allows >= 65
            if user >= 65:
                info.pop(0)
                info.insert(0, str(user))

            else:
                print "Timeout has to be no less than 65."
                time.sleep(3)

        elif user == "2":
            user = str(raw_input("Enter a starting command: ").strip())
            info.pop(1)
            info.insert(1, user)

        elif user == "3":
            user = str(raw_input("Enter a username: ").strip().strip("@"))
            info.pop(2)
            info.insert(2, user)

        # If user chooses 4 OR 5 OR 6:
        # 4 - Delete settings.
        # 5 - Delete history.
        # 6 - Delete login information.
        # 7 - Delete all settings (Return to default settings).
        elif user == "4":

            # Generate a random number for confirmation.
            num = self.randomNumber()
            user = str(raw_input("Please enter %s to delete settings (Enter anything to keep them):" %num))

            # If user enters number right:
            if user == str(num):

                # Catches errors.
                try:
                    # Removes ".settings" file, prints a
                    # message and sleeps for 3 seconds.
                    os.remove(".settings")
                    print "Settings have been successfully removed."
                    time.sleep(3)

                # Prints a message when an error occurs
                # when accessing a file.
                except OSError:
                    print "File is not found."
                    time.sleep(3)

                # Prints a message when any error is
                # raised.
                except:
                    print "Unexpected error."
                    time.sleep(3)

            # If user enters number wrong:
            else:
                # Does nothing and sleeps for 3 seconds.
                print "Nothing has been changed."
                time.sleep(3)

        elif user == "5":
            # Generate a random number for confirmation.
            num = self.randomNumber()
            user = str(raw_input("Please enter %s to delete settings (Enter anything to keep them):" %num))

            # If user enters number right:
            if user == str(num):
                try:
                    # Removes ".history" file, prints a
                    # message and sleeps for 3 seconds.
                    os.remove(".history")
                    print "Settings have been successfully removed."
                    time.sleep(3)

                except OSError:
                    print "File is not found."
                    time.sleep(3)

                except:
                    print "Unexpected error."
                    time.sleep(3)

            # If user enters number wrong:
            else:
                # Does nothing and sleeps for 3 seconds.
                print "Nothing has been changed."
                time.sleep(3)

        elif user == "6":
            num = self.randomNumber()
            user = str(raw_input("Please enter %s to reset login information (Enter anything to keep them):" %num))

            if user == str(num):
                try:
                    os.remove(".consumer")
                    os.remove(".access")
                    print "Login information have been successfully reset."
                    time.sleep(3)

                except OSError:
                    print "File is not found."
                    time.sleep(3)

                except:
                    print "Unexpected error."
                    time.sleep(3)

            else:
                print "Nothing has been changed."
                time.sleep(3)

        elif user == "7":
            num = self.randomNumber()
            user = str(raw_input("Please enter %s to reset all settings (Enter anything to keep everything):" %num))

            if user == str(num):
                try:
                    os.remove(".settings")
                    os.remove(".consumer")
                    os.remove(".access")
                    os.remove(".history")
                    print "All settings have been successfully removed."
                    time.sleep(3)

                except OSError:
                    print "File is not found."
                    time.sleep(3)

                except:
                    print "Unexpected error."
                    time.sleep(3)
            else:
                print "Nothing has been changed."
                time.sleep(3)

        # Quits if user enters -1.
        elif user == "-1":
            return "-1"

        # If user enters an invalid input:
        else:
            # Prints a message and sleeps for 2 seconds.
            print "Invalid input"
            time.sleep(2)

        # Saves settings to file after applying changes.
        if os.path.exists(".settings"):
            info = ','.join(info)
            os.remove(".settings")
            f = open(".settings", "w")
            f.write(info)
            f.close()

    # Lists the available commands.
    def commandsList(self):

        # Runs loop until user enters -1.
        user = ''
        while user != '-1':

            # Clears screen.
            config.clearScreen()

            print "Commands list\n"
            print "    shutdown"
            print "    restart"
            print "    sleep"
            print "    hibernate"
            print "    logoff"
            #print "    status"

            user = raw_input("\nEnter -1 to quit: ")

    # Add to history method.
    def addHistory(self, command):

        # Opens .history and assigns the content
        # to a variable.
        f = open(".history", "a")
        f.write(command + "\n")
        f.close()

    # Display history method.
    def displayHistory(self):

        # Clears screen
        self.clearScreen()

        print "History\n"

        # Checks if file exists.
        if os.path.exists(".history"):

            # Opens and reads file.
            f = open(".history", "r")
            info = f.read()
            f.close()

            # Checks if file is empty. Program will
            # display all commands in history.
            if len(info) == 0:
                print "    History file is empty."
                time.sleep(2)

            else:
                # Splits lines.
                info = info.split("\n")

                # Runs loop until user enters -1
                user = ''
                while user != '-1':

                    # Runs loop until all items in list
                    # are displayed.
                    counter = 0
                    while counter < len(info):

                        # Prints items.
                        print "    " + info[counter]
                        counter += 1

                    user = raw_input("Enter -1 to quit: ")

        else:
            print "    History file is empty."
            time.sleep(2)

# Main method
def main():

    # Config global variable.
    global config
    config = Config()

    # Creates missing files.
    config.fileCheck()

    # Stream global variable.
    global stream
    stream = Stream()

    # Functions global variable.
    global functions
    functions = Functions()

    try:
        # While-loop.
        while True:

            # Checks that all needed files
            # are available.
            config.fileCheck()

            # Clears screen.
            config.clearScreen()

            # Prints main menu.
            print "Twerminal"
            print "\n    1. Start"       # Starts listening.
            print "    2. Settings"      # Settings menu.
            print "    3. Commands list" # Commands list.
            print "    4. History"       # History.
            print "    5. Exit"          # Exit.

            # Prompts user for a number.
            user = raw_input("\nI choose: ")

            # Runs the appropriate class and method.
            if user == '1':
                stream.streamMentions()

            elif user == '2':
                while user != '-1':
                    user = config.settings()

            elif user == '3':
                config.commandsList()

            elif user == '4':
                config.displayHistory()

            elif user == '5':
                # Prints a message, sleeps for 2 seconds,
                # clears screen, and returns false to break
                # loop.
                print "Good bye!"
                time.sleep(2)
                config.clearScreen()
                return False

            else:
                # Prints a message and sleeps for 2 seconds
                # when user enters an invalid input.
                print "Invalid input."
                time.sleep(2)

    # Closes program when user hits <Ctrl + C>
    except KeyboardInterrupt:
        print "\n"

# Runs main method when __name__ == "__main__"
if __name__ == "__main__":
    main()
