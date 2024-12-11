from playwright.sync_api import sync_playwright, Playwright
import json
from sqlalchemy import create_engine, Column, Integer, String, SmallInteger, Text, CHAR
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, Session
from sqlalchemy.orm import mapped_column
# from sqlalchemy.orm import relationship
import argparse
import os
import sys
from settings import *
from dbclass import Bundle, Base, Box, Item
import time

engine = create_engine('mysql+pymysql://{}:{}@localhost:{}/{}'.format(USER, PASSWORD, PORT, DBNAME) , echo=False)

def parse(playwright: Playwright, start: int, end: int, year: int):
    url = 'https://arsip-sda.pusair-pu.go.id/admin/archive/{}'.format(year)
    username = PUSAIR_USER
    password = PUSAIR_PASSWORD
    firefox = playwright.firefox
    browser = firefox.launch(headless=True)
    page = browser.new_page()
    page.goto(url, wait_until="networkidle")
    page.fill('input[name="login"]', username)
    page.fill('input[name="password"]', password)
    page.click('text=Log in', timeout=20000)
    datalist = []
    while True:
        page.wait_for_selector("ul.pagination")
        page.get_by_label('Show').select_option('100')
        trs = page.locator("tbody > tr")
        trscount = trs.count()
        
        for idx in range(0, trscount):
            # print(trscount)
            boxno = trs.nth(idx).locator('td').nth(1).locator("h6").inner_text()
            if int(boxno) >= start and int(boxno) <= end:
                href = trs.nth(idx).locator('td').nth(4).locator("a").get_attribute("href")
                print(boxno, href.split("/")[-1])
                datalist.append({"boxno": boxno, "link": href, "year": year, "data": {}})
        time.sleep(0.5)    
        try:
            # breakpoint()
            page.wait_for_selector("li[class='paginate_button page-item next disabled']", timeout=1000)
            break
        except:
            page.click("li[id='dt-box-year_next']", timeout=1000)

        


    for idx, data in enumerate(datalist):
        # breakpoint()
        page.goto("https://arsip-sda.pusair-pu.go.id{}".format(data["link"]), wait_until="networkidle")

        while True:
            page.wait_for_selector("ul.pagination")
            page.get_by_label('Show').select_option('100')
            trs = page.locator("tbody > tr")
            trscount = trs.count()
            ke = 0
            for idx2 in range(0, trscount):
                # breakpoint()
                tds = trs.nth(idx2).locator("td")
                # breakpoint()
                try:
                    berkasno = tds.nth(1).inner_text()
                    urutno = tds.nth(2).inner_text()
                    href =  tds.nth(7).locator("a").nth(1).get_attribute('href')
                    print(berkasno, urutno, href.split("/")[-2])
                    datalist[idx]["data"][ke] = {"noberkas": berkasno, "nourut": urutno, "id": href.split("/")[-2]}
                except:
                    # breakpoint()
                    break
                ke += 1
            time.sleep(0.5)
            
            try:
                # breakpoint()
                page.wait_for_selector("li[class='paginate_button page-item next disabled']", timeout=1000)
                break
            except:
                page.click("li[id='dt-box-year_next']", timeout=1000)
            # breakpoint()
        # break


    browser.close()
    return datalist    



def main():
    parser = argparse.ArgumentParser(description="UPDATE BOX ID BOT")
    parser.add_argument('-s', '--start', type=str,help="Start Box Number")
    parser.add_argument('-e', '--end', type=str,help="End Box Number")
    parser.add_argument('-t', '--year', type=str,help="Year")

    args = parser.parse_args()
    if not args.start or not args.end or not args.year:
        print("use command python syncpusair.py -s [start_box] -e [end_box] -t [year]")
        sys.exit()
    session = Session(engine)
    with sync_playwright() as playwright:
        datalist = parse(playwright, start=int(args.start), end=int(args.end), year=int(args.year))    
    
    for data in datalist:
        session.query(Box).filter(Box.box_number==data["boxno"], Box.yeardate==data["year"]).update({'token': str(data["link"]).split("/")[-1]})
        for detail in data["data"]:
            session.query(Item).filter(Item.item_number==detail["nourut"], Item.yeardate==data["year"]).update({'token': detail["id"]})
    jawab = input("Simpan Perubahan (Y/N)?")
    if jawab == 'Y' or jawab == 'y':
        session.flush()
        session.commit()

    print("End Process...")
if __name__ == '__main__':
    main()
