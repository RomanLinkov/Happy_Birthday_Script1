import random

# --- Варианты поздравлений ---

starts = [
    "С днём рождения, {name}!",
    "Уважаемый(ая) {name}, поздравляем Вас с днём рождения!",
    "{name}, примите наши искренние поздравления!",
    "Поздравляем Вас с праздником, {name}!",
]

wishes_main = [
    "Желаем Вам крепкого здоровья и отличной физической формы.",
    "Желаем энергии, силы и новых спортивных достижений.",
    "Пусть тренировки приносят удовольствие и заметные результаты.",
    "Желаем уверенности, выносливости и гармонии.",
    "Пусть каждый день будет шагом к новым победам.",
]

club_mentions = [
    "Мы всегда рады видеть Вас в нашем клубе.",
    "Спасибо, что выбираете наш фитнес-клуб.",
    "Будем рады новым встречам и совместным тренировкам.",
]

endings = [
    "С уважением, команда фитнес-клуба.",
    "С наилучшими пожеланиями, Ваш фитнес-клуб.",
    "",
]


# --- Генерация текста ---

def generate_greeting(name, discount):
    discount_block = ""
    if discount:
        discount_block = (
            f"В честь Вашего дня рождения дарим Вам персональную скидку {discount}% "
            "на услуги нашего клуба. "
        )

    text = (
        random.choice(starts).format(name=name) + " " +
        random.choice(wishes_main) + " " +
        discount_block +
        random.choice(club_mentions) + " " +
        random.choice(endings)
    )

    return " ".join(text.split())


def extract_first_name(full_line):
    full_name = full_line.split(" сегодня")[0].strip()
    return full_name.split()[0]


def main():
    input_file = "birthdays_today.txt"
    output_file = "greetings_ready.txt"

    # --- Запрос оператору ---
    discount_input = input("Введите размер скидки (только число, без %). Если без скидки — нажмите Enter: ").strip()

    if discount_input:
        try:
            discount_value = int(discount_input)
        except ValueError:
            print("Некорректное значение скидки. Будет использовано без скидки.")
            discount_value = None
    else:
        discount_value = None

    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    results = []

    for line in lines:
        if not line.strip():
            continue

        first_name = extract_first_name(line)
        greeting = generate_greeting(first_name, discount_value)

        results.append(f"{line.strip()}\nПоздравление:\n{greeting}\n")
        results.append("-" * 60 + "\n")

    with open(output_file, "w", encoding="utf-8") as f:
        f.writelines(results)

    print("Готово. Файл greetings_ready.txt создан.")


if __name__ == "__main__":
    main()
