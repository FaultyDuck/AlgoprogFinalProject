import pygame as py

def scale_image(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return py.transform.scale(img, size)

def blit_rotate_center(win, image, top_left, angle):
    rotated_image = py.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft = top_left).center) #original image, top left is equal to its own x and y value and the center of that image is still centered on that point
    win.blit(rotated_image, new_rect.topleft)