import pygame
import numpy as np

pygame.init()

BLACK = (0, 0, 0)
GREY = (128, 128, 128)
YELLOW = (255, 255, 0)

WIDTH, HEIGHT = 800, 800
TILE_SIZE = 20
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()


def draw_grid(position_heat):

    for row in range(GRID_HEIGHT):
        pygame.draw.line(screen, BLACK, (0, row * TILE_SIZE), (WIDTH, row * TILE_SIZE))

    for col in range(GRID_WIDTH):
        pygame.draw.line(screen, BLACK, (col * TILE_SIZE, 0), (col * TILE_SIZE, HEIGHT))

    for x in range(0, GRID_WIDTH):
        for y in range(0, GRID_HEIGHT):
            heat = position_heat[x, y]
            top_left = (x * TILE_SIZE, y * TILE_SIZE)
            pygame.draw.rect(screen, (heat, heat, heat), (*top_left, TILE_SIZE, TILE_SIZE))


def adjust_heat_a(position_heat):
    for x in range(1, GRID_WIDTH-1):
        for y in range(1, GRID_HEIGHT-1):
            position_heat[x, y] = (position_heat[x, y+1] + position_heat[x+1, y+1] + position_heat[x+1, y]
                                   - position_heat[x, y-1] - position_heat[x-1, y-1] - position_heat[x-1, y])
            if position_heat[x, y] > 255:
                position_heat[x, y] = 255
            elif position_heat[x, y] < 0:
                position_heat[x, y] = 0

    return position_heat

def adjust_heat_b(position_heat):
    for x in range(1, GRID_WIDTH-1):
        for y in range(1, GRID_HEIGHT-1):
            position_heat[x, y] = (position_heat[x+1, y+1] + 5)
            if position_heat[x, y] > 255:
                position_heat[x, y] = 255
            elif position_heat[x, y] < 0:
                position_heat[x, y] = 0

    return position_heat

def main():
    running = True
    playing = False
    count = 0
    update_freq = 10

    position_heat = np.random.randint(0, 256, size=(GRID_WIDTH, GRID_HEIGHT))
    print(position_heat)
    while running:
        clock.tick(FPS)

        if playing:
            count += 1

        if count >= update_freq:
            count = 0
            position_heat = adjust_heat_b(position_heat)

        pygame.display.set_caption("Playing" if playing else "Paused")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x_p, y_p = pygame.mouse.get_pos()
                x = x_p // TILE_SIZE
                y = y_p // TILE_SIZE

                if position_heat[x, y] > 128:
                    position_heat[x, y] = 10
                else:
                    position_heat[x, y] = 200

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playing = not playing

                if event.key == pygame.K_c:
                    playing = False
                    count = 0

        screen.fill(GREY)
        draw_grid(position_heat)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
