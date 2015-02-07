from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import urllib2, sys
import json


def get_all_job_links():
    all_links = []
    url = 'https://www.internmatch.com/search/internships?geotype=&lat=&lng=&location=&q=&utf8=%E2%9C%93&viewport='
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib2.Request(url,headers=hdr)
    page = urllib2.urlopen(req)
    soup = bs(page)
    while (len(soup.find_all(class_='pageIconLink rightChevron')) != 0):
        divs = soup.find_all(class_='role textLink stopPropagation')
        for i in range(len(divs)):
            all_links.append('https://www.internmatch.com' + str(divs[i]['href']))
        url = 'https://www.internmatch.com' + str(soup.find_all(class_='pageIconLink rightChevron')[0]['href'])
        req = urllib2.Request(url,headers=hdr)
        page = urllib2.urlopen(req)
        soup = bs(page)
    return all_links


'''Put info in a list of dictionaries, where each dictionary
    represents a job posting, and company entry is a dictionary itself
    format:{
            job_name:
            company: {
                        company_name:
                        description:
                        number_of_employees:
                        sector:
                        established:
                        HQ:
                      }
            type:
            date_posted:
            location:
            description:
            job_url:
            }
''' 
def get_info(all_links):
    list_of_ds = []
    companies = {}
    for link in all_links:
        job_dic = {}
        company_dic = {}
        url = link
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = urllib2.Request(url,headers=hdr)
        page = urllib2.urlopen(req)
        soup = bs(page)
        #get job name
        try:
            job_dic['job_name'] = str(soup.find_all(class_='companyInfo')[0].find_next('h1').contents[0])# + str(soup.find_all(class_='facts')[0].find_next('span').contents[0])
        except IndexError:
            job_dic['job_name'] = ''
        #get location
        try:
            job_dic['location'] = str(soup.find_all(class_='facts')[0].find_next('span').contents[0])
        except IndexError:
            job_dic['location'] = ''
        #get type
        try:
            if len(soup.find_all(class_='badge badgeTipper internship')) != 1:
                s = 'Full-time -- Entry-level'
            else:
                s = 'Internship'
            job_dic['type'] = s
        except IndexError:
            job_dic['type'] = ''
        #get date posted
        try:
            job_dic['date_posted'] = str(soup.find_all(class_='facts')[0].find_next('span').find_next('span').find_next('span').contents[0])
        except IndexError:
            job_dic['date_posted'] = ''
        #get job description
        try:
            job_dic['description'] = str(oup.find_all(id='description')[0].get_text())
        except IndexError:
            job_dic['description'] = ''
        #get job link
        #NOTE: YOU NEED AN INTERNMATCH ACCOUNT TO ACCESS
        try:
            job_dic['link'] = 'https://www.internmatch.com' + str(soup.find_all(class_='remoteModal action applyFatRollover trackGAEvent js-apply-button')[0]['href'])
        except IndexError:
            job_dic['link'] = ''

#################################################
            
        #get company name and all of its info
        #this dictionary entry will be a dictionary too so it can contain all the info
        try:
            name = str(soup.find_all(class_='infoLink info')[0].find_next('span').contents[0])
            if name not in companies:
                try:
                    soup.find_all(class_='infoLink info')[0]['href']
                    url = 'https://www.internmatch.com' + str(soup.find_all(class_='infoLink info')[0]['href'])
                    hdr = {'User-Agent': 'Mozilla/5.0'}
                    req = urllib2.Request(url,headers=hdr)
                    page = urllib2.urlopen(req)
                    soup = bs(page)
                    company_dic['company_name'] = name
                    try:
                        company_dic['description'] = str(soup.find_all(class_='description')[0].get_text())
                    except IndexError:
                        company_dic['description'] = ''
                    try:
                        company_dic['number_of_employees'] = str(soup.find_all(class_='quickFacts')[0].find_next('strong').contents[0])
                    except IndexError:
                        company_dic['number_of_employees'] = ''
                    try:
                        company_dic['sector'] = str(soup.find_all(class_='quickFacts')[0].find_next('strong').find_next('strong').contents[0])
                    except IndexError:
                        company_dic['sector'] = ''
                    try:
                        company_dic['established'] = str(soup.find_all(class_='quickFacts')[0].find_next('strong').find_next('strong').find_next('strong').contents[0])
                    except IndexError:
                        company_dic['established'] = ''
                    try:
                        company_dic['HQ'] = str(soup.find_all(class_='quickFacts')[0].find_next('strong').find_next('strong').find_next('strong').find_next('strong').contents[0])
                    except IndexError:
                        company_dic['HQ'] = ''
                except IndexError:
                    company_dic['company_name'] = name
                    company_dic['description'] = ''
                    company_dic['number_of_employees'] = ''
                    company_dic['sector'] = ''
                    company_dic['established'] = ''
                    company_dic['HQ'] = ''
                job_dic['company'] = company_dic
                companies[name] = company_dic
            else:
                job_dic['company'] = companies[name]
        except IndexError:
            job_dic['company'] = ''

        list_of_ds.append(job_dic)
    return list_of_ds

'''save all the data to a file called netimpact_data.json'''
def save_to_json(dics):
    fname = 'internMatch_data.json'
    with open(fname, 'w') as fout:
        json.dump(dics, fout, indent=2)


if __name__ == '__main__':
    save_to_json(get_info(get_all_job_links()))

