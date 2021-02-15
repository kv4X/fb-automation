from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from pynput.keyboard import Key, Controller
from numpy import random
from time import time, sleep
from datetime import datetime, timedelta
import pytz
from operator import methodcaller


class Bot:
    XPATHS = {
        'loginEmail': "//input[@id='email']",
        'loginPass': "//input[@id='pass']",
        'loginBtn': "//button[text()='Log In']",
        'accountSetting': "//div[text()='Account Settings']",
        'logoutBtn': "//span[text()='Log Out']",
        'storyView': "//a[contains(@href, '/stories')]",
        "storyViewNext": "//div[@aria-label='Next Card Button' or @aria-label='Next Bucket Button']",
        "homePageLikePostButtons": "//div[@aria-label='Like' and @role='button']",
        "homePageLinkOpenPost": "//a[@rel='nofollow noopener' and @role='link']",
        "homePageRightAds": "//a[@aria-label='Advertiser link' and @role='link']",
        "addMutual": "//div[@aria-label='Add Friend' and @role='button']",
        "confirmFriendRequest": "//div[@aria-label='Confirm' and @role='button']",
        "ToHomePage": "//a[@aria-label='Facebook' and @href='/']", #tab
        #"ToFriendsPage": "//a[contains(@aria-label, 'Friends') and @href='/friends/']", #tab
        "ToFriendsPage": "//a[contains(@href, '/friends/')]",
        "ToGroupFeedPage": "//a[contains(@aria-label, 'Groups') and @href='/groups/']", #tab
        "GroupFeedOpenLikesPopup": "//span[@role='toolbar']//div[contains(@aria-label, 'Like')]",
        #MY FEED
        "createPostMe": "//span[contains(text(), 'on your mind?')]",
        "peopleYouMayKnow": "//div[contains(@aria-label, 'People You May Know')]//div[@aria-label='OK']",
        #PAGE
        "clickOnSharePage": "//div[contains(@aria-label, 'Send this to friends or post it on your') and @role='button']",
        "shareToTimeline": "//div[@role='button']//span[contains(text(), 'Share now (Friends)')]",
        #EVENTS
        "clickOnEventsPage": "//span[contains(text(), 'Events')]",
        "clickOnBirthday": "//span[contains(text(), 'Birthdays')]"
    }

    ACTIONS={
        "scrollDown":"window.scrollTo(0, document.body.scrollHeight);",
        "scrollTop":"window.scrollTo(0, 0);"
    }

    MISC = {
        'url': "https://www.facebook.com/",
        'urlFriends': "https://www.facebook.com/friends/",
        'urlMe': "https://www.facebook.com/me",
        'chromePath': 'C:\Users\840 G2\Desktop\chromedriver.exe', 
    }

    #GROUPS ID
    GROUPS = ['19854780xxxxxxx']
    #MAIN PAGE
    MAIN_PAGE = 'https://www.facebook.com/page'

    PAGE_LOAD_TIME = 600
    WAIT_TIME = 100

    def __init__(self, setting_options=None,email=None,password=None):
        """
        self.setting_options = setting_options
        self.driver = webdriver.Chrome(
                                    chrome_options=self.setting_options, executable_path=Bot.MISC['chromePath'])
        """
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-notifications')
        #chrome_options.add_argument('--headless')
       # self.driver = webdriver.Chrome("C:\Users\840 G2\Desktop\chromedriver.exe", chrome_options=chrome_options)
        self.driver = webdriver.Chrome(executable_path=r"C:\Users\840 G2\Desktop\chromedriver.exe", chrome_options=chrome_options)
        self.driver.maximize_window()
        self.driver.set_page_load_timeout(Bot.PAGE_LOAD_TIME)
        self.wait = WebDriverWait(self.driver, Bot.WAIT_TIME)
        self.keyboard = Controller()
        self.email="acc@gmail.com"
        self.password="pw"

    @classmethod
    def change_page_load_time(cls, time):
        cls.PAGE_LOAD_TIME = time

    @classmethod
    def change_wait_time(cls, time):
        cls.WAIT_TIME = time

    def go_home(self):
        self.driver.get(Bot.MISC['url'])

    def go_home2(self):
        button = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, Bot.XPATHS['ToHomePage']))
        )
        try:
            button[0].click()
        except:
            self.go_home()

    def scroll_bottom(self, times=3):
        for i in range(times):
            print("Scrolling..")
            self.driver.execute_script(Bot.ACTIONS['scrollDown'])
            sleep(random.randint(2, 5))
    
    def scroll_top(self):
        self.driver.execute_script(Bot.ACTIONS['scrollTop'])

    def facebook_login(self):
        self.driver.get(Bot.MISC['url'])
        self.wait.until(EC.presence_of_element_located(
    (By.XPATH, Bot.XPATHS['loginEmail'])))
        self.driver.find_element_by_xpath(
                                        Bot.XPATHS['loginEmail']).send_keys(self.email)
        self.driver.find_element_by_xpath(
                                        Bot.XPATHS['loginPass']).send_keys(self.password)
        self.driver.find_element_by_xpath(
                                        Bot.XPATHS['loginBtn']).click()
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//body")))
        print("Successfully Logged In Facebook")


    def story_view(self):
        self.go_home()
        self.wait.until(EC.presence_of_element_located((By.XPATH, Bot.XPATHS['storyView'])))
        self.driver.find_elements_by_xpath(Bot.XPATHS['storyView'])[0].click()
        max = random.randint(2, 5)
        for i in range(max):
            sleep(random.randint(2, 7))
            try:
                self.wait.until(EC.presence_of_element_located((By.XPATH, Bot.XPATHS['storyViewNext'])))
                self.driver.find_elements_by_xpath(Bot.XPATHS['storyViewNext'])[0].click()
            except:
                print("[GRESKA] Ne mogu kliknuti na next story button!")
        
        self.driver.execute_script("window.history.go(-1)")

    def like_random_posts_on_homepage(self):
        num_like = random.randint(3, 5)
        self.go_home()
        self.scroll_bottom()
        buttons = self.driver.find_elements_by_xpath(Bot.XPATHS['homePageLikePostButtons'])
        print("[INFO] Pocinjem random lajkat postove na homepage!")
        i = 0
        for button in buttons:
            sleep(random.randint(2, 4))
            i += 1
            try:
                button.click()
            except:
                i -= 1
                continue
            print("[INFO] Lajkovao!")
            if i > num_like:
                break

    def open_random_posts_link_on_homepage(self):
        #open random posts with link in new tab
        main_window = self.driver.current_window_handle
        num_open = random.randint(1, 3)
        self.go_home()
        self.scroll_bottom()
        links = self.driver.find_elements_by_xpath(Bot.XPATHS['homePageLinkOpenPost'])
        print("[INFO] Pocinjem random otvarati linkove na homepage!")
        i = 0
        for link in links:
            sleep(random.randint(2, 4))
            i += 1
            try:
                link.click()
                #otvaranje linka i sleep 10-15sec
                #close trenutnog taba i prebacivanje na main tab
                sleep(random.randint(5, 9))
                self.driver.switch_to.window(self.driver.window_handles[1])
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
            except:
                i -= 1
                continue
            print("[INFO] Link otvoren!")
            if i > num_open:
                break
        self.scroll_bottom()

    def click_on_ad(self):
        #open random posts with link in new tab
        num_open = 1
        self.go_home()
        self.scroll_bottom(2)
        links = self.driver.find_elements_by_xpath(Bot.XPATHS['homePageRightAds'])
        print("[INFO] Otvaram ad link na homepage!")
        i = 0
        for link in links:
            sleep(random.randint(2, 4))
            i += 1
            try:
                link.click()
                sleep(random.randint(5, 9))
                self.driver.switch_to.window(self.driver.window_handles[1])
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
            except:
                i -= 1
                continue
            print("[INFO] Ad Link otvoren!")
            if i == num_open:
                break
                
    def share_rand_post(self):
        pass
    
    def add_mutual_friend(self):
        #self.driver.get(Bot.MISC['urlFriends'])
        self.wait.until(EC.presence_of_element_located((By.XPATH, Bot.XPATHS['ToFriendsPage'])))
        self.driver.find_elements_by_xpath(Bot.XPATHS['ToFriendsPage'])[0].click()
        num_add = random.randint(2, 5)

        self.wait.until(EC.presence_of_element_located((By.XPATH, Bot.XPATHS['addMutual'])))
        mutuals = self.driver.find_elements_by_xpath(Bot.XPATHS['addMutual'])
        print("[INFO] Pocinjem slati zahtjeve za prijateljstvo!")

        i=0
        for mutual in mutuals:
            sleep(random.randint(2, 4))
            i += 1
            try:
                mutual.click()
                print("[INFO] Zahtjev poslat!")
            except:
                i -= 1
                continue
            if i == num_add:
                break
        #vraca na homepage
        self.go_home2()
        print("[INFO] Vracam na homepage!")

    def like_random_posts_group_feed(self):
        self.wait.until(EC.presence_of_element_located((By.XPATH, Bot.XPATHS['ToGroupFeedPage'])))
        self.driver.find_elements_by_xpath(Bot.XPATHS['ToGroupFeedPage'])[0].click()
        num_like = random.randint(3, 5)
        self.scroll_bottom()
        buttons = self.driver.find_elements_by_xpath(Bot.XPATHS['homePageLikePostButtons'])
        print("[INFO] Pocinjem random lajkat postove na group feedu!")
        i = 0
        for button in buttons:
            sleep(random.randint(2, 4))
            i += 1
            try:
                button.click()
            except:
                i -= 1
                continue
            print("[INFO] Lajkovao!")
            if i > num_like:
                break
        #vraca na homepage
        self.go_home2()
        print("[INFO] Vracam na homepage!")

    def post_on_timeline(self, message, link):
        #ne radi
        #//div[@aria-label='Send this to friends or post it on your timeline.']
        self.driver.get(Bot.MISC['urlMe'])
        sleep(2)
        post = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, Bot.XPATHS['createPostMe']))
        )
        try:
            post.click()
            sleep(2)
            element = self.driver.switch_to.active_element
            ActionChains(self.driver).send_keys_to_element(element, link, Keys.ENTER).perform()
            eleme.clear()
            sleep(5)
            ActionChains(self.driver).send_keys_to_element(element, message, Keys.ENTER).perform()

        except:
            print("[GRESKA] Ne mogu paste link!")
            self.go_home2()

    def wish_birthday(self):
        messages = ('Sretan rodjendan!',
                        'Nadam se da cete imati sjajan rodjendan!',
                        'Sretan rodjendan  \u263A',
                        'Sretan rodjendan, imate pozdrav od moje porodice!',
                        '\U0001F382 Sretan rodjendan \U0001F382 ',
                        'Sretan rodjendan, proslavite ga u zdravlju i veselju <3',
                        '\U0001F389 \U0001F38A \U0001F389 Sretan rodjendan \U0001F389  \U0001F38A  \U0001F389',
                        '\U0001F381 Sretan rodjendan \U0001F381 ')
        self.go_home2()
        event = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, Bot.XPATHS['clickOnEventsPage']))
        )
        event.click()
        sleep(2)
        #klik na birthdays buton na events page
        birthday = WebDriverWait(self.driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, Bot.XPATHS['clickOnBirthday']))
        )
        birthday[0].click()
        sleep(5)

        count_post = self.driver.find_elements_by_css_selector("[method='POST']")
        len_count = len(count_post)-1
        print len_count
        for send_msg in range(0, random.randint(1, len_count)):
            #cestitka
            for cv in range(0, 13):
                ActionChains(self.driver).send_keys(Keys.TAB).perform()
                element = self.driver.switch_to.active_element
                try:
                    if element.find_element_by_tag_name('br').get_attribute('data-text') == 'true':
                        try:
                            cmess = self.driver.find_elements_by_css_selector('[method="POST"]')
                            cmess[0].location_once_scrolled_into_view
                            ActionChains(self.driver).send_keys_to_element(element, messages[random.randint(0, 7)], Keys.ENTER).perform()
                            sleep(5)
                            ActionChains(self.driver).reset_actions()
                        except Exception as e:
                            #print e
                            break
                except Exception as e:
                    #print e
                    pass

    def accept_friend_request(self):
        #self.driver.get(Bot.MISC['urlFriends'])
        self.wait.until(EC.presence_of_all_elements_located((By.XPATH, Bot.XPATHS['ToFriendsPage'])))
        self.driver.find_elements_by_xpath(Bot.XPATHS['ToFriendsPage'])[0].click()

        sleep(5)
        try:
            confirms = self.driver.find_elements_by_xpath(Bot.XPATHS['confirmFriendRequest'])
            print("[INFO] Pocinjem prihvatati zahtjeve za prijateljstvo!")

            num_confirm = random.randint(0, len(confirms)-1)
            i=0
            for confirm in confirms:
                sleep(random.randint(2, 4))
                i += 1
                try:
                    confirm.click()
                except:
                    i -= 1
                    continue
                print("[INFO] Zahtjev prihvacen!")
                if i > num_confirm:
                    break
            print("[INFO] Vracam na homepage!")
        except:
            print("[INFO] Nema zahtjeva za prijateljstvo!")
        self.go_home2()

    def random_send_friend_request_on_group_feed(self):
        self.go_home2()
        sleep(5)
        self.wait.until(EC.presence_of_all_elements_located((By.XPATH, Bot.XPATHS['ToGroupFeedPage'])))
        self.driver.find_element_by_xpath(Bot.XPATHS['ToGroupFeedPage']).click()
        sleep(5)
        self.scroll_bottom()
        posts = self.driver.find_elements_by_xpath(Bot.XPATHS['GroupFeedOpenLikesPopup'])
        print("[INFO] Pocinjem random slati zahtjeve za prijateljstvo na group feedu!")

        num_posts = 2
        i = 0
        for post in posts:
            sleep(random.randint(2, 4))
            i += 1
            try:
                post.click()
                sleep(2)
                try:
                    sleep(2)
                    """ 
                    for i in range(3):
                        self.driver.find_element_by_tag_name('body').send_keys(Keys.END)
                    """
                   # sleep(2)
                    
                    buttons = self.driver.find_elements_by_xpath("//div[contains(@aria-label, 'Add Friend')]")
                    j = 0

                    num_req = random.randint(5, len(buttons))
                    for button in buttons:
                        sleep(random.randint(2, 4))
                        j += 1
                        try:
                            try:
                                op = self.driver.find_elements_by_xpath(Bot.XPATHS['peopleYouMayKnow'])
                                op[0].click()
                                print("[INFO] People Your may know is bypassed!")
                            except:
                                pass

                            button.click()
                        except:
                            j -= 1
                            continue
                        print("[INFO] Zahtjev poslat!")
                        if j > num_req:
                            break
                except:
                    continue
            except:
                i -= 1
                continue
            if i > num_posts:
                print("DA")
                break
        #vraca na homepage
        self.go_home2()
        print("[INFO] Vracam na homepage!")

    def share_latest_page_post_on_timeline(self):
        self.driver.get(self.MAIN_PAGE)
        sleep(4)
        posts = WebDriverWait(self.driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, Bot.XPATHS['clickOnSharePage']))
        )
        print("[INFO] Dijeljenje posljednje objave!")
        try:
            posts[0].click()
            button = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, Bot.XPATHS['shareToTimeline']))
            )
            button.click()
            print("[INFO] Objava podjeljena!")
            sleep(2)
            self.go_home2()
        except:
            pass
    def go_sleep(self):
        self.driver.get("https://google.com")

if __name__ == "__main__":
    #https://medium.com/pythoneers/automate-facebook-posts-using-python-4d17b3a26100
    fbdriver=Bot()
    fbdriver.facebook_login()
    #fbdriver.open_random_posts_link_on_homepage()
    #fbdriver.like_random_posts_on_homepage()
    #fbdriver.story_view()
    #fbdriver.click_on_ad()
    #fbdriver.add_mutual_friend()
    #fbdriver.like_random_posts_group_feed()
    #fbdriver.wish_birthday()
    #fbdriver.post_on_timeline('Najlaksi cokoladni kolac BEZ PEcENJA! Sve domacice ce ga obozavati', 'http://svakidan.info/2021/01/najlaksi-cokoladni-kolac-bez-pecenja-sve-domacice-ce-ga-obozavati-9/')
    #sleep(5)
    #print("prebac")
    #fbdriver.accept_friend_request()
    #skrol unutar diva potrebno uraditi
    #fbdriver.random_send_friend_request_on_group_feed()
    #fbdriver.share_latest_page_post_on_timeline()
    #145 - frends
    fbdriver.story_view()
    fbdriver.like_random_posts_group_feed()
    fbdriver.random_send_friend_request_on_group_feed()
    fbdriver.story_view()
    fbdriver.like_random_posts_group_feed()
    fbdriver.random_send_friend_request_on_group_feed()
    fbdriver.story_view()
    fbdriver.like_random_posts_group_feed()
    fbdriver.random_send_friend_request_on_group_feed()
    fbdriver.story_view()
    fbdriver.like_random_posts_group_feed()
    fbdriver.random_send_friend_request_on_group_feed()
    #vrijeme u kojem ce bot raditi
    spavaj = 0
    sleep_time = 30
    running_hours = ["07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "01"]
    tz = pytz.timezone('Europe/Sarajevo')

    myFunctions = [
        'like_random_posts_on_homepage',
        'open_random_posts_link_on_homepage',
        'story_view',
        'click_on_ad',
        'add_mutual_friend',
        'like_random_posts_group_feed',
        'wish_birthday',
        'accept_friend_request',
       ' random_send_friend_request_on_group_feed'
    ]

    """
    #ako je jedan proces u toku drugi ne moze biti pokrenut
    locked = 0
    while True:
        datetime_local = datetime.now(tz)
        if datetime_local.strftime("%H") in running_hours:
            if spavaj == 1:
                #ako dolazi iz sleepa prvo prebacujemo na facebook.com
                fbdrive.go_home()
                spavaj = 0
            #random.choice(myFunctions)()
            try:
                methodcaller(random.choice(myFunctions))(fbdriver)
            except:
                print("GRESKA")
            #fbdriver.click_on_ad()
        else:
            #zatvaramo current tab poslije 21:59
            fbdriver.go_sleep()
            spavaj = 1

        sleep(sleep_time - time() % sleep_time)
    """








