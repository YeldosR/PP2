import pygame
from player import MusicPlayer

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((500, 300))
pygame.display.set_caption("Music Player")

font = pygame.font.Font(None, 36)

playlist = [
    "music/sample_tracks/track1.mp3",
    "music/sample_tracks/track2.mp3"
]

player = MusicPlayer(playlist)

running = True
while running:
    screen.fill((0, 0, 0))

    text = font.render(f"Track: {player.index}", True, (255, 255, 255))
    screen.blit(text, (50, 100))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player.play()
            elif event.key == pygame.K_s:
                player.stop()
            elif event.key == pygame.K_n:
                player.next()
            elif event.key == pygame.K_b:
                player.prev()
            elif event.key == pygame.K_q:
                running = False

    pygame.display.flip()

pygame.quit()