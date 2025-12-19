from .selenium import By, WebDriverWait, EC, TimeoutException
from .logger import log
import os

def collect_players_from_games(driver, iframe_src):
    log("Сбор игроков из списка.", "ACTION")
    total_games = 0
    total_players = 0
    try:
        with open("game_ids.txt", 'r', encoding='utf-8') as file:
            for game_id in file:
                game_id = game_id.strip()
                if not game_id:
                    continue

                total_games += 1
                game_url = iframe_src + f"#/game_info/:gameID={game_id}"
                log(f"Открываю {game_url}", "ACTION")
                driver.get(game_url)

                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located(
                            (By.CSS_SELECTOR, "div.name.text_overflow_ellipsis")
                        )
                    )
                except TimeoutException:
                    log(f"Игроки не загрузились для игры {game_id}.", "WARNING")

                players = {
                    el.text.strip()
                    for el in driver.find_elements(By.CSS_SELECTOR, "div.name.text_overflow_ellipsis")
                    if el.text.strip()
                }

                if players:
                    os.makedirs("games", exist_ok=True)
                    filename = os.path.join("games", f"{game_id}.txt")
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write("\n".join(sorted(players)))
                    log(f"{len(players)} игроков сохранено → {filename}.", "SUCCESS")
                    total_players += len(players)
                else:
                    log(f"Игроков не найдено для игры {game_id}.", "WARNING")

    except Exception as e:
        log(f"Ошибка при обработке файла game_ids.txt: {e}.", "ERROR")

    log(f"Завершено: {total_games} игр, {total_players} игроков найдено.", "INFO")