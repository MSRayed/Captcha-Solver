import time
import pytesseract
import cv2
from pytesseract import image_to_string
from selenium import webdriver
from selenium.webdriver import ActionChains


PATH = "C:\/Users\/Rayed\/Downloads\/Programs\/chromedriver.exe"
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Rayed\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

# Global variables
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
# Driver
driver = webdriver.Chrome(options=options, executable_path=PATH)
driver.get("https://ipindiaonline.gov.in/eregister/eregister.aspx")

write_file = "captcha.jpg"


def find_captcha_img():
    # Get the navigating button to go to the required page
    driver.switch_to.frame("eregoptions")
    tdm_index_button = driver.find_element_by_css_selector("#web-buttons-idgsuam > tbody > tr:nth-child(2) > td > a")

    # Actions to click the button
    actions = ActionChains(driver)
    actions.click(on_element=tdm_index_button)
    actions.perform()

    # Get the captcha finally
    driver.switch_to.default_content()
    driver.switch_to.frame("showframe")
    captcha = driver.find_element_by_id("ImageCaptcha").get_attribute("src")

    return captcha


def detect_captcha():
    # Processing the image
    image = cv2.imread("captcha.jpg")
    h, w = image.shape[:2]
    cv2.imshow("img", image)
    image = cv2.resize(image, (w*4, h*4))
    cv2.imshow("image", image)
    image = cv2.threshold(image, 0, 255, cv2.THRESH_TRUNC)[1]
    cv2.imshow("image thresh", image)

    text = image_to_string(image)
    print(text)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return text


def save_image(image_link):
    with open(write_file, "wb") as file:
        file.write(driver.find_element_by_css_selector("#ImageCaptcha").screenshot_as_png)


def enter_code(code):
    input_box = driver.find_element_by_id("txtCaptcha")
    input_box.send_keys(code)


# Find the captcha
captcha_img = find_captcha_img()

# Save the captcha
save_image(captcha_img)

# Detect the captcha
captcha_code = detect_captcha()

enter_code(captcha_code)

time.sleep(5)
driver.close()
