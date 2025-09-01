import json
import random

import pygame


# --- CONFIG ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FONT_SIZE = 48
OPTION_FONT_SIZE = 36
BG_COLOR = (255, 255, 255)
TEXT_COLOR = (0, 0, 0)
SELECTED_COLOR = (0, 120, 255)
CORRECT_COLOR = (0, 200, 0)
WRONG_COLOR = (200, 0, 0)

KANJIS_PATH = "kanjis.json"
WORDS_PATH = "words.json"

# --- LOAD DATA ---
def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Kanji Quiz")
    font = pygame.font.SysFont(None, FONT_SIZE)
    option_font = pygame.font.SysFont(None, OPTION_FONT_SIZE)
    clock = pygame.time.Clock()

    kanji_infos = load_json(KANJIS_PATH)
    two_kanji_words = load_json(WORDS_PATH)
    words = list(two_kanji_words.keys())

    # Quiz state
    current_word = None
    left_pick = None
    right_pick = None
    feedback = ""
    show_next = False
    left_options = []
    right_options = []
    left_selected = 0
    right_selected = 0
    selecting_left = True

    def next_round():
        nonlocal current_word, left_pick, right_pick, feedback, show_next
        nonlocal left_options, right_options, left_selected, right_selected, selecting_left
        current_word = random.choice(words)
        left_pick = None
        right_pick = None
        feedback = ""
        show_next = False
        selecting_left = True
        # Generate options
        decoys = list(kanji_infos.keys())
        options = list(current_word)
        while len(options) < 8:
            decoy = random.choice(decoys)
            if decoy not in options:
                options.append(decoy)
        random.shuffle(options)
        left_indices = [0, 2, 4, 6]
        right_indices = [1, 3, 5, 7]
        random.shuffle(left_indices)
        random.shuffle(right_indices)
        left_options = [options[i] for i in left_indices]
        right_options = [options[i] for i in right_indices]
        left_selected = 0
        right_selected = 0

    def check_answer():
        nonlocal feedback, show_next
        left = current_word[0]
        right = current_word[1]
        if left_options[left_selected] == left and right_options[right_selected] == right:
            feedback = "Correct!"
        else:
            feedback = "Wrong!"
        show_next = True

    def draw():
        screen.fill(BG_COLOR)
        y = 40
        # Show translation
        translation = two_kanji_words[current_word]
        text = font.render(translation, True, TEXT_COLOR)
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, y))
        y += 80
        # Show word (kanji)
        word_text = font.render(current_word, True, TEXT_COLOR)
        screen.blit(word_text, (SCREEN_WIDTH//2 - word_text.get_width()//2, y))
        y += 80
        # Show left options
        lx = 80
        ly = y
        for i, kanji in enumerate(left_options):
            color = SELECTED_COLOR if selecting_left and i == left_selected else TEXT_COLOR
            if show_next:
                if kanji == current_word[0]:
                    color = CORRECT_COLOR
                elif i == left_selected and kanji != current_word[0]:
                    color = WRONG_COLOR
            btn = option_font.render(kanji, True, color)
            screen.blit(btn, (lx, ly))
            # Show hint
            hint = kanji_infos[kanji]["readings"][0] + " = " + kanji_infos[kanji]["meanings"]
            hint_text = pygame.font.SysFont(None, 24).render(hint, True, (100,100,100))
            screen.blit(hint_text, (lx, ly+40))
            ly += 80
        # Show right options
        rx = SCREEN_WIDTH - 120
        ry = y
        for i, kanji in enumerate(right_options):
            color = SELECTED_COLOR if not selecting_left and i == right_selected else TEXT_COLOR
            if show_next:
                if kanji == current_word[1]:
                    color = CORRECT_COLOR
                elif i == right_selected and kanji != current_word[1]:
                    color = WRONG_COLOR
            btn = option_font.render(kanji, True, color)
            screen.blit(btn, (rx, ry))
            # Show hint
            hint = kanji_infos[kanji]["readings"][0] + " = " + kanji_infos[kanji]["meanings"]
            hint_text = pygame.font.SysFont(None, 24).render(hint, True, (100,100,100))
            screen.blit(hint_text, (rx-40, ry+40))
            ry += 80
        # Show feedback
        if feedback:
            fb = font.render(feedback, True, CORRECT_COLOR if feedback=="Correct!" else WRONG_COLOR)
            screen.blit(fb, (SCREEN_WIDTH//2 - fb.get_width()//2, SCREEN_HEIGHT-120))
        # Show reading
        reading = kanji_infos[current_word[0]]["readings"][0] + kanji_infos[current_word[1]]["readings"][0]
        reading_text = font.render(reading, True, TEXT_COLOR)
        screen.blit(reading_text, (SCREEN_WIDTH//2 - reading_text.get_width()//2, SCREEN_HEIGHT-180))
        # Show NEXT
        if show_next:
            next_text = font.render("Press A/B/Enter for NEXT", True, (80,80,80))
            screen.blit(next_text, (SCREEN_WIDTH//2 - next_text.get_width()//2, SCREEN_HEIGHT-60))
        pygame.display.flip()

    next_round()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if show_next:
                    if event.key in (pygame.K_RETURN, pygame.K_a, pygame.K_b):
                        next_round()
                else:
                    if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                        selecting_left = not selecting_left
                    elif event.key == pygame.K_UP:
                        if selecting_left:
                            left_selected = (left_selected - 1) % len(left_options)
                        else:
                            right_selected = (right_selected - 1) % len(right_options)
                    elif event.key == pygame.K_DOWN:
                        if selecting_left:
                            left_selected = (left_selected + 1) % len(left_options)
                        else:
                            right_selected = (right_selected + 1) % len(right_options)
                    elif event.key in (pygame.K_a, pygame.K_RETURN):
                        if selecting_left:
                            left_pick = left_options[left_selected]
                            selecting_left = False
                        else:
                            right_pick = right_options[right_selected]
                            if left_pick is not None:
                                check_answer()
                    elif event.key == pygame.K_b:
                        if not selecting_left:
                            right_pick = right_options[right_selected]
                            if left_pick is not None:
                                check_answer()
        draw()
        clock.tick(30)
    pygame.quit()

if __name__ == "__main__":
    main()
