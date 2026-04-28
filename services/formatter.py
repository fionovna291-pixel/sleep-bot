def format_response(analysis, wb):

    if analysis["status"] == "overtired":
        text = "Есть признаки перегула 😵"

    elif analysis["status"] == "undertired":
        text = "Похоже на недогул 🙂"

    elif analysis["status"] == "balanced":
        text = "Сейчас всё хорошо 👍"

    else:
        return "Недостаточно данных"

    return f"""{text}

Рекомендуемое окно бодрствования: ~{wb} минут"""