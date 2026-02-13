from playwright.sync_api import sync_playwright

# Путь к профилю Yandex Browser или отдельный профиль
PROFILE_PATH = r"C:\Users\Admin\Documents\GitHub\Happy_Birthday_Script1\yandex_profile"

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        user_data_dir=PROFILE_PATH,
        headless=False
    )

    page = browser.new_page()
    page.goto("https://vk.com/friends?section=all&w=calendar")

    input("Когда страница загрузится полностью, нажми Enter...")

    import re

    page.wait_for_selector("div.bd_name", timeout=15000)

    birthday_rows = page.locator("div.bd_name").all()
    print(f"Найдено строк с именами: {len(birthday_rows)}\n")

    results = []

    for el in birthday_rows:

        # Имя
        name = el.locator("a").first.text_content().strip()

        # Родительский контейнер строки
        row = el.locator("xpath=ancestor::div[1]")
        full_text = row.text_content().strip()

        if "сегодня" not in full_text.lower():
            continue

        # Ссылка
        href = el.locator("a").first.get_attribute("href")

        user_id = "не найден"

        if href:
            # Если формат /id123456
            match = re.search(r"id(\d+)", href)
            if match:
                user_id = match.group(1)
            else:
                user_id = href  # если это username

        clean_text = f"{name} сегодня отмечает день рождения | ID: {user_id}"

        print(clean_text)
        results.append(clean_text)

    # Сохранение
    with open("birthdays_today.txt", "w", encoding="utf-8") as f:
        for line in results:
            f.write(line + "\n")
