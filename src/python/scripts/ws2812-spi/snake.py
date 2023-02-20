#!/usr/bin/python
import spidev
import ws2812


write=ws2812.write2812


# def test_off(spi, nLED):
#     ws2812.write2812(spi, [0,0,0]*nLED)

# if __name__=="__main__":
#     spi = spidev.SpiDev()
#     spi.open(1,1)
    
#     test_pattern_sin(spi, nLED=50, intensity=255)
#     #test_fixed(spi)


import pygame
import time
import random
import keyboard

 
pygame.init()
 
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
 
dis_width = 10
dis_height = 5
num_led = dis_width * dis_height
 
led_board_indices = [
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 
    19, 18, 17, 16, 15, 14, 13, 12, 11, 10,
    20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
    39, 38, 37, 36, 35, 34, 33, 32, 31, 30,
    40, 41, 42, 43, 44, 45, 46, 47, 48, 49]

def clear_board(spi, nLED=8):
    write(spi, [[0,0,0]]*nLED)

def draw_board(spi, snake_list, food):
    info_to_write = []
    for i in range(0, num_led):
        info_to_write.append([0, 0, 0])

    info_to_write[led_board_indices[food[1] * dis_width + food[0]]] = yellow
    for coord in snake_list:
        info_to_write[led_board_indices[coord[1] * dis_width + coord[0]]] = white
    
    write(spi, info_to_write)

# dis = pygame.display.set_mode((dis_width, dis_height))
# pygame.display.set_caption('Snake Game by Edureka')
 
clock = pygame.time.Clock()
 
snake_block = 1
snake_speed = 1
 
# font_style = pygame.font.SysFont("bahnschrift", 25)
# score_font = pygame.font.SysFont("comicsansms", 35)
 
 
# def Your_score(score):
#     value = score_font.render("Your Score: " + str(score), True, yellow)
#     dis.blit(value, [0, 0])
 
 
 
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])
 
 
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])
 

x1_change = 0
y1_change = 0

def kbdCallback(e):
    found = False
    if e.name == "escape":
        game_over = True
    if e.name == "left":
        x1_change = -snake_block
        y1_change = 0
    elif e.name == "right":
        x1_change = snake_block
        y1_change = 0
    elif e.name == "up":
        y1_change = -snake_block
        x1_change = 0
    elif e.name == "down":
        y1_change = snake_block
        x1_change = 0

keyboard.on_press(kbdCallback)
# same as keyboard.on_press_key, but it does this for EVERY key
 
def gameLoop():
    spi = spidev.SpiDev()
    spi.open(1,1)
    game_over = False
    game_close = False
 
    x1 = dis_width // 2
    y1 = dis_height // 2
 
    x1_change = 0
    y1_change = 0
 
    snake_List = []
    Length_of_snake = 1
 
    foodx = int(round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0)
    foody = int(round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0)
 
    while not game_over:
        clear_board(spi, num_led)

        while game_close == True:
            if keyboard.is_pressed('q'):
                game_over = True
                game_close = False
                break  # finishing the loop
 
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        # dis.fill(blue)
        # pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]
 
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True
 
        # our_snake(snake_block, snake_List)
        # Your_score(Length_of_snake - 1)

        draw_board(spi, snake_List, [foodx, foody])
 
        # pygame.display.update()
 
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1
 
        clock.tick(snake_speed)
 
    pygame.quit()
    quit()

gameLoop()