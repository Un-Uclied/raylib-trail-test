import raylibpy as rl
import os

BASE_IMAGE_PATH = "assets/sprites/"

def load_texture_default(path):
    return rl.load_texture(BASE_IMAGE_PATH + path)

def load_textures(path):
    images = []
    for img_name in sorted(os.listdir(BASE_IMAGE_PATH + path)):
        images.append(rl.load_texture(BASE_IMAGE_PATH + path + '/' + img_name))
    return images