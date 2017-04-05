from bs4 import BeautifulSoup as b_soup
import requests
import os
from time import sleep
import random

# Timeout for connection time
timeout = 10

url_base = 'https://scholar.google.com'
url_scolar = 'https://scholar.google.com/citations?view_op=top_venues&hl=en'
url_top_publication = ''


# Opening file with proxies and creates list of proxies
with open('good_ssl_proxies_2.txt', 'r') as file:
    content = file.readlines()
    proxies_list = [item.replace('\n', '') for item in content]

# Google chrome user agent 
user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'             
headers = {'User_Agent': user_agent} 

def connect(url):
    """ Function for connection to the url
    """
    
    while True:
        print('Number Proxies in list = {}'.format(len(proxies_list)))
        # Choosing random proxy from the list of proxies
        proxy = random.choice(proxies_list)
        proxies = {
              'http': 'https://{}/'.format(proxy),
              'https': 'https://{}/'.format(proxy)
              } 
        
        try:
            # Trying to connect to the url via proxy
            print('\nConnecting, wait 0 - 10 sec...')
            req = requests.get(url, proxies = proxies, headers = headers, timeout = timeout)        
            status = req.status_code
            print('Status Code = {}\n'.format(status))
            
            if status != 200:
                raise Exception
            
        except:  
            # If status code is not == 200, removing bad proxy from the list, random wait and retry connection 
            print('Exception when connecting')         
            proxies_list.remove(proxy)
            print('Sleeping, wait 2 - 6 sec...\n')
            sleep(2 + 4 * random.random())
            
        else:
            # If status code is 200, break the Try loop and exit from the function
            break        
    return req   
 
# Scraping for top h5-index   
req = connect(url_scolar)
print('Top publications\n')
soup = b_soup(req.content, 'html.parser')

table = soup.find('table', id = 'gs_cit_list_table')    
for row in table.find_all('tr')[1:]:
    position = row.find('td', class_ ="gs_pos").text.replace('.', '')
    print('Position = {}'.format(position)) 
    print('Publication = {}'.format(row.find('td', class_ ="gs_title").text))
    print('h5-index = {}'.format(row.find_all('td', class_ = "gs_num")[0].text))  
    print('h5_median = {}'.format(row.find_all('td', class_ = "gs_num")[1].text))
    url_publication = (os.path.join(url_base, row.find('a').get('href').replace('/', ''))).replace('\\', '/')  
    print('URL = {}'.format(url_publication))
    
    # URL of the h5-index is in the position 1
    if position == '1':    
        url_top_publication = url_publication + '&cstart=0'
    print()
    

# Scraping for top publications
print('\n\n\nCited by\n')       
 
step = 20
next_step = 0
position = 1
while True: 
    # Running over pages
    print('URL Top Publication = {}\n'.format(url_top_publication))
    req = connect(url_top_publication)          
    
    soup = b_soup(req.content, 'html.parser')
       
    table = soup.find('table', id = 'gs_cit_list_table')
    rows = table.find_all('tr')[1:] 
    
    # Checking for the last page, if no rows on the page, break the while loop and end the program
    if len(rows) < 1:
        break
    
    for row in rows:
        print('Position = ', position)
        title = row.find('td', class_ ="gs_title")
        print('Article name = {}'.format(title.find('a').text.encode('utf-8')))
        url_to_publication = title.find('a').get('href')
        print('Publication, url = ', url_to_publication)        
        print('Authors = {}'.format(title.find('span', class_ = "gs_authors").text.encode('utf-8')))
        print('Published = {}'.format(title.find('span', class_ = "gs_pub").text))    
        sited_by = row.find_all('td', class_ ="gs_num")[0]
        print('Cited by = {}'.format(sited_by.text))    
        url_sited_by = (os.path.join(url_base, sited_by.find('a').get('href').replace('/', ''))).replace('\\', '/')
        print('Cited by, url = {}'.format(url_sited_by))
        print('Year = {}'.format(row.find_all('td', class_ ="gs_num")[1].text))
        
        position += 1
        print()

    next_step += step     
    url_top_publication = url_top_publication.rsplit('=', 1)[0] + '=' + str(next_step) 
 
    print('\nSleeping, wait 2 - 6 sec...\n')
    sleep(2 + 4 * random.random()) 

print('Scraping Job Done')
