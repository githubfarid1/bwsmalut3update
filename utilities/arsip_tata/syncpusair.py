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

def parse(playwright: Playwright):
    url = 'https://arsip-sda.pusair-pu.go.id/admin/archive/2024'
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
            href = trs.nth(idx).locator('td').nth(4).locator("a").get_attribute("href")
            print(boxno, href.split("/")[-1])
            datalist.append({"boxno": boxno, "link": href, "data": {}})
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
        break


    browser.close()
    return datalist    



def main():
    parser = argparse.ArgumentParser(description="UPDATE BOX ID BOT")
    args = parser.parse_args()
    # if not args.input:
    #     print('use: python arsipbot.py -i <filename>')
    #     exit()

    # if args.input[-5:] != '.xlsx':
    #     print('File input have to XLSX file')
    #     exit()
    # page = browser_init()
    with sync_playwright() as playwright:
        datalist = parse(playwright)    
    
    breakpoint()
    # breakpoint()
    print("End Process...")
if __name__ == '__main__':
    main()
