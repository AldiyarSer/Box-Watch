import cv2
import argparse
import os

def check_box_integrity(image_path):
    # Проверяем, существует ли файл
    if not os.path.exists(image_path):
        return f"ОШИБКА: Файл {image_path} не найден."

    # Загружаем изображение
    img = cv2.imread(image_path)
    if img is None:
        return "ОШИБКА: Не удалось прочитать изображение."

    # Переводим в черно-белый формат для упрощения поиска контуров
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Немного размываем, чтобы убрать мелкий шум
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Ищем границы объектов (Canny Edge Detection)
    edges = cv2.Canny(blurred, 50, 150)
    
    # Находим контуры
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        return "DEFECT" # Если вообще ничего не найдено

    # Берем самый большой контур (предполагаем, что это наша коробка)
    largest_contour = max(contours, key=cv2.contourArea)
    area = cv2.contourArea(largest_contour)
    
    if area < 500: # Если объект слишком маленький, это тоже дефект или мусор
        return "DEFECT"

    # Аппроксимируем (сглаживаем) контур, чтобы посчитать количество углов
    # Коэффициент 0.04 определяет, насколько точно мы повторяем изгибы
    epsilon = 0.04 * cv2.arcLength(largest_contour, True)
    approx = cv2.approxPolyDP(largest_contour, epsilon, True)

    # Идеальная или целая коробка должна иметь 4 угла (прямоугольник/квадрат)
    if len(approx) == 4:
        return "OK"
    else:
        # Если углов больше (например 5, 6, 8) — форма нарушена, коробка помята
        return "DEFECT"

if __name__ == "__main__":
    # Настраиваем прием аргументов из командной строки
    parser = argparse.ArgumentParser(description='Детектор дефектов коробок.')
    parser.add_argument('image_path', type=str, help='Путь к изображению (например, ok.png или defect.png)')
    
    args = parser.parse_args()
    
    # Запускаем анализ и печатаем результат
    result = check_box_integrity(args.image_path)
    print(result)
