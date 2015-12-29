__author__ = 'yin'

import sys
from urllib import request
from bs4 import BeautifulSoup
import sqlite3
import time
import datetime
import re
import csv

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
infile = open('TotalDoconOnePageTEST.html', 'rb')
html = infile.read()
soup = BeautifulSoup(html)
print(soup)
'''
# first round: parse data from search page and write on csv
PageToList = {}
Page_table = soup.find_all('div', class_ = 'listing')
outfile = open('ListTEST.csv','w', encoding='utf-8',newline='')
writer = csv.writer(outfile)
writer.writerows(['ID','Name','LAT','LNG','RevCnt','StarRating','User'])
for piece in Page_table:
    dataID = piece['data-id']
    dataLAT = piece['data-lat']
    dataLNG = piece['data-lng']
    dataName = piece['data-name']
    dataRevCnt = piece['data-review-count']
    dataStarRating = piece['data-star-rating']
    dataUser = piece['data-user']
    PageToList[dataID] = [dataID, dataName, dataLAT, dataLNG, dataRevCnt, dataStarRating, dataUser]
    writer.writerows(PageToList[dataID])
outfile.close()

print(PageToList)
'''

# Parse each web from search page and visit them

# find individual listed webpages from the general search page
Individualurl = []
SearchPage_table = soup.find_all('h3')

#print(SearchPage_table[0].a['href'])
# ==> /rooms/8091566?s=cfLkGI_G
for Piece in SearchPage_table:
    Individualurl = 'https://www.airbnb.com/' + Piece.a['href']
    IndividualLinks.append(IndividualLink)
print(IndividualLinks)


#IndividualLinkDataFetchingTest
'''
url = 'https://www.airbnb.com//rooms/7574192?s=cfLkGI_G'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
req = request.Request(url=url,headers=headers)
response = request.urlopen(req)
html = response.read()
outfile = open('InvidualPageTEST.html','wb')
outfile.write(html)
outfile.close()

infile = open('InvidualPageTEST.html', 'rb')
html = infile.read()
soup = BeautifulSoup(html)

IndividualList = []  # it should be a dic={}, dic[propertyid] = individualList
Page_table = soup.find_all('div', class_ = 'col-md-6')
IndList1 = Page_table[0].find_all('strong')
IndList2 = Page_table[1].find_all('strong')
for piece in IndList1:
    IndividualList.append(piece.text)
for piece in IndList2:
    IndividualList.append(piece.text)
# After loop1, the values are: Accommodates, Bathrooms, Bed type, Bedrooms, Beds
# After loop2, the additional values are: CheckIn, CheckOut, Property type, Room type
# Still Lack: HostID, DateReserved
print(IndividualList)


#outfile = open('ListTEST.csv','w', encoding='utf-8',newline='')
#writer = csv.writer(outfile)
#writer.writerows(['ID','Name','LAT','LNG','RevCnt','StarRating','User'])
#for piece in Page_table:


#def VisitListWebs():
'''