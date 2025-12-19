from .selenium import By, WebDriverWait, EC, time
from .logger import log

def go_to_games(driver):
    log("Получаем iframe с ссылкой на основную страницу.", "ACTION")
    try:
        iframe = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "ifm"))
        )
        iframe_src = iframe.get_attribute("src")
        if not iframe_src:
            log("Не удалось получить ссылку.", "ERROR")
            return None

        games_url = iframe_src + "#/games/new/"
        log(f"Переходим по ссылке: {games_url}.", "ACTION")
        driver.get(games_url)
        time.sleep(8)
        return iframe_src

    except Exception as e:
        log(f"Ошибка при поиске iframe: {e}.", "ERROR")
        return None