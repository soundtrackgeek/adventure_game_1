import pygame
import json
import os
from pathlib import Path

class OpeningMenu:
    def __init__(self):
        self.screen = pygame.display.set_mode((1024, 768))
        pygame.display.set_caption("Adventure Game - Select Story")
        self.font = pygame.font.Font(None, 32)
        self.running = True
        self.stories = self.load_stories()

    def load_stories(self):
        stories = []
        stories_path = Path('stories')
        for file in stories_path.glob('*.json'):
            with open(file, 'r') as f:
                story_data = json.load(f)
                stories.append({
                    'title': story_data.get('title', 'Untitled'),
                    'file': str(file)
                })
        return stories

    def display_text(self, text, y_position):
        rendered = self.font.render(text, True, (255, 255, 255))
        text_rect = rendered.get_rect(center=(self.screen.get_width() // 2, y_position))
        self.screen.blit(rendered, text_rect)

    def run(self):
        selected_story = None
        
        while self.running:
            self.screen.fill((0, 0, 0))
            
            self.display_text("Choose Your Adventure", 100)
            
            y_pos = 200
            for idx, story in enumerate(self.stories):
                self.display_text(f"{idx + 1}. {story['title']}", y_pos)
                y_pos += 40

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif pygame.K_1 <= event.key <= pygame.K_9:
                        story_idx = event.key - pygame.K_1
                        if story_idx < len(self.stories):
                            selected_story = self.stories[story_idx]['file']
                            self.running = False

        return selected_story
