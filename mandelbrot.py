import pygame
from pygame.locals import *
import sys


class ZoomableSurface:
        def __init__(self, w, h, l):
	    self.width = w 
	    self.height = h
	    self.zoom_factor = 1.2
	    self.x0 = -1.4
	    self.x1 = 0.6
	    self.y0 = -1
	    self.y1 = 1
#            self.x0, self.x1, self.y0, self.y1 = -1.75299606368, -1.75299128661, 0.0141757522401, 0.0141805293092
            self.iter_limit = l
	    self.screen_size = (self.width, self.height)
	    self.screen = pygame.display.set_mode(self.screen_size)
	    self.surface = pygame.display.get_surface() 
	    self.pixels = pygame.PixelArray(self.surface)

	def render(self):
        	start = pygame.time.get_ticks()
		x_step = 1.0*(self.x1-self.x0)/self.width
		y_step = 1.0*(self.y1-self.y0)/self.height
		x , y = self.x0, self.y1
		for row in range(0, self.height):
			for col in range(0, self.width):
				self.pixels[col, row] = self.get_pixel_color_at(x,y)
				#self.screen.set_at((row, col), pixel_color)
				x += x_step
			y -= y_step
			x = self.x0
 
		pygame.display.flip()
        	end = pygame.time.get_ticks()	
        	print end-start, "miliseconds to render"

        def get_pixel_color_at(self, x0, y0):
            iterations = 0
            x, y = 0, 0
            while iterations < self.iter_limit:
                if x*x + y*y > 4:
                    intensity = 255-255*iterations/self.iter_limit
                    return ( intensity, intensity,0)
                x , y = (x*x -y*y) + x0, (2*x*y) + y0
                iterations += 1
            return (0, 0, 0)


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
                self.render()

	def zoom_in(self):
		self.zoom(1/self.zoom_factor)

	def zoom_out(self):
		self.zoom(self.zoom_factor)

        def hshift(self, factor, direction):
                shift= (self.x1 - self.x0)*(factor-1)
                self.x0 += direction * shift
                self.x1 += direction * shift
                self.render()

        def vshift(self, factor, direction):
                shift= (self.y1 - self.y0)*(factor-1)
                self.y0 += direction * shift
                self.y1 += direction * shift
                self.render()

        def shift_down(self):
                self.vshift(self.zoom_factor, -1)    
                
        def shift_up(self):
                self.vshift(self.zoom_factor, 1)    

        def shift_left(self):
                self.hshift(self.zoom_factor, -1)    
                
        def shift_right(self):
                self.hshift(self.zoom_factor, 1)    


clock = pygame.time.Clock()

w, h = 320, 320
iterations_limit = 64

if len(sys.argv) > 1:
    w, h, iterations_limit = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]) 
zsurface = ZoomableSurface(w,h, iterations_limit)
zsurface.render()

running = True
while running:

	# clock.tick(200)
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
	    break
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
	    if event.button == 4: #scroll whell up
		zsurface.zoom_out()
	    elif event.button == 5: #scroll whell up
	       	zsurface.zoom_in()
        elif event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
	       break
            if event.key == K_DOWN:
               zsurface.shift_down()
            elif event.key == K_UP:
               zsurface.shift_up()
            elif event.key == K_LEFT:
               zsurface.shift_left()
            elif event.key == K_RIGHT:
               zsurface.shift_right()

pygame.quit()
