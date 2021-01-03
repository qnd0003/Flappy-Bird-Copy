import pygame, sys, random

def load_numbers():
	arr = []
	for i in range(10):
		num_img = pygame.image.load('./assets/sprites/{}.png'.format(i))
		a = {'img': num_img, 'score': i}
		arr.append(a)
	return arr

def pipe_y():
	return random.randint(150,330)

def draw_pipes(screen, pipe_up, pipe_down, pipe_local, p_height, upside_down):
	screen.blit(pipe_up, (pipe_local, p_height))
	screen.blit(pipe_down, (pipe_local, upside_down))

def showscore(screen, score, img):
	# score on screen
	score_x = 0
	for i in score:
		screen.blit(img[int(i)]['img'], (score_x,0))
		score_x += 20
