import function as f
import pygame, sys
import math
pygame.init()
pygame.mixer.init()
wind_bg = (0,0,0)

pygame.font.init()
pygame.display.set_caption('Flappy Bird Rip-Off')

# icon
icon_img = pygame.image.load('./assets/favicon.ico')
pygame.display.set_icon(icon_img)
# load assets
background_img = pygame.image.load('./assets/sprites/background-day.png')
ybird_down = pygame.image.load('./assets/sprites/yellowbird-downflap.png')
ybird_middle = pygame.image.load('./assets/sprites/yellowbird-midflap.png')
ybird_up = pygame.image.load('./assets/sprites/yellowbird-upflap.png')
base = pygame.image.load('./assets/sprites/base.png')
pipe_up = pygame.image.load('./assets/sprites/pipe-green.png')
pipe_down = pygame.transform.rotate(pipe_up, 180)
num_img = f.load_numbers()

# load sounds
wing_sound = pygame.mixer.Sound('./assets/audio/wing.wav')
die_sound = pygame.mixer.Sound('./assets/audio/die.wav')
hit_sound = pygame.mixer.Sound('./assets/audio/hit.wav')
point_sound = pygame.mixer.Sound('./assets/audio/point.wav')
swoosh_sound = pygame.mixer.Sound('./assets/audio/swoosh.wav')

# current score
score = num_img[0]['img'];
score_num = 0

# pip_arr
pipe_arr = []

# window variables
wind_w = background_img.get_width()
wind_h = background_img.get_height()

screen = pygame.display.set_mode((wind_w, wind_h))

running = True
startgame = False
base_local = 0
loop_num = 1
loop_num1 = 1
motion = ybird_up
bird_x = wind_w/2 - ybird_down.get_width()
bird_y = wind_h/2 - ybird_down.get_height()

time = pygame.time.Clock()

# jump distance
drop = 2.4
fly = 50

# image rotation
rotate = 30

# speed
speed = 1000

# pipes variables
gap = 100 # space between top and bottom pipes
space = 160	# space between the each pipes
p_height = 150
pipe_local = wind_w

def upside_down(p):
	return 0 - pipe_up.get_height() + p - gap

# all pipes
pipe_arr = []
pip1 = {
	'p_local': wind_w,
	'p_height': f.pipe_y(),
	'checked': False,
}
pip2 = {
	'p_local': pip1['p_local'] + space,
	'p_height': f.pipe_y(),
	'checked': False,
}
pip3 = {
	'p_local': pip2['p_local'] + space,
	'p_height': f.pipe_y()
}
pipe_arr.append(pip1)
pipe_arr.append(pip2)
# pipe_arr.append(pip3)

startgame = False
spacebar = 0

score_x = 0

# score arr
score_arr = []
# get keyboard inputs
keys = pygame.key.get_pressed()

# game loop
while running:
	timedelta = time.tick(60)
	timedelta /= speed

	# background image
	screen.blit(background_img, (0,0))
		
	# bird on screen
	if loop_num > 0 and loop_num < 9:
		motion = ybird_up
		loop_num += 1
	elif loop_num > 8 and loop_num < 19:
		motion = ybird_middle
		loop_num += 1
	elif loop_num > 18 and loop_num < 29:
		motion = ybird_down
		loop_num += 1
	elif loop_num > 9:
		loop_num = 1
	screen.blit(motion, (bird_x, bird_y))
	
	# bird up and down motion
	if loop_num1 <= 20:
		bird_y += 0.5
		loop_num1 += 1
	elif loop_num1 > 20 and loop_num1 < 41:
		bird_y -= 0.5
		loop_num1 += 1
	elif loop_num1 > 40:
		loop_num1 = 1

	if startgame:
		# pipes on screen
		for i in pipe_arr:
			f.draw_pipes(screen, pipe_up, pipe_down, i['p_local'], i['p_height'], upside_down(i['p_height']))
		
		# moving the pipes left
		for i in pipe_arr:
			if i['p_local'] <= 0 - pipe_up.get_width():
				i['p_local'] = wind_w
				i['checked'] = False
				i['collision_checked'] = False
				i['p_height'] = f.pipe_y()
			else:
				i['p_local'] -= 100 * timedelta

	# base on screen
	screen.blit(base, (base_local, wind_h-base.get_height()))
	screen.blit(base, (base_local+base.get_width(), wind_h-base.get_height()))
	base_local -= 100 * timedelta
	if base_local <= 0 - base.get_width():
		base_local = 0
	
	# keys detection
	for e in pygame.event.get():
		if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
			if startgame:
				bird_y -= fly
				pygame.mixer.Sound.play(wing_sound)
				pygame.mixer.music.stop()
			else:
				startgame = True
		elif e.type ==  pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
			pygame.time.delay(10000)
		elif e.type == pygame.QUIT:
			running = False
	
	# score counter
	for i in pipe_arr:
		if not i['checked']:
			if bird_x >= i['p_local'] + pipe_up.get_width():	
				score_num += 1
				pygame.mixer.Sound.play(point_sound)
				pygame.mixer.music.stop()
				i['checked'] = True


	# pipe collision
	for i in pipe_arr:
		bottom_rect = pygame.Rect(i['p_local'], i['p_height'], pipe_up.get_width(), pipe_up.get_height())
		top_rect = pygame.Rect(i['p_local'], upside_down(i['p_height']), pipe_up.get_width(), pipe_up.get_height())
		bird_rect = pygame.Rect(bird_x, bird_y, motion.get_width(), motion.get_height())
		if top_rect.colliderect(bird_rect) or bottom_rect.colliderect(bird_rect):
			pygame.mixer.Sound.play(hit_sound)
			pygame.mixer.music.stop()
			running = False

	# display score on screen
	f.showscore(screen, str(score_num), num_img)

	# bird drop
	if startgame:
		bird_y += drop
	
	# hit the base object
	if bird_y + motion.get_height() >= wind_h-base.get_height():
		pygame.mixer.Sound.play(die_sound)
		pygame.mixer.music.stop()
		running = False
	
	# update
	pygame.display.flip()

pygame.quit()
