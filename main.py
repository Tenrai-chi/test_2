"""
Редактирование изображения
Вырезать, заданный пользователем координатами кусок изображения и сохранить
Новые файлы сохраняются в папке "new" в директории программы с пометкой new
"""

import os

from PIL import Image, ImageDraw
from typing import Tuple


def import_image() -> Tuple[Image.Image, str, str] | None:
    """
    Запрашивает у пользователя путь к файлу и импортирует его
    """

    image_path = input('Введите путь к изображению: ')

    if not os.path.exists(image_path):
        print('Ошибка: Указанный файл не существует')
        return

    try:
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        ext = os.path.splitext(os.path.basename(image_path))[1]
        image = Image.open(image_path)
        image.convert('RGB')
        return image, base_name, ext
    except Exception as _:
        print(f'Ошибка при открытии файла. Проверьте корректность пути к файлу: {_}')
        return


def get_coordinates() -> Tuple[int, int, int, int] | None:
    """
    Запрашивает координаты у пользователя
    """

    try:
        print('Введите координаты области для вырезания. Помните что 0,0 - верхний левый угол, n, m - правый нижний угол')
        x1: int = int(input('Координата x1 (верхний левый угол): '))  # Запрашиваем координату x верхнего левого угла
        y1: int = int(input('Координата y1 (верхний левый угол): '))  # Запрашиваем координату y верхнего левого угла
        x2: int = int(input('Координата x2 (нижний правый угол): '))  # Запрашиваем координату x нижнего правого угла
        y2: int = int(input('Координата y2 (нижний правый угол): '))  # Запрашиваем координату y нижнего правого угла
        return x1, y1, x2, y2
    except Exception as _:
        print(f'Ошибка при обработке ввода координат. Проверьте, что координаты целые числа: {_}')
        return


def save_image(image: Image.Image, base_name: str, ext: str) -> None:
    """
    Сохраняет изображение в папку new директории
    """

    try:
        image.save(f'new/{base_name}_new{ext}')
        print(f'Изображение успешно сохранено в папке new')
    except Exception as _:
        print(f'Ошибка при сохранении файла: {_}')
        return


def delete_region_1(image, coordinates: Tuple[int, int, int, int]) -> Image.Image | None:
    """
    Удаляет заданный пользователем участок изображения путем перекрывания блоком черного цвета
    """

    try:
        draw = ImageDraw.Draw(image)
        draw.rectangle(coordinates, fill=(0, 0, 0))
        return image

    except Exception as _:
        print(f'Ошибка при вырезании изображения. Проверьте корректность координат. {_}')
        return


def delete_region_2(image: Image.Image, coordinates: Tuple[int, int, int, int]) -> Image.Image | None:
    """
    Удаляет заданный пользователем участок изображения путем перекрашивания заданных пикселей в черный
    """

    try:
        for x in range(coordinates[0], coordinates[2]):
            for y in range(coordinates[1], coordinates[3]):
                image.putpixel((x, y), (0, 0, 0))  # Делает каждый пиксель черным в цикле
        return image

    except Exception as _:
        print(f'Ошибка при вырезании изображения. Проверьте корректность координат. {_}')
        return


def process_image() -> None:
    """
    Обработка изображение от его импорта, до сохранения
    """

    image, base_name, ext = import_image()
    coordinates = get_coordinates()

    new_image = delete_region_1(image, coordinates)  # Если нужно просто перекрыть черным блоком участок
    # new_image = delete_region_2(image, coordinates)  # Если нужно перекрасить участок самого изображения в черный
    save_image(new_image, base_name, ext)


if __name__ == '__main__':
    process_image()
