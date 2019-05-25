from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
import time
import mysql.connector
import sys
import random


mydb = mysql.connector.connect(
    host = "",
    user = "",
    password = "",
    database = ""
)

mycursor = mydb.cursor()
print(mydb)
print()

options = Options()
mycursor.execute("DROP TABLE table2")
mycursor.execute("CREATE TABLE table2 (date VARCHAR(255), profile VARCHAR(255), follower_number INTEGER (10), follower VARCHAR(255))")


def print_same_line(text):
    sys.stdout.write('\r')
    sys.stdout.flush()
    sys.stdout.write(text)
    sys.stdout.flush()

class InstagramBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        # Instead of using GUI version of Firefox, use the headless one, for both client and server usecase
        options.headless = False
        self.driver = webdriver.Firefox(options=options)

    def closeBrowser(self):
            self.driver.close()

    def login(self):
        driver = self.driver
        driver.get("https://www.instagram.com/")
        time.sleep(2)
        login_button = driver.find_element_by_xpath("//a[@href='/accounts/login/?source=auth_switcher']")
        login_button.click()
        time.sleep(2)
        user_name_elem = driver.find_element_by_xpath("//input[@name='username']")
        user_name_elem.clear()
        user_name_elem.send_keys(self.username)
        time.sleep(1)
        passworword_elem = driver.find_element_by_xpath("//input[@name='password']")
        passworword_elem.clear()
        passworword_elem.send_keys(self.password)
        time.sleep(1)
        passworword_elem.send_keys(Keys.RETURN)
        time.sleep(2)


    def checkPrivate(self, profile):
        driver = self.driver
        try:
            driver.get("https://www.instagram.com/" + profile + "/")
            driver.find_element_by_css_selector('ul li a.-nal3')
        except NoSuchElementException:
            return True
        return False


    def addLinktoDB(self, follower, profile, count):
        profileName = follower.find_element_by_css_selector('a').get_attribute('href')
        print(profileName)
        print('')
        slqformula = "INSERT INTO table2 (date, profile, follower_number, follower) VALUES (%s, %s, %s, %s)"
        follower = (date, profile, count, profileName)
        mycursor.execute(slqformula, follower)
        mydb.commit()



    def findFollowers(self, profile):
        driver = self.driver
        followersLink = driver.find_element_by_css_selector('ul li a')
        followersLink.click()
        time.sleep(1.9)

        
        # For reason, using "find_element_by_css_selector" will block by other elements, so just going to use JS instead
        driver.execute_script('document.querySelector("a.-nal3").click()')
        time.sleep(1.9) 

        rangeUpper = (followersPerProfile / 10) + 2
        rangeUpper = int(rangeUpper) # Converting float data type to integer.
        for i in range(0, rangeUpper):
            try:
                # Scroll follower list far down enough to find at least requested number of user Followers (may not always find).
                driver.execute_script('''
                    var fList = document.querySelector('div[role="dialog"] .isgrP');
                    fList.scrollTop = fList.scrollHeight
                ''') 
                time.sleep(1.2)

                followersList = driver.find_element_by_css_selector('div[role=\'dialog\'] ul')
                followerDiv = followersList.find_elements_by_css_selector('li')
            except Exception:
                continue
    
        # In certain cases, bot will not always find requested number of user Followers, may be higher OR lower than requested number.
        # If higher.
        if len(followerDiv) > followersPerProfile:
            finalFollowerbatch = []
            count = 0
            # Put in a new list with cutoff at requested number of user Followers.
            for follower in followerDiv:
                if count < followersPerProfile:
                    finalFollowerbatch.append(follower)
                else:
                    break
                count = count + 1

            count = 0
            random.choice(finalFollowerbatch) # Randomize array for better variety of users profiles.
            for follower in finalFollowerbatch:
                ig.addLinktoDB(follower, profile, count)
                count = count + 1
            print(followersPerProfile, "profiles randomly selected from", len(followerDiv))

        # If equal or lower.
        else:
            count = 0
            for follower in followerDiv:
                ig.addLinktoDB(follower, profile, count)
                count = count + 1
            print(len(followerDiv), " profiles selected")



    def followUsers(self, profileName):
        driver = self.driver
        print("Following " + profileName +  "'s followers now")
        print()
        usersfollowed = 0

        select_stmt = "SELECT follower FROM table2 WHERE profile = %(profileName)s"
        mycursor.execute(select_stmt, {'profileName': profileName})

        username_data = mycursor.fetchall()
        for username in username_data:
            user_string = (" ".join(username))
            driver.get(user_string)
            hrefs_in_view = driver.find_elements_by_tag_name('a')
            hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view
                             if '.com/p/' in elem.get_attribute('href')]
            follow = driver.find_element_by_css_selector('button')
            if follow.text == "Follow":
                follow.click()
                usersfollowed += 1
                print("Username: ", username, " followed")
                print()

        print("Total number of users followed: ", usersfollowed)


#________________________________________________________TO BE FILLED___________________________________________________________________
#_______________________________________________________________________________________________________________________________________
#_______________________________________________________________________________________________________________________________________
username = "example_username"
password = "example_password"

profiles = ['example_profile']
date = '26_May'
followersPerProfile = 100 # Number of follower profiles to be scraped from user.
path_to_autoEmail_scripts_file = '/path/to/autoEmail_script/folder/on/local/desktop' # Add the path to the autoEmail_script folder on local environment
##______________________________________________________________________________________________________________________________________
#_______________________________________________________________________________________________________________________________________
#_______________________________________________________________________________________________________________________________________



#________________________________________________________MAIN FUNCTION___________________________________________________________________
sys.path.append(path_to_autoEmail_scripts_file)
import autoemail

ig = InstagramBot(username, password)
try: 
    ig.login()

    for profileName in profiles:
        if ig.checkPrivate(profileName):
            continue
        ig.findFollowers(profileName)
        ig.followUsers(profileName)

    subject = "InstaBOT has completed work! (userFolllowersBased_follow.py)"
    message = "All followers from all users, have been followed SUCCESSFULLY."
    autoemail.send_email(subject, message)

except:
    subject = "Something has gone wrong with InstaBOT :( (userFolllowersBased_follow.py)"
    message = "BOT may or may not have failed to complete tasks. Re-run same program, if problem still persits, PLEASE TROUBLESHOOT or open issue on Github"
    autoemail.send_email(subject, message)

ig.closeBrowser()
#______________________________________________________________________________________________________________________________________