import pgzrun
import random
'''v2'''
WIDTH = 800
HEIGHT = 600
TILE_SIZE = 50

# Oyun Durumları
GAME_MENU = 0
GAME_PLAY = 1
GAME_OVER = 2

game_state = GAME_MENU
score = 0
enemy_move_timer = 0
enemy_move_delay = 30
enemies = []
map_grid = []
game_over_timer = 0

# Ses Durumu
music_playing = True  # Müzik varsayılan olarak açık

# Ninja Sprite'ları
ninja_run_images = ['run_001', 'run_002', 'run_003', 'run_004', 'run_005']
ninja_die_image = 'dead'
ninja_idle_images = ['idle_001', 'idle_002']

# Düşman Animasyonları
enemy_run_images = ['meteorbrown_001', 'meteorbrown_002']
enemy_idle_image = 'meteorbrown'


# Düğme Boyutları
button_width = 200
button_height = 50
buttons = [
    {"text": "Oyuna Başla", "x": WIDTH // 2 - button_width // 2, "y": 200, "action": "start_game"},
    {"text": "Müzik Aç/Kapat", "x": WIDTH // 2 - button_width // 2, "y": 300, "action": "toggle_music"},
    {"text": "Çıkış", "x": WIDTH // 2 - button_width // 2, "y": 400, "action": "exit_game"},
]

# Ninja Sınıfı
class Ninja:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = "idle"  # "idle", "run", "dead"
        self.image_index = 0
        self.actor = Actor(ninja_idle_images[0], (self.x * TILE_SIZE + TILE_SIZE // 2, self.y * TILE_SIZE + TILE_SIZE // 2))

    def draw(self):
        self.actor.draw()

    def update_animation(self):
        """Duruma göre animasyonu güncelle."""
        if self.state == "idle":
            self.image_index = (self.image_index + 1) % len(ninja_idle_images)
            self.actor.image = ninja_idle_images[self.image_index]
        elif self.state == "walk":
            self.image_index = (self.image_index + 1) % len(ninja_run_images)
            self.actor.image = ninja_run_images[self.image_index]
            sounds.run_voice.play()
        elif self.state == "dead":
            self.actor.image = ninja_die_image


    def move(self, dx, dy):
        global game_state, game_over_timer
        if self.state == "dead":  # Ölüm durumunda hareket etme
            return
        new_x = self.x + dx
        new_y = self.y + dy

        if 0 <= new_y < len(map_grid) and 0 <= new_x < len(map_grid[0]):
            if map_grid[new_y][new_x] == "E":
                self.state = "dead"
                game_state = GAME_OVER
                game_over_timer = 120
            elif map_grid[new_y][new_x] == "G":
                global score
                score += 10
                create_random_map()
            elif map_grid[new_y][new_x] == " ":
                self.x, self.y = new_x, new_y
                self.state = "walk"
                animate(self.actor, pos=(self.x * TILE_SIZE + TILE_SIZE // 2, self.y * TILE_SIZE + TILE_SIZE // 2), duration=0.2, on_finished=self.stop)
    def stop(self):
        """Hareket bittiğinde durumu idle olarak ayarla."""
        if self.state != "dead":
            self.state = "idle"
ninja = Ninja(1, 1)

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = "idle"  # "idle", "run"
        self.image_index = 0

    def draw(self):
        if self.state == "idle":
            image = enemy_idle_image
        elif self.state == "run":
            self.image_index = (self.image_index + 1) % len(enemy_run_images)
            image = enemy_run_images[self.image_index]
        screen.blit(image, (self.x * TILE_SIZE, self.y * TILE_SIZE))

    def move(self):
        dx, dy = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
        new_x = self.x + dx
        new_y = self.y + dy
        if map_grid[new_y][new_x] == " ":
            self.state = "run"
            map_grid[self.y][self.x] = " "
            self.x = new_x
            self.y = new_y
            map_grid[self.y][self.x] = "E"
        else:
            self.state = "idle"

def draw_menu():
    screen.clear()
    screen.draw.text("ANA MENÜ", center=(WIDTH // 2, 100), fontsize=60, color="white")
    for button in buttons:
        screen.draw.filled_rect(Rect(button["x"], button["y"], button_width, button_height), "blue")
        screen.draw.text(button["text"], center=(button["x"] + button_width // 2, button["y"] + button_height // 2), fontsize=30, color="white")

def on_mouse_down(pos):
    global game_state, music_playing
    if game_state == GAME_MENU:
        for button in buttons:
            if Rect(button["x"], button["y"], button_width, button_height).collidepoint(pos):
                if button["action"] == "start_game":
                    start_game()
                elif button["action"] == "toggle_music":
                    toggle_music()
                elif button["action"] == "exit_game":
                    exit_game()

def start_game():
    global game_state, score
    game_state = GAME_PLAY
    score = 0
    ninja.x, ninja.y = 1, 1  # Ninja başlangıç pozisyonuna yerleştir
    ninja.draw()
    create_random_map()

def toggle_music():
    global music_playing
    if music_playing:
        sounds.background.stop()
        music_playing = False
    else:
        sounds.background.play()  # Arka plan müziği
        music_playing = True

def exit_game():
    exit()

def draw_game():
    screen.clear()
    for row in range(len(map_grid)):
        for col in range(len(map_grid[row])):
            x, y = col * TILE_SIZE, row * TILE_SIZE
            if map_grid[row][col] == "#":
                screen.draw.filled_rect(Rect(x, y, TILE_SIZE, TILE_SIZE), "grey")
            elif map_grid[row][col] == "G":
                screen.draw.filled_rect(Rect(x, y, TILE_SIZE, TILE_SIZE), "green")
    ninja.draw()
    for enemy in enemies:
            enemy.draw()
    screen.draw.text(f"Score: {score}", (10, 10), fontsize=24, color="white")

def update_game():
    global enemy_move_timer
    ninja.update_animation()
    enemy_move_timer += 1
    if enemy_move_timer >= enemy_move_delay:
        enemy_move_timer = 0
        for enemy in enemies:
            enemy.move()

def create_random_map():
    global map_grid, enemies
    map_grid = [[" " if random.random() > 0.2 else "#" for _ in range(WIDTH // TILE_SIZE)] for _ in range(HEIGHT // TILE_SIZE)]
    for i in range(HEIGHT // TILE_SIZE):
        map_grid[i][0] = map_grid[i][-1] = "#"
    for j in range(WIDTH // TILE_SIZE):
        map_grid[0][j] = map_grid[-1][j] = "#"
    map_grid[ninja.y][ninja.x] = "H"
    exit_x = random.randint(2, (WIDTH // TILE_SIZE) - 2)
    exit_y = random.randint(2, (HEIGHT // TILE_SIZE) - 2)
    map_grid[exit_y][exit_x] = "G"
    enemies.clear()
    for _ in range(4):  # 2 düşman
        while True:
            enemy_x = random.randint(2, (WIDTH // TILE_SIZE) - 2)
            enemy_y = random.randint(2, (HEIGHT // TILE_SIZE) - 2)
            if map_grid[enemy_y][enemy_x] == " ":
                map_grid[enemy_y][enemy_x] = "E"
                enemies.append(Enemy(enemy_x, enemy_y))
                break

def update():
    global game_state, score,game_over_timer # Global değişkenleri tanımlıyoruz
    ninja.update_animation()
    if game_state == GAME_PLAY:

        update_game()
    elif game_state == GAME_OVER:
        # Game Over durumunda oyunu sıfırlayıp baştan başlat
        if game_over_timer > 0:
            game_over_timer -= 1
            ninja.state="dead"
            screen.draw.text("Game Over", center=(WIDTH // 2, HEIGHT // 2), fontsize=60, color="red")
        else:
            # "Game Over" yazısını gösterdikten sonra oyunu yeniden başlat
            game_state = GAME_PLAY
            score = 0
            ninja.state="idle"
            ninja.x, ninja.y = 1, 1
            create_random_map()


def on_key_down(key):
    if key == keys.UP:
        ninja.move(0, -1)
    elif key == keys.DOWN:
        ninja.move(0, 1)
    elif key == keys.LEFT:
        ninja.move(-1, 0)
    elif key == keys.RIGHT:
        ninja.move(1, 0)



def draw():
    if game_state == GAME_MENU:
        draw_menu()
    elif game_state == GAME_PLAY:
        draw_game()

# Uygulama başladığında müzik otomatik başlatılır
sounds.background.play()
music_playing = True

pgzrun.go()
