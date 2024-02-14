import pygame
from math import cos, sin, radians, degrees


class Entity:
    def __init__(self, canvas, color, position, controls, size):
        self.canvas = canvas
        self.color = color
        self.x, self.y = position
        self.px, self.py = position
        self.controls = controls
        self.size = size
        self.coordinates = self.x + size, self.y + size

        self.theta = 0
        self.sight_x = sin(self.theta)
        self.sight_y = cos(self.theta)

        self.speed = 5
        self.detected_time = 1

        self.detection_dots = []

    def draw(self):
        pygame.draw.circle(self.canvas, self.color, (self.x, self.y), self.size)

    def move(self, obstacles, keys):
        self.px = self.x
        self.py = self.y

        if 'w' in self.controls:

            if keys[pygame.K_w]:
                self.y += self.sight_y * self.speed
                self.x += self.sight_x * self.speed
            if keys[pygame.K_s]:
                self.y -= self.sight_y * self.speed
                self.x -= self.sight_x * self.speed

        elif 'i' in self.controls:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_j]:
                self.x -= 2
            if keys[pygame.K_l]:
                self.x += 2
            if keys[pygame.K_i]:
                self.y -= 2
            if keys[pygame.K_k]:
                self.y += 2

        self.coordinates = self.x + self.size, self.y + self.size

        for obstacle in obstacles:
            if obstacle.collision_circle(self):
                # Calculate the overlap of the circle and rectangle in both X and Y directions
                overlap_x = max(0, min(self.x + self.size, obstacle.rect[0] + obstacle.rect[2]) - max(
                    self.x - self.size, obstacle.rect[0]))
                overlap_y = max(0, min(self.y + self.size, obstacle.rect[1] + obstacle.rect[3]) - max(
                    self.y - self.size, obstacle.rect[1]))

                # Calculate the direction of the obstacle from the circle's center
                dx = obstacle.rect[0] + obstacle.rect[2] / 2 - self.x
                dy = obstacle.rect[1] + obstacle.rect[3] / 2 - self.y

                # Adjust the circle's position based on the overlap
                if overlap_x < overlap_y:
                    # Adjust horizontally
                    self.x += -overlap_x * (1 if dx > 0 else -1)
                else:
                    # Adjust vertically
                    self.y += -overlap_y * (1 if dy > 0 else -1)

    def detect(self, other):

        distance = (((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** (1/2))
        detect_radius = 100

        # How to do speed = proportional inverse distance?
        while distance <= detect_radius:
            print((self.x - other.x) / detect_radius)
            a = pygame.Vector2(other.x - self.x, other.y - self.y).normalize()
            self.x += a.x * (1 - distance / detect_radius) * self.speed
            self.y += a.y * (1 - distance / detect_radius) * self.speed
            self.detected_time *= 1.005
            #print(self.detected_time)
            return pygame.draw.line(self.canvas, "yellow", (self.x, self.y), (other.x, other.y), 2)
        self.detected_time = 1

    def sight(self):
        pygame.draw.line(self.canvas, "green", (self.x, self.y), (self.x + self.sight_x * 50, self.y + self.sight_y * 50), 2)


    def rotate(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.theta -= .1
        if keys[pygame.K_d]:
            self.theta += .1

        self.sight_x = sin(self.theta)
        self.sight_y = cos(self.theta)

    def circumference(self):
        self.detection_dots = []
        self.detection_dots.append(cos)


class Player(Entity):
    max_ray_length = 400
    fov = 100
    resolution = 50

    def __init__(self, doom_canvas, canvas, color, position, controls, size):
        super().__init__(canvas, color, position, controls, size)
        self.doom_canvas = doom_canvas

    def draw(self, obstacles):
        super().draw()
        for n in range(self.resolution + 1):
            angle = (-self.fov / 2) + (self.fov/self.resolution)*n
            distance = self.cast_ray(obstacles, angle)
            self.doom_canvas.draw(n, distance, radians(angle))

    def cast_ray(self, obstacles, angle):
        direction = sin(radians(angle) + self.theta), cos(radians(angle) + self.theta)

        min_distance = self.max_ray_length
        for obstacle in obstacles:
            distance = self.get_ray_distance(direction, obstacle)
            if distance < min_distance:
                min_distance = distance

        end_pos = self.x + direction[0] * min_distance, self.y + direction[1] * min_distance
        pygame.draw.line(self.canvas, 'turquoise', (self.x, self.y), end_pos, 2)

        return min_distance

    def get_ray_distance(self, direction, obstacle):
        for d in range(self.max_ray_length // 3):
            distance = d * 3
            end_pos = self.x + direction[0] * distance, self.y + direction[1] * distance
            if obstacle.colltion_point(end_pos):
                return distance

        return self.max_ray_length


class DoomStyle:
    def __init__(self, surface):
        self.surface = surface
        self.pixel_width = surface.get_width() / (Player.resolution)

    def draw(self, i, ray_distance, ray_angle):
        ray_distance *= cos(ray_angle)

        normal_length = 1 - (ray_distance / Player.max_ray_length)

        height = self.surface.get_height() * normal_length
        x = i * self.pixel_width
        y = self.surface.get_height() / 2 - height / 2

        c = 5 + int(255 * normal_length)

        pygame.draw.rect(self.surface, (c, c, c), (x, y, self.pixel_width, height))
