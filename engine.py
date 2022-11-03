from math import sin, cos, radians, sqrt
import numpy
import PIL.Image

class Texture:
    __slots__ = ('data')
    def __init__(self, file_path):
        self.data = numpy.array(PIL.Image.open(file_path).getdata())
        
class Constants:
    __slots__ = ('win_size', 'rays', 'fov', 'text_res', 'ren_dist',
                 'center', 'line_width',
                 'rotations', 'x', 'base_offset', 'index_multi')
    def __init__(self, window_size=(1920, 1080), rays=120, fov=90, texture_resolution=256, render_distance=10):
        self.win_size = window_size
        self.rays = rays
        self.fov = fov
        self.text_res = texture_resolution
        self.ren_dist = render_distance
        
        self.center = (window_size[0] // 2, window_size[1] // 2)
        self.line_width = window_size[0] // rays
        
        self.rotations = []
        self.x         = []
        for ray in range(rays):
            self.rotations.append(radians(ray/(rays/fov) - fov/2))
            self.x.append(self.line_width*ray)
            
        self.base_offset = []
        self.index_multi = []
        for pixel in range(texture_resolution):
            self.base_offset.append(pixel - texture_resolution/2)
            self.index_multi.append(pixel * texture_resolution)

def vector_add(v1, v2):
    return [v1[0] + v2[0], v1[1] + v2[1]]

def vector_int_multiply(v1, number):
    return [v1[0] * number, v1[1] * number]

def calculate_direction(rotation):
    return (cos(rotation) + 0.00001, sin(rotation) + 0.00001)

def forward(start_pos, direction, speed):
    return [start_pos[0] + direction[0] * speed, start_pos[1] + direction[1] * speed]

def check_collision(environment, position):
    return environment[int(position[1])][int(position[0])]

def cast_ray(cts, start_pos, direction, environment):
    pos = [int(start_pos[0]), int(start_pos[1])]
    unit_step_size = (sqrt(1 + (direction[1] / direction[0]) ** 2), sqrt(1 + (direction[0] / direction[1]) ** 2))
    
    step = [0, 0]
    ray_length = [0, 0]
    if direction[0] < 0:
        step[0] = -1
        ray_length[0] = (start_pos[0] - pos[0]) * unit_step_size[0]
    else:
        step[0] = 1
        ray_length[0] = (pos[0] + 1 - start_pos[0]) * unit_step_size[0]
    if direction[1] < 0:
        step[1] = -1
        ray_length[1] = (start_pos[1] - pos[1]) * unit_step_size[1]
    else:
        step[1] = 1
        ray_length[1] = (pos[1] + 1 - start_pos[1]) * unit_step_size[1]
    
    distance = 0
    while distance < cts.ren_dist:
        if ray_length[0] < ray_length[1]:
            pos[0] += step[0]
            distance = ray_length[0]
            ray_length[0] += unit_step_size[0]
        else:
            pos[1] += step[1]
            distance = ray_length[1]
            ray_length[1] += unit_step_size[1]
        
        collision = check_collision(environment, pos)
        if collision > 0:
            collide_pos = vector_add(start_pos, vector_int_multiply(direction, distance))
            return (distance, collide_pos, collision)
    return (False, False, False)

def calculate_lines(cts, distance, ray_pos, rotation, ray, texture):
    height = 1 / (distance * cos(rotation)) * 3
    if ray_pos[0] - int(ray_pos[0]) / 1 < 0.01 or ray_pos[0] - int(ray_pos[0]) / 1 > 1 - 0.01:
        color_index = int(cts.text_res * (ray_pos[1] - int(ray_pos[1])))
    else:
        color_index = int(cts.text_res * (ray_pos[0] - int(ray_pos[0])))
    lines = []
    for pixel in range(cts.text_res):
        offset = cts.base_offset[pixel] * height
        lines.append((texture.data[color_index + cts.index_multi[pixel]][:-1], (cts.x[ray], cts.center[1] + offset), (cts.x[ray], cts.center[1] + offset - height), cts.line_width))
    return lines