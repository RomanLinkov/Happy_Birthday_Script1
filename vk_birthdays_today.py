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

    # -------------------
    # 1️⃣ Выводим весь HTML страницы (для проверки)
    html_content = page.content()
    print("=== Начало HTML страницы ===")
    print(html_content[:1000])  # показываем первые 1000 символов
    print("=== Конец HTML страницы ===\n")
    # -------------------

    # 2️⃣ Ищем все div.bd_name > a
    birthday_elements = page.locator("div.bd_name a").all()
    print(f"Найдено элементов с именами друзей: {len(birthday_elements)}")

    birthdays_today = []

    # 3️⃣ Проходим по найденным элементам
    for i, el in enumerate(birthday_elements, start=1):
        text = el.text_content()
        print(f"Элемент {i}: {text}")  # печатаем, что нашёл Python
        if text:
            name = text.strip()
            birthdays_today.append(name)

    # 4️⃣ Вывод финального списка
    print("\nСегодня день рождения у:")
    for name in birthdays_today:
        print(name)

    # 5️⃣ Сохраняем в файл
    with open("birthdays_today.txt", "w", encoding="utf-8") as f:
        for name in birthdays_today:
            f.write(name + "\n")

    browser.close()