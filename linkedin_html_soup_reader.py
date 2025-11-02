import time
import warnings         
import requests
import os
import csv
import numpy as np
import itertools
from pathlib import Path
from bs4 import BeautifulSoup

def get_experience_list(soup):
    
    try:
        experience_div = soup.find('div', {'id': 'experience'})
        experience_list = experience_div.find_next('ul')

        experience_list_itens = [child for child in experience_list.children if child.name]
        
        return experience_list_itens

    except:
        print('Soup not found')
        return None

'''sub-region'''
def get_subregion(soup): # the URL of this section follows a different pattern than the details/experience one
    
    try:
        subregion = soup.find('span', {'class': 'text-body-small inline t-black--light break-words'})
    
        subregion = subregion.get_text(strip=True)
        return subregion
    
    except:
        subregion = 'sub-region not found'

'''current firm name - single job title structure'''
def get_firm_name_single_jobtitle_standard(current_experience):
    
    try:
        current_firm_name = current_experience.find_all_next('span', {'class': 'visually-hidden'})
        current_firm_name = current_firm_name[1].get_text(strip=True)
        return current_firm_name
    
    except:
        current_firm_name = 'current firm name not found'
        return current_firm_name

'''current firm name - multiple job title structure'''
def get_firm_name_multiple_jobtitle_standard(current_experience):
    
    try:
        current_firm_name = current_experience.find_all_next('span', {'class': 'visually-hidden'})
        current_firm_name = current_firm_name[0].get_text(strip=True)
        return current_firm_name
    
    except:
        current_firm_name = 'current firm name not found'
        return current_firm_name

'''start date at current firm - single job title structure'''
def get_start_date_at_fund_single_jobtitle_standard(current_experience):
    
    try:
        start_date_at_fund = current_experience.find_all_next('span', {'class': 'visually-hidden'})
        start_date_at_fund = start_date_at_fund[2].get_text(strip=True)
        return start_date_at_fund

    except:
        start_date_at_fund = 'start date at fund not found'
        return start_date_at_fund

'''start date at current firm - multiple job title structure (standard)'''
def get_start_date_at_fund_multiple_jobtitle_standard(current_experience):
    
    try:
        start_date_at_fund = current_experience.find_all_next('span', {'class': 'visually-hidden'})
        start_date_at_fund = start_date_at_fund[1].get_text(strip=True)
        return start_date_at_fund
    
    except:
        start_date_at_fund = 'start date at fund not found'
        return start_date_at_fund

'''start date at current firm - multiple job title structure (alternative)'''
def get_start_date_at_fund_multiple_jobtitle_standard_alternative(current_experience):
    
    try:
        jobtitle_ul = current_experience.find('ul')
        li_inside_jobtitle_ul = jobtitle_ul.find_all('li')
        first_jobtitle = li_inside_jobtitle_ul[
            (len(li_inside_jobtitle_ul)) -1  # The total number of bullet points minus 1 gives the first job title
        ]

        start_date_at_fund = first_jobtitle.find_all('span', {'class': 'visually-hidden'})
        start_date_at_fund = start_date_at_fund[1].get_text(strip=True)
        return start_date_at_fund

    except:
        start_date_at_fund = 'start date at fund not found'
        return start_date_at_fund

'''job title - single job title structure'''
def get_jobtitle_single_jobtitle_standard(current_experience):
    
    try:
        job_title = current_experience.find_all_next('span', {'class': 'visually-hidden'})
        job_title = job_title[0].get_text(strip=True)
        return job_title
    
    except:
        job_title = 'job title not found'
        return job_title

'''job title - multiple job title structure'''
def get_jobtitle_multiple_jobtitle_standard(current_experience):
    
    try:
        jobtitle_ul = current_experience.find('ul')
        li_inside_jobtitle_ul = jobtitle_ul.find_all('li')
        current_jobtitle = li_inside_jobtitle_ul[0]

        jobtitle = current_jobtitle.find_all('span', {'class': 'visually-hidden'})
        jobtitle = jobtitle[0].get_text(strip=True)
        return jobtitle
    
    except:
        jobtitle = 'job title not found'
        return jobtitle


folder = Path(r"") # insert the path to the folder containing the downloaded HTML files here

files = sorted(
    [f for f in folder.iterdir() if f.is_file() and f.suffix.lower() == ".html"],
    key=lambda f: f.stat().st_ctime
)

csv_data = []

for path in files:
    current_file_name = path.name
    print(f'Reading: {current_file_name}')

    with path.open("r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        print(current_file_name[:-5:]) # skip the '.html' extension             

        subregion = get_subregion(soup)

        # check if the experience list exists
        experience_list = get_experience_list(soup)
        if experience_list == None:
            continue
      
        # check if the current experience has a <ul> inside the <li> (single or multiple job title structure)
        current_firm_ul_check = experience_list[0].find_all('ul')
        if current_firm_ul_check == []:
            
            current_firm_name = get_firm_name_single_jobtitle_standard(experience_list[0])
            jobtitle = get_jobtitle_single_jobtitle_standard(experience_list[0])
            start_date_at_fund = get_start_date_at_fund_single_jobtitle_standard(experience_list[0])
        
        else:
            current_firm_name = get_firm_name_multiple_jobtitle_standard(experience_list[0])
            jobtitle = get_jobtitle_multiple_jobtitle_standard(experience_list[0])
            start_date_at_fund = get_start_date_at_fund_multiple_jobtitle_standard(experience_list[0])

        # check if there is more than one experience
        if len(experience_list) == 1:
            previous_firm_name = "no previous firm found"    
            csv_data.append([current_file_name[:-5:], subregion, current_firm_name, previous_firm_name, jobtitle, start_date_at_fund])   
            continue

        else:
            # check if the previous experience has a <ul> inside the <li> (single or multiple job title structure)
            previous_firm_ul_check = experience_list[1].find_all('ul')
            if previous_firm_ul_check == []:
                previous_firm_name = get_firm_name_single_jobtitle_standard(experience_list[1])
            else:
                previous_firm_name = get_firm_name_multiple_jobtitle_standard(experience_list[1])  
            
    csv_data.append([current_file_name[:-5:], subregion, current_firm_name, previous_firm_name, jobtitle, start_date_at_fund])    


csv_output_location = "" # insert your output location here
with open(csv_output_location, 'w', encoding='utf-8', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['contact_id', 'contact_sub_region', 'current_account_name', 'previous_account_name', 'jobtitle', 'start_date_at_fund'])
    writer.writerows(csv_data)
