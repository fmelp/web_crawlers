from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import json


uastring = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36'


'''get all urls for all positions
    get each link from each available page'''
def get_all_job_links(driver):
    all_links = []
    url = 'http://www.crunchboard.com/jobs/'
    cb_url = 'http://www.crunchboard.com'
    driver.get(url)
    soup = bs(driver.page_source)
    #all but last page links
    while (len(soup.find_all(text=' Next >')) != 0):
        divs = soup.find_all(class_='JobLink')
        for i in range(1, len(divs)):
            all_links.append(cb_url + str(divs[i]['href']))
        driver.find_element_by_partial_link_text('Next').click()
        soup = bs(driver.page_source)
    #last page links
    divs = soup.find_all(class_='JobLink')
    for i in range(1, len(divs)):
        all_links.append(cb_url + str(divs[i]['href']))
    return all_links


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
            d['job_name'] = soup.find_all('h3')[0].contents[0]
        except IndexError, UnicodeEncodeError:
            d['job_name'] = ''
        #get job category
        try:
            d['category'] = str(soup.find_all(text='Job Category:')[0].parent.find_next('td').contents[1].contents[1].contents[0].contents[1].contents[0]).strip()
        except IndexError:
            d['category'] = ''
        #get experience level
        try:
            d['experience'] = str(soup.find_all(text='Career Level:')[0].parent.find_next('td').contents[1].contents[1].contents[0].contents[1].contents[0]).strip()
        except IndexError:
            d['experience'] = ''
        #get job type
        try:
            d['type'] = str(soup.find_all(text='Job Type:')[0].parent.find_next('td').contents[1].contents[1].contents[0].contents[1].contents[0]).strip()
        except IndexError:
            d['type'] = ''
        #get company name
        try:
            d['company'] = str(soup.find_all(text='Company Name:')[0].parent.find_next('td').contents[1].contents[1].contents[0].contents[1].contents[0]).strip()
        except IndexError:
            d['company'] = ''
        #get city
        try:
            d['city'] = str(soup.find_all(text='City:')[0].parent.find_next('td').contents[1].contents[1].contents[0].contents[1].contents[0]).strip()
        except IndexError:
            d['city'] = ''
        #get country
        try:
            d['country'] = str(soup.find_all(text=' Country:')[0].parent.find_next('td').contents[1].contents[1].contents[0].contents[1].contents[0]).strip()
        except IndexError:
            d['country'] = ''
        #get description (with HTML)
        try:
            d['description'] = str(soup.find_all(style='text-align:justify;')[0])
        except IndexError:
            d['description'] = ''
        #get job url
##        try:
##            
##        except IndexError:
##            d['job_url'] = ''
        list_of_ds.append(d)
#    print len(list_of_ds)
    return list_of_ds

'''save all the data to a file called netimpact_data.json'''
def save_to_json_file(dics):
    fname = 'crunchboard_data.json'
    with open(fname, 'w') as fout:
        json.dump(dics, fout, indent=2)

    

if __name__ == '__main__':
    dcap = webdriver.DesiredCapabilities.PHANTOMJS
    dcap["phantomjs.page.settings.userAgent"] = uastring
    exec_path = '/usr/local/bin/phantomjs'
    driver = webdriver.PhantomJS(exec_path)
    driver.set_window_size(1024, 768)
    save_to_json_file(get_info(driver, get_all_job_links(driver)))
    
