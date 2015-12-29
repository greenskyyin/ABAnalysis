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
'''
# first round: parse data from search page and write on csv
PageToList = {}
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
    dataUser = piece['data-user']
    PageToList[dataID] = [dataID, dataName, dataLAT, dataLNG, dataRevCnt, dataStarRating, dataUser]
    writer.writerow(PageToList[dataID])
outfile.close()

print(PageToList)


# Parse each web from search page and visit them

# find individual listed webpages from the general search page
IndividualurlList = []
SearchPage_table = soup.find_all('h3')
print(SearchPage_table)
#print(SearchPage_table[0].a['href'])
# ==> IndividualLink: '/rooms/8091566?s=cfLkGI_G'
for Piece in SearchPage_table:
    link = Piece.a['href']
    IndividualLink = re.search('([\d]+)\?[\w=]', link)
    DataID = IndividualLink.group(1)
    Individualurl = 'https://www.airbnb.com/' + link
    IndividualurlList.append([DataID,Individualurl])
print(IndividualurlList)


#IndividualLinkDataFetchingTest

url = 'https://www.airbnb.com//rooms/8843995?s=tQ4aHQBR'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
req = request.Request(url=url,headers=headers)
response = request.urlopen(req)
html = response.read()
outfile = open('InvidualPageTEST.html','wb')
outfile.write(html)
outfile.close()
'''

infile = open('InvidualPageTEST.html', 'rb')
html = infile.read()
soup = BeautifulSoup(html)
IndividualList = []
Page_table = soup.find_all('div', class_ = 'col-md-6')
IndList1 = Page_table[0].find_all('strong')
IndList2 = Page_table[1].find_all('strong')
IndList3 = Page_table[2].find_all('strong')
IndList4 = Page_table[3].find_all('strong')
IndList5 = Page_table[4].find_all('strong')
print(IndList1, IndList2, IndList3, IndList4, IndList5)
'''
IndDic = {}
RangeList = ['Accommodates', 'Bathrooms', 'Bed type', 'Bedrooms', 'Beds', 'Check In', 'Check Out', 'Property type', 'Room type']
for piece in IndList1:
    match = re.search('\$([\w\s]+)\=[\d.]+\"\>([\w\d\s\D.]+)\<\/[\w]+\>',str(piece))
    #print(match.group(1), match.group(2)): Accommodates 2
    key = match.group(1)
    value = match.group(2)
    IndDic[key] = value
    #IndividualList.append(piece.text)
for piece in IndList2:
    match = re.search('\$([\w\s]+)\=[\d.]+\"\>([\w\d\s\D.]+)\<\/[\w]+\>',str(piece))
    #print(match.group(1), match.group(2)): Check In 6:00 AM
    key = match.group(1)
    value = match.group(2)
    IndDic[key] = value
#print(IndDic)
#print(RangeList)

for key in IndDic:
    if key == RangeList[0]:
        print(int(IndDic[key]))
    if key == RangeList[1]:
        print(float(IndDic[key]))
    if key == RangeList[2]:
        print(IndDic[key])
    if key == RangeList[3]:
        print(float(IndDic[key]))
    if key == RangeList[4]:
        print(int(IndDic[key]))
    if key == RangeList[5]:
        print(IndDic[key])
    if key == RangeList[6]:
        print(IndDic[key])
    if key == RangeList[7]:
        print('')
    if key == RangeList[8]:
        print(IndDic[key])
    if key == RangeList[9]:
        print(IndDic[key])

for element in RangeList:
    #for b in IndDic:
        #if element == b:
            #print(IndDic[b])
    if element in IndDic:
        print(IndDic[element])
    else:
        print('')

#IndividualList.append(piece.text)
# After loop1, the values are: Accommodates, Bathrooms, Bed type, Bedrooms, Beds
# After loop2, the additional values are: CheckIn, CheckOut, Property type, Room type
# Still Lack: HostID, DateReserved



#outfile = open('ListTEST.csv','w', encoding='utf-8',newline='')
#writer = csv.writer(outfile)
#writer.writerow(['ID','Name','LAT','LNG','RevCnt','StarRating','User'])
#for piece in Page_table:


#def VisitListWebs():
'''