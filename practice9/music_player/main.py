import pygame
from player import MusicPlayer

pygame.init()

screen = pygame.display.set_mode((600, 250))
font = pygame.font.SysFont(None, 30)
clock = pygame.time.Clock()

songs = [
    "music_player/music/Laufey-Let You Break My Heart Again.mp3",
    "music_player/music/Little Bit - Lykke Li.mp3",
    "music_player/music/Modern Baseball-Tears Over Beers.mp3",
    "music_player/music/Noize MC, Марина Кацуба - М.mp3",
    "music_player/music/Olivia Rodrigo - lacy.mp3"
]

player = MusicPlayer(songs)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player.play()
            elif event.key == pygame.K_s:
                player.stop()
            elif event.key == pygame.K_n:
                player.next()
            elif event.key == pygame.K_b:
                player.back()
            elif event.key == pygame.K_q:
                run = False

    screen.fill((255, 255, 255))

    t1 = font.render("Track: " + player.name(), True, (0, 0, 0))
    t2 = font.render("P-play S-stop N-next B-back Q-quit", True, (0, 0, 0))
    t3 = font.render("Time: " + str(player.time()) + " sec", True, (0, 0, 0))

    screen.blit(t1, (50, 60))
    screen.blit(t2, (50, 110))
    screen.blit(t3, (50, 160))

    pygame.display.update()
    clock.tick(30)

pygame.quit()