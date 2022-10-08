import neat
import pygame
from player import Player
from pipe import Pipe
from threading import Timer
import os
from random import *
from timer import RepeatedTimer
import math
running = True
# evaluate function


def add_pipe(pipes: list):
    y = randint(100, 200)
    p1 = Pipe(y + 250)
    p2 = Pipe(y - (200 + 700))

    pipes.append(p1)
    pipes.append(p2)


ges = []


def eval_genomes(genomes, config):
    ges.clear()
    nets = []
    global running
    players = []
    for i in range(100):
        players.append(Player())
    dead = []
    pipes = []
    pipe_timer = RepeatedTimer(1.2, add_pipe, True, pipes)

    screen = pygame.display.set_mode((1920 / 1.75, 1080 / 1.75))

    # Set the caption of the screen
    pygame.display.set_caption('ai')
    for genome_id, genome in genomes:
        genome.fitness = 0
        ges.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
    clock = pygame.time.Clock()
    while running and players:
        dt = clock.tick(60) / 1000
        screen.fill((0, 200, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pipe_timer.stop()
                os._exit(os.EX_OK)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j:
                    players.clear()

        for pipe in pipes:

            pipe.update(dt)
            pygame.draw.rect(screen, (0, 255, 0), pipe.rect)

            for p, x in enumerate(players):
                if pygame.Rect.colliderect(players[p].rect, pipe.rect):
                    players[p].jump_timer.stop()
                    players.pop(p)
        for player, x in enumerate(players):
            ges[player].fitness += 0.1
            if players[player].jumping:
                players[player].rect.top -= 1
            else:
                players[player].rect.bottom += 200 * dt

            if players[player].rect.bottom > 620:
                players[player].jump_timer.stop()
                players.pop(player)
                continue

            p = pygame.draw.rect(screen, (250, 250, 90), players[player].rect)
            players[player].fitness += 0.1
            if pipes:
                index = pipes.index(pipes[-1])
                output = nets[player].activate((
                players[player].rect.bottom, 
                abs(players[player].rect.bottom - pipes[index].rect.bottom),
                abs(players[player].rect.bottom - pipes[index-1].rect.bottom),
                620 - players[player].rect.bottom))

                if output[0] > 0.5:
                    players[player].jump()

        if not players:
            players.clear()
            break

        pygame.display.flip()
    dead.clear()


config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     'config-feedforward')

# Create the population, which is the top-level object for a NEAT run.
p = neat.Population(config)

# Add a stdout reporter to show progress in the terminal.
p.add_reporter(neat.StdOutReporter(False))

# Run until a solution is found.
winner = p.run(eval_genomes)
