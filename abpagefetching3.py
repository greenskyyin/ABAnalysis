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
c.execute('CREATE TABLE airbnb (dataID INT, dataName TEXT, dataLAT REAL, dataLNG REAL, dataRevCnt INT, '
          'dataStarRating REAL, UserID INT, WebPage TEXT, Accommodates INT, Bathrooms REAL, BedType TEXT, '
          'Bedrooms REAL, Beds REAL, CheckIn TEXT, CheckOut TEXT, PropertyType TEXT, RoomType TEXT, '
          'CleaningFee INT, SecurityDeposit INT, WeeklyDiscount REAL, MonthlyDiscount REAL, PermitTaxID TEXT)')

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


def RoomPageParse(RoomUrl):
    soup = BeautifulSoup(RoomUrl)
    RmPage_table = soup.find_all('div', class_ = 'col-md-6')
    #print(RmPage_table)
    if len(RmPage_table) < 2:
        print(RmPage_table)
    return RmPage_table

def RoomPageTableParseLong(IndDic, IndList):
    for piece in IndList:
        match = re.search('\$([\w\s\/]+)\=[\d.]+\"\>([\w\d\s\D.]+)\<\/[\w]+\>',str(piece))
        #print(match.group(1), match.group(2)): Accommodates 2
        key = match.group(1)
        value = match.group(2)
        IndDic[key] = value
    return IndDic

def RoomPageTableParseShort(IndDic, IndList):
    for piece in IndList:
        match = re.search('\<[\w]+\>([\w\d\s\D.]+)\<\/[\w]+\>',str(piece))
        #print(match.group(1), match.group(2)): Accommodates 2
        value = match.group(1)
        IndDic['MinimumStay'] = value
    return IndDic

def RoomPageTableforSql(IndDic, writeList):
    RangeList = ['Accommodates', 'Bathrooms', 'Bed type', 'Bedrooms', 'Beds', 'Check In', 'Check Out', 'Property type', 'Room type', 'Cleaning Fee', 'Security Deposit', 'Weekly discount', 'Monthly discount', 'Permit / Tax ID']
    for element in RangeList:
        if element in IndDic:
            writeList.append(IndDic[element])
        else:
            writeList.append('')
    return writeList

def SqlTupleWriting(writeList):
    for i in (2,3,5,9,11,12):
        if writeList[i] == '':
            writeList[i] = None
        else:
            writeList[i] = float(writeList[i])
    for i in (19,20):
        if writeList[i] == '':
            writeList[i] = None
        else:
            writeList[i] = float(writeList[i][:-1])/100
    for i in (0,4,6,8):
        if writeList[i] == '':
            writeList[i] = None
        else:
            writeList[i] = int(writeList[i])
    for i in (17,18):
        if writeList[i] == '':
            writeList[i] = None
        else:
            writeList[i] = int(writeList[i][1:])
    SqlTuple = (writeList[0], writeList[1], writeList[2], writeList[3], writeList[4],writeList[5], writeList[6], writeList[7], writeList[8], writeList[9], writeList[10], writeList[11], writeList[12], writeList[13], writeList[14], writeList[15], writeList[16], writeList[17], writeList[18], writeList[19], writeList[20], writeList[21])
    return SqlTuple

def dataEntry(SqlList):
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    for SqlTuple in SqlList:
        c.execute('INSERT INTO airbnb VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', SqlTuple)
        conn.commit()


def main():
    SqlList = []
    html = fetchweb("https://www.airbnb.com/s/New-York--NY")
    PageToDic = SearchPageParse(html)
    for dataID in PageToDic:
        RoomUrl = PageToDic[dataID][-1]
        RmPageTable = RoomPageParse(fetchweb(RoomUrl))
        IndList_list = []
        for item in RmPageTable:
            strongFound = item.find_all('strong')
            strongWOSpan = []
            for i in strongFound:
                if not i.find_all('span'):
                    #print("@@@@@",i)
                    strongWOSpan.append(i)
                #else:
                    #print("%%%%%", i)
            if strongWOSpan != []:
                IndList_list.append(strongWOSpan)

        IndDic = {}
        for IndList in IndList_list[0:-2]:
            IndDic = RoomPageTableParseLong(IndDic, IndList)
        IndDic = RoomPageTableParseShort(IndDic, IndList_list[-1])
        #print(IndDic)
        writeList = RoomPageTableforSql(IndDic, PageToDic[dataID])
        print(writeList)
        SqlTuple = SqlTupleWriting(writeList)
        #print(len(SqlTuple))
        SqlList.append(SqlTuple)
        print(SqlList)
    dataEntry(SqlList)
# After loop1, the values are: Accommodates, Bathrooms, Bed type, Bedrooms, Beds
# After loop2, the additional values are: CheckIn, CheckOut, Property type, Room type
# After loop3, the additional values are: Extra people, Weekly discount
# After loop4, the additional values are: Monthly discount, Cancellation
# After loop5, the additional values are: Minimum Stay & loop 5 has different Regular expression: <strong>2 nights</strong>
# Still Lack: DateReserved


'''

infile = open('TotalDoconOnePageTEST.html', 'rb')
html = infile.read()
soup = BeautifulSoup(html)
'''

if __name__ == "__main__":
    main()
