# Example file showing a circle moving on screen
from math import *

import pygame

# pygame setup
pygame.init()
pygame.event.set_grab(True)
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

cube = [
        [-3, -3, -3, 1],
        [3, -3, -3, 1],
        [3, -3, 3, 1],
        [-3, -3, 3, 1],
        [-3, 3, -3, 1],
        [3, 3, -3, 1],
        [3, 3, 3, 1],
        [-3, 3, 3, 1]
        ]

scale = 1
pitch, yaw = 0, 0

def multiple_4d_matrices(A, B):
    C = []
    for m in range(4):
        dC = []
        for n in range(4):
            dC.append(sum([A[m][0]*B[0][n], A[m][1]*B[1][n], A[m][2]*B[2][n], A[m][3]*B[3][n]]))
        C.append(dC)
    return C

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    pygame.draw.circle(screen, "white", player_pos, 40)

    sens = 0.1
    if pygame.mouse.get_focused():
        x_rel, y_rel = pygame.mouse.get_rel()
        pitch += radians(y_rel * dt * sens)
        yaw += radians(x_rel * dt * sens)

    yaw_matrix = [
        [cos(yaw), 0, sin(yaw), 0],
        [0, 1, 0, 0],
        [-sin(yaw), 0, cos(yaw), 0],
        [0, 0, 0, 1]
    ]

    pitch_matrix = [
        [1, 0, 0, 0],
        [0, cos(pitch), -sin(pitch), 0],
        [0, sin(pitch), cos(pitch), 0],
        [0, 0, 0, 1]
    ]

    rotation_matrix = multiple_4d_matrices(pitch_matrix, yaw_matrix)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        scale += 0.1 * dt
    elif keys[pygame.K_s]:
        scale -= 0.1 * dt
    if scale <= 0.1: scale = 0.1

    scale_matrix = [
        [scale, 0, 0, 0],
        [0, scale, 0, 0],
        [0, 0, scale, 0],
        [0, 0, 0, 1]
    ]

    view_matrix = multiple_4d_matrices(scale_matrix, rotation_matrix)

    cube_translation_matrix = [
        [1, 0, 0, 5],
        [0, 1, 0, 5],
        [0, 0, 1, -15],
        [0, 0, 0, 1]
    ]

    view_matrix = multiple_4d_matrices(cube_translation_matrix, view_matrix)



    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()