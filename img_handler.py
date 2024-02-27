from playwright.sync_api import expect, sync_playwright
import pytesseract.pytesseract
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import cv2 as cv

def get_screenshots():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.mmoga.com")
        locator_timer_frame = page.locator("ul#mainDealCountdown")
        #locator_banner = page.locator("div.swiper-slide").nth(5)
        #locator_banner.wait_for(timeout=2000)
        page.wait_for_timeout(2000)
        locator_deals = page.locator("div.row").nth(0)
        expect(locator_timer_frame).to_be_visible()
        locator_timer_frame.scroll_into_view_if_needed()
        locator_timer_frame.screenshot(path = "timer.png")
        current_time = datetime.now()
        locator_deals.screenshot(path = "deals.png", mask=[locator_timer_frame], mask_color="gray")
    return current_time


def img_split(img):
    assert img is not None, "file could not be read, check with os.path.exists()"
    _, thresh = cv.threshold(img,200,255,0)
    contours, _ = cv.findContours(thresh, 1, 2)

    cropped_images = []
    threshhold_area = 100
    for cnt in contours:
        area = cv.contourArea(cnt)
        if area > threshhold_area and len(cropped_images) < 3:
            x,y,w,h = cv.boundingRect(cnt) 
            cropped_images.append(img[y:y+h, x:x+w])

    return cropped_images



def get_rem_time():
    img = cv.imread('timer.png', cv.IMREAD_GRAYSCALE)
    splitted_imgs = img_split(img)

    time = []

    for counter, i in enumerate(splitted_imgs):
        #cv.imwrite(f"{counter}.png", i)
        time.append(int(pytesseract.image_to_string(i, config='--psm 6 --oem 1 -c tessedit_char_whitelist=0123456789')))

    #print (reversed(time))
    return time


def calculate_end_deal__time(current_time, time):
    deal_end_time = current_time  + timedelta(hours=time[2], minutes=time[1], seconds=time[0])
    print(deal_end_time.isoformat(timespec='seconds'))

if __name__ == '__main__':
    current_time = get_screenshots()
    time = get_rem_time()
    calculate_end_deal__time(current_time, time)
    
    