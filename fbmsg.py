from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time 
import sys
import signal
import datetime
import pickle


lastMessages = {}
driver = None

def signal_handler(sig, frame):
	driver.quit()
	sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


def initBrowser():
	global driver

	options = Options()	
	options.add_argument("--headless")
	options.set_preference("dom.webnotifications.enabled", False)	
	driver = webdriver.Firefox(firefox_options=options)

	driver.get('https://www.facebook.com/')

	a = driver.find_element_by_id('email')
	a.send_keys('abhaytyagi1998@gmail.com')

	b = driver.find_element_by_id('pass')
	b.send_keys('password')

	try:
		c = driver.find_element_by_id('loginbutton')
		c.click()
	except:
		c = driver.find_element_by_name('login')
		c.click()

	return driver


def sendReply(msg):
	global driver
	d = driver.find_element_by_class_name('_5rpu')

	dt = datetime.datetime.now()
	if dt.hour >= 0 and dt.hour <= 7:
		msg = "Automated reply: I am sleeping"
	elif dt.hour >= 19 and dt.hour <= 20:
		msg = "Automated reply: I am eating"
	elif dt.hour >= 9 and dt.hour <= 13 and datetime.datetime.today().weekday() < 5:
		msg = "Automated reply: I am in class"
	else:
		msg = "(y)"

	d.send_keys(msg)
	d.send_keys(Keys.RETURN)

	time.sleep(1)


def messagePerson(username):
	global driver

	driver.get("https://www.facebook.com/messages/t/" + username)
	
	element_present = EC.presence_of_element_located((By.CLASS_NAME, '_5rpu'))
	WebDriverWait(driver, 60).until(element_present)

	d = driver.find_element_by_class_name('_5rpu')

	d.send_keys("I am a dumb bot. Make me smarter.")
	d.send_keys(Keys.RETURN)

	time.sleep(1)

def checkLastMessages():
	global driver
	driver.get("https://www.facebook.com/messages/t/")

	element_present = EC.presence_of_element_located((By.CSS_SELECTOR, 'a._1ht5'))
	WebDriverWait(driver, 60).until(element_present)

	a = driver.find_elements_by_css_selector('a._1ht5')[: 5]

	for friend in a:
		friend.click()

		element_present = EC.presence_of_element_located((By.XPATH, "//div[@class='_aok']"))
		WebDriverWait(driver, 60).until(element_present)

		element_present = EC.presence_of_element_located((By.CLASS_NAME, '_41ud'))
		WebDriverWait(driver, 60).until(element_present)

		sender = driver.find_elements_by_xpath("//div[@class='_41ud']/h5")[-1].get_attribute('innerHTML')
		username = driver.find_element_by_xpath("//span[@class='_3oh-']").get_attribute('innerHTML')

		msg = driver.find_elements_by_xpath("//div[@class='_aok']")

		changed = False
		if len(msg) > 0:
			content = msg[len(msg) - 1].get_attribute('aria-label')

			if username in lastMessages:
				if lastMessages[username] != content and sender in username:
					changed = True
					sendReply(content)
					lastMessages[username] = content
			else:
				changed = True
				lastMessages[username] = content

			if changed:
				with open('lastMessages.pkl', 'wb') as f:
					print("dumped " + str(lastMessages))
					pickle.dump(lastMessages, f, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == "__main__":
	initBrowser()

	try:
		with open('lastMessages.pkl', 'rb') as f:
		    lastMessages = pickle.load(f)
	    	print "loaded " + str(lastMessages)
	except:
		pass

	while True:
		checkLastMessages()
		time.sleep(5)

	driver.quit()
