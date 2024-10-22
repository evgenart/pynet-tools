#!/usr/bin/env python
import pytest
import time
import json
import smtplib
import email.message
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from time import sleep
from os.path import basename

email_list = ['servicedesk@domain.com', 'helpdesk@domain.com' ]
FILENAME = 'out.png'
FILEPATH = 'C:/Users/myuser/Desktop/' 
FREQUENCY = 40


class TestNetgraph():
  def setup_method(self, method):
    print('constructor RUN')
    self.options = webdriver.ChromeOptions()
    self.options.add_argument('ignore-certificate-errors')
    self.options.add_argument('headless')
    self.driver = webdriver.Chrome(options = self.options);
    self.vars = {}
  
  def teardown_method(self, method):
    print('Destructor RUN')
    self.driver.quit()
  
  
  def test_netgraph(self):
    # Test name: net_graph
    # Step # | name | target | value | comment
    # 1 | open | /login |  | 
    self.driver.get("https://net-graph.domain.com/login")
    # 2 | setWindowSize | 1445x914 |  | 
    self.driver.set_window_size(1445, 914)
    # 3 | click | linkText=Sign in with SSO |  | 
    self.driver.find_element(By.LINK_TEXT, "Sign in with SSO").click()
    # 4 | runScript | window.scrollTo(0,0) |  | 
    self.driver.execute_script("window.scrollTo(0,0)")
    # 5 | click | linkText=Manage |  | 
    self.driver.get("https://net-graph.domain.com/goto/Y169s9iHk")
    print('#SAVE_SCREENSHOT')
    time.sleep(20)

    self.driver.save_screenshot(FILEPATH+FILENAME);
  

def send_email(email_list):
    for email in email_list:
        print(f'SNEDING EMAIL TO: {email}')
        from_addr = 'myusername@domain.com'
        cc = 'myusername@domain.com'
        to_addr = email
        rcpt = cc.split(",") + [to_addr]
        msg = MIMEMultipart()
        msg['From'] = "myusername@domain.com"
        msg['To'] = email
        msg['Cc'] = cc
        msg['Subject'] = "NET-GRAPH-MONITORING CYPRUS"
        frequency = FREQUENCY
        body = f"\
        <html>\
            <body>\
                <p>Hi, this is a temporary fix, until acess is approved or the NMS moved. </p>\
                <img src='cid:photoimage1'></a>\
                <p>Auto-update each {frequency} minutes<p>\
            </body>\
        </html>"

        fp = open(FILEPATH + FILENAME, 'rb')

        image = MIMEImage(fp.read())
        fp.close()

        # Specify the ID according to the img src in the HTML part
        image.add_header('Content-ID', '<photoimage1>')
        msg.attach(image)

        msg.attach(MIMEText(body, 'html')) 

        # # for attchement
        # part = MIMEApplication(open(FILEPATH, "rb").read())
        # part['Content-Disposition'] = 'attachment; filename='+basename(FILENAME)
        # msg.attach(part)
        
        s = smtplib.SMTP('smtp.ourdomain.local')
        s.ehlo
        #s.login(user, pwd)
        text = msg.as_string() 
        s.sendmail(from_addr, rcpt, text)
        s.quit()
        s.close()


print('the script started')
selenium_instance = TestNetgraph()
selenium_instance.setup_method(None)
selenium_instance.test_netgraph()
selenium_instance.teardown_method(None)
sleep(3)
print('SENDING PHOTO')

send_email(email_list)

print('the script ended')


