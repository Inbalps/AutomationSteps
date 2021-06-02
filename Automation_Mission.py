import os
#installing selenium, if end up ok 0 else 1
install_status = os.system('pip install selenium')
#install chrome driver
os.system('pip install chromedriver-autoinstaller')

import requests
import chromedriver_autoinstaller

def get_cred(driver,add_link):
    """
    this function get credential that is already on add user page
    get: webdriver, add user link
    return: current username and password
    """
    #open add user link 
    driver.get(add_link)

    #get user and password
    cred_tag =  driver.find_elements_by_xpath('/html/body/table/tbody/tr/td[1]/blockquote/blockquote[2]/blockquote')[0].text #get specific blockquote with credential
    cred_tag = cred_tag.splitlines()
    username = (cred_tag[0].split(":")[1]).strip() #split by : and remove spaces
    password = (cred_tag[1].split(":")[1]).strip()
    return username,password

def login_func(username,password,driver,login_link):
    """
    this function get username and passeord and make login at the login page
    input: username, password
    return: login status
    """
    #go to login page
    driver.get(login_link)
    
    #try to do post, this is not working 
    """
    #post request
    data = {'username':username,'password':password}
    requests.post(login_link, data=data)
    """
    #working login
    user_lmnt = driver.find_element_by_xpath("/html/body/table/tbody/tr/td[1]/form/div/center/table/tbody/tr/td[1]/table/tbody/tr[1]/td[2]/p/input")
    pass_lmnt = driver.find_element_by_xpath("/html/body/table/tbody/tr/td[1]/form/div/center/table/tbody/tr/td[1]/table/tbody/tr[2]/td[2]/p/input")
    #write credential for login
    user_lmnt.send_keys(username)
    pass_lmnt.send_keys(password)
    #press login button
    driver.find_element_by_xpath("/html/body/table/tbody/tr/td[1]/form/div/center/table/tbody/tr/td[1]/table/tbody/tr[3]/td[2]/p/input").click()
    
    #get status from tag
    status = driver.find_element_by_xpath('/html/body/table/tbody/tr/td[1]/big/blockquote/blockquote/font/center/b').text
    return status
   
    
def main():
    
    if install_status == 0:
        #import needed from selenium
        from selenium import webdriver

  
        #get driver to use chrome
        driver = webdriver.Chrome('./chromedriver')
        #open given link
        driver.get("http://thedemosite.co.uk/")

        #gets all a tag(tags with link in it) in page 
        #for each tag check if it is add a user page or login page
        #if it is one of them it save it in a variable 
        add_link = ""
        login_link = ""
        for linktag in driver.find_elements_by_xpath('.//a'):
            if "addauser.php" in linktag.get_attribute('href'):
                add_link = linktag.get_attribute('href')
            elif "login.php" in linktag.get_attribute('href'):
                login_link = linktag.get_attribute('href')


        #get credential
        username,password = get_cred(driver,add_link)
        #making login
        status = login_func(username,password,driver,login_link)
        #if login failed stop running
        if status != "**Successful Login**":
            print("login failed")
            pass 
      
        #go back to add a user page
        driver.get(add_link)
        #setting new credentials
        username = 'Hello'
        password = 'world'
        #getting the form to feel 
        user_lmnt = driver.find_element_by_xpath("/html/body/table/tbody/tr/td[1]/form/div/center/table/tbody/tr/td[1]/div/center/table/tbody/tr[1]/td[2]/p/input")
        pass_lmnt = driver.find_element_by_xpath("/html/body/table/tbody/tr/td[1]/form/div/center/table/tbody/tr/td[1]/div/center/table/tbody/tr[2]/td[2]/p/input")
        #write credential to insert
        user_lmnt.send_keys(username)
        pass_lmnt.send_keys(password)
        #submit new user form 
        driver.find_element_by_xpath("/html/body/table/tbody/tr/td[1]/form/div/center/table/tbody/tr/td[1]/div/center/table/tbody/tr[3]/td[2]/p/input").click()
        
        #login with new credential
        login_func(username,password,driver,login_link)
        #if login failed stop running
        if status != "**Successful Login**":
            print("login failed")
            pass 
      
         #close browser at the end
            driver.quit()

if __name__ == "__main__":
    main()