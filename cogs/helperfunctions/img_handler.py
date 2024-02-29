from playwright.async_api import async_playwright
import pytesseract.pytesseract
from datetime import datetime, timedelta
import cv2 as cv
import os
import logging

# Get the directory of the current Python file
current_directory = os.path.dirname(os.path.abspath(__file__))


async def get_screenshots():
    #with sync_playwright() as p:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://www.mmoga.com")
        locator_timer_frame = page.locator("ul#mainDealCountdown")
        #locator_banner = page.locator("div.swiper-slide").nth(5)
        #locator_banner.wait_for(timeout=2000)
        await page.wait_for_timeout(2000)
        locator_deals = page.locator("div.row").nth(0)
        await locator_timer_frame.scroll_into_view_if_needed()
        await locator_timer_frame.screenshot(path = os.path.join(current_directory, "./images/timer.png"))
        current_time = datetime.now()
        await locator_deals.screenshot(path = os.path.join(current_directory, "./images/deals.png"), mask=[locator_timer_frame], mask_color="gray")
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



    #return modify_cropped_images(cropped_images)
    return(cropped_images)


#def modify_cropped_images(cropped_images):
#
#    modified_cropped_images = []
#
#    for img in cropped_images:
#        modified_img = img
#        modified_cropped_images.append(modified_img)
#
#    return modified_cropped_images


async def get_rem_time():
    img = cv.imread(os.path.join(current_directory, "./images/timer.png"), cv.IMREAD_GRAYSCALE)
    splitted_imgs = img_split(img)

    time = []
    if len(splitted_imgs) < 3:
        logging.warning(f"3 numbers needs to be cropped! Only {len(splitted_imgs)}")


    for counter, i in enumerate(splitted_imgs):
        cv.imwrite(f"{counter}.png", i)
        
        
        try:
            int_conv = int(pytesseract.image_to_string(i, config='--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789'))
        except ValueError:
            logging.warning("One Number from Timer wasn't recognized. Value will be assumed as 44")
            int_conv = 44

        time.append(int_conv)

    #print (reversed(time))
    #print("Everything worked!")
    return time


async def calculate_end_deal__time(current_time, time):
    deal_end_time = current_time  + timedelta(hours=time[2], minutes=time[1], seconds=time[0])
    #print(deal_end_time.isoformat(timespec='seconds'))
    return deal_end_time#.isoformat(timespec='seconds')


async def prepare_deal_imgs():
    current_time = await get_screenshots()
    #print(current_time)
    time = await get_rem_time()
    #print(time)
    return await calculate_end_deal__time(current_time, time)

if __name__ == '__main__':
    prepare_deal_imgs()
    
    
    