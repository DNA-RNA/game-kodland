import random

# Set up the game screen
TITLE = 'Flappy Bird'
WIDTH = 640
HEIGHT = 480

# Colors
ground_color = (50, 50, 50)  # Koyu gri renk (RGB)
button_color = (100, 100, 255)  # Mavi buton rengi
button_hover_color = (150, 150, 255)  # Açık mavi (üzerine gelindiğinde)
text_color = "white"  # Buton metin rengi

# Game state
game_state = 'menu'  # Başlangıç durumu menü
mouse_position = (0, 0)  # Fare pozisyonunu tutacak değişken

# Button positions and sizes
buttons = {
    "start": Rect((220, 150), (200, 50)),
    "toggle_sound": Rect((220, 220), (200, 50)),
    "exit": Rect((220, 290), (200, 50))
}

# Sound state
sound_on = True


def draw():
    if game_state == 'menu':
        draw_menu()
    elif game_state == 'playing':
        draw_game()


def draw_menu():
    screen.fill((0, 0, 0))  # Siyah arka plan
    screen.draw.text("Flappy Bird", center=(WIDTH // 2, 50), fontsize=50, color=text_color)

    # Butonları çiz
    for name, rect in buttons.items():
        if rect.collidepoint(mouse_position):  # Fare butonun üzerine gelirse
            screen.draw.filled_rect(rect, button_hover_color)
        else:
            screen.draw.filled_rect(rect, button_color)
        screen.draw.text(name.replace("_", " ").capitalize(), center=rect.center, color=text_color, fontsize=30)


def draw_game():
    screen.fill((135, 206, 235))  # Açık mavi bir arka plan
    screen.draw.filled_rect(Rect((0, HEIGHT - 50), (WIDTH, 50)), ground_color)  # Koyu gri zemin
    screen.draw.text('Score: ', color='white', midtop=(50, 10), shadow=(0.5, 0.5), scolor='black', fontsize=30)


def on_mouse_move(pos):
    global mouse_position
    mouse_position = pos  # Fare pozisyonunu güncelle


def on_mouse_down(pos):
    global game_state, sound_on

    if game_state == 'menu':
        if buttons["start"].collidepoint(pos):
            game_state = 'playing'
        elif buttons["toggle_sound"].collidepoint(pos):
            sound_on = not sound_on
        elif buttons["exit"].collidepoint(pos):
            exit()  # Exit


def update():
    if game_state == 'playing':
        pass  # Oyun güncellemeleri buraya eklenecek
