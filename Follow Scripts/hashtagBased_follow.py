from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
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

print('')
print('')

# mycursor.execute("DROP TABLE table1")
# mycursor.execute("CREATE TABLE table1 (date VARCHAR(255), number INTEGER (10), username VARCHAR(255))")

def print_same_line(text):
    sys.stdout.write('\r')
    sys.stdout.flush()
    sys.stdout.write(text)
    sys.stdout.flush()
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


    def like_photo(self, hashtag):
        driver = self.driver
        driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
        time.sleep(2)

        # gathering photos
        pic_hrefs = []
        for i in range(1, 7):
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                # get tags
                hrefs_in_view = driver.find_elements_by_tag_name('a')
                # finding relevant hrefs
                hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view
                                 if '.com/p/' in elem.get_attribute('href')]
                # building list of unique photos
                [pic_hrefs.append(href) for href in hrefs_in_view if href not in pic_hrefs]
                random.shuffle(pic_hrefs)

                final_pic_hrefs = []
                count = 0
                while count < photos_per_hashtag: # Number of photos per hashtag
                    final_pic_hrefs.append(pic_hrefs[count]) # adding first photos from count number of photos from gathered array to different array
                    count += 1
                # print("Check: pic href length " + str(len(pic_hrefs)))
            except Exception:
                continue

        # Liking photos
        unique_photos = len(final_pic_hrefs)
        follow_count = 0
        for pic_href in final_pic_hrefs:
            follow_count+=1
            driver.get(pic_href)
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                time.sleep(random.randint(2, 4))
                # gathering the usernames of the owners of the photos
                follow_user = driver.find_elements_by_css_selector('a.FPmhX.notranslate.nJAzx')
                for a in follow_user:
                    following_username = a.get_attribute('title')
                    print("Photo Liked: ", pic_href, "from user ---------- ", following_username)

                slqformula = "INSERT INTO table1 (date, number, username) VALUES (%s, %s, %s)"
                follower = (session_date, follow_count, following_username)
                mycursor.execute(slqformula, follower)
                mydb.commit()

                time.sleep(1)

                like_button = lambda: driver.find_element_by_xpath('//span[@aria-label="Like"]').click()
                like_button().click()


                # for second in reversed(range(0, random.randint(18, 28))):
                #     print_same_line("#" + hashtag + ': unique photos left: ' + str(unique_photos)
                #                     + " | Sleeping " + str(second))
                #     time.sleep(1)

            except Exception as e:
                time.sleep(2)
            unique_photos -= 1
            print("Remaining photos from", tag, ":", unique_photos)
            print()



    def follow_user(self):
        driver = self.driver
        print("Following users now")
        usersfollowed = 0

        mycursor.execute("SELECT username FROM table1")
        username_data = mycursor.fetchall()

        for username in username_data:
            user_string = (" ".join(username))
            driver.get("https://www.instagram.com/" + user_string + "/")
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





#____________________________________________________________TO BE FILLED______________________________________________________________
#______________________________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________________________
username = "example_username"
password = "example_password"

session_date = "28_Mar"
photos_per_hashtag = 2
hashtags = ['life', 'football']
#______________________________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________________________



ig = InstagramBot(username, password)
ig.login()

while True:
        # Choose a random tag from the list of tags
        # ig = InstagramBot(username, password)
        # ig.login()

        hashtag_count = 0
        hashtags_array_count = len(hashtags)

        while (hashtags_array_count > 0):
            tag = hashtags[hashtag_count]
            ig.like_photo(tag)
            hashtags_array_count -= 1
            hashtag_count += 1
            ig.follow_user()

        print('InstaBot has COMPLETED liking and following profiles from stated hashtags!')
        ig.closeBrowser()
        time.sleep(120)
