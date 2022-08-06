import requests
from bs4 import BeautifulSoup
import csv
import time

def get_links():
    i=1
    while i<=20:
        r=requests.get(f'https://www.wicpa.org/find-a-cpa?name=&location=&county=&industry=&service=&page={i}')
        soup=BeautifulSoup(r.content,'html5lib')
        a=soup.find('div',attrs={'class':'modules panes'})
        for content in a.find_all('a',attrs={'class':'ga-event'}):
            link='https://www.wicpa.org'+content['href']
            links.append(link)
        i+=1

def export_data():
    try:
        for link in links:
            result={}
            
            r=requests.get(link)
            
            soup=BeautifulSoup(r.content,'html5lib')
            
            result['Firm Name']=soup.find('div',attrs={'class':'col-sm'}).find('h2').text.strip()
            result['Specific Business']=soup.find('div',attrs={'class':'col-sm'}).find('p').text.strip()
            
            address=soup.find('address').text.strip().split()
            address=" ".join(address)
            
            result['Address']=address
            result['City']=soup.find('span',attrs={'class':'city'}).text
            result['State']=soup.find('span',attrs={'class':'state'}).text
            result['Postal Code']=soup.find('span',attrs={'class':'postal_code'}).text
            
            aa=soup.find_all('dd')
            
            phone=''
            fax=''
            website=''
            n=1
            for i in aa:
                if n==1:
                    if i.text.strip()[:2].isdigit():
                        phone=i.text.strip()
                if i.text.strip()=='Visit website':
                    website=i.find('a')['href']
                if n>1:
                    if i.text.strip()[:2].isdigit():
                        fax=i.text.strip()
                n+=1

            result['Phone']=phone
            
            if fax=='':
                result['Fax']='NA'
            else:
                result['Fax']=fax
            
            if website=='':
                result['Website']='NA'
            else:
                result['Website']=website

            print(result)
            results.append(result)
    
    except Exception as e:
        pass

def get_data(results):
    filename='wipca.csv'
    with open(filename,'w',newline="") as f:
        w = csv.DictWriter(f,['Firm Name','Specific Business','Address','City','State','Postal Code','Phone','Fax','Website'])
        w.writeheader()
        for row in results:
            try:
                w.writerow(row)
            except Exception as e:
                continue


st=time.time()
links=[]
results=[]
get_links()
export_data()
get_data(results)
print(len(links))
et=time.time()

print('Total time taken: ',et-st)

