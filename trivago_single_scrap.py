#!/usr/bin/env python

""" trivago_single_scrap.py contains the functionality to execute automated scraping of trivago.com and deliver prices
for hotels in a specific date range
"""

# import
from re import findall,sub
from lxml import html
from time import sleep
from selenium import webdriver
from pprint import pprint
from xvfbwrapper import Xvfb

__author__ = "Cyril Welschen"
__email__ = "cj.welschen@gmail.com"


def parse(url):
    print("Starting")
    searchKey = "Zermatt" # Change this to your city
    checkInDate = "2018-12-21" # Change this to your city
    checkOutDate = "2018-12-23" # Change this to your city
    response = webdriver.Chrome('/home/cyril/Desktop/Hotel_Neu/simple_scrap/chromedriver')
    response.get(url)
    searchKeyElement = response.find_elements_by_xpath('//input[@id="horus-querytext"]')
    searchKeyElement[0].clear()
    searchKeyElement[0].send_keys(searchKey)
    submitButton = response.find_elements_by_xpath('//button[contains(@class, "horus-btn-search")]')
    if submitButton:
        print("Found {} submit button".format(len(submitButton)))
    sleep(1)
    submitButton[0].click()
    sleep(10)
    parser = html.fromstring(response.page_source,response.current_url)
    print(" ")
    print("currently on")
    print(response.current_url)

    checkInOutElements = response.find_elements_by_xpath('//time[contains(@class, "btn-horus__value")]')
    checkIn = checkInOutElements[0]
    check_in_frame = response.find_elements_by_xpath('//time[@datetime="2018-12-21"]')
    if check_in_frame:
        print("check in frame found")
        check_in_frame[0].click()
    sleep(1)
    check_out_frame = response.find_elements_by_xpath('//time[@datetime="2018-12-27"]')
    if check_out_frame:
        print("check in frame found")
        check_out_frame[0].click()
    sleep(1)

    submitButton[0].click()
    sleep(10)
    parser = html.fromstring(response.page_source,response.current_url)
    print(" ")
    print("currently on")
    print(response.current_url)

    hotels = parser.xpath('//li[contains(@class, "item-order__list-item")]')
    print("found {} hotels".format(len(hotels)))
    for hotel in hotels: #Replace 5 with 1 to just get the cheapest hotel
        hotelName = hotel.xpath('.//h3[contains(@class, "name__copytext")]')
        if len(hotelName) > 0:
            print(hotelName[0].text_content())
        prices = hotel.xpath('.//strong[contains(@class, "deals__price")]')
        nr_of_prices = len(prices)
        if nr_of_prices > 0:
            print(nr_of_prices)
            # print(prices[0].text_content())
            print([prices[i].text_content() for i in range(nr_of_prices)])
    print("done")

if __name__ == '__main__':
    vdisplay = Xvfb()
    vdisplay.start()
    parse('http://www.trivago.com')
    vdisplay.stop()