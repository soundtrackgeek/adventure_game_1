# main.py
import pygame
import json
import os
from pathlib import Path
from opening_menu import OpeningMenu

class AdventureGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Choose Your Adventure")
        self.font = pygame.font.Font(None, 32)
        self.current_story = None
        self.current_node = None
        self.running = True

    def load_story(self, story_file):
        with open(story_file, 'r') as f:
            self.current_story = json.load(f)
            self.current_node = 'start'

    def display_text(self, text, y_position):
        rendered = self.font.render(text, True, (255, 255, 255))
        text_rect = rendered.get_rect(center=(400, y_position))
        self.screen.blit(rendered, text_rect)

    def run(self):
        while self.running:
            self.screen.fill((0, 0, 0))
            
            node = self.current_story['scenes'][self.current_node]
            
            # Split text into lines and display with wrapping
            y_pos = 50
            for line in node['text'].split('\n'):
                words = line.split()
                current_line = []
                for word in words:
                    current_line.append(word)
                    test_line = ' '.join(current_line)
                    if self.font.size(test_line)[0] > 700:  # Width limit
                        final_line = ' '.join(current_line[:-1])
                        self.display_text(final_line, y_pos)
                        y_pos += 30
                        current_line = [word]
                if current_line:
                    self.display_text(' '.join(current_line), y_pos)
                    y_pos += 30
            
            # Display choices
            y_pos += 20  # Add some space between text and choices
            for idx, choice in enumerate(node.get('choices', [])):
                self.display_text(f"{idx + 1}. {choice['text']}", y_pos)
                y_pos += 40

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