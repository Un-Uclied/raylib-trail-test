import raylibpy as rl
from .animation import Animation
from .ghost_trail import GhostTrail

class GameEntity:
    def __init__(self, rect : rl.Rectangle, animations : dict[str, Animation], animation_offset : rl.Vector2 = rl.Vector2(0, 0)):
        self.rect = rect

        self.animations = animations
        self.current_animation = self.animations["idle"].copy()
        self.animation_offset = animation_offset
        self.animation_render_pos = self.rect.x + self.animation_offset.x, self.rect.y + self.animation_offset.y

        self.trail = GhostTrail(self.current_animation)
        self.trail.enable()

    def set_animation(self, action_name : str):
        self.current_animation = self.animations[action_name].copy()
        self.trail.animation = self.current_animation

    def get_center_pos(self) -> rl.Vector2:
        return rl.Vector2(self.rect.x + self.rect.width / 2, self.rect.y + self.rect.height / 2)

    def update(self):
        self.animation_render_pos = self.rect.x + self.animation_offset.x, self.rect.y + self.animation_offset.y
        self.current_animation.update()

    def draw(self, debug = False):
        if debug : rl.draw_rectangle_rec(self.rect, rl.RED)
        rl.draw_texture_v(self.current_animation.img(), self.animation_render_pos, rl.WHITE)

class Player(GameEntity):
    def __init__(self, game, rect : rl.Rectangle, animations : dict[str, Animation], animation_offset : rl.Vector2 = rl.Vector2(0, 0)):
        super().__init__(rect, animations, animation_offset)
        self.game = game

        self.movement_speed = 12

    def set_animation(self, action_name):
        super().set_animation(action_name)

    def update(self):
        super().update()
        if (rl.is_key_down(rl.KEY_A)):
            self.rect.x -= self.movement_speed
        if rl.is_key_down(rl.KEY_D):
            self.rect.x += self.movement_speed
        if (rl.is_key_down(rl.KEY_W)):
            self.rect.y -= self.movement_speed
        if rl.is_key_down(rl.KEY_S):
            self.rect.y += self.movement_speed

        self.trail.update()

    def draw(self, debug=False):
        self.trail.draw()
        super().draw(debug)



class Enemy(GameEntity):
    def __init__(self, game, rect : rl.Rectangle, animations : dict[str, Animation], animation_offset : rl.Vector2 = rl.Vector2(0, 0)):
        super().__init__(rect, animations, animation_offset)
        self.game = game

    def follow_target(self, target : rl.Vector2, speed : float):
        direction = rl.Vector2(target.x - self.get_center_pos().x, target.y - self.get_center_pos().y)
        rl.vector2_normalize(direction)
        self.rect.x += direction.x * speed
        self.rect.y += direction.y * speed