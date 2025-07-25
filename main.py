import pygame
from screens import OpeningScreen, CharacterSelectScreen, HomeScreen, InteractionScreen, NameInputScreen
from minigames.fire_invaders import FireInvadersMinigame
from minigames.puzzle import PuzzleMinigame
from minigames.drag_nest import DragNestMinigame

# Game settings
SCREEN_WIDTH, SCREEN_HEIGHT = 960, 640
FPS = 60

# Game stages
STAGE_OPENING = 'opening'
STAGE_CHARACTER_SELECT = 'character_select'
STAGE_NAME_INPUT = 'name_input'
STAGE_HOME = 'home'
STAGE_INTERACTION = 'interaction'


def fade_in(screen, draw_func, duration=700):
    clock = pygame.time.Clock()
    overlay = pygame.Surface(screen.get_size())
    overlay.fill((0, 0, 0))
    for alpha in range(255, -1, -15):
        draw_func()
        overlay.set_alpha(alpha)
        screen.blit(overlay, (0, 0))
        pygame.display.flip()
        clock.tick(60)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Tropical Rainforest Adventure')
    clock = pygame.time.Clock()

    # Start at opening screen
    stage = STAGE_OPENING
    current_screen = OpeningScreen(screen)
    selected_character = None
    player_name = "Player"  # Placeholder for now
    interaction_target = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Let the current screen handle events
            result = current_screen.handle_event(event)
            if stage == STAGE_OPENING and result == 'next':
                stage = STAGE_CHARACTER_SELECT
                current_screen = CharacterSelectScreen(screen)
            elif stage == STAGE_CHARACTER_SELECT and result:
                selected_character = result
                stage = STAGE_NAME_INPUT
                current_screen = NameInputScreen(screen)
            elif stage == STAGE_NAME_INPUT and result:
                player_name = result
                stage = STAGE_HOME
                home_screen = HomeScreen(screen, selected_character, player_name)
                fade_in(screen, home_screen.draw)
                current_screen = home_screen
            elif stage == STAGE_HOME and result:
                # result is the name of the character to interact with
                interaction_target = result
                stage = STAGE_INTERACTION
                current_screen = InteractionScreen(screen, interaction_target)
            elif stage == STAGE_INTERACTION and result:
                print(f'Interaction screen action: {result}')
                if result == 'back':
                    stage = STAGE_HOME
                    current_screen = HomeScreen(screen, selected_character, player_name)
                elif result == 'minigame':
                    # Launch the appropriate minigame
                    if interaction_target == 'Capybara':
                        FireInvadersMinigame(screen).run()
                    elif interaction_target == 'Jaguar':
                        PuzzleMinigame(screen).run()
                    elif interaction_target == 'Macaw':
                        DragNestMinigame(screen).run()
                    # After minigame, return to interaction screen
                    current_screen = InteractionScreen(screen, interaction_target)
                elif result == 'facts':
                    print('Facts would be shown here!')

        current_screen.update()
        current_screen.draw()
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    main()