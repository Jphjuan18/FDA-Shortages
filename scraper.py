
# scrape_web collects and filters data then creates a pandas dataframe 
def scrape_web():   
    from bs4 import BeautifulSoup as bs
    import requests as req
    import pandas as pd
    import re

    res = req.get('https://www.accessdata.fda.gov/scripts/drugshortages/')

    B_URL = 'https://www.accessdata.fda.gov/scripts/drugshortages/'
   
    soup = bs(res.content,features = 'lxml')
    divs = soup.find_all(['tbody'])
    #print(divs)
    divs = divs[0].find_all('tr')
    #print(type(soup))
    #print(type(divs))
    #print(len(divs))

    status_l = []
    count = 0
    while count < len(divs):
        for i in divs[count].find_all('strong'):
            status_l.append(i)
            count += 1

    status_f = []
    for i in status_l:
        w = i.string.strip()
        status_f.append(w)

    href_l = []
    title_l = []
    count = 0
    subcount = 0
    while count < len(divs):
        for i in divs[count].find_all('a'):
                i.find_all('a')
                href = i.get('href')
                href_l.append(href)
                title = i.get('title')
                title_l.append(title)
                subcount +=1
        if subcount == 2:
                subcount = 0
                count += 1

    href_f = []
    for i in range(1,len(divs)*2,2):
        words = href_l[i].split(' ')
        wordsjoin = '%20'.join(words)
        href_f.append(wordsjoin)
        #print(wordsjoin)
        #print(i)

    S_URL = 'https://www.accessdata.fda.gov/scripts/drugshortages/'
    
    href_link = []
    for i in href_f: 
        href_link.append(S_URL + i)

    title_f = []
    for i in range(1,len(divs)*2,2):
        q = title_l[i]
        w = q.replace(' detail', '')
        title_f.append(re.sub('Link to ', '', w))  

    subs = {'Drug': [], 'Link':[],'Status':[]}   

    subs['Drug'] = title_f
    subs['Link'] = href_link
    subs['Status'] = status_f 

    #Create a new dataframe
    sub_df = pd.DataFrame(subs, columns=['Drug','Link','Status'])
    print('sub_df Created')

    return sub_df