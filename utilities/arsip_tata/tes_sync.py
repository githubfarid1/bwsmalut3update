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

username = PUSAIR_USER
password = PUSAIR_PASSWORD

user_data_dir = "./playwright_profile"
with sync_playwright() as playwright:
    context = playwright.chromium.launch_persistent_context(headless=False, user_data_dir=user_data_dir)
    page = context.new_page()
    # browser = playwright.chromium.launch(headless=False)
    # context = browser.new_context()
    # page = context.new_page()

    url = "https://arsip-sda.pusair-pu.go.id/admin/dashboard"
    page.goto(url, wait_until="networkidle")
    # breakpoint()
    if page.get_by_role("textbox", name="Email or username").count() != 0:
        page.fill('input[name="login"]', username)
        page.fill('input[name="password"]', password)
        page.click('text=Log in', timeout=20000)
    input("pause")