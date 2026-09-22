from math import *
import pygame

pygame.init()
pygame.event.set_grab(True)
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

dots = []
for x in range(-10, 10):
    for y in range(-10, 10):
        for z in range(-10, 10):
            dots.append([x,y,z,1])

scale = 1
pitch, yaw = 0, 0
basis = "i / j / k"
axis = "x / y / z"
m = {'ix':1, 'iy':0, 'iz':0, 'jx':0, 'jy':1, 'jz':0, 'kx':0, 'ky':0, 'kz':1}
M = {'ix':1, 'iy':0, 'iz':0, 'jx':0, 'jy':1, 'jz':0, 'kx':0, 'ky':0, 'kz':1}
translation_matrix = [
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, -15],
    [0, 0, 0, 1]
]
basis_keys = {pygame.K_i: 'i', pygame.K_j: 'j', pygame.K_k: 'k'}
axis_keys = {pygame.K_x: 'x', pygame.K_y: 'y', pygame.K_z: 'z'}
font = pygame.font.SysFont(["Arial", None], 20)
color_cache = {}
for y in range(-10, 10):
    hue = int(((y + 10) / 20) * 360) % 360
    color = pygame.Color(0)
    color.hsva = (hue, 100, 100, 100)
    color_cache[y] = color

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

def get_matrix_determinant(A):
    return A[0][0]*A[1][1]*A[2][2]+A[0][1]*A[1][2]*A[2][0]+A[0][2]*A[1][0]*A[2][1]-(A[0][2]*A[1][1]*A[2][0]+A[0][1]*A[1][0]*A[2][2]+A[0][0]*A[1][2]*A[2][1])

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False


    screen.fill("black")
    keys = pygame.key.get_pressed()


    if keys[pygame.K_r]:
        pitch = 0
        yaw = 0
        m = M.copy()

    if keys[pygame.K_c]:
        if len(axis) == 1 and len(basis) == 1:
            m[f'{basis}{axis}'] = M[f'{basis}{axis}']


    if pygame.mouse.get_focused():
        x_rel, y_rel = pygame.mouse.get_rel()
        pitch += radians(y_rel * dt * 10)
        yaw += radians(x_rel * dt * 10)
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


    if keys[pygame.K_w]:
        scale += 1 * dt
    elif keys[pygame.K_s]:
        scale -= 1 * dt
    if scale <= 0.1: scale = 0.1
    if scale >= 3: scale = 3

    scale_matrix = [
        [scale, 0, 0, 0],
        [0, scale, 0, 0],
        [0, 0, scale, 0],
        [0, 0, 0, 1]
    ]

    user_input_matrix = [
        [m['ix'], m['jx'], m['kx'], 0],
        [m['iy'], m['jy'], m['ky'], 0],
        [m['iz'], m['jz'], m['kz'], 0],
        [0, 0, 0, 1],
    ]

    for key, char in basis_keys.items():
        if keys[key]: basis = char

    for key, char in axis_keys.items():
        if keys[key]: axis = char

    if len(axis+basis) == 2:
        if keys[pygame.K_e]:
            m[f'{basis}{axis}'] += 0.5 * dt
        elif keys[pygame.K_q]:
            m[f'{basis}{axis}'] -= 0.5 * dt


    custom_matrix = multiply_4d_matrices(user_input_matrix, scale_matrix)
    rotation_matrix = multiply_4d_matrices(pitch_matrix, yaw_matrix)
    model_matrix = multiply_4d_matrices(rotation_matrix, custom_matrix)
    view_matrix = multiply_4d_matrices(translation_matrix, model_matrix)


    scale_surface = font.render(f'scale: {scale:.1f} | w / s', True, "white")
    screen.blit(scale_surface, (10, screen.get_height() - (70 + 20 + 20+20)))

    edit_surface = font.render(f"edit: {basis}-{axis}{' | e / q' if len(basis+axis)==2 else ''}", True, "white")
    screen.blit(edit_surface, (10, screen.get_height() - (20 + 70+20)))

    matrix_row_x = font.render(f"{m['ix']:.1f}|{m['jx']:.1f}|{m['kx']:.1f}", True, "white")
    matrix_row_y = font.render(f"{m['iy']:.1f}|{m['jy']:.1f}|{m['ky']:.1f}", True, "white")
    matrix_row_z = font.render(f"{m['iz']:.1f}|{m['jz']:.1f}|{m['kz']:.1f}", True, "white")
    screen.blit(matrix_row_x, (10, screen.get_height() - (10 + 20 + 20 + 20+20)))
    screen.blit(matrix_row_y, (10, screen.get_height() - (10 + 20 + 20+20)))
    screen.blit(matrix_row_z, (10, screen.get_height() - (10 + 20+20)))

    matrix_determinant = font.render(f"det: {get_matrix_determinant([[m['ix'], m['jx'], m['kx']],[m['iy'], m['jy'], m['ky']],[m['iz'], m['jz'], m['kz']]]):.4f}", True, "white")
    screen.blit(matrix_determinant, (10, screen.get_height() - (10 + 20)))


    screen_points = []
    for d in dots:
        transformed_dot = multiply_matrix_vector(d, view_matrix)

        if transformed_dot[2] >= -0.1: continue

        screen_points.append({'dot': transformed_dot,'y': d[1]})

    screen_points.sort(key=lambda i: i['dot'][2])

    for sp in screen_points:
        transformed_dot = sp['dot']
        x_projected, y_projected = world_to_screen(transformed_dot)

        screen_x = screen.get_width() / 2 + x_projected * 700
        screen_y = screen.get_height() / 2 - y_projected * 700

        pygame.draw.circle(screen, color_cache[sp['y']], (screen_x, screen_y), 2)

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()