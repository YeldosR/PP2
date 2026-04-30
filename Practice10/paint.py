import pygame
import sys

# окно размеры
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600

# Ширина панели инструментов (слева)
TOOLBAR_WIDTH = 180

# Область холста (где рисуем)
CANVAS_X = TOOLBAR_WIDTH
CANVAS_Y = 0
CANVAS_W = SCREEN_WIDTH - TOOLBAR_WIDTH
CANVAS_H = SCREEN_HEIGHT

# цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (60, 60, 60)
BG_COLOR = (40, 40, 40)

# Палитра цветов
PALETTE = [
    (0, 0, 0), (255, 255, 255), (200, 20, 20), (220, 120, 30),
    (220, 220, 0), (20, 180, 20), (0, 150, 200), (30, 80, 200),
    (130, 30, 200), (200, 30, 140), (100, 100, 100), (160, 80, 20),
    (0, 200, 150), (255, 165, 0), (128, 0, 128), (0, 128, 128),
    (255, 105, 180), (144, 238, 144), (135, 206, 250), (255, 222, 173)
]

# Список инструментов
TOOLS = ["Pencil", "Rectangle", "Circle", "Eraser"]


# кнопка 
class Button:
    def __init__(self, rect, label, color=DARK_GRAY, text_color=WHITE):
        self.rect = pygame.Rect(rect)  # область кнопки
        self.label = label             # текст
        self.color = color
        self.text_color = text_color
        self.active = False            # выбрана ли кнопка

    def draw(self, surface, font):
        # если кнопка активна — зелёная
        bg = (100, 180, 100) if self.active else self.color

        pygame.draw.rect(surface, bg, self.rect, border_radius=5)
        pygame.draw.rect(surface, LIGHT_GRAY, self.rect, 1, border_radius=5)

        # текст кнопки
        text = font.render(self.label, True, self.text_color)
        surface.blit(text, text.get_rect(center=self.rect.center))

    def is_clicked(self, pos):
        # проверка клика по кнопке
        return self.rect.collidepoint(pos)


# главная функция
def main():
    pygame.init()

    # окно
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Paint")

    clock = pygame.time.Clock()

    # шрифты
    font = pygame.font.SysFont("Arial", 14, bold=True)
    small = pygame.font.SysFont("Arial", 12)

    # холст (где рисуем)
    canvas = pygame.Surface((CANVAS_W, CANVAS_H))
    canvas.fill(WHITE)

    # текущие настройки
    current_tool = "Pencil"
    draw_color = BLACK
    brush_size = 5
    eraser_size = 20

    drawing = False      # рисуем ли сейчас
    start_pos = None     # начальная точка (для фигур)
    temp_canvas = None   # копия для предпросмотра

    # кнопки
    tool_buttons = []
    for i, name in enumerate(TOOLS):
        btn = Button((10, 60 + i * 45, TOOLBAR_WIDTH - 20, 36), name)

        if name == current_tool:
            btn.active = True

        tool_buttons.append(btn)

    # слайдер размера кисти
    size_slider_rect = pygame.Rect(10, 340, TOOLBAR_WIDTH - 20, 10)
    MAX_BRUSH = 40

    # параметры палитры
    palette_start_y = 380
    swatch_size = 26
    cols_in_palette = 4

    # кнопка очистки
    clear_btn = Button(
        (10, SCREEN_HEIGHT - 50, TOOLBAR_WIDTH - 20, 36),
        "Clear",
        color=(150, 40, 40)
    )

    # игровой цикл
    while True:
        clock.tick(60)

        mouse_pos = pygame.mouse.get_pos()

        # координаты мыши относительно холста
        canvas_mouse = (mouse_pos[0] - CANVAS_X, mouse_pos[1] - CANVAS_Y)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # нажатие мыши 
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = mouse_pos

                # если клик в панели инструментов
                if mx < TOOLBAR_WIDTH:

                    # выбор инструмента
                    for btn in tool_buttons:
                        if btn.is_clicked(mouse_pos):
                            current_tool = btn.label
                            for b in tool_buttons:
                                b.active = False
                            btn.active = True

                    # очистка холста
                    if clear_btn.is_clicked(mouse_pos):
                        canvas.fill(WHITE)

                    # изменение размера кисти
                    if size_slider_rect.collidepoint(mouse_pos):
                        ratio = (mx - size_slider_rect.x) / size_slider_rect.width
                        brush_size = max(1, min(MAX_BRUSH, int(ratio * MAX_BRUSH)))
                        eraser_size = brush_size * 4

                    # выбор цвета
                    for idx, color in enumerate(PALETTE):
                        sx = 10 + (idx % cols_in_palette) * (swatch_size + 4)
                        sy = palette_start_y + (idx // cols_in_palette) * (swatch_size + 4)

                        if pygame.Rect(sx, sy, swatch_size, swatch_size).collidepoint(mouse_pos):
                            draw_color = color
                            current_tool = "Pencil"

                            # активируем карандаш
                            for b in tool_buttons:
                                b.active = (b.label == "Pencil")

                # если клик на холсте
                elif 0 <= canvas_mouse[0] < CANVAS_W and 0 <= canvas_mouse[1] < CANVAS_H:
                    drawing = True
                    start_pos = canvas_mouse

                    # сохраняем холст (для предпросмотра фигур)
                    temp_canvas = canvas.copy()

                    # сразу рисуем точку
                    if current_tool == "Pencil":
                        pygame.draw.circle(canvas, draw_color, canvas_mouse, brush_size)
                    elif current_tool == "Eraser":
                        pygame.draw.circle(canvas, WHITE, canvas_mouse, eraser_size)

            # отпускание мыши 
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if drawing and start_pos and current_tool in ("Rectangle", "Circle"):
                    ex, ey = canvas_mouse
                    sx, sy = start_pos

                    rect = pygame.Rect(
                        min(sx, ex),
                        min(sy, ey),
                        abs(ex - sx),
                        abs(ey - sy)
                    )

                    # рисуем фигуру
                    if current_tool == "Rectangle":
                        pygame.draw.rect(canvas, draw_color, rect, brush_size)
                    elif current_tool == "Circle":
                        radius = max(abs(ex - sx), abs(ey - sy)) // 2
                        pygame.draw.circle(
                            canvas,
                            draw_color,
                            ((sx + ex) // 2, (sy + ey) // 2),
                            radius,
                            brush_size
                        )

                drawing = False
                start_pos = None
                temp_canvas = None

            # движение мыши для рисовки 
            if event.type == pygame.MOUSEMOTION:
                if drawing and 0 <= canvas_mouse[0] < CANVAS_W and 0 <= canvas_mouse[1] < CANVAS_H:

                    if current_tool == "Pencil":
                        # предыдущая точка
                        prev = (
                            event.pos[0] - event.rel[0] - CANVAS_X,
                            event.pos[1] - event.rel[1] - CANVAS_Y
                        )

                        pygame.draw.line(canvas, draw_color, prev, canvas_mouse, brush_size * 2)
                        pygame.draw.circle(canvas, draw_color, canvas_mouse, brush_size)

                    elif current_tool == "Eraser":
                        pygame.draw.circle(canvas, WHITE, canvas_mouse, eraser_size)

        # отрисовка
        screen.fill(BG_COLOR)

        # предпросмотр фигур
        if drawing and temp_canvas and current_tool in ("Rectangle", "Circle"):
            preview = temp_canvas.copy()

            ex, ey = canvas_mouse
            sx, sy = start_pos

            rect = pygame.Rect(min(sx, ex), min(sy, ey), abs(ex - sx), abs(ey - sy))

            if current_tool == "Rectangle":
                pygame.draw.rect(preview, draw_color, rect, brush_size)

            elif current_tool == "Circle":
                radius = max(abs(ex - sx), abs(ey - sy)) // 2
                if radius > 0:
                    pygame.draw.circle(preview, draw_color,
                        ((sx + ex) // 2, (sy + ey) // 2),
                        radius,
                        brush_size)

            screen.blit(preview, (CANVAS_X, CANVAS_Y))
        else:
            screen.blit(canvas, (CANVAS_X, CANVAS_Y))

        # панель инструментов
        pygame.draw.rect(screen, BG_COLOR, (0, 0, TOOLBAR_WIDTH, SCREEN_HEIGHT))
        pygame.draw.line(screen, LIGHT_GRAY, (TOOLBAR_WIDTH, 0), (TOOLBAR_WIDTH, SCREEN_HEIGHT), 1)

        screen.blit(font.render("TOOLS", True, LIGHT_GRAY), (10, 10))

        for btn in tool_buttons:
            btn.draw(screen, font)

        # слайдер размера
        screen.blit(font.render(f"Size: {brush_size}", True, LIGHT_GRAY), (10, 320))
        pygame.draw.rect(screen, LIGHT_GRAY, size_slider_rect)
        pygame.draw.rect(screen, (100, 200, 100),
            (size_slider_rect.x, size_slider_rect.y,
             int(size_slider_rect.width * brush_size / MAX_BRUSH), 10))
        pygame.draw.rect(screen, WHITE, size_slider_rect, 1)

        # палитра
        screen.blit(font.render("Colors:", True, LIGHT_GRAY), (10, palette_start_y - 20))

        for idx, color in enumerate(PALETTE):
            sx = 10 + (idx % 4) * 30
            sy = palette_start_y + (idx // 4) * 30

            swatch = pygame.Rect(sx, sy, swatch_size, swatch_size)
            pygame.draw.rect(screen, color, swatch, border_radius=4)

            # рамка выбранного цвета
            if color == draw_color:
                pygame.draw.rect(screen, WHITE, swatch, 2, border_radius=4)

        # текущий цвет
        pygame.draw.rect(screen, draw_color,
            (10, palette_start_y + 140, TOOLBAR_WIDTH - 20, 28),
            border_radius=5)

        # инфо про ластик
        if current_tool == "Eraser":
            screen.blit(small.render(f"Eraser: {eraser_size}px", True, LIGHT_GRAY),
                        (10, palette_start_y + 175))

        # кнопка очистки
        clear_btn.draw(screen, font)

        pygame.display.flip()


# запуск программы
if __name__ == "__main__":
    main()