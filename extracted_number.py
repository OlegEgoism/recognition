import re
import requests
from PIL import Image
import pytesseract

# Откройте изображение
image_path = 'photo/gg1.jpg'
image = Image.open(image_path)

# Используйте pytesseract для распознавания текста
text = pytesseract.image_to_string(image, lang='eng+rus')

# Последовательность из 9 цифр
match = re.search(r'\b\d{9}\b', text)

# Если найдено совпадение, извлеките его
if match:
    extracted_number = match.group()
    print("Найденный номер:", extracted_number)

    # Подставьте номер в URL и выполните запрос
    url = f'https://apiv1.kartoteka.by/unp/{extracted_number}'
    response = requests.get(url)

    if response.status_code == 200:
        result = response.json()
        print("Результат запроса:", result)
        # Запись результата в файл (например, result.json)
        with open(f'{extracted_number}.json', 'w', encoding='utf-8') as f:
            import json

            json.dump(result, f, ensure_ascii=False, indent=4)
    else:
        print(f"Ошибка при выполнении запроса: {response.status_code}")
else:
    print("Номер не найден.")
