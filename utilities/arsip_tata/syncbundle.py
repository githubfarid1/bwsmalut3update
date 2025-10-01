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

def getboxtoken(page, nobox, url):
    page.goto(url, wait_until="networkidle")
    page.wait_for_selector("ul.pagination")
    page.get_by_label('Show').select_option('100')

    boxtoken = ""
    while True:
        trs = page.locator("tbody > tr")
        trscount = trs.count()

        for idx in range(0, trscount):
            boxno = trs.nth(idx).locator('td').nth(1).locator("h6").inner_text()
            if boxno == nobox:
                boxtoken = trs.nth(idx).locator("a").nth(1).get_attribute('href').split("/")[-1]
                break
        if boxtoken != "":
            break
        try:
            # breakpoint()
            page.wait_for_selector("li[class='paginate_button page-item next disabled']", timeout=1000)
            break
        except:
            page.click("li[id='dt-box-year_next']", timeout=1000)
    
    return boxtoken
def parse():
    while True:
        session = Session(engine)
        bundles = session.query(Bundle).filter(Bundle.syncstatus==2)
        print(bundles.count())
        # breakpoint()
        for bundle in bundles:
            bundledict = {
            "noberkas": str(bundle.bundle_number),
            "thcipta": str(bundle.year_bundle),
            "thtata": str(bundle.yeardate),
            "klasifikasi": bundle.code,
            "nobox": str(bundle.box.box_number),
            "title": bundle.creator,
            "uraian": bundle.description,
            "rak": '1',
            "box_token": bundle.box.token,
            "jenisarsip": "Dinamis",
            "boxid": bundle.box.id
            }
            items = session.query(Item).filter(Item.bundle==bundle)
            itemlist = []
            for idx, item in enumerate(items):
                title = item.title
                if idx == 0:
                    title = item.title + "\n" + bundledict["uraian"]
                if item.accesstype == 'B':
                    acdisp = 'Biasa' 
                elif item.accesstype == 'T':
                    acdisp = 'Terbatas'
                else:
                    acdisp = 'Rahasia'
                itemdict = {
                    "title": title,
                    "total": str(item.total),
                    "item_number": str(item.item_number),
                    "accestype": acdisp,
                    "token": item.token,
                    "bentukarsip": 'Buku',
                    "ket": "COPY",
                    "id": item.id
                }
                itemlist.append(itemdict)
            bundledict["items"] = itemlist
            # print(bundledict)
            
            username = PUSAIR_USER
            password = PUSAIR_PASSWORD
            RAK = '1 - Kelurahan Ngade'
            itemtokenlist = []
            # breakpoint()
            user_data_dir = PLAYWRIGHT_PROFILE
            with sync_playwright() as playwright:
                # browser = playwright.chromium.launch(headless=True)
                # context = browser.new_context()
                # page = context.new_page()
                browser = playwright.chromium.launch_persistent_context(headless=False, user_data_dir=user_data_dir)
                page = browser.new_page()
                url = "https://arsip-sda.pusair-pu.go.id/admin/dashboard"
                page.goto(url, wait_until="networkidle")
                # breakpoint()
                if page.get_by_role("textbox", name="Email or username").count() != 0:
                    page.fill('input[name="login"]', username)
                    page.fill('input[name="password"]', password)
                    page.click('text=Log in', timeout=20000)
                
                boxtoken = ""
                if bundledict['box_token'] == "PROSES" or bundledict['box_token'] == "":
                    url = 'https://arsip-sda.pusair-pu.go.id/admin/archive/{}'.format(bundledict['thtata'])
                    page.goto(url, wait_until="networkidle")
                    boxtoken = getboxtoken(page=page, nobox=bundledict['nobox'], url=url)
                    # breakpoint()
                    if boxtoken == "":
                        url = "https://arsip-sda.pusair-pu.go.id/admin/master/box"
                        page.goto(url, wait_until="networkidle")
                        page.wait_for_selector("input[name='name_box']")
                        page.fill("input[name='name_box']", bundledict['nobox'])

                        page.locator("input[name='year_box']").click()
                        page.keyboard.press("Escape")
                        page.locator("input[name='year_box']").fill(bundledict['thtata'], force=True)

                        page.locator("span[class='select2-selection__rendered']").nth(0).click()
                        page.fill("input[class='select2-search__field']", RAK)
                        page.locator("li[class='select2-results__option select2-results__option--highlighted']").click()
                        submit = page.wait_for_selector("button[type='submit']")
                        # breakpoint()
                        try:
                            submit.click()
                        except:
                            time.sleep(0.5)
                            submit.click()
                        time.sleep(1)
                        # breakpoint()
                        url = 'https://arsip-sda.pusair-pu.go.id/admin/archive/{}'.format(bundledict['thtata'])
                        boxtoken = getboxtoken(page=page, nobox=bundledict['nobox'], url=url)

                else:
                    boxtoken = bundledict['box_token']
                
                session.query(Box).filter(Box.id==bundledict['boxid']).update({'token': boxtoken})
                session.commit()
                for item in bundledict['items']:
                    url = f"https://arsip-sda.pusair-pu.go.id/admin/archive/box/{boxtoken}"
                    page.goto(url, wait_until="networkidle")
                    page.wait_for_selector("ul.pagination")
                    page.get_by_label('Show').select_option('100')
                    trs = page.locator("tbody > tr")
                    trscount = trs.count()
                    itemfound = False
                    # breakpoint()
                    if page.locator("td[class='dataTables_empty']").count() == 0:
                        for idx in range(0, trscount):
                            bundle_number = trs.nth(idx).locator('td').nth(1).inner_text()
                            item_number = trs.nth(idx).locator('td').nth(2).inner_text()
                            token = trs.nth(idx).locator('td').nth(7).locator("a").nth(1).get_attribute('href').split("/")[-2]
                            if bundle_number == bundledict['noberkas'] and item_number == item['item_number']:
                                itemfound = True
                                break
                    if itemfound:
                        url = f"https://arsip-sda.pusair-pu.go.id/admin/archive/{token}/doc"
                        print(f"update {token}")
                    else:
                        url = "https://arsip-sda.pusair-pu.go.id/admin/archive/add"

                    # breakpoint()
                    page.goto(url, wait_until="networkidle")
                    # login(page)
                    page.fill("input[name='file_num']", bundledict['noberkas'])
                    page.fill("input[name='item_num']", item['item_number'])
                    
                    page.locator("input[name='year_file']").click()
                    page.keyboard.press("Escape")
                    page.locator("input[name='year_file']").fill(bundledict["thcipta"], force=True)
                    
                    page.locator("input[name='year_archive']").click()
                    page.keyboard.press("Escape")
                    page.locator("input[name='year_archive']").fill(bundledict['thtata'], force=True)
                    
                    page.locator("span[class='select2-selection__rendered']").nth(1).click()
                    page.fill("input[class='select2-search__field']", bundledict['klasifikasi'])
                    page.locator("li[class='select2-results__option select2-results__option--highlighted']").click()
                    
                    page.locator("span[class='select2-selection__rendered']").nth(2).click()
                    page.fill("input[class='select2-search__field']", f"{bundledict['nobox']} - Rak/Lemari {bundledict['rak']}({bundledict['thtata']})")
                    page.locator("li[class='select2-results__option select2-results__option--highlighted']").click()
                    
                    page.fill("input[name='document_name']", bundledict['title'])
                    page.fill("textarea[name='document_note']", item['title'])
                    page.locator("select[name='daftar_archive']").select_option(item["accestype"])
                    page.locator("select[name='archive_type']").select_option(bundledict["jenisarsip"])
                    page.locator("select[name='satuan']").select_option(item["bentukarsip"])
                    page.fill("input[name='total']", item['total'])
                    page.locator("input[id='inline-{}']".format(item['ket'])).click()
                    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    submit = page.wait_for_selector("button[type='submit']")
                    try:
                        submit.click()
                    except:
                        time.sleep(0.5)
                        submit.click()
                    
                    time.sleep(1)
                    itemtokenlist.append({"id": item['id'], "token":page.url.split("/")[-2]})
            session.query(Bundle).filter(Bundle.id==bundle.id).update({'syncstatus': 3})
            for ditem in itemtokenlist:
                session.query(Item).filter(Item.id==ditem['id']).update({'token': ditem['token']})
            session.commit()
        idletime = 60
        print("Idle", idletime, "Seconds...")
        time.sleep(idletime)

def main():
    while True:
        try:
            parse()
        except:
            time.sleep(60)
            continue
    
if __name__ == '__main__':
    main()
