# Example file showing a circle moving on screen
from math import *

import pygame

# pygame setup
pygame.init()
pygame.event.set_grab(True)
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

dots = []
for x in range(-10, 10):
    for y in range(-10, 10):
        for z in range(-10, 10):
            dots.append([x,y,z,1])

scale = 1
pitch, yaw = 0, 0

def multiply_4d_matrices(A, B):
    C = []
    for m in range(4):
        dC = []
        for n in range(4):
            dC.append(sum([A[m][0]*B[0][n], A[m][1]*B[1][n], A[m][2]*B[2][n], A[m][3]*B[3][n]]))
        C.append(dC)
    return C

def multiply_matrix_vector(A, B):
    V = []
    for m in range(4):
        V.append(sum([B[m][0] * A[0], B[m][1] * A[1], B[m][2] * A[2], B[m][3] * A[3]]))
    return V

def world_to_screen(V):
    return V[0]/-V[2], V[1]/-V[2]

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    translation_matrix = [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, -15],
        [0, 0, 0, 1]
    ]

    sens = 10
    if pygame.mouse.get_focused():
        x_rel, y_rel = pygame.mouse.get_rel()
        pitch += radians(y_rel * dt * sens)
        yaw += radians(x_rel * dt * sens)
        pygame.mouse.set_pos(screen.get_width()/2, screen.get_height()/2)

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

    rotation_matrix = multiply_4d_matrices(pitch_matrix, yaw_matrix)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        scale += 1 * dt
    elif keys[pygame.K_s]:
        scale -= 1 * dt
    if keys[pygame.K_r]:
        pitch = 0
        yaw = 0
    if scale <= 0.1: scale = 0.1
    if scale >= 3: scale = 3

    scale_matrix = [
        [scale, 0, 0, 0],
        [0, scale, 0, 0],
        [0, 0, scale, 0],
        [0, 0, 0, 1]
    ]

    model_matrix = multiply_4d_matrices(rotation_matrix, scale_matrix)

    view_matrix = multiply_4d_matrices(translation_matrix, model_matrix)

    sharp_matrix = [
        [1, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ]

    view_matrix = multiply_4d_matrices(sharp_matrix, view_matrix)

    screen_points = []
    for d in dots:
        transformed_dot = multiply_matrix_vector(d, view_matrix)

        if transformed_dot[2] >= -0.1:
            continue

        screen_points.append({
            'dot': transformed_dot,
            'y': d[1]
        })

    screen_points.sort(key=lambda i: i['dot'][2])

    for sp in screen_points:
        transformed_dot = sp['dot']
        x_projected, y_projected = world_to_screen(transformed_dot)

        screen_x = screen.get_width() / 2 + x_projected * 700
        screen_y = screen.get_height() / 2 - y_projected * 700

        hue = int(((sp['y'] + 10) / 20) * 360) % 360
        color = pygame.Color(0)
        color.hsva = (hue, 100, 100, 100)

        pygame.draw.circle(screen, color, (screen_x, screen_y), 2)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()