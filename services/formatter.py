def format_response(analysis, decision):

    text = []

    if analysis["overtired"] > 0.6:
        text.append("Похоже, накопилась усталость — это видно по последнему сну.")

    elif analysis["undertired"] > 0.6:
        text.append("Скорее всего, ребёнок ещё не до конца устал.")

    else:
        text.append("Сейчас ситуация стабильная.")

    text.append(f"Ориентир следующего сна: ~{decision['wb']} минут бодрствования.")

    return "\n\n".join(text)