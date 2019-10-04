from urllib.request import urlopen
import requests
import time
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re

testLink = "https://www.list-org.com/company/131049"

fileCompanies = "companies.txt"
fileXML = "data.xml"

listNextPageFullTag = []
listNextPageHref = []

listRegionFullTag = []
listRegionHref = []

listCompanyFullTag = []
listCompanyHref = []

listPreviousLink = []

headers = {
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q-0.8"
}

mainSite = "https://www.list-org.com"

def GetPage(url):
    time.sleep(3)
    session = requests.Session()
    try:
        html = session.get(url, headers=headers)
    except HTTPError:
        return None
    
    try:
        bsObjPage = BeautifulSoup(html.text, "lxml")
    except AttributeError:
        return None

    return bsObjPage

def GetRegions(page):
    listRegionFullTag = page.find("div", {"class":"content"}).findAll("a")

    for a in listRegionFullTag:
        listRegionHref.append(a.attrs['href'])

def FindBalance(page):
    if page.find(text="Доходы") != None:
        result = []

        year = page.find(text="Доходы").parent.parent.nextSibling
        
        while year != None:
            obj = str(year.encode('utf-8'))
            
            fullStrings = re.findall(r'<td.*?>(.*?)</td>', obj)
            
            for a in fullStrings:
                if a.find('i') > -1:
                    b = re.findall(r'(.*?)<i.*?>', a)
                    b = b[0]
                else:
                    b = a
                result.append(b)

            year = year.nextSibling
            print(result)
    else:
        result = "Нет информации о доходах"

    return result

def FindCompaniesOnPage(page):
    listNextPageFullTag = page.findAll("a", {"class":"pgn_a"})

    for a in listNextPageFullTag:
        if a.attrs['href'] not in listNextPageHref:
            listNextPageHref.append(a.attrs['href'])

    listCompanyFullTag = page.find("div", {"class":"org_list"}).findAll("a")

    if listCompanyFullTag is None:
        print('error')
    else:
        for a in listCompanyFullTag:
            if a.attrs['href'] not in listCompanyHref:

                currentCompany = GetPage(mainSite + a.attrs['href'])

                balance = FindBalance(currentCompany)

                # listCompanyHref.append(a.attrs['href']) # add into list, the same into file


                f = open(fileCompanies, 'a')
                # TODO: find company info
                f.write("--------------------------------------------------------------------------------" + '\n\r')

                f.write(a.get_text() + " --- " + a.attrs['href'] + '\n\r')
                i = 1
                if type(balance) is str:
                    f.write(balance + '\n\r')
                else:
                    f.write("Год" + '\t' + "Доходы" + '\t' + "Расходы" + '\t' + "Доходы - Расходы" + '\n\r')
                    for item in balance:
                        if i & 4:
                            f.write('\n\r')
                        else:
                            f.write(item + '\t') 
                f.close()

def main():
    page = GetPage("https://www.list-org.com/list?okato=63202801&page=2")
    
    if page == None:
        print("Page couldn't be found")
    else:
        GetRegions(page)
        
        for regionLink in listRegionHref:
            newPage = GetPage(mainSite + regionLink)

            listNextPageHref.append(regionLink)
            
            f = open(fileCompanies, 'a')
            f.write(mainSite + regionLink + '\n\r')
            f.close

            for a in listNextPageHref:
                print("link_a = " + a)

                if a not in listPreviousLink:
                    newPage = GetPage(mainSite + a)
                    FindCompaniesOnPage(newPage)

                    listPreviousLink.append(a)
            
            
def test(page):
    testCompanyElement = GetPage(page)
    balance = FindBalance(testCompanyElement)
    i = 1
    if type(balance) is str:
        print(balance + '\n\r')
    else:
        print("Год" + '\t' + "Доходы" + '\t\t' + "Расходы" + '\t\t' + "Доходы - Расходы" + '\n\r')
        for item in balance:
            print(item + '\t', end='') 

# количество работников
# уставный капитал
# сумма гос контрактов
# наличие гос контрактов

        # for a in allLinksList:
        #     y = a.findAll("a")
        #     for t in y:
        #         print(t.get_text())

    

# main()

test(testLink)
