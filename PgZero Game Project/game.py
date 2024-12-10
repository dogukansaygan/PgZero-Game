import pgzrun
import random

WIDTH = 720
HEIGHT = 480

current_level = 1
win = False  # Kazanma durumu kontrolü
game_over = False  # Kaybetme durumu kontrolü

player = Actor("myslime1", (WIDTH / 2, HEIGHT / 2))
player.images = ["myslime1", "myslime2"]
player.frame_index = 0
player.animation_speed = 5
player.animation_counter = 0

enemy = Actor("enemyslime1", (WIDTH / 4, HEIGHT / 4))
enemy.images = ["enemyslime1", "enemyslime2"]
enemy.frame_index = 0
enemy.animation_speed = 5
enemy.animation_counter = 0
enemy_speed = 0.5

start_button = Actor("start", (WIDTH / 2, 125))
sound_button = Actor("sound_turn_off", (WIDTH / 2, 225))
sound_button.images = ["sound_turn_off", "sound_turn_on"]
exit_button = Actor("exit", (WIDTH / 2, 325))

gate = Actor("next_scene2", (WIDTH / 2, HEIGHT / 2))
gate.visible = False

coins = []
total_coins_collected = 0
total_coins_count = 5

game_started = False
game_music_enabled = True
gate_visible = False

def generate_coins():
    global coins
    coins = []
    for _ in range(total_coins_count):
        x = random.randint(50, WIDTH - 50)
        y = random.randint(50, HEIGHT - 50)
        coin = Actor("coin", (x, y))
        coins.append(coin)

def draw():
    screen.fill((0, 0, 0))
    
    if win:  # Kazanma ekranı
        screen.draw.text("Tebrikler! Oyunu Kazandınız!", center=(WIDTH / 2, HEIGHT / 2), fontsize=50, color="green")
        return
    
    if game_over:  # Kaybetme ekranı
        screen.draw.text("Kaybettin!", center=(WIDTH / 2, HEIGHT / 2), fontsize=50, color="red")
        return
    
    player.draw()
    enemy.draw()
    
    for coin in coins:
        coin.draw()
    
    if not game_started:
        start_button.draw()
        sound_button.draw()
        exit_button.draw()
    
    screen.draw.text(f"Bolum Sayisi: {current_level}", (10, 10), fontsize=30, color="yellow")
    screen.draw.text(f"Toplanan Altin: {total_coins_collected}", (10, 40), fontsize=30, color="white")
    
    if gate_visible:
        gate.draw()

def on_mouse_down(pos):
    global game_started, game_music_enabled
    if not game_started:
        if 270 <= pos[0] <= 450 and 85 <= pos[1] <= 165:  # Start button
            game_started = True
        elif 270 <= pos[0] <= 450 and 185 <= pos[1] <= 265:  # Sound on/off button
            game_music_enabled = not game_music_enabled
            if game_music_enabled:
                sound_button.image = "sound_turn_off"
                sounds.bg_music.play(-1)
            else:
                sound_button.image = "sound_turn_on"
                sounds.bg_music.stop()
        elif 270 <= pos[0] <= 450 and 285 <= pos[1] <= 365:  # Exit button
            quit()

def update():
    global total_coins_collected, game_over, gate_visible, current_level, win

    if win or game_over:  # Kazanma veya kaybetme durumu
        return
    
    moving = False
    
    if game_started:
        if keyboard.left:
            player.x -= 5
            moving = True
        if keyboard.right:
            player.x += 5
            moving = True
        if keyboard.up:
            player.y -= 5
            moving = True
        if keyboard.down:
            player.y += 5
            moving = True
    
    player.animation_counter += 1
    if player.animation_counter >= player.animation_speed:
        player.frame_index = (player.frame_index + 1) % len(player.images)
        player.image = player.images[player.frame_index]
        player.animation_counter = 0
    
    for coin in coins[:]:
        if player.colliderect(coin):
            if game_music_enabled:
                sounds.gold.play()
            coins.remove(coin)
            total_coins_collected += 1
    
    if len(coins) == 0:
        gate_visible = True
        gate.visible = True
    
    if gate_visible and player.colliderect(gate):
        current_level += 1
        gate_visible = False
        gate.visible = False
        generate_coins()
        total_coins_collected = 0
        
        if current_level == 5:  # Kazanma kontrolü
            win = True
    
    if game_started:
        move_enemy()
    
    if player.colliderect(enemy):
        game_over = True  # Oyunu kaybetme durumu

def move_enemy():
    if enemy.x < player.x:
        enemy.x += enemy_speed
    elif enemy.x > player.x:
        enemy.x -= enemy_speed
    
    if enemy.y < player.y:
        enemy.y += enemy_speed
    elif enemy.y > player.y:
        enemy.y -= enemy_speed
    
    enemy.animation_counter += 1
    if enemy.animation_counter >= enemy.animation_speed:
        enemy.frame_index = (enemy.frame_index + 1) % len(enemy.images)
        enemy.image = enemy.images[enemy.frame_index]
        enemy.animation_counter = 0

generate_coins()
if game_music_enabled:
    sounds.bg_music.play(-1)

pgzrun.go()