import raylibpy as rl

class Animation:
    def __init__(self, images, img_dur = 5, loop=True):
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)
    
    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True

    def img(self):
        return self.images[int(self.frame / self.img_duration)]
    
    def relative_next_img(self, add: int):
        next_frame = self.frame + (add * self.img_duration)
        
        if self.loop:
            next_frame %= self.img_duration * len(self.images)
        else:
            next_frame = min(next_frame, self.img_duration * len(self.images) - 1)

        return self.images[int(next_frame / self.img_duration)]