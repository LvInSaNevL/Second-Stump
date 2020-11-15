import json
import os, sys
import names
import random

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriver
from selenium.webdriver.common.keys import Keys
from tooling import prettyPrint, bcolors, fullPath

titles = []
# load list from a file (capitalize and remove trailing \n characters)
with open(fullPath('data/adjectives.txt')) as f:
    titles = [line.capitalize().rstrip() for line in f]


arguments = ["--disable-web-security",
             "--allow-running-insecure-content",
             "--allow-automation",
             "--disable-extensions",
             "--disable-popup-blocking",
             "--ignore-certificate-errors",
             "--disable-plugins-discovery",
             "--user-data-dir=data/browser/secondStump",
             "--incognito"
             "user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/60.0.3112.50 Safari/537.36'"]

def newUpload():
  with open(fullPath("data/auth.json")) as jsonfile:
        auth = json.load(jsonfile)


  opts = webdriver.ChromeOptions()
  opts.binary_location="/usr/bin/google-chrome"
  opts.accept_untrusted_certs = True
  opts.assume_untrusted_cert_issuer = True
  for arg in arguments:
    opts.add_argument(arg)

  driver = webdriver.Chrome(executable_path="data/browser/chromedriver", options=opts)

  # Authenticate into Youtube Studio
  driver.get("https://accounts.google.com/o/oauth2/v2/auth/oauthchooseaccount?redirect_uri=https%3A%2F%2Fdevelopers.google.com%2Foauthplayground&prompt=consent&response_type=code&client_id=407408718192.apps.googleusercontent.com&scope=email&access_type=offline&flowName=GeneralOAuthFlow")
  # Get to upload screen
  CREATE = driver.find_element_by_id("create-icon").click()
  UPLOAD = driver.find_element_by_id("text-item-0").click()
  content = os.listdir(fullPath("data/output"))[0]
  selectFiles = driver.find_element_by_id("select-files-button").click()
  selectFiles.send_keys(content)

  # Publish video to youtube
  title = "{} memes for {}".format(random.choice(titles), names.get_first_name())
  titleBox = driver.find_element_by_id("textbox").send_keys(title)
  nextButon = driver.find_element_by_id("next-button")
  nextButon.click()
  nextButon.click()

  # Finally uploads the video 
  doneButton = driver.find_element_by_id("done-button").click()

  driver.close()

  prettyPrint(bcolors.OKGREEN, "Video finished uploading, closing connection")


# A little bit of structure. Allows me to call `videoUploader.py newUpload` from the command line
if __name__ == '__main__':
   globals()[sys.argv[1]]()