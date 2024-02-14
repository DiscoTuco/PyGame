import pygame

class Obstacle:
    def __init__(self, canvas, rect, color):
        self.canvas = canvas
        self.rect = rect
        self.color = color

    def draw(self):
        pygame.draw.rect(self.canvas, self.color, self.rect)


    def collision(self, entity):

        left = entity.x - entity.size
        right = entity.x + entity.size
        top = entity.y - entity.size
        bottom = entity.y + entity.size

        left_side = self.rect[0]
        top_side = self.rect[1]
        right_side = self.rect[0] + self.rect[2]
        bottom_side = self.rect[1] + self.rect[3]

        return not (right < left_side or left > right_side or bottom < top_side or top > bottom_side)


    def colltion_point(self, point):
        left_side = self.rect[0]
        top_side = self.rect[1]
        right_side = self.rect[0] + self.rect[2]
        bottom_side = self.rect[1] + self.rect[3]

        return left_side < point[0] and right_side > point[0] and top_side < point[1] and bottom_side > point[1]


    def collision_circle(self, entity):

        left_side = self.rect[0]
        top_side = self.rect[1]

        right_side = self.rect[0] + self.rect[2]
        bottom_side = self.rect[1] + self.rect[3]

        temp_x = entity.x
        temp_y = entity.y
        if entity.x < left_side:
            temp_x = left_side
        elif entity.x > right_side:
            temp_x = right_side
        if entity.y < top_side:
            temp_y = top_side
        elif entity.y > bottom_side:
            temp_y = bottom_side

        distance = (((temp_x - entity.x) ** 2 + (temp_y - entity.y) ** 2) ** (1 / 2))

        return distance < entity.size
