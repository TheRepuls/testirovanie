from .selenium import By, time
from .logger import log
import os

def collect_game_ids(driver, iframe_src):
    #log("Переход на вкладку с играми.", "ACTION")
    #driver.get(iframe_src + "#/games/new/")
    #time.sleep(8)

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

    if ids:
        os.makedirs("games", exist_ok=True)
        with open("game_ids.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(sorted(ids)))
        log(f"Найдено ID игр: {len(ids)}.", "SUCCESS")
    else:
        log("Игры не найдены.", "WARNING")

    return list(ids)
