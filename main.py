# main.py
import pygame
import json
import os
from pathlib import Path
from opening_menu import OpeningMenu

class AdventureGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1024, 768))
        pygame.display.set_caption("Choose Your Adventure")
        self.font = pygame.font.Font(None, 32)
        self.current_story = None
        self.current_node = None
        self.running = True
        self.scroll_offset = 0
        self.scroll_speed = 30
        
        # Define story box dimensions
        self.story_box = {
            'width': 800,
            'height': 600,
            'x': (1024 - 800) // 2,  # Center horizontally
            'y': 50  # Some padding from top
        }

    def load_story(self, story_file):
        with open(story_file, 'r') as f:
            self.current_story = json.load(f)
            self.current_node = 'start'

    def display_text(self, text, y_position):
        rendered = self.font.render(text, True, (255, 255, 255))
        text_rect = rendered.get_rect(center=(self.screen.get_width() // 2, y_position))
        self.screen.blit(rendered, text_rect)

    def run(self):
        while self.running:
            self.screen.fill((0, 0, 0))
            
            # Draw story box border
            pygame.draw.rect(self.screen, (100, 100, 100), 
                           (self.story_box['x'], self.story_box['y'], 
                            self.story_box['width'], self.story_box['height']), 2)
            
            node = self.current_story['scenes'][self.current_node]
            
            # Calculate text wrapping based on story box width
            text_lines = []
            for line in node['text'].split('\n'):
                words = line.split()
                current_line = []
                for word in words:
                    current_line.append(word)
                    test_line = ' '.join(current_line)
                    if self.font.size(test_line)[0] > 750:  # Slightly less than box width
                        text_lines.append(' '.join(current_line[:-1]))
                        current_line = [word]
                if current_line:
                    text_lines.append(' '.join(current_line))
            total_height = len(text_lines) * 30

            # Render text within story box
            y_pos = self.story_box['y'] + 20 - self.scroll_offset
            for line in text_lines:
                if self.story_box['y'] <= y_pos <= self.story_box['y'] + self.story_box['height'] - 30:
                    self.display_text(line, y_pos)
                y_pos += 30
            
            # Show choices below story box
            choices_start = self.story_box['y'] + self.story_box['height'] + 20
            for idx, choice in enumerate(node.get('choices', [])):
                self.display_text(f"{idx + 1}. {choice['text']}", choices_start + idx * 40)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                        choice_idx = event.key - pygame.K_1
                        choices = node.get('choices', [])
                        if choice_idx < len(choices):
                            self.current_node = choices[choice_idx]['next_scene']
                            self.scroll_offset = 0
                    elif event.key == pygame.K_UP:
                        self.scroll_offset = max(0, self.scroll_offset - self.scroll_speed)
                    elif event.key == pygame.K_DOWN:
                        max_scroll = max(0, total_height - (self.story_box['height'] - 40))
                        self.scroll_offset = min(max_scroll, self.scroll_offset + self.scroll_speed)
                elif event.type == pygame.MOUSEWHEEL:
                    max_scroll = max(0, total_height - (self.story_box['height'] - 40))
                    self.scroll_offset = max(0, min(max_scroll,
                                                  self.scroll_offset - event.y * self.scroll_speed))

        pygame.quit()

if __name__ == "__main__":
    pygame.init()
    menu = OpeningMenu()
    selected_story = menu.run()
    
    if selected_story:
        game = AdventureGame()
        game.load_story(selected_story)
        game.run()
    
    pygame.quit()