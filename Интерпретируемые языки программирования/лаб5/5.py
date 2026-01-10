import re
def is_phone_number(text):
    pattern = r'^(\+7|8)[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}$'
    return bool(re.match(pattern, text.strip()))

def validate_phone_number(text):
    if not isinstance(text, str):
        raise ValueError("Аргумент должен быть строкой")

    cleaned_text = text.strip()

    if not cleaned_text:
        raise ValueError("Строка не может быть пустой")

    if not is_phone_number(cleaned_text):
        raise ValueError(f"Строка '{cleaned_text}' не является корректным телефонным номером")

    if is_phone_number(cleaned_text):
        return cleaned_text

print(is_phone_number('+7(953)075-39-16'))
print(validate_phone_number('abc'))