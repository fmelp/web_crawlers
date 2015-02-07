from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import json


url_string = 'https://netimpact.org/jobs'
username = 'melpignanof@gmail.com'
password = '3938pine'
login_page = 'https://netimpact.org/user?destination=jobs'
uastring = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36'

#log in to NetImpact
def crawl(driver):
    driver.get(login_page)
    driver.find_element_by_id('edit-name').send_keys(username)
    enter_pw = driver.find_element_by_id('edit-pass')
    enter_pw.send_keys(password)
    driver.find_element_by_id('edit-submit').click()
    

'''Put info in a list of dictionaries, where each dictionary
    represents a job posting
    format:{
            job_name:
            company:
            type:
            date_posted:
            location:
            description:
            job_url:
            }
'''           
def get_info(driver, all_links):
    list_of_ds = []
    for link in all_links:
        d = {}
        driver.get(link)
        soup = bs(driver.page_source)
        #get job name
        try:
            d['job_name'] = str(soup.select('#page-title')[0].contents[0]).strip()
        except IndexError:
            d['job_name'] = ''
        #get company name
        try:
            company = soup.find_all(class_='field field-name-job-posting-metadata field-type-ds field-label-hidden field-wrapper')[0].find_next(text=True)
            d['company'] = str(company)
        except IndexError:
            d['company'] = ''
        #get type
        try:
            d['type'] = str(soup.find_all(class_='label-above block-title')[1].find_next('p').contents[0])
        except IndexError:
            d['type'] = ''
        #date posted
        try:
            d['date'] = str(soup.find_all(class_='metadata')[0].contents[0])
        except IndexError:
            d['date'] = ''
        #link to actual job application
        try:
            d['job_url'] = str(soup.find_all(class_='label-inline')[0].find_next('a').contents[0])
        except IndexError:
            d['job_url'] = ''
        #description
        try:
            d['description'] = str(soup.find_all(class_='field field-name-body field-type-text-with-summary field-label-hidden field-wrapper body field')[0].contents)
        except IndexError:
            d['description'] = ''
        #city
        try:
            d['city'] = str(soup.find_all(class_='locality')[0].contents[0])
        except IndexError:
            d['city'] = ''
        #state
        try:
            d['state'] = str(soup.find_all(class_='state')[0].contents[0])
        except IndexError:
            d['state'] = ''
        #country
        try:
            d['country'] = str(soup.find_all(class_='country')[0].contents[0])
        except IndexError:
            d['country'] = ''
        try:
            d['post_code'] = str(soup.find_all(class_='postal-code')[0].contents[0])
        except IndexError:
            d['post_code'] = ''
        list_of_ds.append(d)
    return list_of_ds


'''get all urls for all positions.
    get each link from all available pages'''
def get_all_job_links(driver):
    all_links = []
    url = 'https://netimpact.org/jobs?k=&d=-&l='
    driver.get(url)
    soup = bs(driver.page_source)
    while (len(soup.find_all(title='Go to next page')) != 0):
        divs = soup.find_all(class_='views-more-link')
        for i in range(len(divs)):
            all_links.append(str(divs[i]['href']))
        driver.find_element_by_partial_link_text('next').click()
        soup = bs(driver.page_source)
    return all_links


'''save all the data to a file called netimpact_data.json'''
def save_to_json_file(dics):
    fname = 'netimpact_data.json'
    with open(fname, 'w') as fout:
        json.dump(dics, fout, indent=2)

if __name__ == '__main__':
    dcap = webdriver.DesiredCapabilities.PHANTOMJS
    dcap["phantomjs.page.settings.userAgent"] = uastring
    exec_path = '/usr/local/bin/phantomjs'
 #   driver = webdriver.PhantomJS(desired_capabilities=dcap)
    driver = webdriver.PhantomJS(exec_path)
    driver.set_window_size(1024, 768)
    crawl(driver)
    #saves to a file called netimpact_data.json
    save_to_json_file(get_info(driver, get_all_job_links(driver)))
    
