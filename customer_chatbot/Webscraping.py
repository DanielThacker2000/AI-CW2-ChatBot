import nltk
from nltk import word_tokenize, pos_tag, ne_chunk

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, \
    ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import time
import warnings
from datetime import datetime

warnings.filterwarnings("ignore", category=UserWarning, module="urllib3")

user_agent = 'Chrome/88.0.4324.182 Safari/537.36'
chrome_options = Options()
chrome_options.add_argument(f'user-agent={user_agent}')


def click_cookie(driver):
    try:
        button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
        button.click()
        print('Clicked on cookie consent')
    except Exception as e:
        print('Error clicking on cookie consent:', e)

def click_ga_cookie(driver):
    try:
        button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "CybotCookieDialogBodyLevelButtonLevelOptinAllowAll")))
        button.click()
        print('Clicked on cookie consent')
    except Exception as e:
        print('Error clicking on cookie consent:', e)


def extract_locations(text):
    tokens = word_tokenize(text)
    tagged = pos_tag(tokens)
    entities = ne_chunk(tagged)
    locations = []
    for entity in entities:
        if isinstance(entity, nltk.tree.Tree):
            if entity.label() == 'GPE':  # Geo-Political Entity, often locations
                locations.append(' '.join([child[0] for child in entity]))
    return locations


def click_journey(driver):
    #
    try:
        plan_journey = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="jp-form-preview"]/section/div/button')))
        plan_journey.click()
    except TimeoutException:
        print("Timeout when clicking plan your journey")


def get_user_input():
    departure_location = input("Please enter your departure location: ")
    destination_location = input("Please enter your destination location: ")
    choose_date = input("Please enter your departure date: ")
    choose_hour = input("Please enter your departure hour: ")
    choose_minute = input("Please enter departure minute")
    passenger_number_adult = input("How many adult passengers are there?: ")
    passenger_number_child = input("How many child passengers are there?: ")
    railcard = input("Which railcard do you have?").upper()
    return departure_location, destination_location, choose_date, choose_hour, choose_minute, passenger_number_adult, passenger_number_child, railcard


def departure(driver, origin, destination):
    try:
        board = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="jp-form-preview"]/section/div/button')))
        board.click()
        print('Clicked on departure board')

        for attempt in range(3):
            try:
                origin_input = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'jp-origin')))
                origin_input.clear()
                origin_input.send_keys(origin)

                destination_input = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.ID, 'jp-destination')))
                destination_input.clear()
                destination_input.send_keys(destination)

                print('Entered origin and destination:', origin, destination)
                break
            except StaleElementReferenceException:
                print(f"Stale element reference, retrying {attempt + 1}")

    except TimeoutException:
        print('Departure input not found')
    except Exception as e:
        print('Error occurred during departure input:', e)


def input_locations(driver, departure_location, destination_location):
    # Wait for element to be clickable
    try:
        departure_input = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "jp-origin"))
        )
        departure_input.clear()
        departure_input.send_keys(departure_location)
        print("Departure location entered:", departure_location)
        # Input locations using nlp
        destination_input = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "jp-destination"))
        )
        destination_input.clear()
        destination_input.send_keys(destination_location)
        print("Destination location entered:", destination_location)

    except Exception as e:
        print("Error occurred while inputting locations:", e)


def input_departure_date(driver, choose_date):
    try:
        # Parses the date from a string to a datetime object
        choose_date_obj = datetime.strptime(choose_date, "%d %B %Y")
        target_month = choose_date_obj.strftime("%B %Y")
        # target_day = choose_date_obj.day

        # Open Cal
        date_picker = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "leaving-date"))
        )
        date_picker.click()
        time.sleep(1)

        # Navigate to the correct month PLS
        while True:
            current_month_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'react-datepicker__current-month'))
            )
            current_month = current_month_element.text
            if current_month == target_month:
                break
            next_button = driver.find_element(By.CLASS_NAME, 'react-datepicker__navigation--next')
            next_button.click()
            time.sleep(1)

        # Select the day PLS
        chosen_day = choose_date_obj.strftime('%d')
        day_class_name = f'react-datepicker__day.react-datepicker__day--0{chosen_day}'
        print(day_class_name)
        day_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, day_class_name))
        )
        # day_element = WebDriverWait(driver, 10).until(
        #     EC.element_to_be_clickable(By.CLASS_NAME, "react-datepicker__day.react-datepicker__day--{choose_date_obj.strftime('%d')}"))

        #(By.XPATH, f"//div[contains(@aria-label, '{choose_date_obj.strftime('%A, %d %B %Y')}')]")
        day_element.click()
        time.sleep(1)

        # Check if the date has been set correctly HOPEFULLY PLEASE
        date_input = driver.find_element(By.ID, 'leaving-date')
        current_value = date_input.get_attribute('value')
        print(current_value)
        # if current_value == choose_date:
        #     print("Date inserted successfully:", choose_date)
        # else:
        #     # Use to sending keys if JavaScript isnt working
        #     date_input.click()
        #     # date_input.clear()
        #     date_input.send_keys(Keys.CONTROL, "a")
        #     date_input.send_keys(Keys.DELETE)
        #     date_input.send_keys(choose_date)
        #     print("Date inserted via send_keys:", choose_date)
        #
        #     # Check to see if the date is set correctly
        #     current_value = date_input.get_attribute('value')
        #     if current_value == choose_date:
        #         print("Date inserted successfully via send_keys:", choose_date)
        #     print(f"Failed to insert date. Current value: {current_value}")

    except TimeoutException:
        # Use to sending keys if JavaScript isnt working
        date_input = driver.find_element(By.ID, 'leaving-date')
        date_input.click()
        # date_input.clear()
        date_input.send_keys(Keys.CONTROL, "a")
        date_input.send_keys(Keys.DELETE)
        date_input.send_keys(choose_date)
        print("Date inserted via send_keys:", choose_date)

        # Check to see if the date is set correctly
        current_value = date_input.get_attribute('value')
        if current_value == choose_date:
            print("Date inserted successfully via send_keys:", choose_date)
        print(f"Failed to insert date. Current value: {current_value}")


    except Exception as e:
        print(f"An error occurred: {e}")
        # Use to sending keys if JavaScript isnt working
        date_input = driver.find_element(By.ID, 'leaving-date')
        date_input.click()
        # date_input.clear()
        date_input.send_keys(Keys.CONTROL, "a")
        date_input.send_keys(Keys.DELETE)
        date_input.send_keys(choose_date)
        print("Date inserted via send_keys:", choose_date)

        # Check to see if the date is set correctly
        current_value = date_input.get_attribute('value')
        if current_value == choose_date:
            print("Date inserted successfully via send_keys:", choose_date)
        print(f"Failed to insert date. Current value: {current_value}")


def select_departure_hour(driver, hour):
    try:
        hour_dropdown = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="leaving-hour"]')))
        select = Select(hour_dropdown)
        select.select_by_visible_text(hour)
        print("Selected departure hour:", hour)
    except TimeoutException:
        print("Timeout occurred while waiting for departure hour dropdown")
    except Exception as e:
        print("Error occurred while selecting departure hour:", e)


def select_departure_minute(driver, minute):
    try:
        minute_dropdown = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="leaving-min"]')))
        select = Select(minute_dropdown)
        select.select_by_visible_text(minute)
        print("Selected departure minute:", minute)
    except TimeoutException:
        print("Timeout occurred while waiting for departure minute dropdown")
    except Exception as e:
        print("Error occurred while selecting departure minute:", e)


def select_adults(driver, passenger_number):
    try:
        adults = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'adults')))
        select = Select(adults)
        select.select_by_value(str(passenger_number))
        time.sleep(0.5)
        print("Adult passengers entered:", passenger_number)
    except TimeoutException:
        print("Timeout occurred waiting for passenger input")
    except Exception as e:
        print("Error occurred while inputting passengers:", e)


def select_children(driver, passenger_number):
    try:
        children = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'children')))
        select = Select(children)
        select.select_by_value(str(passenger_number))
        time.sleep(0.5)
        print("Child passengers entered:", passenger_number)
    except TimeoutException:
        print("Timeout occurred waiting for passenger input")
    except Exception as e:
        print("Error occurred while inputting passengers:", e)


def add_railcard(driver, railcard):
    try:
        railcard_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="jp-form"]/section/div[5]/div/div/button')))
        railcard_button.click()
        time.sleep(1)

        select_railcard = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'railcard-0'))
        )
        time.sleep(1)

        select = Select(select_railcard)

        select.select_by_value(railcard)
        print(f"selected railcard with value: {railcard}")

    except TimeoutException:
        print('timeout occurred whilst waiting')
    except Exception as e:
        print('error occurred:', e)


def click_show_trains(driver):
    global show_trains
    try:
        show_trains = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'button-jp')))
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element((By.CLASS_NAME, 'react-datepicker__day--0')))
        driver.execute_script("arguments[0].scrollIntoView();", show_trains)
        driver.execute_script("arguments[0].click();", show_trains)

        print('Clicked on show live trains')
    except TimeoutException:
        print('Timeout occurred while waiting for show live trains button')
    except ElementClickInterceptedException:
        print('Element click intercepted, retrying...')
        driver.execute_script("arguments[0].click();", show_trains)


def click_feedback(driver):
    try:
        click_no = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="fsrInvite"]/section[3]/button[2]')))
        time.sleep(1)
        click_no.click()
        time.sleep(1)
        print("No feedback clicked")
    except TimeoutException:
        print("timeout occurred whilst waiting for feedback click")


def click_continue(driver):
    try:
        click_ticket = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@id, "outward-0")][1]')))
        # print(click_ticket)
        # click_ticket_price = click_ticket.find_elements(By.XPATH, ".//span[contains(text(), '£')]")
        # cheapest = float(click_ticket_price[0].text.replace('£', ''))
        #
        # available_tickets = driver.find_elements(By.XPATH, '//*[contains(@id, "outward-")][1]')
        # print(len(available_tickets))
        # counter = 0
        # for ticket_option in available_tickets[:5]:
        #     counter += 1
        #     current_ticket_price = ticket_option.find_elements(By.XPATH, ".//span[contains(text(), '£')]")
        #     if current_ticket_price:
        #         current_ticket_price = float(current_ticket_price[0].text.replace('£', ''))
        #         if current_ticket_price < cheapest:
        #             click_ticket = ticket_option
        #             cheapest = current_ticket_price
        # print(click_ticket)
        #
        # cheapest_ticket_string = f'//*[contains(@id, "outward-{counter-1}")][1]'
        # print(cheapest_ticket_string)
        # cheapest_ticket = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, cheapest_ticket_string)))

        #click_ticket = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'result-card-selection-outward-0-422def92')))
        time.sleep(0.5)
        click_ticket.click()
        driver.execute_script("arguments[0].click();", click_ticket)
        time.sleep(0.5)
        cont_button = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="jp-summary-buy-link"]/span[1]')))
        #cont_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'jp-summary-buy-link')))
        time.sleep(0.5)
        cont_button.click()
    except TimeoutException as e:
        print(f'timed out: {e}')


def click_buy(driver):
    try:
        #buy_button = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="jp-summary-buy-link"]/span[1]')))
        buy_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'jp-summary-buy-link')))
        time.sleep(0.5)
        buy_button.click()
    except TimeoutException as e:
        print(f'timed out: {e}')

def extract_train_ticket(driver):
    try:
        ticket_elements = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="outward-0"]/div/div/div[4]/div[1]/a'))
        )
        # ticket_links = [elem.get_attribute('href') for elem in ticket_elements]
        ticket_links = ticket_elements.get_attribute('href')
        return ticket_links
    except TimeoutException:
        print('timeout occurred whilst waiting for ticket links')
        return []


def main(destination, departure, date, train_time, adults, children, railcard):
    # Get inputs from Experta
    destination_location = destination
    departure_location = departure
    choose_date = date
    #choose_date = "07 June 2024"
    choose_hour = train_time[0]
    choose_minute = train_time[1]
    passenger_number_adult = adults
    passenger_number_child = children
    railcard = railcard

    # if railcard == "no":
    #     railcard = ""

    driver = webdriver.Chrome()
    driver.get("https://www.nationalrail.co.uk")
    click_cookie(driver)
    click_journey(driver)

    # Get user input for departure and destination locations
    # destination_location, departure_location, choose_date, choose_hour, choose_minute, passenger_number_adult, passenger_number_child, railcard = get_user_input()

    # Input locations on the webpage
    input_locations(driver, departure_location, destination_location)
    # Input departure time
    input_departure_date(driver, choose_date)
    # time.sleep(3)
    select_departure_hour(driver, choose_hour)
    select_departure_minute(driver, choose_minute)
    select_adults(driver, passenger_number_adult)
    select_children(driver, passenger_number_child)
    if railcard != "no":
        add_railcard(driver, railcard)

    # GET URLS
    ticket_links = []
    click_show_trains(driver)
    time.sleep(0.5)
    click_feedback(driver)
    time.sleep(0.5)
    click_continue(driver)
    click_feedback(driver)
    ticket_links.append(driver.current_url)
    click_buy(driver)
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(6)
    click_ga_cookie(driver)
    ticket_links.append(driver.current_url)
    # except:
    #     pass
    #ticket_links = extract_train_ticket(driver)
    # try:
    #     click_continue(driver)
    # except:
    #     pass
    # ticket_links = extract_train_ticket(driver)
    if ticket_links:
        print(f"Train ticket link: {ticket_links}")
        return ticket_links
    else:
        fail_message = "Failed to retrieve ticket link"
        return fail_message

    # time.sleep(160)
    driver.quit()



if __name__ == "__main__":
    main("NORWICH", "STRATFORD", "07 July 2024", ["18", "45"], 3, 3, "no")
