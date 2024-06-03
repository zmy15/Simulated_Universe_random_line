import cv2
import numpy as np
import random


def detect_hexagons(image_path, output_path):
    # 读取图片
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 获取图片的分辨率
    height, width = gray.shape
    diagonal = np.sqrt(height ** 2 + width ** 2)

    # 根据图片的分辨率设置min_size和max_size
    min_size = diagonal * 0.03  # 设置为对角线的3%
    max_size = diagonal * 0.055  # 设置为对角线的5.5%

    # 增强对比度
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)

    # 模糊处理以减少噪音
    blurred = cv2.GaussianBlur(enhanced, (5, 5), 0)

    # 边缘检测
    edged = cv2.Canny(blurred, 50, 150)

    # 找到轮廓
    contours, _ = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    detected_hexagons = []

    for contour in contours:
        # 逼近多边形
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        if len(approx) == 6:
            # 确保它是一个正六边形
            if is_regular_hexagon(approx):
                # 计算六边形的外接圆直径
                diameter = calculate_enclosing_circle_diameter(approx)

                if min_size <= diameter <= max_size:
                    M = cv2.moments(contour)
                    if M['m00'] != 0:
                        cx = int(M['m10'] / M['m00'])
                        cy = int(M['m01'] / M['m00'])

                        # 检查是否有重叠的六边形
                        if not is_duplicate_hexagon(detected_hexagons, cx, cy):
                            detected_hexagons.append((cx, cy))
                            cv2.drawContours(image, [approx], 0, (0, 255, 0), 3)

    # 保存输出图片
    cv2.imwrite(output_path, image)
    return detected_hexagons


def is_regular_hexagon(approx):
    # 计算各边长
    sides = [np.linalg.norm(approx[i][0] - approx[(i + 1) % 6][0]) for i in range(6)]
    max_side = max(sides)
    min_side = min(sides)

    # 放宽正六边形的判断标准
    return (max_side - min_side) / max_side < 0.5


def is_duplicate_hexagon(detected_hexagons, cx, cy, threshold=50):
    # 检查是否有重叠的六边形
    for (x, y) in detected_hexagons:
        if np.sqrt((cx - x) ** 2 + (cy - y) ** 2) < threshold:
            return True
    return False


def calculate_enclosing_circle_diameter(approx):
    # 计算六边形的外接圆直径
    (x, y), radius = cv2.minEnclosingCircle(approx)
    return radius * 2


def find_neighbors(hexagons, hexagon, distance_threshold):
    cx, cy = hexagon
    neighbors = []
    for (x, y) in hexagons:
        if cx < x and np.sqrt((cx - x) ** 2 + (cy - y) ** 2) <= distance_threshold:
            neighbors.append((x, y))
    return neighbors


def draw_path(image, path):
    for i in range(len(path) - 1):
        cv2.line(image, path[i], path[i + 1], (0, 0, 255), 2)


def main(image_path, output_path):
    hexagons = detect_hexagons(image_path, output_path)
    if not hexagons:
        print("No hexagons detected.")
        return

    hexagons.sort(key=lambda x: x[0])  # Sort by x-coordinate
    left_most_hexagon = hexagons[0]

    path = [left_most_hexagon]
    current_hexagon = left_most_hexagon
    distance_threshold = (np.sqrt(
        (hexagons[1][0] - left_most_hexagon[0]) ** 2 + (hexagons[1][1] - left_most_hexagon[1]) ** 2)) * 1.05

    while current_hexagon[0] < max(hexagons, key=lambda x: x[0])[0]:
        neighbors = find_neighbors(hexagons, current_hexagon, distance_threshold)
        if not neighbors:
            print(114514)
            break
        current_hexagon = random.choice(neighbors)
        path.append(current_hexagon)

    image = cv2.imread(output_path)
    draw_path(image, path)
    cv2.imwrite(output_path, image)
