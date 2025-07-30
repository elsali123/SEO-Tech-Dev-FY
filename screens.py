import pygame
import os
import sys
from pygame import Surface
from conversation import ConversationManager

class OpeningScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('Arial', 64)
        self.button_font = pygame.font.SysFont('Arial', 36)
        self.instruction_font = pygame.font.SysFont('Arial', 18)
        self.title_text = self.font.render('Tropical Rainforest Adventure', True, (34, 139, 34))
        self.button_rect = pygame.Rect(0, 0, 220, 60)
        self.button_rect.center = (screen.get_width() // 2, screen.get_height() // 2 + 200)
        self.button_color = (70, 130, 180)
        self.button_hover_color = (100, 180, 220)
        self.button_text = self.button_font.render('Start', True, (255, 255, 255))
        self.hovered = False
        # Instructions
        self.instructions = [
            "Pick a rainforest animal avatar and enter your name to begin.",
            " ",
            "Use the arrow keys to move toward another animal and press Enter",
            "to learn what they’re facing.",
            " ",
            "You can play a mini-game or ask the in-game chatbot to learn more",
            "about each animal",
            " ",
            "Return to the home screen after interactions"
        ]

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.button_rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.button_rect.collidepoint(event.pos):
                return 'next'
        return None

    def update(self):
        pass

    def draw(self):
        self.screen.fill((220, 255, 220))
        # Draw title
        title_rect = self.title_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 180))
        self.screen.blit(self.title_text, title_rect)
        # Draw instructions
        start_y = title_rect.bottom + 35
        for line in self.instructions:
            text_surf = self.instruction_font.render(line, True, (60, 90, 60))
            text_rect = text_surf.get_rect(center=(self.screen.get_width() // 2, start_y))
            self.screen.blit(text_surf, text_rect)
            start_y += 28
         # Draw button
        color = self.button_hover_color if self.hovered else self.button_color
        pygame.draw.rect(self.screen, color, self.button_rect, border_radius=12)
        text_rect = self.button_text.get_rect(center=self.button_rect.center)
        self.screen.blit(self.button_text, text_rect)

class CharacterSelectScreen:
    def __init__(self, screen):
        self.screen = screen
        self.bg_color = (220, 255, 220)
        self.font = pygame.font.SysFont('Arial', 36)
        self.small_font = pygame.font.SysFont('Arial', 28)
        self.characters = [
            {'name': 'Capybara', 'file': 'capybara.png'},
            {'name': 'Jaguar', 'file': 'jaguar.png'},
            {'name': 'Macaw', 'file': 'macaw.png'},
        ]
        self.images = []
        self.rects = []
        self.hovered = -1
        self._load_images()

    def _load_images(self):
        base_path = os.path.join('assets', 'characters')
        img_size = (180, 180)
        spacing = 80
        total_width = len(self.characters) * img_size[0] + (len(self.characters) - 1) * spacing
        start_x = (self.screen.get_width() - total_width) // 2
        y = self.screen.get_height() // 2 - 60
        for i, char in enumerate(self.characters):
            img_path = os.path.join(base_path, char['file'])
            img = pygame.image.load(img_path).convert_alpha()
            img = pygame.transform.smoothscale(img, img_size)
            x = start_x + i * (img_size[0] + spacing)
            rect = pygame.Rect(x, y, img_size[0], img_size[0])
            self.images.append(img)
            self.rects.append(rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = -1
            for i, rect in enumerate(self.rects):
                if rect.collidepoint(event.pos):
                    self.hovered = i
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, rect in enumerate(self.rects):
                if rect.collidepoint(event.pos):
                    return self.characters[i]['name']
        return None

    def update(self):
        pass

    def draw(self):
        self.screen.fill(self.bg_color)
        # Title
        title = self.font.render('Pick Your Character', True, (34, 139, 34))
        title_rect = title.get_rect(center=(self.screen.get_width() // 2, 100))
        self.screen.blit(title, title_rect)
        # Draw characters
        for i, (img, rect, char) in enumerate(zip(self.images, self.rects, self.characters)):
            border_color = (255, 215, 0) if i == self.hovered else (180, 180, 180)
            pygame.draw.rect(self.screen, border_color, rect.inflate(12, 12), border_radius=16)
            self.screen.blit(img, rect)
            # Draw name
            name_surf = self.small_font.render(char['name'], True, (60, 60, 60))
            name_rect = name_surf.get_rect(center=(rect.centerx, rect.bottom + 28))
            self.screen.blit(name_surf, name_rect)

class SVDExplanationScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('Arial', 36)
        self.small_font = pygame.font.SysFont('Arial', 24)
        self.continue_button = pygame.Rect(0, 0, 220, 60)
        self.continue_button.center = (screen.get_width() // 2, screen.get_height() - 150)
        self.hovered = False
        self.button_color = (70, 130, 180)
        self.button_hover_color = (100, 180, 220)

        self.lines = [
            "As you interact with animals and complete mini-games,",
            "you will notice that the rainforest backrgound becomes clearer.",
            "",
            "This is because your actions restore the image using",
            "a mathematical method called the SVD (Singular Value Decomposition).",
            "",
            "You're helping rebuild the forest! Your goal is to complete at least 3 interactions."
        ]

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.continue_button.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.continue_button.collidepoint(event.pos):
                return 'home'
        return None

    def update(self):
        pass

    def draw(self):
        self.screen.fill((220, 255, 220))
        y = 130
        for line in self.lines:
            text_surf = self.small_font.render(line, True, (40, 70, 40))
            text_rect = text_surf.get_rect(center=(self.screen.get_width() // 2, y))
            self.screen.blit(text_surf, text_rect)
            y += 40
        #Continue button
        color = self.button_hover_color if self.hovered else self.button_color
        pygame.draw.rect(self.screen, color, self.continue_button, border_radius=12)
        btn_text = self.font.render("Continue", True, (255, 255, 255))
        btn_rect = btn_text.get_rect(center=self.continue_button.center)
        self.screen.blit(btn_text, btn_rect)

class HomeScreen:
    def __init__(self, screen, player_character, player_name="Player", background_path=None):
        self.screen = screen
        self.player_character = player_character
        self.player_name = player_name
        self.font = pygame.font.SysFont('Arial', 32)
        self.small_font = pygame.font.SysFont('Arial', 28)
        # Load background
        if background_path is None:
            bg_path = os.path.join('assets', 'background', 'rainforest.png')
        else:
            bg_path = background_path
        self.background_path = bg_path
        self.background = pygame.image.load(bg_path).convert()
        self.background = pygame.transform.smoothscale(self.background, (screen.get_width(), screen.get_height()))
        # Load player character image
        char_path = os.path.join('assets', 'characters', f'{player_character.lower()}.png')
        self.char_img = pygame.image.load(char_path).convert_alpha()
        self.char_img = pygame.transform.smoothscale(self.char_img, (160, 160))
        # Player character movement
        self.char_x = 100
        self.char_y = int(screen.get_height() * 2 / 3) + 40  # bottom 1/3
        self.char_speed = 8
        self.char_rect = self.char_img.get_rect(midbottom=(self.char_x, self.char_y + 80))
        # Determine unselected characters
        all_chars = ['Capybara', 'Jaguar', 'Macaw']
        self.other_names = [c for c in all_chars if c != player_character]
        # Place other animals along the same y-line as player
        self.other_imgs = []
        self.other_rects = []
        self.other_xs = [screen.get_width() // 3, 2 * screen.get_width() // 3]
        self.other_y = self.char_y + 80
        for i, name in enumerate(self.other_names):
            img_path = os.path.join('assets', 'characters', f'{name.lower()}.png')
            img = pygame.image.load(img_path).convert_alpha()
            img = pygame.transform.smoothscale(img, (160, 160))
            rect = img.get_rect(midbottom=(self.other_xs[i], self.other_y))
            self.other_imgs.append(img)
            self.other_rects.append(rect)
        self.other_lit = [False, False]
        self.proximity_threshold = 120

    def set_background(self, background_path):
        self.background_path = background_path
        self.background = pygame.image.load(background_path).convert()
        self.background = pygame.transform.smoothscale(self.background, (self.screen.get_width(), self.screen.get_height()))

    def handle_event(self, event):
        # No mouse hover, only proximity
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            for i, rect in enumerate(self.other_rects):
                if self.other_lit[i]:
                    return self.other_names[i]
        return None

    def update(self):
        # Move player character with arrow keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.char_x -= self.char_speed
        if keys[pygame.K_RIGHT]:
            self.char_x += self.char_speed
        # Constrain to screen bounds
        min_x = 80
        max_x = self.screen.get_width() - 80
        self.char_x = max(min_x, min(max_x, self.char_x))
        # Update rect for drawing
        self.char_rect = self.char_img.get_rect(midbottom=(self.char_x, self.char_y + 80))
        # Proximity highlight
        for i, rect in enumerate(self.other_rects):
            dist = abs(self.char_rect.centerx - rect.centerx)
            self.other_lit[i] = dist < self.proximity_threshold

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        # Draw player's character (bottom 1/3, movable)
        self.screen.blit(self.char_img, self.char_rect)
        name_surf = self.font.render(self.player_name, True, (255, 255, 255))
        name_rect = name_surf.get_rect(midbottom=(self.char_rect.centerx, self.char_rect.top - 10))
        self.screen.blit(name_surf, name_rect)
        # Draw other characters along the same line
        for i, (img, rect, name) in enumerate(zip(self.other_imgs, self.other_rects, self.other_names)):
            if self.other_lit[i]:
                border_color = (255, 215, 0)
                pygame.draw.rect(self.screen, border_color, rect.inflate(16, 16), border_radius=16)
            self.screen.blit(img, rect)
            other_name_surf = self.small_font.render(name, True, (255, 255, 255))
            other_name_rect = other_name_surf.get_rect(midbottom=(rect.centerx, rect.top - 10))
            self.screen.blit(other_name_surf, other_name_rect)

class InteractionScreen:
    def __init__(self, screen, animal_name):
        self.screen = screen
        self.animal_name = animal_name
        self.font = pygame.font.SysFont('Arial', 32)
        self.small_font = pygame.font.SysFont('Arial', 24)
        # Load and blur background
        bg_path = os.path.join('assets', 'background', 'rainforest.png')
        bg = pygame.image.load(bg_path).convert()
        bg = pygame.transform.smoothscale(bg, (screen.get_width()//8, screen.get_height()//8))
        self.background = pygame.transform.smoothscale(bg, (screen.get_width(), screen.get_height()))
        # Load animal image
        char_path = os.path.join('assets', 'characters', f'{animal_name.lower()}.png')
        self.animal_img = pygame.image.load(char_path).convert_alpha()
        self.animal_img = pygame.transform.smoothscale(self.animal_img, (200, 200))
        self.animal_rect = self.animal_img.get_rect(center=(screen.get_width()//2, screen.get_height()//2 - 60))
        # Buttons
        self.buttons = [
            {'label': 'Learn Facts', 'action': 'facts'},
            {'label': 'Play Minigame', 'action': 'minigame'},
            {'label': 'Back', 'action': 'back'}
        ]
        self.button_rects = []
        self.hovered = -1
        self._layout_buttons()
        '''
        self.facts = {
            'Capybara': [
                'Capybaras are hunted for their meat and hides.',
                'Fires have destroyed capybara habitat on a large scale.'
            ],
            'Jaguar': [
                'Habitat loss, poaching, and conflicts with livestock owners threaten jaguars.',
                'Habitat corridors are vital for jaguars.'
            ],
            'Macaw': [
                'Many macaws are targeted for their bright feathers.',
                'Deforestation reduces nesting sites and feeding areas.'
            ]
        }
        '''

    def _layout_buttons(self):
        btn_w, btn_h = 260, 54
        spacing = 40
        total_w = len(self.buttons) * btn_w + (len(self.buttons) - 1) * spacing
        start_x = (self.screen.get_width() - total_w) // 2
        y = self.screen.get_height() - 120
        self.button_rects = []
        for i in range(len(self.buttons)):
            rect = pygame.Rect(start_x + i * (btn_w + spacing), y, btn_w, btn_h)
            self.button_rects.append(rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = -1
            for i, rect in enumerate(self.button_rects):
                if rect.collidepoint(event.pos):
                    self.hovered = i
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, rect in enumerate(self.button_rects):
                if rect.collidepoint(event.pos):
                    return self.buttons[i]['action']
        return None

    def update(self):
        pass

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        # Draw animal in center
        self.screen.blit(self.animal_img, self.animal_rect)
        # Draw animal name
        name_surf = self.font.render(self.animal_name, True, (255, 255, 255))
        name_rect = name_surf.get_rect(center=(self.screen.get_width()//2, self.animal_rect.bottom + 20))
        self.screen.blit(name_surf, name_rect)
        # Draw facts (top left)
        # facts = self.facts.get(self.animal_name, [])
        # for i, fact in enumerate(facts):
        #     fact_surf = self.small_font.render(fact, True, (255, 255, 255))
        #     self.screen.blit(fact_surf, (40, 40 + i * 32))
        # Draw buttons
        for i, (btn, rect) in enumerate(zip(self.buttons, self.button_rects)):
            color = (100, 180, 220) if i == self.hovered else (70, 130, 180)
            pygame.draw.rect(self.screen, color, rect, border_radius=10)
            label_surf = self.font.render(btn['label'], True, (255, 255, 255))
            label_rect = label_surf.get_rect(center=rect.center)
            self.screen.blit(label_surf, label_rect) 

class NameInputScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('Arial', 36)
        self.small_font = pygame.font.SysFont('Arial', 28)
        self.input_box = pygame.Rect(screen.get_width() // 2 - 180, screen.get_height() // 2, 360, 60)
        self.name = ''
        self.active = True
        self.cursor_visible = True
        self.cursor_timer = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN and self.name.strip():
                return self.name.strip()
            elif event.key == pygame.K_BACKSPACE:
                self.name = self.name[:-1]
            elif len(self.name) < 16 and event.unicode.isprintable():
                self.name += event.unicode
        return None

    def update(self):
        self.cursor_timer += 1
        if self.cursor_timer % 60 < 30:
            self.cursor_visible = True
        else:
            self.cursor_visible = False

    def draw(self):
        self.screen.fill((220, 255, 220))
        prompt = self.font.render('Enter Your Name:', True, (34, 139, 34))
        prompt_rect = prompt.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 80))
        self.screen.blit(prompt, prompt_rect)
        # Draw input box
        pygame.draw.rect(self.screen, (255, 255, 255), self.input_box, border_radius=10)
        pygame.draw.rect(self.screen, (70, 130, 180), self.input_box, 3, border_radius=10)
        name_surf = self.font.render(self.name, True, (60, 60, 60))
        self.screen.blit(name_surf, (self.input_box.x + 16, self.input_box.y + 12))
        # Draw cursor
        if self.active and self.cursor_visible:
            cursor_x = self.input_box.x + 16 + name_surf.get_width() + 2
            cursor_y = self.input_box.y + 12
            pygame.draw.rect(self.screen, (60, 60, 60), (cursor_x, cursor_y, 3, 36)) 

class ConversationScreen:
    def __init__(self, screen, character_name, player_name):
        self.screen = screen
        self.character_name = character_name
        self.player_name = player_name
        self.font = pygame.font.SysFont('Arial', 24)
        self.small_font = pygame.font.SysFont('Arial', 18)
        self.title_font = pygame.font.SysFont('Arial', 32)
        
        # Conversation manager
        try:
            self.conversation_manager = ConversationManager()
            self.conversation_started = False
        except:
            self.conversation_manager = None
            self.conversation_started = False
        
        # UI elements
        self.input_box = pygame.Rect(50, screen.get_height() - 80, screen.get_width() - 300, 40)
        self.send_button = pygame.Rect(screen.get_width() - 230, screen.get_height() - 80, 80, 40)
        self.back_button = pygame.Rect(screen.get_width() - 130, screen.get_height() - 80, 80, 40)
        
        # Conversation state - only keep recent messages
        self.input_text = ""
        self.messages = []
        self.suggestions = []
        
        # Load character image
        char_path = os.path.join('assets', 'characters', f'{character_name.lower()}.png')
        self.char_img = pygame.image.load(char_path).convert_alpha()
        self.char_img = pygame.transform.smoothscale(self.char_img, (120, 120))
        
        # Load background
        bg_path = os.path.join('assets', 'background', 'rainforest.png')
        bg = pygame.image.load(bg_path).convert()
        bg = pygame.transform.smoothscale(bg, (screen.get_width()//8, screen.get_height()//8))
        self.background = pygame.transform.smoothscale(bg, (screen.get_width(), screen.get_height()))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.back_button.collidepoint(event.pos):
                return 'back'
            elif self.send_button.collidepoint(event.pos):
                self.send_message()
            else:
                # Check suggestion buttons
                for i, suggestion in enumerate(self.suggestions):
                    suggestion_rect = pygame.Rect(50 + (i % 2) * 300, 200 + (i // 2) * 40, 280, 30)
                    if suggestion_rect.collidepoint(event.pos):
                        self.input_text = suggestion
                        self.send_message()
                        break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.send_message()
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            elif len(self.input_text) < 100 and event.unicode.isprintable():
                self.input_text += event.unicode
        return None

    def send_message(self):
        if not self.input_text.strip():
            return
        
        if not self.conversation_started and self.conversation_manager:
            # Start conversation
            response = self.conversation_manager.start_conversation(self.character_name, self.player_name)
            self.messages.append(("character", response))
            self.conversation_started = True
        
        # Add player message
        self.messages.append(("player", self.input_text))
        
        # Get character response
        if self.conversation_manager:
            response = self.conversation_manager.continue_conversation(self.character_name, self.input_text)
            self.messages.append(("character", response))
        
        # Keep only the last 4 messages (2 exchanges)
        if len(self.messages) > 4:
            self.messages = self.messages[-4:]
        
        self.input_text = ""
        #self.update_suggestions()

    def update_suggestions(self):
        if self.conversation_manager:
            self.suggestions = self.conversation_manager.get_conversation_suggestions(self.character_name)
        else:
            self.suggestions = ["Tell me about yourself", "What threats do you face?"]

    def update(self):
        pass

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        
        # Draw character image and name
        char_rect = self.char_img.get_rect(midtop=(self.screen.get_width() // 2, 20))
        self.screen.blit(self.char_img, char_rect)
        name_surf = self.title_font.render(f"Chat with {self.character_name}", True, (255, 255, 255))
        name_rect = name_surf.get_rect(midtop=(self.screen.get_width() // 2, 150))
        self.screen.blit(name_surf, name_rect)
        
        # Draw conversation area
        conversation_rect = pygame.Rect(50, 200, self.screen.get_width() - 100, self.screen.get_height() - 300)
        pygame.draw.rect(self.screen, (255, 255, 255, 100), conversation_rect, border_radius=10)
        pygame.draw.rect(self.screen, (100, 100, 100), conversation_rect, 2, border_radius=10)
        
        # Draw recent messages (last 4 messages)
        y_offset = 220
        for msg_type, content in self.messages:
            if y_offset < self.screen.get_height() - 120:
                color = (70, 130, 180) if msg_type == "player" else (34, 139, 34)
                bg_color = (200, 220, 255) if msg_type == "player" else (200, 255, 200)
                
                # Word wrap
                words = content.split()
                lines = []
                current_line = ""
                for word in words:
                    test_line = current_line + " " + word if current_line else word
                    if self.font.size(test_line)[0] < conversation_rect.width - 40:
                        current_line = test_line
                    else:
                        if current_line:
                            lines.append(current_line)
                        current_line = word
                if current_line:
                    lines.append(current_line)
                
                # Draw message bubble
                line_height = 25
                bubble_height = len(lines) * line_height + 20
                bubble_rect = pygame.Rect(conversation_rect.x + 20, y_offset, conversation_rect.width - 40, bubble_height)
                pygame.draw.rect(self.screen, bg_color, bubble_rect, border_radius=10)
                pygame.draw.rect(self.screen, color, bubble_rect, 2, border_radius=10)
                
                # Draw text
                for i, line in enumerate(lines):
                    text_surf = self.font.render(line, True, (60, 60, 60))
                    self.screen.blit(text_surf, (bubble_rect.x + 10, bubble_rect.y + 10 + i * line_height))
                
                y_offset += bubble_height + 10
        
        # Draw suggestion buttons
        for i, suggestion in enumerate(self.suggestions):
            suggestion_rect = pygame.Rect(50 + (i % 2) * 300, 200 + (i // 2) * 40, 280, 30)
            pygame.draw.rect(self.screen, (100, 180, 220), suggestion_rect, border_radius=8)
            text_surf = self.small_font.render(suggestion, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=suggestion_rect.center)
            self.screen.blit(text_surf, text_rect)
        
        # Draw input area
        pygame.draw.rect(self.screen, (255, 255, 255), self.input_box, border_radius=8)
        pygame.draw.rect(self.screen, (100, 100, 100), self.input_box, 2, border_radius=8)
        input_surf = self.font.render(self.input_text, True, (60, 60, 60))
        self.screen.blit(input_surf, (self.input_box.x + 10, self.input_box.y + 8))
        
        # Draw buttons
        pygame.draw.rect(self.screen, (70, 130, 180), self.send_button, border_radius=8)
        send_text = self.font.render("Send", True, (255, 255, 255))
        send_rect = send_text.get_rect(center=self.send_button.center)
        self.screen.blit(send_text, send_rect)
        
        pygame.draw.rect(self.screen, (180, 70, 70), self.back_button, border_radius=8)
        back_text = self.font.render("Back", True, (255, 255, 255))
        back_rect = back_text.get_rect(center=self.back_button.center)
        self.screen.blit(back_text, back_rect) 

import pygame
import sys

class EndingScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('Arial', 36)
        self.small_font = pygame.font.SysFont('Arial', 28)
        self.explore_button = pygame.Rect(0, 0, 220, 60)
        self.exit_button = pygame.Rect(0, 0, 180, 60)
        self.explore_button.center = (screen.get_width() // 2 - 150, screen.get_height() // 2 + 60)
        self.exit_button.center = (screen.get_width() // 2 + 150, screen.get_height() // 2 + 60)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.exit_button.collidepoint(event.pos):
                pygame.quit()
                sys.exit()
            elif self.explore_button.collidepoint(event.pos):
                return 'explore'

    def update(self):
        pass

    def draw(self):
        self.screen.fill((0, 100, 50))
        title = self.font.render("The rainforest is restored!", True, (255, 255, 255))
        self.screen.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, 120))
        message = self.small_font.render("You’ve made a big difference. Want to explore more?", True, (230, 230, 230))
        self.screen.blit(message, (self.screen.get_width() // 2 - message.get_width() // 2, 200))
        pygame.draw.rect(self.screen, (70, 180, 70), self.explore_button)
        pygame.draw.rect(self.screen, (180, 70, 70), self.exit_button)
        explore_text = self.small_font.render("Explore More", True, (0, 0, 0))
        exit_text = self.small_font.render("Exit Game", True, (0, 0, 0))
        self.screen.blit(explore_text, (self.explore_button.centerx - explore_text.get_width() // 2, self.explore_button.centery - 15))
        self.screen.blit(exit_text, (self.exit_button.centerx - exit_text.get_width() // 2, self.exit_button.centery - 15))
