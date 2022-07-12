from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from getpass import getpass

login = input('Enter the email: ')
password = getpass('Enter the password: ')

driver = webdriver.Chrome()


def parse():
    authorize()

    driver.get(r'https://student.mirea.ru/hostel/online/queue.php')
    queue_info = driver.find_elements(by=By.CLASS_NAME, value='form-control')
    possible_queue_status = driver.find_elements(by=By.TAG_NAME, value='span')
    result = {
        'ФИО': queue_info[0].text,
        'Дата рождения': queue_info[1].text,
        'Группа': queue_info[2].text,
        'Институт': queue_info[3].text,
        'Форма обучения': queue_info[4].text,
        'Телефон': queue_info[5].text,
        'email': queue_info[6].text,
        'В очереди': is_in_queue(possible_queue_status),
        'Номер в очереди': queue_info[7].text,
        'Коэффициент за сессию': queue_info[8].text,
        'Льгота': None if len(queue_info) == 9 else queue_info[9].text
    }
    for key in result:
        print(f'{key} : {result[key]}')
    driver.quit()
    input()


def authorize():
    auth_button = None

    driver.get(r'https://student.mirea.ru/login/')
    forms = driver.find_elements(by=By.TAG_NAME, value='input')
    for form in forms:
        if form.is_displayed():
            form_name = form.get_attribute('name')
            form_type = form.get_attribute('type')
            form_value = form.get_attribute('value')
            if form_type == 'submit' and form_value == 'Войти':
                auth_button = form
            if form_name == 'login':
                form.send_keys(login)
            elif form_name == 'password':
                form.send_keys(password)
    auth_button.click()


def is_in_queue(possible_queue_status):
    is_in_queue = 'unknown'
    for status in possible_queue_status:
        if status.text == 'В очереди':
            is_in_queue = (True, 'Заявление не продлевалось скриптом')
        elif status.text == 'Ожидает подтверждения':
            is_in_queue = prolongate()
            sleep(3)
            driver.refresh()
    return is_in_queue


def prolongate():
    prolongate_button = None
    hrefs = driver.find_elements(By.TAG_NAME, 'a')
    print(len(hrefs))
    for href in hrefs:
        if href.is_displayed():
            print(href.text)
            if href.text.strip() == 'ПРОДЛИТЬ ЗАЯВЛЕНИЕ':
                prolongate_button = href
                break
    if prolongate_button is not None:
        prolongate_button.click()
        return True, 'Заявление было продлено скриптом'
    return False, 'Не удалось продлить заявление при помощи скрипта'




def main():
    parse()


if __name__ == '__main__':
    main()
