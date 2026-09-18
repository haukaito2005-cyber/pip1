import pygame
import sys
import random
import json
import os

pygame.init()

# ==========================
# COLOR
# ==========================
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (220,60,60)
GREEN = (0,180,0)
BLUE = (0,120,220)
LIGHT_RED = (255,180,180)
LIGHT_BLUE = (70,170,255)
LIGHT_GREEN = (180,255,180)
GRAY = (120,120,120)
LIGHT_GRAY = (220,220,220)
DARK_GRAY = (50,50,50)
YELLOW = (255,255,0)
BACKGROUND_GREEN = (20,120,20)

# ==========================
# DRAW TEXT
# ==========================
def draw_text(
    surface,
    text,
    font,
    color,
    center=None,
    topleft=None
):
    text_surface = font.render(
        str(text),
        True,
        color
    )

    if center:
        rect = text_surface.get_rect(
            center=center
        )
    elif topleft:

        rect = text_surface.get_rect(
            topleft=topleft
        )
    else:
        rect = text_surface.get_rect()
    surface.blit(
        text_surface,
        rect
    )
    return rect

# ======================================================
# DRAW BUTTON
# ======================================================
def draw_button(
    surface,
    rect,
    text,
    font,
    mouse_pos,
    bg_color,
    hover_color,
    text_color=WHITE,
    border_color=BLACK,
    border_width=3,
    radius=10,
    hover_size=8
):
    # Hiệu ứng hover
    if rect.collidepoint(mouse_pos):
        pygame.draw.rect(
            surface,
            hover_color,
            rect.inflate(hover_size, hover_size),
            border_radius=radius + 2
        )

    # Nền
    pygame.draw.rect(
        surface,
        bg_color,
        rect,
        border_radius=radius
    )

    # Viền
    pygame.draw.rect(
        surface,
        border_color,
        rect,
        border_width,
        border_radius=radius
    )

    # Chữ
    draw_text(
        surface,
        text,
        font,
        text_color,
        center=rect.center
    )

WIDTH = 1000
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH,HEIGHT))

pygame.display.set_caption("ベトナム伝統ゲーム　バウクア")

clock = pygame.time.Clock()
title_font = pygame.font.SysFont(
    "Yu Gothic",
    60,
    bold=True
)
info_font = pygame.font.SysFont(
    "Yu Gothic",
    30
)
animal_font = pygame.font.SysFont(
    "Yu Gothic",
    40
)
button_font = pygame.font.SysFont(
    "Yu Gothic",
    30
)

animals = [
    "Bau",
    "Cua",
    "Tom",
    "Ca",
    "Ga",
    "Nai"
]
animal_japanese = {
    "Bau": "瓢箪",
    "Cua": "カニ",
    "Tom": "エビ",
    "Ca": "魚",
    "Ga": "鶏",
    "Nai": "シカ"
}
animal_images = {
    "Bau": pygame.image.load("BAUCUAGAME.py/images/bau.png"),
    "Cua": pygame.image.load("BAUCUAGAME.py//images/cua.png"),
    "Tom": pygame.image.load("BAUCUAGAME.py/images/tom.png"),
    "Ca": pygame.image.load("BAUCUAGAME.py/images/ca.png"),
    "Ga": pygame.image.load("BAUCUAGAME.py/images/ga.png"),
    "Nai": pygame.image.load("BAUCUAGAME.py/images/nai.png")
}

for key in animal_images:
    animal_images[key] = pygame.transform.scale(
        animal_images[key],
        (90,90)
    )

boxes = []
start_x = 190
start_y = 250

for row in range(2):
    for col in range(3):
        rect = pygame.Rect(
            start_x + col * 180,
            start_y + row * 150,
            150,
            100
        )
        boxes.append(rect)

shake_button = pygame.Rect(
    800,   # x
    590,   # y
    150,   # rộng
    60     # cao
)
cancel_button = pygame.Rect(
    800,
    420,
    160,
    55
)
plus_button = pygame.Rect(
    810,
    500,
    55,
    55
)
minus_button = pygame.Rect(
    900,
    500,
    55,
    55
)
yes_button = pygame.Rect(
    320,
    320,
    120,
    60
)
no_button = pygame.Rect(
    560,
    320,
    120,
    60
)
game_over_new_button = pygame.Rect(
    270,
    400,
    220,
    60
)
game_over_menu_button = pygame.Rect(
    520,
    400,
    220,
    60
)
new_yes_button = pygame.Rect(
    320,
    380,
    120,
    60
)
new_no_button = pygame.Rect(
    560,
    380,
    120,
    60
)
new_game_button = pygame.Rect(
    350,
    220,
    300,
    70
)
continue_button = pygame.Rect(
    350,
    320,
    300,
    70
)
quit_button = pygame.Rect(
    350,
    520,
    300,
    70
)
save_button = pygame.Rect(
    800,
    340,
    160,
    55
)
continue_cancel_button = pygame.Rect(
    400,
    420,
    200,
    60
)
exit_button = pygame.Rect(
    900,
    20,
    60,
    60
)
exit_yes_button = pygame.Rect(
    320,
    380,
    120,
    60
)
exit_no_button = pygame.Rect(
    560,
    380,
    120,
    60
)
ranking_button = pygame.Rect(
    350,
    420,
    300,
    70
)
ranking_back_button = pygame.Rect(
    400,
    600,
    200,
    60
)
delete_rank_button = pygame.Rect(
    800,
    75,
    160,
    55
)
rank_ok_button = pygame.Rect(
    440,
    430,
    120,
    60
)
id_error_ok_button = pygame.Rect(
    430,
    380,
    140,
    60
)   
popup_ok_button = pygame.Rect(
    WIDTH//2 - 60,
    HEIGHT//2 + 50,
    120,
    50
)

running = True
game_state = "menu"
input_text = ""
login_message = ""
player_id = str(random.randint(100000,999999))

bets = {
    "Bau": 0,
    "Cua": 0,
    "Tom": 0,
    "Ca": 0,
    "Ga": 0,
    "Nai": 0
}
selected_animals = []
bet_amount = 100
show_confirm = False
show_cancel_confirm = False
show_new_game_confirm = False
show_exit_confirm = False
show_game_over = False
show_rank_popup = False
rank_popup_message = ""
popup_active = False
popup_message = ""
show_id_error = False
rank_scroll = 0

results = [] 
message = ""
message_timer = 0  
money = 10000
player_name = ""
name_input = ""
best_money = 10000
shaking = False
shake_timer = 0

def get_rank(money):

    if best_money >= 1000000:
        return "マスター"
    elif best_money >= 500000:
        return "SSS"
    elif best_money >= 300000:
        return "SS"
    elif best_money >= 150000:
        return "S"
    elif best_money >= 80000:
        return "A"
    elif best_money >= 40000:
        return "B"
    elif best_money >= 20000:
        return "C"
    else:
        return "D"

def save_game():
    global best_money
    data = {
        "player_id": player_id,
        "player_name": player_name,
        "money": money,
        "best_money": best_money,
        "bet_amount": bet_amount,
        "rank": get_rank(money)
    }
    with open(
        f"save_{player_id}.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4
        )

def load_game(player_id_input):

    global money
    global bet_amount
    global player_id
    global player_name
    global best_money

    filename = f"save_{player_id_input}.json"

    if os.path.exists(filename):
        with open(
            filename,
            "r",
            encoding="utf-8"
        ) as file:
            data = json.load(file)
            money = data["money"]
            bet_amount = data["bet_amount"]
            player_id = data["player_id"]
            player_name = data.get(
                "player_name",
                "Player"
            )
            best_money = data.get(
                "best_money",
                money
            )
        return True
    return False

def update_ranking():
    ranking_file = "ranking.json"
    if os.path.exists(ranking_file):
        with open(
            ranking_file,
            "r",
            encoding="utf-8"
        ) as file:
            ranking = json.load(file)
    else:
        ranking = []
    found = False

    for player in ranking:
        if player["player_id"] == player_id:
            player["player_name"] = player_name
            player["money"] = money
            player["rank"] = get_rank(money)
            found = True
            break
    if not found:
        ranking.append({
            "player_id": player_id,
            "player_name": player_name,
            "money": money,
            "best_money": best_money,
            "rank": get_rank(money)
        })
    ranking.sort(
        key=lambda x: x["money"],
        reverse=True
    )
    with open(
        ranking_file,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            ranking,
            file,
            ensure_ascii=False,
            indent=4
        )

def delete_player_from_rank():
    if not os.path.exists("ranking.json"):
        return False
    with open(
        "ranking.json",
        "r",
        encoding="utf-8"
    ) as file:
        ranking = json.load(file)
    original_count = len(ranking)
    ranking = [
        p
        for p in ranking
        if p["player_id"] != player_id
    ]
    with open(
        "ranking.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            ranking,
            file,
            ensure_ascii=False,
            indent=4
        )
    return len(ranking) < original_count

def get_ranking():
    if not os.path.exists("ranking.json"):
        return []
    with open(
        "ranking.json",
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)

while running:
    mouse_pos = pygame.mouse.get_pos()

    # xử lý sự kiện 
    for event in pygame.event.get():                
        if event.type == pygame.QUIT:
            running = False
        
        elif game_state == "login":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if load_game(input_text):
                        login_message = "ロード成功！"
                        game_state = "playing"
                    else:
                        show_id_error = True
                    input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode  

        if game_state == "name_input":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if name_input.strip() != "":
                        player_name = name_input
                        money = 10000
                        best_money = 10000
                        player_id = str(
                            random.randint(100000,999999)
                        )
                        name_input = ""
                        game_state = "playing"
                elif event.key == pygame.K_BACKSPACE:
                    name_input = name_input[:-1]
                else:
                    if len(name_input) < 15:
                        name_input += event.unicode 

        if game_state == "ranking":
            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    rank_scroll -= 1
                elif event.y < 0:
                    rank_scroll += 1
                max_scroll = max(
                    0,
                    len(get_ranking()) - 10
                )
                rank_scroll = max(
                    0,
                    min(rank_scroll, max_scroll)
                 ) 

        if event.type == pygame.MOUSEBUTTONDOWN:

            if popup_active:
                if popup_ok_button.collidepoint(mouse_pos):
                    popup_active = False
                continue

            if show_rank_popup:
                if rank_ok_button.collidepoint(mouse_pos):
                    show_rank_popup = False
                continue

            if show_id_error:
                if id_error_ok_button.collidepoint(mouse_pos):
                    show_id_error = False
                continue

            if game_state == "login":
                if continue_cancel_button.collidepoint(mouse_pos):
                    game_state = "menu"
                    login_message = ""
                    input_text = ""
                    continue

            if show_game_over:
                if game_over_new_button.collidepoint(mouse_pos):
                    money = 10000
                    best_money = 10000
                    bet_amount = 100
                    for animal in bets:
                        bets[animal] = 0
                    selected_animals.clear()
                    results.clear()
                    show_game_over = False
                    game_state = "playing"

                elif game_over_menu_button.collidepoint(mouse_pos):
                    money = 10000
                    best_money = 10000
                    bet_amount = 100
                    for animal in bets:
                        bets[animal] = 0
                    selected_animals.clear()
                    results.clear()
                    show_game_over = False
                    game_state = "menu"
                continue

            if show_exit_confirm:
                if exit_yes_button.collidepoint(mouse_pos):
                    for animal in bets:
                        bets[animal] = 0
                    selected_animals.clear()
                    results.clear()
                    show_confirm = False
                    show_cancel_confirm = False
                    show_exit_confirm = False
                    game_state = "menu"
                elif exit_no_button.collidepoint(mouse_pos):
                    show_exit_confirm = False
                continue

            if show_new_game_confirm:
                if new_yes_button.collidepoint(mouse_pos):
                    money = 10000
                    bet_amount = 100
                    for animal in bets:
                        bets[animal] = 0
                    selected_animals.clear()
                    results.clear()
                    game_state = "playing"
                    show_new_game_confirm = False
                elif new_no_button.collidepoint(mouse_pos):
                    show_new_game_confirm = False
                continue

            if show_confirm:
                if yes_button.collidepoint(mouse_pos):
                    total_bet = sum(bets.values())
                    if total_bet <= money:
                        money -= total_bet
                        shaking = True
                        shake_timer = 60
                        show_confirm = False 
                    else:
                        message = "所持金が足りません！"
                        message_timer = 120   
                elif no_button.collidepoint(mouse_pos):
                        show_confirm = False
                continue

            if show_cancel_confirm:
                if yes_button.collidepoint(mouse_pos):
                    for animal in bets:
                        bets[animal] = 0
                    selected_animals.clear()
                    message = "すべての賭けを取り消しました！"
                    message_timer = 120
                    show_cancel_confirm = False
                elif no_button.collidepoint(mouse_pos):
                    show_cancel_confirm = False
                continue

            if game_state == "menu":
                if new_game_button.collidepoint(mouse_pos):
                    game_state = "name_input"
                elif continue_button.collidepoint(mouse_pos):
                    game_state = "login"
                elif ranking_button.collidepoint(mouse_pos):
                    game_state = "ranking"
                elif quit_button.collidepoint(mouse_pos):
                    running = False

            elif game_state == "ranking":
                if ranking_back_button.collidepoint(mouse_pos):
                    game_state = "menu"
                    continue
                elif delete_rank_button.collidepoint(mouse_pos):
                    if delete_player_from_rank():
                        rank_popup_message = (
                            "ランキングから削除しました"
                        )
                    else:
                        rank_popup_message = (
                            "削除するデータがありません"
                        )
                    show_rank_popup = True
                    continue

            if game_state == "playing":

                if shaking:
                    continue

                if plus_button.collidepoint(mouse_pos):
                    bet_amount += 100

                elif minus_button.collidepoint(mouse_pos):
                    if bet_amount > 100:
                        bet_amount -= 100

                elif exit_button.collidepoint(mouse_pos):
                    show_exit_confirm = True

                elif save_button.collidepoint(mouse_pos):
                    save_game()
                    update_ranking()
                    message = (
                        f"保存成功！ID:{player_id}"
                    )
                    message_timer = 180

                elif cancel_button.collidepoint(mouse_pos):
                    total_bet = sum(bets.values())
                    if total_bet > 0:
                        show_cancel_confirm = True

                elif shake_button.collidepoint(mouse_pos) and not shaking:
                    total_bet = sum(bets.values())
                    if total_bet > 0:
                        show_confirm = True

                if money <= 0:
                    continue

                for i, rect in enumerate(boxes):
                    if rect.collidepoint(mouse_pos):
                        animal = animals[i]

                        # Chuột trái
                        if event.button == 1:
                            if animal in selected_animals:
                                if sum(bets.values()) + bet_amount <= money:
                                    bets[animal] += bet_amount
                            elif len(selected_animals) < 3:
                                selected_animals.append(animal)
                                bets[animal] += bet_amount
                            else:
                                message = "3つまでしか選べません!!!"
                                message_timer = 120

                        elif event.button == 3:
                            if animal in selected_animals:
                                bets[animal] = 0
                                selected_animals.remove(animal)
                                message = f"{animal_japanese[animal]}を取り消しました"
                                message_timer = 120
                        
    # Cập nhật lắc
    if shaking:
        shake_timer -= 1
        results = [
            random.choice(animals),
            random.choice(animals),
            random.choice(animals)
        ]
        if shake_timer <= 0:
            shaking = False
            reward = 0
            for animal in bets:
                count = results.count(animal)
                if count > 0:
                    reward += bets[animal]
                    reward += bets[animal] * count
            money += reward
            if money > best_money:
                best_money = money
            if money == 0:
                show_game_over = True
            if reward > 0:
                popup_message = f"おめでとう!\n+{reward}円"
            else:
                popup_message = "残念!\n0円"
            popup_active = True
            for animal in bets:
                bets[animal] = 0
            selected_animals.clear()
    
    if message_timer > 0:
        message_timer -= 1
        if message_timer == 0:
            message = ""

    mouse_pos = pygame.mouse.get_pos()

    # vẽ nền
    screen.fill(BACKGROUND_GREEN)

    if game_state == "name_input":
            screen.fill(BACKGROUND_GREEN)
            title = title_font.render(
                "名前入力",
                True,
                (255,255,0)
            )       
            screen.blit(
                title,
                title.get_rect(center=(WIDTH//2,120))
            )

            box = pygame.Rect(
                300,
                280,
                400,
                70
            )
            pygame.draw.rect(
                screen,
                WHITE,
                box,
                border_radius=10
            )
            pygame.draw.rect(
                screen,
                BLACK,
                box,
                3,
                border_radius=10
            )

            txt = animal_font.render(
                name_input,
                True,
                (0,0,0)
            )
            screen.blit(
                txt,
                (320,295)
            )

            guide = info_font.render(
                "名前を入力してEnter",
                True,
                (255,255,255)
            )
            screen.blit(
                guide,
                (350,220)
            )

            pygame.display.flip()
            clock.tick(60)
            continue

    if game_state == "menu":
        mouse_pos = pygame.mouse.get_pos()
        title = title_font.render(
            "バウクア",
            True,
            (255,255,0)
        )
        screen.blit(
            title,
            title.get_rect(center=(WIDTH//2,120))
        )

        buttons = [
            (new_game_button,"新しいゲーム"),
            (continue_button,"続きから"),
            (ranking_button,"ランキング"),
            (quit_button,"終了")
        ]

        for rect,text in buttons:
            color = (80,80,80)
            if (
                not show_new_game_confirm
                and rect.collidepoint(mouse_pos)
            ):
                color = (120,120,120)
            pygame.draw.rect(
                screen,
                color,
                rect,
                border_radius=15
            )
            pygame.draw.rect(
                screen,
                BLACK,
                rect,
                3,
                border_radius=15
            )

            txt = animal_font.render(
                text,
                True,
                (255,255,255)
            )
            screen.blit(
                txt,
                txt.get_rect(center=rect.center)
            )

        if show_new_game_confirm:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(120)
            overlay.fill((0,0,0))
            screen.blit(overlay, (0,0))

            popup = pygame.Rect(
                180,
                160,
                640,
                320
            )
            pygame.draw.rect(
                screen,
                (240,240,240),
                popup,
                border_radius=20
            )
            pygame.draw.rect(
                screen,
                BLACK,
                popup,
                3,
                border_radius=20
            )

            title_text = animal_font.render(
                "確認",
                True,
                (0,0,0)
            )
            screen.blit(
                title_text,
                title_text.get_rect(
                    center=(popup.centerx,popup.y + 50)
                )
            )

            line1 = info_font.render(
                "新しいゲームを開始すると",
                True,
                (0,0,0)
            )
            line2 = info_font.render(
                "現在のデータは削除されます。",
                True,
                (0,0,0)
            )
            line3 = info_font.render(
                "よろしいですか？",
                True,
                (0,0,0)
            )

            screen.blit(
                line1,
                line1.get_rect(
                    center=(popup.centerx, 275)
                )
            )
            screen.blit(
                line2,
                line2.get_rect(
                    center=(popup.centerx, 315)
                )
            )
            screen.blit(
                line3,
                line3.get_rect(
                    center=(popup.centerx, 355)
                )
            )
            
            if new_yes_button.collidepoint(mouse_pos):
                pygame.draw.rect(
                    screen,
                    (180,255,180),
                    new_yes_button.inflate(8,8),
                    border_radius=12
                )
            pygame.draw.rect(
                screen,
                (0,180,0),
                new_yes_button,
                border_radius=10
            )
            pygame.draw.rect(
                screen,
                BLACK,
                new_yes_button,
                2,
                border_radius=10
            )

            if new_no_button.collidepoint(mouse_pos):
                pygame.draw.rect(
                    screen,
                    (255,180,180),
                    new_no_button.inflate(8,8),
                    border_radius=12
                )
            pygame.draw.rect(
                screen,
                (200,0,0),
                new_no_button,
                border_radius=10
            )
            pygame.draw.rect(
                screen,
                BLACK,
                new_no_button,
                2,
                border_radius=10
            )

            screen.blit(
                animal_font.render(
                    "はい",
                    True,
                    (255,255,255)
                ),
                animal_font.render(
                    "はい",
                    True,
                    (255,255,255)
                ).get_rect(center=new_yes_button.center)
            )
            screen.blit(
                animal_font.render(
                    "いいえ",
                    True,
                    (255,255,255)
                ),
                animal_font.render(
                    "いいえ",
                    True,
                    (255,255,255)
                ).get_rect(center=new_no_button.center)
            )

        pygame.display.flip()
        clock.tick(60)
        continue

    if game_state == "login":
        screen.fill(BACKGROUND_GREEN)
        title = title_font.render(
            "プレイヤーID入力",
            True,
            (255,255,0)
        )
        screen.blit(
            title,
            title.get_rect(
                center=(WIDTH//2,120)
            )
        )

        if continue_cancel_button.collidepoint(mouse_pos):
            pygame.draw.rect(
                screen,
                (220,220,220),
                continue_cancel_button.inflate(8,8),
                border_radius=12
            )
        pygame.draw.rect(
            screen,
            (120,120,120),
            continue_cancel_button,
            border_radius=10
        )
        pygame.draw.rect(
            screen,
            BLACK,
            continue_cancel_button,
            2,
            border_radius=10
        )

        cancel_text = animal_font.render(
            "キャンセル",
            True,
            (255,255,255)
        )
        screen.blit(
            cancel_text,
            cancel_text.get_rect(
                center=continue_cancel_button.center
            )
        )

        input_box = pygame.Rect(
            300,
            280,
            400,
            70
        )

        pygame.draw.rect(
            screen,
            WHITE,
            input_box,
            border_radius=15
        )
        pygame.draw.rect(
            screen,
            BLACK,
            input_box,
            3,
            border_radius=15
        )

        text_surface = animal_font.render(
            input_text,
            True,
            (0,0,0)
        )
        screen.blit(
            text_surface,
            (320,295)
        )

        guide = info_font.render(
            "プレイヤーIDを入力してEnter",
            True,
            (255,255,255)
        )
        screen.blit(
            guide,
            (290,220)
        )

        msg = info_font.render(
            login_message,
            True,
            (255,100,100)
        )
        screen.blit(
            msg,
            (350,400)
        )

        if show_id_error:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(150)
            overlay.fill((0,0,0))
            screen.blit(overlay,(0,0))
            popup = pygame.Rect(
                250,
                220,
                500,
                250
            )
            pygame.draw.rect(
                screen,
                (240,240,240),
                popup,
                border_radius=20
            )
            pygame.draw.rect(
                screen,
                BLACK,
                popup,
                3,
                border_radius=20
            )

            title = animal_font.render(
                "エラー",
                True,
                (255,0,0)
            )
            screen.blit(
                title,
                title.get_rect(
                    center=(popup.centerx,270)
                )
            )

            text = info_font.render(
                "IDが存在しません",
                True,
                (0,0,0)
            )
            screen.blit(
                text,
                text.get_rect(
                    center=(popup.centerx,330)
                )
            )

            if id_error_ok_button.collidepoint(mouse_pos):
                pygame.draw.rect(
                    screen,
                    (180,255,180),
                    id_error_ok_button.inflate(8,8),
                    border_radius=12
                )
            pygame.draw.rect(
                screen,
                (0,180,0),
                id_error_ok_button,
                border_radius=10
            )
            pygame.draw.rect(
                screen,
                BLACK,
                id_error_ok_button,
                2,
                border_radius=10
            )

            ok_text = animal_font.render(
                "OK",
                True,
                (255,255,255)
            )
            screen.blit(
                ok_text,
                ok_text.get_rect(
                    center=id_error_ok_button.center
                )
            )

        pygame.display.flip()
        clock.tick(60)
        continue

    if game_state == "ranking":
        screen.fill(BACKGROUND_GREEN)
        draw_text(
            screen,
            "ランキング",
            title_font,
            YELLOW,
            center=(WIDTH//2,80)
        )

        ranking = get_ranking()[:100]
        table_x = 70
        table_y = 150
        row_height = 40
        col_rank = 80
        col_name = 250
        col_id = 180
        col_money = 200
        col_rank_name = 120
        pygame.draw.rect(
            screen,
            (50,50,50),
            (
                table_x,
                table_y,
                830,
                row_height
            )
        )

        headers = [
            ("順位", col_rank),
            ("名前", col_name),
            ("ID", col_id),
            ("所持金", col_money),
            ("ランク", col_rank_name)
        ]
        x = table_x

        for text, width in headers:
            pygame.draw.rect(
                screen,
                (80,80,80),
                (
                    x,
                    table_y,
                    width,
                    row_height
                ),
                1
            )

            header_text = info_font.render(
                text,
                True,
                (255,255,255)
            )
            header_rect = header_text.get_rect(
                center=(
                    x + width // 2,
                    table_y + row_height // 2
                )
            )
            screen.blit(
                header_text,
                header_rect
            )
            x += width

        visible_rows = 10
        start_index = rank_scroll
        end_index = min(
            start_index + visible_rows,
            len(ranking)
        )

        for row_index, player_index in enumerate(
            range(start_index, end_index)
        ):
            player = ranking[player_index]
            rank_number = player_index + 1
            crown = ""
            if rank_number == 1:
                crown = "★"
            elif rank_number == 2:
                crown = "◆"
            elif rank_number == 3:
                crown = "●"
            y = table_y + row_height * (row_index + 1)
            columns = [
                f"{crown}{rank_number}",
                player["player_name"],
                player["player_id"],
                str(player["money"]),
                player["rank"]
            ]

            widths = [
                col_rank,
                col_name,
                col_id,
                col_money,
                col_rank_name
            ]

            x = table_x
        
            scroll_x = table_x + 830 + 10
            pygame.draw.rect(
                screen,
                (100,100,100),
                (
                    scroll_x,
                    table_y,
                    20,
                    row_height * 11
                )
            )

            if len(ranking) > 10:
                bar_height = (
                    row_height * 11
                ) * (
                    10 / len(ranking)
                )

                bar_y = table_y + (
                    rank_scroll /
                    (len(ranking) - 10)
                ) * (
                    row_height * 11 - bar_height
                )
                pygame.draw.rect(
                    screen,
                    (220,220,220),
                    (
                        scroll_x,
                        bar_y,
                        20,
                        bar_height
                    )
                )

            for text, width in zip(columns, widths):

                pygame.draw.rect(
                    screen,
                    WHITE,
                    (
                        x,
                        y,
                        width,
                        row_height
                    ),
                    1
                )

                text_surface = info_font.render(
                    str(text),
                    True,
                    (255,255,255)
                )
                text_rect = text_surface.get_rect(
                    center=(
                        x + width // 2,
                        y + row_height // 2,
                    )
                )

                screen.blit(
                    text_surface,
                    text_rect
                )

                x += width

        draw_button(
            screen,
            ranking_back_button,
            "戻る",
            animal_font,
            mouse_pos,
            bg_color=GRAY,
            hover_color=LIGHT_BLUE
        )

        draw_button(
            screen,
            delete_rank_button,
            "ID削除",
            info_font,
            mouse_pos,
            bg_color=RED,
            hover_color=LIGHT_RED
        )

        if message != "":
            msg_text = info_font.render(
                message,
                True,
                (255,255,0)
            )
            screen.blit(
                msg_text,
                (300,120)
            )

        if show_rank_popup:
            overlay = pygame.Surface(
                (WIDTH, HEIGHT),
                pygame.SRCALPHA
            )
            overlay.set_alpha(150)
            overlay.fill((0,0,0))
            screen.blit(
                overlay,
                (0,0)
            )

            popup = pygame.Rect(
                250,
                220,
                500,
                250
            )
            pygame.draw.rect(
                screen,
                (240,240,240),
                popup,
                border_radius=20
            )
            pygame.draw.rect(
                screen,
                BLACK,
                popup,
                3,
                border_radius=20
            )

            title_text = animal_font.render(
                "通知",
                True,
                (0,0,0)
            )
            screen.blit(
                title_text,
                title_text.get_rect(
                    center=(popup.centerx,280)
                )
            )

            msg_text = info_font.render(
                rank_popup_message,
                True,
                (0,0,0)
            )
            screen.blit(
                msg_text,
                msg_text.get_rect(
                    center=(popup.centerx,340)
                )
            )

            if rank_ok_button.collidepoint(mouse_pos):
                pygame.draw.rect(
                    screen,
                    (180,255,180),
                    rank_ok_button.inflate(8,8),
                    border_radius=12
                )
            pygame.draw.rect(
                screen,
                (0,180,0),
                rank_ok_button,
                border_radius=10
            )
            pygame.draw.rect(
                screen,
                BLACK,
                rank_ok_button,
                3,
                border_radius=10
            )

            draw_text(
                screen,
                "OK",
                info_font,
                WHITE,
                center=popup_ok_button.center
            )

        pygame.display.flip()
        clock.tick(60)
        continue

    # vẽ tiêu đề
    title = title_font.render(
        "バウクア",
        True,
        (255,255,0)
    )
    title_rect = title.get_rect(
        center=(WIDTH//2, 50)
    )
    screen.blit(
        title,
        title_rect
    )

    if exit_button.collidepoint(mouse_pos):
        pygame.draw.rect(
            screen,
            (255,180,180),
            exit_button.inflate(6,6),
            border_radius=12
        )
    pygame.draw.rect(
        screen,
        (220,0,0),
        exit_button,
        border_radius=10
    )
    pygame.draw.rect(
        screen,
        (0,0,0),
        exit_button,
        2,
        border_radius=10
    )

    exit_text = animal_font.render(
        "X",
        True,
        (255,255,255)
    )
    screen.blit(
        exit_text,
        exit_text.get_rect(
            center=exit_button.center
        )
    )

    money_text = animal_font.render(
        f"所持金: {money}円",
        True,
        (255,255,255)
    )
    screen.blit(
        money_text,
        (30,30)
    )

    id_text = info_font.render(
        f"ID : {player_id}",
        True,
        (255,255,255)
    )
    screen.blit(
        id_text,
        (30,200)
    )

    name_text = info_font.render(
        f"名前 : {player_name}",
        True,
        (255,255,255)
    )

    screen.blit(
        name_text,
        (30,230)
    )

    selected_text = info_font.render(
        f"選択中: {len(selected_animals)}/3",
        True,
        (255,255,255)
    )
    screen.blit(
        selected_text,
        (30,130)
    )

    guide_font = pygame.font.SysFont(
        "Yu Gothic",
        22
    ).render(
        "左クリックで賭ける・右クリックで取り消し",
        True,
        (255,255,200)
    )
    screen.blit(
        guide_font,
        (30,170)
    )

    bet_text = animal_font.render(
        f"賭け金: {bet_amount}円",
        True,
        (255,255,255)
    )
    screen.blit(
        bet_text,
        (30,80)
    )

    # vẽ 6 ô
    for i, rect in enumerate(boxes):
        color = (255,255,255)

        # Hover chuột
        if rect.collidepoint(mouse_pos):
            pygame.draw.rect(
            screen,
            (255,255,150),
            rect.inflate(8,8),
            border_radius=10
        )

        # Đã đặt cược
        if bets[animals[i]] > 0:
            color = (255,220,100)

        # Đang chọn
        if animals[i] in selected_animals:
            color = (255,255,0)

        pygame.draw.rect(
            screen,
            color,
            rect,
            border_radius=10
        )
        pygame.draw.rect(
            screen,
            (0,0,0),
            rect,
            3,
            border_radius=10
        )

        image = animal_images[animals[i]]
        image_rect = image.get_rect(
            center=rect.center
        )
        screen.blit(image, image_rect)

        name_text = info_font.render(
            animal_japanese[animals[i]],
            True,
            (255, 255, 255)
        )
        name_rect = name_text.get_rect(
            center=(rect.centerx, rect.bottom - 12)
        )
        screen.blit(
            name_text,
            name_rect
        )

        bet_text = animal_font.render(
            str(bets[animals[i]]),
            True,
            (255,0,0)
        )
        bet_rect = bet_text.get_rect(
            center=(rect.centerx, rect.y + 25)
        )
        screen.blit(
            bet_text,
            bet_rect
        )

    plus_color = (0, 180, 0)
    if plus_button.collidepoint(mouse_pos):
        pygame.draw.rect(
            screen,
            (150, 255, 150),
            plus_button.inflate(6,6),
            border_radius=10
        )
    pygame.draw.rect(
            screen,
            (0,180,0),
            plus_button,
            border_radius=8
        )
    pygame.draw.rect(
        screen,
        (0,0,0),
        plus_button,
        2,
        border_radius=8
    )
    
    minus_color = (180,0,0)
    if minus_button.collidepoint(mouse_pos):
        pygame.draw.rect(
            screen,
            (255, 150, 150),
            minus_button.inflate(6,6),
            border_radius=10
        )
    pygame.draw.rect(
            screen,
            (180,0,0),
            minus_button,
            border_radius=8
        )
    pygame.draw.rect(
        screen,
        (0,0,0),
        minus_button,
        2,
        border_radius=8
    )
    
    cancel_color = (120,120,120)
    if cancel_button.collidepoint(mouse_pos):
        pygame.draw.rect(
            screen,
            (220, 220, 220),
            cancel_button.inflate(8,8),
            border_radius=12
        )
    
    if save_button.collidepoint(mouse_pos):
        pygame.draw.rect(
            screen,
            (180,220,255),
            save_button.inflate(8,8),
            border_radius=12
        )

    pygame.draw.rect(
        screen,
        (0,100,220),
        save_button,
        border_radius=10
    )
    pygame.draw.rect(
        screen,
        (0,0,0),
        save_button,
        2,
        border_radius=10
    )

    save_text = animal_font.render(
        "保存",
        True,
        (255,255,255)
    )
    screen.blit(
        save_text,
        save_text.get_rect(
            center=save_button.center
        )
    )

    pygame.draw.rect(
        screen,
        (120,120,120),
        cancel_button,
        border_radius=10
    )
    pygame.draw.rect(
        screen,
        (0,0,0),
        cancel_button,
        2,
        border_radius=10
    )
    cancel_text = animal_font.render(
        "取消",
        True,
        (255,255,255)
    )
    screen.blit(
        cancel_text,
        cancel_text.get_rect(
            center=cancel_button.center
        )
    )

    shake_color = (200,0,0)
    if shake_button.collidepoint(mouse_pos):
        pygame.draw.rect(
            screen,
            (255, 200, 200),
            shake_button.inflate(8,8),
            border_radius=12
        )
    pygame.draw.rect(
            screen,
            (200,0,0),
            shake_button,
            border_radius=10
        )
    pygame.draw.rect(
        screen,
        (0,0,0),
        shake_button,
        2,
        border_radius=10
    )
    
    plus_text = animal_font.render(
        "+",
        True,
        (255,255,255)
        )

    minus_text = animal_font.render(
        "-",
        True,
        (255,255,255)
    )
    screen.blit(
        plus_text,
        plus_text.get_rect(
            center=plus_button.center
        )
    )
    screen.blit(
        minus_text,
        minus_text.get_rect(
            center=minus_button.center
        )
    )
        
    # vẽ nút lắc
    button_name = "振る"
    if shaking:
        button_name = "抽選中"
    shake_text = button_font.render(
        button_name,
        True,
        (255,255,255)
    )
    shake_text_rect = shake_text.get_rect(
        center=shake_button.center
    )
    screen.blit(
        shake_text,
        shake_text_rect
    )

    result_label = animal_font.render(
        "結果:",
        True,
        (255,255,0)
    )
    screen.blit(
        result_label,
        (50,550)
    )

    if len(results) > 0:
        for i in range(3):
            shake_x = 0
            shake_y = 0
            if shaking:
                shake_x = random.randint(-10,10)
                shake_y = random.randint(-10,10)
            dice_rect = pygame.Rect(
                220 + i * 180 + shake_x,
                540 + shake_y,
                100,
                100
            )
            pygame.draw.rect(
                screen,
                (255, 255, 255),
                dice_rect,
                border_radius=15
            )
            pygame.draw.rect(
                screen,
                (0, 0, 0),
                dice_rect,
                2
            )

            dice_image = animal_images[results[i]]
            screen.blit(
                dice_image,
                (
                    dice_rect.centerx - 45,
                    dice_rect.centery - 45
                )
            )

            result_name = info_font.render(
                animal_japanese[results[i]],
                True,
                (0,0,0)
            )
            screen.blit(
                result_name,
                (
                    dice_rect.x + 25,
                    dice_rect.bottom - 25
                )
            )

    if message != "":
        msg_text = animal_font.render(
            message,
            True,
            (255,255,0)
        )
        screen.blit(
            msg_text,
            (200,620)
        )

    if show_confirm:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(120)
        overlay.fill((0,0,0))
        screen.blit(overlay, (0,0))
        popup = pygame.Rect(
            250,
            180,
            500,
            250
        )
        pygame.draw.rect(
            screen,
            (240,240,240),
            popup
        )
        pygame.draw.rect(
            screen,
            (0,0,0),
            popup,
            3
        )

        popup_title = animal_font.render(
            "確認",
            True,
            (0,0,0)
        )
        popup_title_rect = popup_title.get_rect(
            center=(popup.centerx, popup.y + 35)
        )
        screen.blit(
            popup_title,
            popup_title_rect
        )

        total_bet = sum(bets.values())
        text = animal_font.render(
            f"合計賭け金: {total_bet}",
            True,
            (0,0,0)
        )
        text_rect = text.get_rect(
            center=(500,270)
        )
        screen.blit(
            text,
            text_rect
        )

        yes_color = (0,200,0)
        if yes_button.collidepoint(mouse_pos):
            pygame.draw.rect(
                screen,
                (180,255,180),
                yes_button.inflate(10,10),
                border_radius=12
            )
        pygame.draw.rect(
            screen,
            yes_color,
            yes_button,
            border_radius=10
        )
        pygame.draw.rect(
            screen,
            (0,0,0),
            yes_button,
            2,
            border_radius=10
        )

        no_color = (200,0,0)
        if no_button.collidepoint(mouse_pos):
            pygame.draw.rect(
                screen,
                (255,180,180),
                no_button.inflate(10,10),
                border_radius=12
            )
        pygame.draw.rect(
            screen,
            no_color,
            no_button,
            border_radius=10
        )
        pygame.draw.rect(
            screen,
            (0,0,0),
            no_button,
            2,
            border_radius=10
        )

        yes_text = animal_font.render(
            "はい",
            True,
            (255,255,255)
        )

        no_text = animal_font.render(
            "いいえ",
            True,
            (255,255,255)
        )
        screen.blit(
            yes_text,
            yes_text.get_rect(
                center=yes_button.center
            )
        )
        screen.blit(
            no_text,
            no_text.get_rect(
                center=no_button.center
            )
        )

    if show_cancel_confirm:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(120)
        overlay.fill((0,0,0))
        screen.blit(overlay, (0,0))
        popup = pygame.Rect(
            250,
            180,
            500,
            250
        )
        pygame.draw.rect(
            screen,
            (240,240,240),
            popup
        )
        pygame.draw.rect(
            screen,
            (0,0,0),
            popup,
            3
        )

        popup_title = animal_font.render(
            "確認",
            True,
            (0,0,0)
        )
        popup_title_rect = popup_title.get_rect(
            center=(popup.centerx, popup.y + 35)
        )
        screen.blit(
            popup_title,
            popup_title_rect
        )

        text = animal_font.render(
            "すべて取り消しますか？",
            True,
            (0,0,0)
        )
        text_rect = text.get_rect(
            center=(500,270)
        )
        screen.blit(
            text,
            text_rect
        )

        yes_color = (0,200,0)
        if yes_button.collidepoint(mouse_pos):
            pygame.draw.rect(
                screen,
                (180,255,180),
                yes_button.inflate(10,10),
                border_radius=12
            )
        pygame.draw.rect(
            screen,
            yes_color,
            yes_button,
            border_radius=10
        )
        pygame.draw.rect(
            screen,
            (0,0,0),
            yes_button,
            2,
            border_radius=10
        )

        no_color = (200,0,0)
        if no_button.collidepoint(mouse_pos):
            pygame.draw.rect(
                screen,
                (255,180,180),
                no_button.inflate(10,10),
                border_radius=12
            )
        pygame.draw.rect(
            screen,
            no_color,
            no_button,
            border_radius=10
        )
        pygame.draw.rect(
            screen,
            (0,0,0),
            no_button,
            2,
            border_radius=10
        )

        yes_text = animal_font.render(
            "はい",
            True,
            (255,255,255)
        )
        no_text = animal_font.render(
            "いいえ",
            True,
            (255,255,255)
        )

        screen.blit(
            yes_text,
            yes_text.get_rect(
                center=yes_button.center
            )
        )
        screen.blit(
            no_text,
            no_text.get_rect(
                center=no_button.center
            )
        )

    if show_exit_confirm:
        overlay = pygame.Surface(
            (WIDTH, HEIGHT)
        )
        overlay.set_alpha(120)
        overlay.fill((0,0,0))
        screen.blit(overlay,(0,0))

        popup = pygame.Rect(
            200,
            180,
            600,
            280
        )
        pygame.draw.rect(
            screen,
            (240,240,240),
            popup,
            border_radius=20
        )
        pygame.draw.rect(
            screen,
            (0,0,0),
            popup,
            3,
            border_radius=20
        )

        title_text = animal_font.render(
            "確認",
            True,
            (0,0,0)
        )
        screen.blit(
            title_text,
            title_text.get_rect(
                center=(popup.centerx,230)
            )
        )

        line1 = info_font.render(
            "メニューに戻ると",
            True,
            (0,0,0)
        )
        line2 = info_font.render(
            "現在の賭けは取り消されます。",
            True,
            (0,0,0)
        )
        line3 = info_font.render(
            "よろしいですか？",
            True,
            (0,0,0)
        )

        screen.blit(
            line1,
            line1.get_rect(
                center=(popup.centerx,280)
            )
        )
        screen.blit(
            line2,
            line2.get_rect(
                center=(popup.centerx,320)
            )
        )
        screen.blit(
            line3,
            line3.get_rect(
                center=(popup.centerx,360)
            )
        )

        if exit_yes_button.collidepoint(mouse_pos):
            pygame.draw.rect(
                screen,
                (180,255,180),
                exit_yes_button.inflate(8,8),
                border_radius=12
            )
        pygame.draw.rect(
            screen,
            (0,180,0),
            exit_yes_button,
            border_radius=10
        )
        pygame.draw.rect(
            screen,
            (0,0,0),
            exit_yes_button,
            2,
            border_radius=10
        )

        if exit_no_button.collidepoint(mouse_pos):
            pygame.draw.rect(
                screen,
                (255,180,180),
                exit_no_button.inflate(8,8),
                border_radius=12
            )
        pygame.draw.rect(
            screen,
            (200,0,0),
            exit_no_button,
            border_radius=10
        )
        pygame.draw.rect(
            screen,
            (0,0,0),
            exit_no_button,
            2,
            border_radius=10
        )

        screen.blit(
            animal_font.render(
                "はい",
                True,
                (255,255,255)
            ),
            animal_font.render(
                "はい",
                True,
                (255,255,255)
            ).get_rect(center=exit_yes_button.center)
        )
        screen.blit(
            animal_font.render(
                "いいえ",
                True,
                (255,255,255)
            ),
            animal_font.render(
                "いいえ",
                True,
                (255,255,255)
            ).get_rect(center=exit_no_button.center)
        )

        pygame.display.flip()
        clock.tick(60)
        continue

    if show_game_over:

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(150)
        overlay.fill((0,0,0))
        screen.blit(overlay, (0,0))

        popup = pygame.Rect(
            200,
            180,
            600,
            300
        )

        pygame.draw.rect(
            screen,
            (240,240,240),
            popup,
            border_radius=20
        )
        pygame.draw.rect(
            screen,
            (0,0,0),
            popup,
            3,
            border_radius=20
        )

        title_text = animal_font.render(
            "ゲームオーバー",
            True,
            (255,0,0)
        )
        screen.blit(
            title_text,
            title_text.get_rect(
                center=(popup.centerx,240)
            )
        )

        line1 = info_font.render(
            "所持金がなくなりました。",
            True,
            (0,0,0)
        )
        line2 = info_font.render(
            "メニューに戻ります。",
            True,
            (0,0,0)
        )

        screen.blit(
            line1,
            line1.get_rect(
                center=(popup.centerx,310)
            )
        )
        screen.blit(
            line2,
            line2.get_rect(
                center=(popup.centerx,350)
            )
        )

        # ------------------
        # 新しいゲーム
        # ------------------

        if game_over_new_button.collidepoint(mouse_pos):
            pygame.draw.rect(
                screen,
                (180,255,180),
                game_over_new_button.inflate(8,8),
                border_radius=12
            )

        pygame.draw.rect(
            screen,
            (0,180,0),
            game_over_new_button,
            border_radius=10
        )

        pygame.draw.rect(
            screen,
            (0,0,0),
            game_over_new_button,
            2,
            border_radius=10
        )

        new_text = info_font.render(
            "新しいゲーム",
            True,
            (255,255,255)
        )

        screen.blit(
            new_text,
            new_text.get_rect(
                center=game_over_new_button.center
            )
        )

        # ------------------
        # メニューへ戻る
        # ------------------

        if game_over_menu_button.collidepoint(mouse_pos):
            pygame.draw.rect(
                screen,
                (180,220,255),
                game_over_menu_button.inflate(8,8),
                border_radius=12
            )

        pygame.draw.rect(
            screen,
            (0,100,220),
            game_over_menu_button,
            border_radius=10
        )

        pygame.draw.rect(
            screen,
            (0,0,0),
            game_over_menu_button,
            2,
            border_radius=10
        )

        menu_text = info_font.render(
            "メニューへ",
            True,
            (255,255,255)
        )

        screen.blit(
            menu_text,
            menu_text.get_rect(
                center=game_over_menu_button.center
            )
        )

    if popup_active:    
        overlay = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )
        overlay.fill((0,0,0,150))
        screen.blit(overlay,(0,0))

        popup_rect = pygame.Rect(
            WIDTH//2 - 200,
            HEIGHT//2 - 120,
            400,
            240
        )
        pygame.draw.rect(
            screen,
            (240,240,240),
            popup_rect,
            border_radius=15
        )
        pygame.draw.rect(
            screen,
            (0,0,0),
            popup_rect,
            3,
            border_radius=15
        )

        lines = popup_message.split("\n")
        for i, line in enumerate(lines):
            text = info_font.render(
                line,
                True,
                (0,0,0)
            )
            screen.blit(
                text,
                text.get_rect(
                    center=(
                        WIDTH//2,
                        HEIGHT//2 - 40 + i*40
                    )
                )
            )

        if popup_ok_button.collidepoint(mouse_pos):
            pygame.draw.rect(
                screen,
                (220,220,220),
                popup_ok_button.inflate(8,8),
                border_radius=12
            )

        if popup_ok_button.collidepoint(mouse_pos):
            color = (70,170,255)
        else:
            color = (40,120,220)

        pygame.draw.rect(
            screen,
            color,
            popup_ok_button,
            border_radius=12
        )
        pygame.draw.rect(
            screen,
            (0,0,0),
            popup_ok_button,
            3,
            border_radius=12
        )

        ok_text = info_font.render(
            "OK",
            True,
            (255,255,255)
        )
        screen.blit(
            ok_text,
            ok_text.get_rect(
                center=popup_ok_button.center
            )
        )

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()
