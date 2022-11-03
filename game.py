import pygame as pg
import engine as e

c = e.Constants(render_distance=50)

pg.init()
win = pg.display.set_mode(c.win_size)
win.set_alpha(False)
clk = pg.time.Clock()

t = e.Texture('engine\\bricks.png')

font = pg.font.Font('freesansbold.ttf', 20)

env = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,0,0,0,0,0,1,1,1,1,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,1,0,0,1],
    [1,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
    [1,0,1,0,0,1,0,0,0,0,1,0,1,0,1],
    [1,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,1,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

pos = [1.1, 1.1]
rot = 0

run = True
while run:
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            run = False
    
    keys = pg.key.get_pressed()
    mov = pos
    if keys[pg.K_w]: mov = e.forward(pos, e.calculate_direction(rot), 0.04)
    if keys[pg.K_s]: mov = e.forward(pos, e.calculate_direction(rot), -0.04)
    if keys[pg.K_a]: rot -= 0.04
    if keys[pg.K_d]: rot += 0.04
    if e.check_collision(env, mov) == 0: pos = mov
        
    win.fill((0, 0, 0))
    for ray in range(c.rays):
        direction = e.calculate_direction(rot + c.rotations[ray])
        dis, position, block = e.cast_ray(c, pos, direction, env)
        if dis and position:
            for l in e.calculate_lines(c, dis, position, c.rotations[ray], ray, t):
                pg.draw.line(win, l[0], l[1], l[2], l[3])
                
    fps_counter = font.render(f'FPS: {round(clk.get_fps())}', True, (255, 255, 255))
    win.blit(fps_counter, (0, 0))
                
    clk.tick(60)
                
    pg.display.flip()