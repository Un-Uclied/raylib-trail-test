import raylibpy as rl
from .animation import Animation

class GhostTrail:
    def __init__(self, animation: Animation, count = 5):
        self.animation = animation
        self.enabled = False
        self.spawn_speed = 10

        self.max_trail_count = count
        self.current_trail_count = 0

        self.trail_distance = 25

        self.start_trail_transparency = 120
        self.trail_transparency = 35
    
    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def update(self):
        pass

    def draw(self):
        for i in range(self.current_trail_count):
            rl.draw_texture_v(self.current_animation.relative_next_img(-i - 1), self.animation_render_pos + rl.Vector2((i + 1) * self.trail_distance, 0), rl.Color(255, 0, 0, max(self.start_trail_transparency - i * self.trail_transparency, 0)))