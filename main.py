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
            self.current_node = self.current_story['start']

    def display_text(self, text, y_position):
        rendered = self.font.render(text, True, (255, 255, 255))
        text_rect = rendered.get_rect(center=(400, y_position))
        self.screen.blit(rendered, text_rect)

    def run(self):
        while self.running:
            self.screen.fill((0, 0, 0))
            
            node = self.current_story['nodes'][self.current_node]
            self.display_text(node['text'], 200)
            
            # Display choices
            y_pos = 300
            for idx, choice in enumerate(node.get('choices', [])):
                self.display_text(f"{idx + 1}. {choice['text']}", y_pos)
                y_pos += 40

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                        choice_idx = event.key - pygame.K_1
                        choices = node.get('choices', [])
                        if choice_idx < len(choices):
                            self.current_node = choices[choice_idx]['next']

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