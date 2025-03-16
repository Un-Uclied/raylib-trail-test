import raylibpy as rl
from abc import ABC, abstractmethod

from scripts.entites import Player, Enemy, GameEntity
from scripts.utils import load_textures, load_texture_default
from scripts.animation import Animation

class Game:
    def __init__(self):
        rl.init_window(1200, 900, "trail test")
        rl.set_target_fps(60)
        
        self.scenes = {
            "menu" : MainMenu(self),
            "game" : MainGame(self)
        }
        self.scene = self.scenes["menu"]

        self.debug = False

    def run(self):
        while not rl.window_should_close():
            self.scene.update()
            self.scene.draw()

class Scene(ABC):
    def __init__(self, game : Game):
        self.game = game
    @abstractmethod
    def update(self):
        pass
    @abstractmethod
    def draw(self):
        pass

class MainMenu(Scene):
    def __init__(self, game):
        super().__init__(game)

    def update(self):
        if (rl.is_key_pressed(rl.KEY_SPACE)):
            self.game.scene = self.game.scenes["game"]

    def draw(self):
        rl.begin_drawing()
        rl.clear_background(rl.BLANK)

        rl.draw_text("Main Menu\nSPACE TO CONTINUE", 10, 10, 40, rl.WHITE)

        rl.end_drawing()

class MainGame(Scene):
    def __init__(self, game):
        super().__init__(game) 

        # Create Player Object
        self.player = Player(self.game, rl.Rectangle(100, 100, 200, 200), {
            "idle" : Animation(load_textures("enemy"))
        }, animation_offset=rl.Vector2(-150, -130))

        # Add to update list
        self.game_entites : list[GameEntity] = [
            self.player,
            Enemy(self.game, rl.Rectangle(100, 600, 200, 200), {
                "idle" : Animation(load_textures("player"))
            })
        ]

        # set Camera
        self.camera = rl.Camera2D(rl.Vector2(rl.get_screen_width() / 2, rl.get_screen_height() / 2), rl.Vector2(0, 0), 0, 1)
        self.camera_speed = .1

        # sperate world to ui
        self.world = rl.load_render_texture(rl.get_screen_width(), rl.get_screen_height())

        # background image
        self.bg = load_texture_default("desert_1.png")

    def update(self):
        for entity in self.game_entites:
            entity.update()
            if hasattr(entity, "follow_target"):
                entity.follow_target(self.player.get_center_pos(), .01)

        # follow camera to player center pos
        self.camera.target = rl.vector2_lerp(self.camera.target, self.player.get_center_pos(), self.camera_speed)

    def draw(self):
        rl.begin_drawing()
        rl.clear_background(rl.BLANK)

        
        rl.begin_texture_mode(self.world)
        rl.begin_mode2d(self.camera)
        rl.clear_background(rl.BLANK)
        # Begin World Render
        rl.draw_texture(self.bg, 0, 0, rl.WHITE)

        for entity in self.game_entites:
            entity.draw(self.game.debug)
        
        # End World Render
        rl.end_mode2d()
        rl.end_texture_mode()
        
        # Begin Ui Render
        rl.draw_text("Main Game Scene", 10, 10, 40, rl.WHITE)
        rl.draw_fps(10, 80)
        #End Ui Render
        rl.end_drawing()

        rl.draw_texture_rec(self.world.texture, rl.Rectangle(0, 0, rl.get_screen_width(), -rl.get_screen_height()), rl.Vector2(0, 0), rl.WHITE)

if __name__ == "__main__":
    Game().run()