import cv2
import numpy as np


def detect_coins(image_path):
    img = cv2.imread(image_path)

    img_blur = cv2.medianBlur(img, 3)
    img_gray = cv2.cvtColor(img_blur, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(img_gray, 500, 650, apertureSize=5)

    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 90, minLineLength=50, maxLineGap=5)

    x_coords = [line[0][0] for line in lines]
    y_coords = [line[0][1] for line in lines]
    min_x = min(x_coords)
    max_x = max(x_coords)
    min_y = min(y_coords)
    max_y = max(y_coords)

    cv2.rectangle(img, (min_x, min_y), (max_x, max_y), (255, 255, 255), 2)
    tray_area = (max_x - min_x) * (max_y - min_y)
    tray_area = round(tray_area, 2)

    circles = cv2.HoughCircles(img_gray, cv2.HOUGH_GRADIENT, 1, 15, param1=80, param2=35, minRadius=15, maxRadius=40)
    circles = np.uint16(np.around(circles))

    count_inside = {'big': 0, 'small': 0}
    count_outside = {'big': 0, 'small': 0}

    total_area_all_coins = 0
    total_area_5zl_coins = 0

    for circle in circles[0]:
        x, y, r = circle[0], circle[1], circle[2]

        coin_area = np.pi * r ** 2
        total_area_all_coins += coin_area

        if min_x < x < max_x and min_y < y < max_y:
            if r > 32:
                total_area_5zl_coins += coin_area
                count_inside['big'] += 1
                color = (0, 255, 255)
                print('Zad. 1: Moneta 5 zł, x:', x, 'y:', y)
            else:
                count_inside['small'] += 1
                color = (0, 255, 0)
                print('Zad. 1: Moneta 5 gr, x:', x, 'y:', y)
            cv2.circle(img, (x, y), 2, (255, 255, 255), 4)
        else:
            if r > 32:
                total_area_5zl_coins += coin_area
                count_outside['big'] += 1
                color = (0, 255, 255)
                print('Zad. 1: Moneta 5 zł (poza tacą), x:', x, 'y:', y)
            else:
                count_outside['small'] += 1
                color = (0, 255, 0)
                print('Zad. 1: Moneta 5 gr (poza tacą), x:', x, 'y:', y)
        cv2.circle(img, (x, y), r, color, 2)

    print('---------------------------------------------------------------------------------------------')
    total_inside = count_inside['big'] * 5 + count_inside['small'] * 0.05
    total_outside = count_outside['big'] * 5 + count_outside['small'] * 0.05
    total = round(total_inside + total_outside, 2)

    # Oblicz wartość całkowitej powierzchni monet na tacy
    total_area_all_coins = round(total_area_all_coins, 2)
    total_area_5zl_coins = round(total_area_5zl_coins, 2)

    # Oblicz stosunek powierzchni monet 5 zł do powierzchni tacy
    ratio_5zl_to_tray = tray_area / total_area_5zl_coins

    print('Zad. 2: Całkowita powierzchnia monet:', total_area_all_coins, 'pikseli kwadratowych')
    print('Zad. 2: Liczba monet 5 zł:', count_inside['big'] + count_outside['big'], 'i monety 5 gr:',
          count_outside['small'] + count_outside['small'])
    print('---------------------------------------------------------------------------------------------')

    print('Zad. 3: Krawędzie tacy: min_x =', min_x, 'max_x =', max_x, 'min_y =', min_y, 'max_y =', max_y)
    print('Zad. 3: Powierzchnia tacy:', tray_area, 'pikseli kwadratowych')
    print('Zad. 3: Całkowita powierzchnia monet 5 zł:', total_area_5zl_coins, 'pikseli kwadratowych')
    print('Zad. 3: Stosunek powierzchni tacy do powierzchni monet 5 zł:', ratio_5zl_to_tray)
    print('---------------------------------------------------------------------------------------------')

    print('Zad. 4: Kwota na tacy:', total_inside, 'zl')
    print('Zad. 4: Kwota poza tacą:', total_outside, 'zl')
    print('Zad. 4: Całkowita kwota:', total, 'zl')
    print('---------------------------------------------------------------------------------------------')

    cv2.imshow('detected coins', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main():
    image_path = 'images/tray4.jpg'
    detect_coins(image_path)


if __name__ == "__main__":
    main()
