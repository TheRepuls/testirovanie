from functions.selenium import By, WebDriverWait, EC, TimeoutException, time
from functions.login import login
from functions.go_to_games import go_to_games
from selenium import webdriver
import pytest
import os

URL = "https://www.callofwar.com"
USERNAME = "MC. MIF"
PASSWORD = "@@@@OXYMIRON@@@@"
WUSERNAME = "!!)@(#*$)"
WPASSWORD = "@(#!*)@$!(@)$()"

@pytest.fixture(scope="session")
def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    driver.get(URL)
    time.sleep(1)
    yield driver
    driver.quit()

@pytest.fixture
def wait(init_driver):
    return(WebDriverWait(init_driver, 3))

def clickon(driver, wait):
    try:
        login_toggle = wait.until(EC.element_to_be_clickable((By.ID, "func_sg_loginform_button")))
        driver.execute_script("arguments[0].click();", login_toggle)
    except Exception as e:
        return False

def test_wrong_login(init_driver, wait):
    driver = init_driver
    clickon(driver, wait)

    try:
        username_input = wait.until(EC.visibility_of_element_located((By.ID, "loginbox_login_input")))
        password_input = driver.find_element(By.ID, "loginbox_password_input")
        username_input.send_keys(WUSERNAME)
        password_input.send_keys(WPASSWORD)
    except Exception as e:
        return False
    try:
        login_button = wait.until(EC.element_to_be_clickable((By.ID, "func_loginbutton")))
        driver.execute_script("arguments[0].click();", login_button)
        time.sleep(1)
        try:
            login_error_message = wait.until(EC.visibility_of_element_located((By.ID, "login_error_message_div")))
            error_text = login_error_message.text
            assert login_error_message.is_displayed(), "Нет сообщения об ошибке"
            assert "Неверное имя пользователя или пароль" in error_text, "Проблема не в пароле или логине"
            return True
        except TimeoutException:
            time.sleep(6)
            return True
    except Exception as e:
        return False

def test_not_wrong_login(init_driver, wait):
    driver = init_driver
    clickon(driver, wait)

    try:
        username_input = wait.until(EC.visibility_of_element_located((By.ID, "loginbox_login_input")))
        password_input = driver.find_element(By.ID, "loginbox_password_input")
        username_input.send_keys(USERNAME)
        password_input.send_keys(PASSWORD)
    except Exception as e:
        return False
    try:
        login_button = wait.until(EC.element_to_be_clickable((By.ID, "func_loginbutton")))
        driver.execute_script("arguments[0].click();", login_button)
        time.sleep(3)
        assert driver.current_url == "https://www.callofwar.com/game.php?L=14&bust=1#/home/overview/", "Попали куда-то не туда или неверный логин"
        return True
    except Exception as e:
        return False

def test_write(init_driver, wait):
    driver = init_driver
    login(driver)
    go_to_games(driver)
    ids = set()
    scroll_attempts = 0
    prev_height = 0

    while scroll_attempts < 7:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)

        elements = driver.find_elements(By.CSS_SELECTOR, "div.hup_game_controls[data-game-id]")
        for el in elements:
            gid = el.get_attribute("data-game-id")
            if gid and gid.isdigit():
                ids.add(gid)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == prev_height:
            break
        prev_height = new_height
        scroll_attempts += 1

    assert ids, "Игры не найдены"
    if os.path.exists("game_ids.txt"):
        os.remove("game_ids.txt")
    with open("game_ids.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(sorted(ids)))
    assert os.path.exists("game_ids.txt"), "Файла не существует"
    assert os.path.getsize("game_ids.txt") > 0, "Файл пустой" 