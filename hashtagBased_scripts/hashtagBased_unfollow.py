from selenium import webdriver
from selenium.webdriver.common.keys import Keys
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
print()

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

    def unfollow_user(self):
        driver = self.driver
        mycursor.execute("SELECT username FROM table1 WHERE date = %s", (session_date,))
        username_data = mycursor.fetchall()

        for username in username_data:
            user_string = (" ".join(username))
            try:
                driver.get("https://www.instagram.com/" + user_string + "/")
                hrefs_in_view = driver.find_elements_by_tag_name('a')
                hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view
                                if '.com/p/' in elem.get_attribute('href')]

                unfollowButton = driver.find_element_by_css_selector('section.zwlfE button')
                if unfollowButton.text != "Follow":
                    unfollowButton.click()
                    confirmButton = driver.find_element_by_xpath('//button[text() = "Unfollow"]')
                    confirmButton.click()
                    print("User ", follower_string, " unfollowed sucessfully")
                    print() 
                else:
                    print("User ", follower_string, " is already unfollowed")
                    print() 
                     
            except:
                print("The user (" + user_string + ") is currently unavaliable and is automatically unfollowed.")
                print() 

            mycursor.execute("SET SQL_SAFE_UPDATES = 0")
            mycursor.execute("DELETE FROM table1 WHERE date = %s AND username = %s", (session_date, user_string,))
            mydb.commit()

#____________________________________________________________TO BE FILLED______________________________________________________________
#______________________________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________________________
username = "nickumarr"
password = "Nikiltommy98"

session_date = '29_Mar'
#______________________________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________________________

#________________________________________________________MAIN FUNCTION___________________________________________________________________
ig = InstagramBot(username, password)
ig.login()
ig.unfollow_user()
ig.closeBrowser()
time.sleep(1200)
#______________________________________________________________________________________________________________________________________