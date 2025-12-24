import asyncio
import sys

import pygame
from pygame.locals import K_ESCAPE, K_SPACE, K_UP, KEYDOWN, QUIT

from .entities import (
    Background,
    Floor,
    GameOver,
    Pipes,
    Player,
    PlayerMode,
    Score,
    WelcomeMessage,
)
from .utils import GameConfig, Images, Sounds, Window

import numpy as np
import pandas as pd
import time
from .ai.q import Q

Agent = Q(alpha=0.1, gamma=0.99, epsilon=0)
Agent.Q = np.load("q.npy", allow_pickle=True)

with open("episode.txt", "r") as f:
    start_episode = int(f.read().strip())

with open("max_score.txt", "r") as f:
    max_score = int(f.read().strip())

class Flappy:
    def __init__(self):
        pygame.init()
        try:
            pygame.mixer.init()
        except Exception:
            pass
        pygame.display.set_caption("Flappy Bird")
        window = Window(288, 512)
        screen = pygame.display.set_mode((window.width, window.height))
        images = Images()

        self.config = GameConfig(
            screen=screen,
            clock=pygame.time.Clock(),
            fps=30,
            window=window,
            images=images,
            sounds=Sounds(),
        )
        self.font = pygame.font.SysFont(None, 24) 
        self.start_time = None

    async def start(self):
        self.sumscore = 0
        self.max = max_score
        for ep in range(start_episode, 200000):
            if ep % 100 == 0:
                avg_score = self.sumscore / 100
                print(f"Episode {ep}, Average Score: {avg_score}")
                self.sumscore = 0

            if ep % 10 == 0:
                Agent.Q.dump("q.npy")
                df = pd.DataFrame(Agent.Q)
                df.to_csv("q.csv", index=False)
                with open("episode.txt", "w") as f:
                    f.write(str(ep))
            Agent.epsilon = max(0, Agent.epsilon * 0.995)
            self.episode = ep

            self.background = Background(self.config)
            self.floor = Floor(self.config)
            self.player = Player(
                self.config,
                x=int(self.config.window.width * 0.2),
                y=int(self.config.window.vh * 0.5),
            )
            
            self.pipes = Pipes(self.config)
            self.score = Score(self.config)

            # print(f"epsilon={Agent.epsilon:.3f}")
            await self.play()

            

    def check_quit_event(self, event):
        if event.type == QUIT or (
            event.type == KEYDOWN and event.key == K_ESCAPE
        ):
            pygame.quit()
            sys.exit()

    def is_tap_event(self, event):
        m_left, _, _ = pygame.mouse.get_pressed()
        space_or_up = event.type == KEYDOWN and (
            event.key == K_SPACE or event.key == K_UP
        )
        screen_tap = event.type == pygame.FINGERDOWN
        return m_left or space_or_up or screen_tap

    def draw_text(self, text, x, y):
        text_surface = self.font.render(text, True, (255, 255, 255))
        self.config.screen.blit(text_surface, (x, y))

    def get_closest_pipe(self):
        for pipe in self.pipes.lower:
            if pipe.x + pipe.w > self.player.x:
                return pipe
        return self.pipes.lower[0]

    def get_state(self):
        pipe = self.get_closest_pipe()
        pipe_center = pipe.y + self.pipes.pipe_gap / 2

        vdiff = int(self.player.y - pipe_center)
        dx = int(pipe.x - self.player.x)
        vel_up = int(self.player.vel_y)

        return Agent.get_state_index(vdiff, dx, vel_up)



    def get_reward(self, collided, passed, diff, prev_diff):
        if collided:
            return -100
        if passed:
            return +30

        r = -0.05  

        if abs(diff) < abs(prev_diff):
            r += 0.3

        if abs(diff) < 20:
            r += 1.0

        return r




    async def play(self):
        self.score.reset()
        self.player.set_mode(PlayerMode.NORMAL)

        action_interval = 1
        action_timer = 0

        s = self.get_state()
        a = Agent.take_action(s)
        prev_abs_diff = 9999

        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (
                    event.type == KEYDOWN and event.key == K_ESCAPE
                ):
                    pygame.quit()
                    sys.exit()

            if action_timer <= 0:
                a = Agent.take_action(s)
                action_timer = action_interval
                if a == 1:
                    self.player.flap()
                    try:
                        self.config.sounds.wing.play()
                    except Exception:
                        pass
            else:
                action_timer -= 1

            self.background.tick()
            self.pipes.tick()
            self.floor.tick()
            self.player.tick()
            self.score.tick()

            passed = False
            for pipe in self.pipes.upper:
                if self.player.crossed(pipe):
                    self.score.add()
                    passed = True
                    try:
                        self.config.sounds.point.play()
                    except Exception:
                        pass

            collided = self.player.collided(self.pipes, self.floor)

            pipe = self.get_closest_pipe()
            diff = self.player.y - (pipe.y + self.pipes.pipe_gap / 2)

            r = self.get_reward(collided, passed, diff, prev_abs_diff)
            prev_abs_diff = abs(diff)

            s_next = self.get_state()
            Agent.update(s, a, r, s_next)

            s = s_next

            if collided:
                try:
                    self.config.sounds.hit.play()
                except Exception:
                    pass
                try:
                    self.config.sounds.die.play()
                except Exception:
                    pass
                break
            self.draw_text(f"Episode: {self.episode}", 10, 10)
            pygame.display.update()
            
            await asyncio.sleep(0)
            self.config.tick()

        self.sumscore += self.score.score
        if self.score.score > self.max:
            self.max = self.score.score
            print(f"New max score: {self.max}")
            with open("max_score.txt", "w") as f:
                f.write(str(self.max))