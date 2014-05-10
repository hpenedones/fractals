import pygame

class ZoomableSurface():
	width = 150 
	height = 150
	screen_size = (width, height)
	zoom_factor = 1.2
	x0 = -100
	x1 = 100
	y0 = -100
	y1 = 100
	screen = pygame.display.set_mode(screen_size)
	surface = pygame.display.get_surface() 
	pixels = pygame.PixelArray(surface)

	def render(self):
		start = pygame.time.get_ticks()
		x_step = 1.0*(self.x1-self.x0)/self.width
		y_step = 1.0*(self.y1-self.y0)/self.height
		x , y = self.x0, self.y0
		for row in range(0, self.height):
			for col in range(0, self.width):
				
				self.pixels[row,col] = (x%255 , y%255 , x*y%255 )
				# aa =  (x % 255, y %255, 0 )
				#self.screen.set_at((row, col), pixel_color)
				x += x_step
			y += y_step
			x = self.x0
 
		mid = pygame.time.get_ticks()	
		pygame.display.flip()
		
		end = pygame.time.get_ticks()	
		print "ms = ", mid -start, end-mid

	def zoom(self, factor):
		center_x = (self.x1 + self.x0)/2
		center_y = (self.y1 + self.y0)/2	
		box_width = (self.x1 - self.x0) * factor
		box_height = (self.y1 - self.y0) * factor
		self.x0 = center_x - box_width/2 
		self.x1 = center_x + box_width/2
		self.y0 = center_y - box_height/2
		self.y1 = center_y + box_height/2
		print self.x0, self.x1, self.y0, self.y1

	def zoom_in(self):
		self.zoom(1/self.zoom_factor)

	def zoom_out(self):
		self.zoom(self.zoom_factor)

running = True
clock = pygame.time.Clock()
zsurface = ZoomableSurface()
zsurface.render()

while running:

	clock.tick(120)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 4: #scroll whell up
				zsurface.zoom_out()
			elif event.button == 5: #scroll whell up
				zsurface.zoom_in()
			
			zsurface.render()
