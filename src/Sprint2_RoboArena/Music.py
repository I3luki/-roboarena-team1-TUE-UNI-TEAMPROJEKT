import pygame

class Music:

    def __init__(self,game):
        self.game = game
        self.current_music = None

    def load_music(self, path, state, volume):
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)  # Loop forever
        self.current_music = state


    def update(self):
        state = self.game.state

        # Main Menu Music
        if state == "MENU" and self.current_music != state:
            self.load_music("Music/Mainmenu-1.mp3", state, 0.5)

        # Ingame Music
        if state == "PLAYING" and self.current_music != state:
            self.load_music("Music/Ingame-1.mp3", state, 0.5)

        if state == "GAME_OVER" and self.current_music != state:
            self.load_music("Music/Death-1.mp3", state, 1.0)

        

        # Pause
        if state == "PAUSE" and self.current_music != state:
            pygame.mixer.music.set_volume(0.2)
        
        if state != "PAUSE":
            pygame.mixer.music.set_volume(0.5)





