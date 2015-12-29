__author__ = 'yin'

import sys
from urllib import request
from bs4 import BeautifulSoup
import sqlite3
import time
import datetime
import re
import csv

conn = sqlite3.connect('test.db')
c = conn.cursor()
c.execute('CREATE TABLE stocks (dataID INT, dataName TEXT, dataLAT REAL, dataLNG REAL, dataRevCnt INT, '
          'dataStarRating REAL, UserID INT, WebPage TEXT, Accommodates INT, Bathrooms REAL, BedType TEXT, '
          'Bedrooms REAL, Beds REAL, CheckIn TEXT, CheckOut TEXT, PropertyType TEXT, RoomType TEXT)')

'''
url = 'https://www.airbnb.com/s/New-York--NY'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
req = request.Request(url=url,headers=headers)
response = request.urlopen(req)
html = response.read()
#print(html)
#soup = BeautifulSoup(html)
outfile = open('TotalDoconOnePageTEST.html','wb')
outfile.write(html)
outfile.close()
'''

def fetchweb(url):
    time.sleep(5)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    req = request.Request(url=url,headers=headers)
    response = request.urlopen(req)
    html = response.read()
    return html

# first round: parse data from search page and write on csv
# find individual listed webpages from the general search page
def SearchPageParse(Html):
    soup = BeautifulSoup(Html)
    PageToDic = {}
    Page_table = soup.find_all('div', class_ = 'listing')
    outfile = open('ListTEST.csv','w', encoding='utf-8',newline='')
    writer = csv.writer(outfile)
    writer.writerow(['ID','Name','LAT','LNG','RevCnt','StarRating','User'])
    for piece in Page_table:
        dataID = piece['data-id']
        dataLAT = piece['data-lat']
        dataLNG = piece['data-lng']
        dataName = piece['data-name']
        dataRevCnt = piece['data-review-count']
        dataStarRating = piece['data-star-rating']
        dataUserID = piece['data-user']
        PageToDic[dataID] = [dataID, dataName, dataLAT, dataLNG, dataRevCnt, dataStarRating, dataUserID]
        writer.writerow(PageToDic[dataID])
    outfile.close()
    #print(PageToDic)

    SearchPage_table = soup.find_all('h3')
    #print(SearchPage_table[0].a['href'])
    # ==> /rooms/8091566?s=cfLkGI_G
    for Piece in SearchPage_table:
        Link = Piece.a['href']
        LinkParse = re.search('([\d]+)\?[\w=]', Link)
        DataID = LinkParse.group(1)
        RoomUrl = 'https://www.airbnb.com/' + Piece.a['href']
        RoomUrlList = [DataID, RoomUrl]
        for key in PageToDic:
            if key == RoomUrlList[0]:
                PageToDic[key].append(RoomUrlList[1])
                #print("#############\n")
    #print(PageToDic)
    return PageToDic


def RoomPageParse(IndividualUrl,writeList):
    soup = BeautifulSoup(IndividualUrl)
    IndividualUrl = []
    Page_table = soup.find_all('div', class_ = 'col-md-6')
    #print(Page_table)
    if len(Page_table) < 2:
        print(Page_table)
    IndList1 = Page_table[0].find_all('strong')
    IndList2 = Page_table[1].find_all('strong')
    for piece in IndList1:
        writeList.append(piece.text)
    for piece in IndList2:
        writeList.append(piece.text)
        if piece.text == '':
            writeList.append('')
# After loop1, the values are: Accommodates, Bathrooms, Bed type, Bedrooms, Beds
# After loop2, the additional values are: CheckIn, CheckOut, Property type, Room type
# Still Lack: DateReserved
    print(writeList)
    return(writeList)

def main():
    html = fetchweb("https://www.airbnb.com/s/New-York--NY")
    PageToDic = SearchPageParse(html)
    for dataID in PageToDic:
        RoomPageParse(fetchweb(PageToDic[dataID][-1]),PageToDic[dataID])


'''
infile = open('TotalDoconOnePageTEST.html', 'rb')
html = infile.read()
soup = BeautifulSoup(html)
'''

if __name__ == "__main__":
    main()
