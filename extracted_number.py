import os
import re
import cv2
import requests
from PIL import Image
import pytesseract

image_path = 'photos/gg4.jpg'  # <---- Это фото с которым мы будем работать!

"""РАСПОЗНАВАНИЕ ТЕКСТА"""
try:
    image = Image.open(image_path)
except FileNotFoundError:
    print('ФАЙЛ НЕ НАЙДЕН')

text = pytesseract.image_to_string(image, lang='eng+rus')  # Используйте pytesseract для распознавания текста
match = re.search(r'\b\d{9}\b', text)  # Последовательность из 9 цифр

# Если найдено совпадение
if match:
    extracted_number = match.group()
    print("Найденный номер:", extracted_number)
    url = f'https://apiv1.kartoteka.by/unp/{extracted_number}'
    response = requests.get(url)
    if response.status_code == 200:
        result = response.json()
        print("Результат запроса:", result)
        with open(f'unp_numbers/{extracted_number}.json', 'w', encoding='utf-8') as f:
            import json

            json.dump(result, f, ensure_ascii=False, indent=4)
    else:
        print(f"Ошибка при выполнении запроса: {response.status_code}")
else:
    print("Номер не найден.")

"""РАСПОЗНАВАНИЕ ЛИЦА"""
if not os.path.exists('photos_faces'):
    os.makedirs('photos_faces')

image = cv2.imread(image_path)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
min_size_range = range(30, 251, 50)  # Диапазон от 50 до 250 с шагом 50
found_faces = False

for min_size in min_size_range:
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(min_size, min_size))
    if len(faces) > 0:
        found_faces = True
        for (x, y, w, h) in faces:
            face = image[y:y + h, x:x + w]
            face_image = Image.fromarray(cv2.cvtColor(face, cv2.COLOR_BGR2RGB))
            face_image.save(f'photos_faces/face_{extracted_number}.jpg')
            print(f"Фотография лица сохранена как: face_minSize_{extracted_number}.jpg")

if not found_faces:
    print("Лицо не найдено.")
