import pygame

pygame.init()

color = (255,255,255)
rect_color = (255, 0, 0)
position = (0,0)

# CREATING CANVAS
canvas = pygame.display.set_mode((600,400))

# TITLE OF CANVAS
pygame.display.set_caption("Show Image")

image = pygame.image.load("./assets/images/background.jpg")
exit = False

while not exit:
	canvas.fill(color)
	canvas.blit(image, dest = position)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit = True

	pygame.draw.rect(canvas, rect_color,
					 pygame.Rect(30, 200, 100, 60))
	pygame.display.update()
