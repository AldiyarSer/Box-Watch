import cv2
import numpy as np

# Создаем белый фон
ok_img = np.ones((400, 400, 3), dtype=np.uint8) * 255
defect_img = np.ones((400, 400, 3), dtype=np.uint8) * 255

# Рисуем ИДЕАЛЬНУЮ коробку (ровный зеленый прямоугольник)
cv2.rectangle(ok_img, (100, 100), (300, 300), (0, 200, 0), -1)
cv2.imwrite('ok.png', ok_img)

# Рисуем ПОМЯТУЮ коробку (многоугольник неправильной формы, красный)
pts = np.array([[100, 100], [250, 80], [320, 150], [280, 300], [150, 320], [80, 200]], np.int32)
pts = pts.reshape((-1, 1, 2))
cv2.fillPoly(defect_img, [pts], (0, 0, 200))
cv2.imwrite('defect.png', defect_img)

print("Файлы ok.png и defect.png успешно созданы!")
