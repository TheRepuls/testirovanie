from .selenium import By, WebDriverWait, EC, TimeoutException, time
from .logger import log

URL = "https://www.callofwar.com"
USERNAME = "MC. MIF"
PASSWORD = "@@@@OXYMIRON@@@@"
WRONG_USERNAME = "!!)@(#*$)"
WRONG_PASSWORD = "@(#!*)@$!(@)$()"

def login(driver):
    log("Вход в аккаунт.", "ACTION")
    wait = WebDriverWait(driver, 3)
    driver.get(URL)
    time.sleep(3)

    try:
        cookies_found = True
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "didomi-notice-agree-button")))
            log("Форма с куками найдена", "SUCCESS")
        except TimeoutException:
            log("Куки отсутствуют.", "WARNING")
            cookies_found = False
    
        if not cookies_found:
            cookie_btn = wait.until(EC.element_to_be_clickable((By.ID, "didomi-notice-agree-button")))
            driver.execute_script("arguments[0].click();", cookie_btn)
            log("Форма с куками убрана", "SUCCESS")
    except TimeoutException:
            log("Куки отсутствуют.", "WARNING")

    try:
        login_toggle = wait.until(EC.element_to_be_clickable((By.ID, "func_sg_loginform_button")))
        driver.execute_script("arguments[0].click();", login_toggle)
        log("Открыта форма входа.", "SUCCESS")
    except Exception as e:
        log(f"Ошибка при открытии формы входа: {e}.", "ERROR")
        return False
    try:
        username_input = wait.until(EC.visibility_of_element_located((By.ID, "loginbox_login_input")))
        password_input = driver.find_element(By.ID, "loginbox_password_input")
        username_input.send_keys(USERNAME)
        password_input.send_keys(PASSWORD)
        log("Введены данные аккаунта.", "SUCCESS")
    except Exception as e:
        log(f"Ошибка при вводе данных: {e}.", "ERROR")
        return False
    try:
        login_button = wait.until(EC.element_to_be_clickable((By.ID, "func_loginbutton")))
        driver.execute_script("arguments[0].click();", login_button)
        time.sleep(1)
        try:
            login_error_message = wait.until(EC.visibility_of_element_located((By.ID, "login_error_message_div")))
            error_text = login_error_message.text
            log(f"{error_text}", "ERROR")
            return False
        except TimeoutException:
            log("Вход в аккаунт выполнен успешно", "SUCCESS")
            time.sleep(6)
            return True
    except Exception as e:
        log(f"Ошибка при входе: {e}.", "ERROR")
        return False

    return True
