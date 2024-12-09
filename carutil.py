import pygame as py

def scale_image(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return py.transform.scale(img, size)

def blit_rotate_center(win, image, top_left, angle):
    rotated_image = py.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft = top_left).center) #original image, top left is equal to its own x and y value and the center of that image is still centered on that point
    win.blit(rotated_image, new_rect.topleft)

def stack(win, images, top_left, angle, spread=2):
    I = py.image.load("img_0.png")
    for i, img in enumerate(images):
        rotated_img = py.transform.rotate(img, angle)
        new_rect = rotated_img.get_rect(center=I.get_rect(topleft = top_left).center)
        win.blit(rotated_img, (top_left[0] - rotated_img.get_width() // 2, top_left[1] - rotated_img.get_height() // 2 - i * spread))