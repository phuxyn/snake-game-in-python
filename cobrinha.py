import pygame
import time
import random

# Inicialização do pygame
pygame.init()

# Definição das cores
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 200, 0)  # Nova cor para a bolinha verde
blue = (50, 153, 213)
light_gray = (200, 200, 200)
dark_gray = (150, 150, 150)
snake_color = (0, 128, 0)  # Verde escuro para a cobrinha
snake_boot_color = (128, 0, 0)  # Vermelho escuro para as cobrinhas boot

# Tamanho da tela
dis_width = 1000
dis_height = 800

# Criação da tela
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Jogo da Cobrinha')

clock = pygame.time.Clock()

snake_block = 20
snake_speed = 30

font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 35)


def our_snake(snake_block, snake_list, color):
    for x in snake_list:
        pygame.draw.rect(dis, color, [x[0], x[1], snake_block, snake_block])


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])


def generate_barrier():
    barrier_list = []  # Lista para armazenar as barreiras

    for _ in range(3):
        barrier_x = round(random.randrange(snake_block * 2, dis_width - snake_block * 3) / snake_block) * snake_block
        barrier_y = round(random.randrange(snake_block * 2, dis_height - snake_block * 3) / snake_block) * snake_block
        barrier_list.append((barrier_x, barrier_y))

    return barrier_list


def generate_snake():
    snake_x = round(random.randrange(snake_block * 2, dis_width - snake_block * 3) / snake_block) * snake_block
    snake_y = round(random.randrange(snake_block * 2, dis_height - snake_block * 3) / snake_block) * snake_block
    return snake_x, snake_y


def move_boot_snake(snake_head, direction, barrier_list, snake_list):
    x = snake_head[0]
    y = snake_head[1]

    if direction == 'up':
        y -= snake_block
    elif direction == 'down':
        y += snake_block
    elif direction == 'left':
        x -= snake_block
    elif direction == 'right':
        x += snake_block

    if (x, y) in barrier_list or (x, y) in [(block[0], block[1]) for block in snake_list]:
        direction = random.choice(['up', 'down', 'left', 'right'])
        return move_boot_snake(snake_head, direction, barrier_list, snake_list)

    return x, y, direction


def check_next_square_color(x, y, direction, barrier_list, snake_list):
    next_x = x
    next_y = y

    if direction == 'up':
        next_y -= snake_block
    elif direction == 'down':
        next_y += snake_block
    elif direction == 'left':
        next_x -= snake_block
    elif direction == 'right':
        next_x += snake_block

    if (next_x, next_y) in barrier_list or (next_x, next_y) in [(block[0], block[1]) for block in snake_list]:
        return black
    else:
        return light_gray


def gameLoop():
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(snake_block * 2, dis_width - snake_block * 3) / snake_block) * snake_block
    foody = round(random.randrange(snake_block * 2, dis_height - snake_block * 3) / snake_block) * snake_block

    barrier_list = generate_barrier()

    snake2_x, snake2_y = generate_snake()
    snake2_List = []
    Length_of_snake2 = 3  # Tamanho da cobrinha 2 aumentado
    snake2_speed = 10  # Velocidade da cobrinha 2 reduzida
    snake2_direction = random.choice(['left', 'right', 'up', 'down'])

    snake3_x, snake3_y = generate_snake()
    snake3_List = []
    Length_of_snake3 = 3  # Tamanho da cobrinha 3 aumentado
    snake3_speed = 10  # Velocidade da cobrinha 3 reduzida
    snake3_direction = random.choice(['left', 'right', 'up', 'down'])

    while not game_over:

        while game_close:
            dis.fill(blue)
            message("Você perdeu! Pressione Q para sair ou C para jogar novamente", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= dis_width - snake_block or x1 < snake_block or y1 >= dis_height - snake_block or y1 < snake_block:
            game_close = True
        x1 += x1_change
        y1 += y1_change

        dis.fill(blue)

        # Desenha as bordas pretas
        pygame.draw.rect(dis, black, [0, 0, dis_width, snake_block])
        pygame.draw.rect(dis, black, [0, dis_height - snake_block, dis_width, snake_block])
        pygame.draw.rect(dis, black, [0, 0, snake_block, dis_height])
        pygame.draw.rect(dis, black, [dis_width - snake_block, 0, snake_block, dis_height])

        for i in range(snake_block, dis_width - snake_block, snake_block):
            for j in range(snake_block, dis_height - snake_block, snake_block):
                if (i // snake_block + j // snake_block) % 2 == 0:
                    pygame.draw.rect(dis, light_gray, [i, j, snake_block, snake_block])
                else:
                    pygame.draw.rect(dis, dark_gray, [i, j, snake_block, snake_block])

        for barrier in barrier_list:
            pygame.draw.rect(dis, black, [barrier[0], barrier[1], snake_block * 2, snake_block * 2])

        for barrier in barrier_list:
            if barrier[0] == x1 and barrier[1] == y1:
                game_close = True

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(snake_block * 2, dis_width - snake_block * 3) / snake_block) * snake_block
            foody = round(random.randrange(snake_block * 2, dis_height - snake_block * 3) / snake_block) * snake_block
            Length_of_snake += 1

        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        snake2_x, snake2_y, snake2_direction = move_boot_snake((snake2_x, snake2_y), snake2_direction, barrier_list, snake_List)

        # Verifica os limites para a cobra 2
        if snake2_x >= dis_width - snake_block or snake2_x < snake_block or snake2_y >= dis_height - snake_block or snake2_y < snake_block:
            game_close = True
        else:
            snake2_Head = []
            snake2_Head.append(snake2_x)
            snake2_Head.append(snake2_y)
            snake2_List.append(snake2_Head)
            if len(snake2_List) > Length_of_snake2:
                del snake2_List[0]

            for x in snake2_List[:-1]:
                if x == snake2_Head:
                    game_close = True
                    break

            # Verifica a cor do próximo quadrado para a cobra 2
            if random.randint(1, 100) == 1 or check_next_square_color(snake2_x, snake2_y, snake2_direction, barrier_list, snake_List) == black:
                snake2_direction = random.choice(['left', 'right', 'up', 'down'])
            else:
                if snake2_direction == 'up':
                    if check_next_square_color(snake2_x, snake2_y, 'left', barrier_list, snake_List) != black:
                        snake2_direction = 'left'
                    elif check_next_square_color(snake2_x, snake2_y, 'right', barrier_list, snake_List) != black:
                        snake2_direction = 'right'
                elif snake2_direction == 'down':
                    if check_next_square_color(snake2_x, snake2_y, 'left', barrier_list, snake_List) != black:
                        snake2_direction = 'left'
                    elif check_next_square_color(snake2_x, snake2_y, 'right', barrier_list, snake_List) != black:
                        snake2_direction = 'right'
                elif snake2_direction == 'left':
                    if check_next_square_color(snake2_x, snake2_y, 'up', barrier_list, snake_List) != black:
                        snake2_direction = 'up'
                    elif check_next_square_color(snake2_x, snake2_y, 'down', barrier_list, snake_List) != black:
                        snake2_direction = 'down'
                elif snake2_direction == 'right':
                    if check_next_square_color(snake2_x, snake2_y, 'up', barrier_list, snake_List) != black:
                        snake2_direction = 'up'
                    elif check_next_square_color(snake2_x, snake2_y, 'down', barrier_list, snake_List) != black:
                        snake2_direction = 'down'

        snake3_x, snake3_y, snake3_direction = move_boot_snake((snake3_x, snake3_y), snake3_direction, barrier_list, snake_List)

        # Verifica os limites para a cobra 3
        if snake3_x >= dis_width - snake_block or snake3_x < snake_block or snake3_y >= dis_height - snake_block or snake3_y < snake_block:
            game_close = True
        else:
            snake3_Head = []
            snake3_Head.append(snake3_x)
            snake3_Head.append(snake3_y)
            snake3_List.append(snake3_Head)
            if len(snake3_List) > Length_of_snake3:
                del snake3_List[0]

            for x in snake3_List[:-1]:
                if x == snake3_Head:
                    game_close = True
                    break

            # Verifica a cor do próximo quadrado para a cobra 3
            if random.randint(1, 100) == 1 or check_next_square_color(snake3_x, snake3_y, snake3_direction, barrier_list, snake_List) == black:
                snake3_direction = random.choice(['left', 'right', 'up', 'down'])
            else:
                if snake3_direction == 'up':
                    if check_next_square_color(snake3_x, snake3_y, 'left', barrier_list, snake_List) != black:
                        snake3_direction = 'left'
                    elif check_next_square_color(snake3_x, snake3_y, 'right', barrier_list, snake_List) != black:
                        snake3_direction = 'right'
                elif snake3_direction == 'down':
                    if check_next_square_color(snake3_x, snake3_y, 'left', barrier_list, snake_List) != black:
                        snake3_direction = 'left'
                    elif check_next_square_color(snake3_x, snake3_y, 'right', barrier_list, snake_List) != black:
                        snake3_direction = 'right'
                elif snake3_direction == 'left':
                    if check_next_square_color(snake3_x, snake3_y, 'up', barrier_list, snake_List) != black:
                        snake3_direction = 'up'
                    elif check_next_square_color(snake3_x, snake3_y, 'down', barrier_list, snake_List) != black:
                        snake3_direction = 'down'
                elif snake3_direction == 'right':
                    if check_next_square_color(snake3_x, snake3_y, 'up', barrier_list, snake_List) != black:
                        snake3_direction = 'up'
                    elif check_next_square_color(snake3_x, snake3_y, 'down', barrier_list, snake_List) != black:
                        snake3_direction = 'down'

        our_snake(snake_block, snake_List, snake_color)
        our_snake(snake_block + 5, snake2_List, snake_boot_color)  # Tamanho da cobrinha 2 aumentado
        our_snake(snake_block + 5, snake3_List, snake_boot_color)  # Tamanho da cobrinha 3 aumentado
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        pygame.display.update()

        clock.tick(snake_speed)
        pygame.time.delay(snake2_speed)  # Delay para controlar a velocidade da cobrinha 2
        pygame.time.delay(snake3_speed)  # Delay para controlar a velocidade da cobrinha 3

    pygame.quit()
    quit()


gameLoop()
