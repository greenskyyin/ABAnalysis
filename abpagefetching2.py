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
conn = sqlite3.connect('test.db')
c = conn.cursor()
c.execute('CREATE TABLE airbnb (dataID INT, dataName TEXT, dataLAT REAL, dataLNG REAL, dataRevCnt INT, '
          'dataStarRating REAL, UserID INT, WebPage TEXT, Accommodates INT, Bathrooms REAL, BedType TEXT, '
          'Bedrooms REAL, Beds REAL, CheckIn TEXT, CheckOut TEXT, PropertyType TEXT, RoomType TEXT, '
          'CleaningFee TEXT, SecurityDeposit TEXT, WeeklyDiscount REAL, MonthlyDiscount REAL, Permit/TaxID TEXT)')


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


def RoomPageParse(IndividualHtml,writeList):
    soup = BeautifulSoup(IndividualHtml)
    Page_table = soup.find_all('div', class_ = 'col-md-6')

    IndList_list = []

    for item in Page_table:
        strongFound = item.find_all('strong')
        strongWOSpan = []
        for i in strongFound:
            if not i.find_all('span'):
                print("@@@@@",i)
                strongWOSpan.append(i)
            else:
                print("%%%%%", i)
        IndList_list.append(strongWOSpan)

    #print(Page_table)
    if len(Page_table) < 2:
        print(Page_table)
    IndList1 = Page_table[0].find_all('strong')
    IndList2 = Page_table[1].find_all('strong')
    IndList3 = Page_table[2].find_all('strong')
    IndList4 = Page_table[3].find_all('strong')
    IndList5 = Page_table[4].find_all('strong')
    """
    IndDic = {}
    RangeList = ['Accommodates', 'Bathrooms', 'Bed type', 'Bedrooms', 'Beds', 'Check In', 'Check Out', 'Property type', 'Room type', 'Cleaning Fee', 'Security Deposit', 'Weekly discount', 'Monthly discount', 'Permit / Tax ID']
    print(type(IndList3))
    print(IndList3)
    print ('33333333333333333')
    print(IndList4)
    print ('444444444444444444444')
    print(IndList5)
    print ('555555555555555555555')
    """
'''
    for piece in IndList1:
        match = re.search('\$([\w\s]+)\=[\d.]+\"\>([\w\d\s\D.]+)\<\/[\w]+\>',str(piece))
        #print(match.group(1), match.group(2)): Accommodates 2
        key = match.group(1)
        value = match.group(2)
        IndDic[key] = value
    for piece in IndList2:
        #writeList.append(piece.text)
        match = re.search('\$([\w\s]+)\=[\d.]+\"\>([\w\d\s\D.]+)\<\/[\w]+\>',str(piece))
        #print(match.group(1), match.group(2)): Check In 6:00 AM
        key = match.group(1)
        value = match.group(2)
        IndDic[key] = value
    for piece in IndList3:
        #writeList.append(piece.text)
        match = re.search('\$([\w\s\/]+)\=[\d.]+\"\>([\w\d\s\D.]+)\<\/[\w]+\>',str(piece))
        #print(match.group(1), match.group(2)): Cleaning Fee $9
        if match == None:
            print(piece)
            continue
        key = match.group(1)
        value = match.group(2)
        IndDic[key] = value
    for piece in IndList4:
        #writeList.append(piece.text)
        match = re.search('\$([\w\s\/]+)\=[\d.]+\"\>([\w\d\s\D.]+)\<\/[\w]+\>',str(piece))
        #print(match.group(1), match.group(2)): Weekly discount 0%; Permit / Tax ID: STR-0000527
        if match == None:
            print(piece)
            continue
        key = match.group(1)
        value = match.group(2)
        IndDic[key] = value
    for piece in IndList5:
        #writeList.append(piece.text)
        match = re.search('\<[\w]+\>([\w\d\s\D.]+)\<\/[\w]+\>',str(piece))
        #print(match.group(1)): 2
        if match == None:
            print(piece)
            continue
        value = match.group(1)
        IndDic['MinimumStay'] = value

    for element in RangeList:
        if element in IndDic:
            writeList.append(IndDic[element])
        else:
            writeList.append('')
    #print(StrList)
# After loop1, the values are: Accommodates, Bathrooms, Bed type, Bedrooms, Beds
# After loop2, the additional values are: CheckIn, CheckOut, Property type, Room type
# Still Lack: DateReserved
    print(writeList)
    return(writeList)
'''
def dataEntry(SqlList):
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute('INSERT INTO airbnb VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', SqlList)
    conn.commit()


def main():
    SqlList = []
    html = fetchweb("https://www.airbnb.com/s/New-York--NY")
    PageToDic = SearchPageParse(html)
    for dataID in PageToDic:
        writeList = RoomPageParse(fetchweb(PageToDic[dataID][-1]),PageToDic[dataID])
        #SqlTuple = (int(writeList[0]), writeList[1], float(writeList[2]), float(writeList[3]), int(writeList[4]),float(writeList[5]), int(writeList[6]), writeList[7], int(writeList[8]), float(writeList[9]), writeList[10], float(writeList[11]), float(writeList[12]), writeList[13], writeList[14], writeList[15], writeList[16])
        #print(len(SqlTuple))
        #SqlList.append(SqlTuple)
        #print(SqlList)
    #dataEntry(SqlList)




'''
infile = open('TotalDoconOnePageTEST.html', 'rb')
html = infile.read()
soup = BeautifulSoup(html)
'''

if __name__ == "__main__":
    main()
