import pygame
import random

# Инициализация Pygame
pygame.init()
pygame.key.set_repeat(500, 200)  # увеличена задержка до 500 мс и интервал до 200 мс

# Настройки экрана
ширина = 800
высота = 600
экран = pygame.display.set_mode((ширина, высота))
pygame.display.set_caption("Тетрис")

# Цвета
ЧЕРНЫЙ = (0, 0, 0)
БЕЛЫЙ = (255, 255, 255)
КРАСНЫЙ = (255, 0, 0)
ЗЕЛЕНЫЙ = (0, 255, 0)
СИНИЙ = (0, 0, 255)

# Настройки игры
размер_блока = 30
ширина_поля = 10
высота_поля = 20
поле_x = (ширина - ширина_поля * размер_блока) // 2
поле_y = высота - высота_поля * размер_блока - 10

# Фигуры
фигуры = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]]
]

# Функции
def новая_фигура():
    return random.choice(фигуры)

def проверка_столкновения(поле, фигура, смещение_x, смещение_y):
    for y, ряд in enumerate(фигура):
        for x, ячейка in enumerate(ряд):
            if ячейка:
                новый_x = x + смещение_x
                новый_y = y + смещение_y
                if новый_x < 0 or новый_x >= ширина_поля or новый_y >= высота_поля or поле[новый_y][новый_x]:
                    return True
    return False

def добавить_фигуру_на_поле(поле, фигура, смещение_x, смещение_y):
    for y, ряд in enumerate(фигура):
        for x, ячейка in enumerate(ряд):
            if ячейка:
                поле[y + смещение_y][x + смещение_x] = 1

def удалить_заполненные_ряды(поле):
    полные_ряды = [i for i, ряд in enumerate(поле) if all(ряд)]
    for ряд in полные_ряды:
        del поле[ряд]
        поле.insert(0, [0 for _ in range(ширина_поля)])
    return len(полные_ряды)

def рисовать_следующую_фигуру(экран, фигура):
    for y, ряд in enumerate(фигура):
        for x, ячейка in enumerate(ряд):
            if ячейка:
                pygame.draw.rect(экран, КРАСНЫЙ, (
                    поле_x + ширина_поля * размер_блока + 50 + x * 20,
                    поле_y + y * 20,
                    19,
                    19
                ))

# Основной игровой цикл
def игра():
    поле = [[0 for _ in range(ширина_поля)] for _ in range(высота_поля)]
    текущая_фигура = новая_фигура()
    следующая_фигура = новая_фигура()
    смещение_x = ширина_поля // 2 - len(текущая_фигура[0]) // 2
    смещение_y = 0
    счет = 0
    скорость = 0.5
    время_падения = 0

    часы = pygame.time.Clock()
    игра_окончена = False

    удерживаем_лево = False
    удерживаем_право = False
    удерживаем_вниз = False

    while not игра_окончена:
        for событие in pygame.event.get():
            if событие.type == pygame.QUIT:
                игра_окончена = True
            if событие.type == pygame.KEYDOWN:
                if событие.key == pygame.K_LEFT:
                    удерживаем_лево = True
                    if not проверка_столкновения(поле, текущая_фигура, смещение_x - 1, смещение_y):
                        смещение_x -= 1
                if событие.key == pygame.K_RIGHT:
                    удерживаем_право = True
                    if not проверка_столкновения(поле, текущая_фигура, смещение_x + 1, смещение_y):
                        смещение_x += 1
                if событие.key == pygame.K_DOWN:
                    удерживаем_вниз = True
                    if not проверка_столкновения(поле, текущая_фигура, смещение_x, смещение_y + 1):
                        смещение_y += 1
                if событие.key == pygame.K_UP:
                    повернутая_фигура = list(zip(*текущая_фигура[::-1]))
                    if not проверка_столкновения(поле, повернутая_фигура, смещение_x, смещение_y):
                        текущая_фигура = повернутая_фигура
                if событие.key == pygame.K_SPACE:
                    # Сброс фигуры вниз максимально возможным образом
                    while not проверка_столкновения(поле, текущая_фигура, смещение_x, смещение_y + 1):
                        смещение_y += 1
            if событие.type == pygame.KEYUP:
                if событие.key == pygame.K_LEFT:
                    удерживаем_лево = False
                if событие.key == pygame.K_RIGHT:
                    удерживаем_право = False
                if событие.key == pygame.K_DOWN:
                    удерживаем_вниз = False

        время_падения += часы.get_rawtime()
        if время_падения > скорость * 1000:
            время_падения = 0
            if not проверка_столкновения(поле, текущая_фигура, смещение_x, смещение_y + 1):
                смещение_y += 1
            else:
                добавить_фигуру_на_поле(поле, текущая_фигура, смещение_x, смещение_y)
                удаленные_ряды = удалить_заполненные_ряды(поле)
                счет += удаленные_ряды * 100
                текущая_фигура = следующая_фигура
                следующая_фигура = новая_фигура()
                смещение_x = ширина_поля // 2 - len(текущая_фигура[0]) // 2
                смещение_y = 0
                if проверка_столкновения(поле, текущая_фигура, смещение_x, смещение_y):
                    игра_окончена = True

        экран.fill(ЧЕРНЫЙ)

        # Рисуем границы стакана
        pygame.draw.rect(экран, БЕЛЫЙ, (поле_x, поле_y, ширина_поля * размер_блока, высота_поля * размер_блока), 2)

        # Рисуем заполненные ячейки
        for y, ряд in enumerate(поле):
            for x, ячейка in enumerate(ряд):
                if ячейка:
                    pygame.draw.rect(экран, БЕЛЫЙ, (поле_x + x * размер_блока, поле_y + y * размер_блока, размер_блока - 1, размер_блока - 1))

        # Рисуем текущую фигуру
        for y, ряд in enumerate(текущая_фигура):
            for x, ячейка in enumerate(ряд):
                if ячейка:
                    pygame.draw.rect(экран, КРАСНЫЙ, (поле_x + (смещение_x + x) * размер_блока, поле_y + (смещение_y + y) * размер_блока, размер_блока - 1, размер_блока - 1))

        # Отображение следующей фигуры
        рисовать_следующую_фигуру(экран, следующая_фигура)

        # Обработка удерживаемых клавиш
        keys = pygame.key.get_pressed()
        if удерживаем_лево:
            if not проверка_столкновения(поле, текущая_фигура, смещение_x - 1, смещение_y):
                смещение_x -= 1
        if удерживаем_право:
            if not проверка_столкновения(поле, текущая_фигура, смещение_x + 1, смещение_y):
                смещение_x += 1
        if удерживаем_вниз:
            if not проверка_столкновения(поле, текущая_фигура, смещение_x, смещение_y + 1):
                смещение_y += 1

        # Отображение счета
        шрифт = pygame.font.Font(None, 36)
        текст_счета = шрифт.render(f"Счет: {счет}", True, БЕЛЫЙ)
        экран.blit(текст_счета, (10, 10))

        pygame.display.flip()
        часы.tick(60)

    pygame.quit()

if __name__ == "__main__":
    игра()