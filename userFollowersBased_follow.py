from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import mysql.connector
import sys


mydb = mysql.connector.connect(
    host = "",
    user = "",
    password = "",
    database = ""
)

mycursor = mydb.cursor()
print(mydb)

# mycursor.execute("DROP TABLE table2")
# mycursor.execute("CREATE TABLE table2 (date VARCHAR(255), profile VARCHAR(255), follower_number INTEGER (10), follower VARCHAR(255))")


def print_same_line(text):
    sys.stdout.write('\r')
    sys.stdout.flush()
    sys.stdout.write(text)
    sys.stdout.flush()

class InstagramBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Firefox()

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


    def findFollowers(self, profile):
        driver = self.driver
        followersLink = driver.find_element_by_css_selector('ul li a')
        followersLink.click()
        time.sleep(1.9)

        # Code that was
        # followersList = self.driver.find_element_by_css_selector('div[role=\'dialog\'] ul')
        #
        # followerNames = followersList.find_elements_by_css_selector('a.FPmhX.notranslate._0imsa')
        # followButton = followersList.find_elements_by_css_selector('button._0mzm-.sqdOP.L3NKy')
        #
        # count = 0
        # for name in followerNames:
        #     profileName = name.get_attribute('title')
        #     count = count + 1
        #     slqformula = "INSERT INTO table2 (date, profile, follower_number, follower) VALUES (%s, %s, %s, %s)"
        #     follower = (date, profile, count, profileName)
        #     mycursor.execute(slqformula, follower)
        #     mydb.commit()


        followersList = self.driver.find_element_by_css_selector('div[role=\'dialog\'] ul')
        followerDiv = followersList.find_elements_by_css_selector('li')
        print(followerDiv)

        count = 0
        for follower in followerDiv:
            count = count + 1
            profileName = follower.find_element_by_css_selector('a').get_attribute('href')
            print(profileName)
            print('')
            slqformula = "INSERT INTO table2 (date, profile, follower_number, follower) VALUES (%s, %s, %s, %s)"
            follower = (date, profile, count, profileName)
            mycursor.execute(slqformula, follower)
            mydb.commit()


    def followUsers(self, profileName):
        driver = self.driver
        print("Following " + profileName +  "'s followers now")
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

profiles = ['gerardpique_fcbarcelona']
date = '09_Feb'
##______________________________________________________________________________________________________________________________________
#_______________________________________________________________________________________________________________________________________
#_______________________________________________________________________________________________________________________________________



#________________________________________________________MAIN FUNCTION___________________________________________________________________
ig = InstagramBot(username, password)
ig.login()

for profileName in profiles:
    if ig.checkPrivate(profileName):
        continue
    ig.findFollowers(profileName)
    ig.followUsers(profileName)

ig.closeBrowser()

