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

    # Ждём появления блоков с именами
    page.wait_for_selector("div.bd_name", timeout=15000)

    # Берём родительский контейнер строки (поднимаемся вверх от bd_name)
    birthday_rows = page.locator("div.bd_name").locator("xpath=ancestor::div[contains(@class,'birthday')]").all()

    print(f"Найдено строк с днями рождения: {len(birthday_rows)}\n")

    results = []

    for i, row in enumerate(birthday_rows, start=1):

        full_text = row.text_content().strip()
        text_lower = full_text.lower()

        if "сегодня" not in text_lower:
            continue

        # Имя и ссылка
        a_tag = row.locator("div.bd_name a")

        if a_tag.count() == 0:
            continue

        name = a_tag.first.text_content().strip()
        href = a_tag.first.get_attribute("href")

        # Достаём ID
        user_id = "не найден"
        if href:
            match = re.search(r"/id(\d+)", href)
            if match:
                user_id = match.group(1)

        line_output = f"{full_text} | ID: {user_id}"

        print(line_output)
        results.append(line_output)

    # Сохраняем в файл
    with open("birthdays_today.txt", "w", encoding="utf-8") as f:
        for line in results:
            f.write(line + "\n")
