import pickle

import pygame
import sys
import datetime
from src.asteroid import *
from src.player import *
from src.world import World
from src.space_body import SpaceBody
import socket
import select

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
TEXT_HEIGHT = 20
FPS = 60
SCALE = 60 # 1 light sec is 60 pixels


class Game:
    game = None

    def __init__(self):
        self.controls = {"up": False,
                         "down": False,
                         "left": False,
                         "right": False}
        Game.game = self

        pygame.init()
        pygame.mixer.music.load("assets/music/420.wav")
        pygame.mixer.music.play(loops=-1, start=0.0)
        self.clock = pygame.time.Clock()

        self.display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.font = pygame.font.Font("assets/fonts/unifont-10.0.06.ttf", TEXT_HEIGHT)
        self.world = World()
        self.player = Player()

        Asteroid(2, 2)
        Asteroid(0, 2)
        Asteroid(2, 0)
        Asteroid(5, 5)
        self.connect_to_server()

    def connect_to_server(self):
        self.host = "127.0.0.1"
        self.port = 2345
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        except socket.error as msg:
            print("Failed to create socket: " + str(msg))

        try:
            server_ip = socket.gethostbyname(self.host)
        except socket.gaierror:
            print("Server could not be resolved")
            raise

        self.sock.connect((server_ip, self.port))
        print("Connected to server")

    def send(self, msg):
        try:
            # Not sure how well this will work with multiple clients
            tuple = {'x': msg.x, 'y': msg.y, 't': msg.t, "vx": msg.vx, "vy": msg.vy, "vt": msg.vt, "rot": msg.rotation}
            string = pickle.dumps(tuple, pickle.HIGHEST_PROTOCOL)
            file = self.sock.makefile("wb")
            file.write(string)
            file.flush()
            print("message sent")
        except socket.error:
            print("Messaging failed: %s" % (socket.error))
        receive = select.select([self.sock], [], [], 0.001)
        if len(receive[0]):
            message = self.sock.recv(6969)
            message = pickle.loads(message)
            self.player.x = message['x']
            self.player.y = message['y']
            self.player.t = message['t']
            self.player.vx = message["vx"]
            self.player.vy = message["vy"]
            self.player.vt = message["vt"]
            self.player.rotation = message["rot"]

    def run(self):
        while True:
            # msg to server
            self.send(self.player)
            self.render_world(self.display)
            self.handle_input()
            self.update_environment()

    def draw_statusbar(self, display):
        pygame.draw.rect(display, pygame.Color(191, 87, 0), pygame.Rect(0, 0, SCREEN_WIDTH, TEXT_HEIGHT + 5))

        surface = self.font.render("Time: " + str("%.1f" % self.player.t) + " seconds | " +
                                   "x: " + "%.1f"%self.player.x + " light seconds | " +
                                   "y: " + "%.1f"%self.player.y + " light seconds"

                                   , True, (144, 238, 144))
        self.display.blit(surface, (0, 0))

    def render_world(self, display):
        display.fill((0, 0, 0))

        self.draw_statusbar(display)

        for body in SpaceBody.space_bodies:
            pos_move, time = body.get_screen_pos(self.player, SCALE, SCREEN_WIDTH, SCREEN_HEIGHT)
            display.blit(body.image, body
                         .image.get_rect()
                         .move(*pos_move))

            time_surface = self.font.render(str("%.1f" % time), True, (200, 238, 144))
            x, y = pos_move
            self.display.blit(time_surface, (x, y - body.image.get_rect().height/2 - 8))

        pygame.display.flip()

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit_game()

                if event.key == pygame.K_UP:
                    self.controls["up"] = True
                if event.key == pygame.K_DOWN:
                    self.controls["down"] = True
                if event.key == pygame.K_RIGHT:
                    self.controls["right"] = True
                if event.key == pygame.K_LEFT:
                    self.controls["left"] = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.controls["up"] = False
                if event.key == pygame.K_DOWN:
                    self.controls["down"] = False
                if event.key == pygame.K_RIGHT:
                    self.controls["right"] = False
                if event.key == pygame.K_LEFT:
                    self.controls["left"] = False

    def update_environment(self):
        dt = self.clock.tick(FPS) / 1000

        if self.controls["up"]:
            self.player.thrust_forward(dt)
        if self.controls["down"]:
            self.player.thrust_backwards(dt)
        if self.controls["right"]:
            self.player.rotate_right(dt)
        if self.controls["left"]:
            self.player.rotate_left(dt)

        for body in SpaceBody.space_bodies:
            body.update(dt)
