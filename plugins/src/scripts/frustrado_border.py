#!/usr/bin/python
# -*- coding: utf8 -*-

import math
from gimpfu import *

class BorderTypeGaussian:
	def __init__(self, img, draw):
		self.img	= img
		self.draw	= draw

	def main(self, borderSize):
		borderSize = float("%s.0" % borderSize)
		pdb.plug_in_gauss(self.img, self.draw, borderSize, borderSize, 1)

class BorderTypeNoiseSpread:
	def __init__(self, img, draw):
		self.img	= img
		self.draw	= draw

	def main(self, borderSize):
		borderSize = float("%s.0" % borderSize)
		pdb.plug_in_spread(self.img, self.draw, borderSize, borderSize)

class BorderTypeWaves:
	def __init__(self, img, draw):
		self.img	= img
		self.draw	= draw

	def main(self, borderSize):
		borderSize = float("%s.0" % borderSize)
		pdb.plug_in_waves(self.img, self.draw, borderSize, 0.0, borderSize, 0, 0)

class BorderTypeShift:
	def __init__(self, img, draw):
		self.img	= img
		self.draw	= draw

	def main(self, borderSize):
		borderSize = float("%s.0" % borderSize)
		pdb.plug_in_shift(self.img, self.draw, borderSize, 0)

class BorderTypeRipple:
	def __init__(self, img, draw):
		self.img	= img
		self.draw	= draw

	def main(self, borderSize):
		borderSize = float("%s.0" % borderSize)
		pdb.plug_in_ripple(self.img, self.draw, borderSize, 10, 0, 1, 1, True, True)

class BorderTypeNewsprint:
	def __init__(self, img, draw):
		self.img	= img
		self.draw	= draw

	def main(self, borderSize):
		pdb.plug_in_gauss(self.img, self.draw, borderSize, borderSize, 1)
		pdb.plug_in_newsprint(self.img, self.draw, 9, 1, 100, borderSize, 0, borderSize, 0, borderSize, 0, borderSize, 0, 14)

class BorderTypePixelize:
	def __init__(self, img, draw):
		self.img	= img
		self.draw	= draw

	def main(self, borderSize):
		borderSizeFloat = float("%s.0" % borderSize)
		pdb.plug_in_gauss(self.img, self.draw, borderSizeFloat, borderSize, 1)
		pdb.plug_in_gauss(self.img, self.draw, borderSizeFloat, borderSize, 1)
		pdb.plug_in_pixelize2(self.img, self.draw, 8, 8)

class Border:
	def __init__(self, img, tdrawable, borderSize, borderType):
		self.img	= img
		self.tdrawable	= tdrawable
		self.borderSize	= borderSize
		self.borderType	= borderType
		
		self.width = tdrawable.width
		self.height = tdrawable.height

		self.layers = {}
		self.main()		
		gimp.displays_flush( )


	def main(self):
    		self.img.disable_undo()
		self.createBorder()
		self.preparePhoto()
		self.hideBackground()
		self.img.enable_undo()

	def createBorder(self):
		if pdb.gimp_selection_is_empty(self.img):
			pdb.gimp_selection_all(self.img)
			pdb.gimp_selection_shrink(self.img, self.borderSize)

	def preparePhoto(self):
		draw = pdb.gimp_image_get_active_drawable(self.img)
		activeLayer = pdb.gimp_image_get_active_layer(self.img)
		lc = pdb.gimp_layer_copy(activeLayer, 1)

		lcMask = pdb.gimp_layer_create_mask(lc, ADD_WHITE_MASK)
		
		self.img.add_layer(lc, 0)
		pdb.gimp_layer_add_mask(lc, lcMask)

		draw = pdb.gimp_image_get_active_drawable(self.img)

		pdb.gimp_selection_invert(self.img)
		selection = pdb.gimp_image_get_selection(self.img)
		pdb.gimp_bucket_fill( draw , FOREGROUND_FILL, NORMAL_MODE, 100, 255, False, 0, 0)
		
		pdb.gimp_selection_none(self.img)

		draw = pdb.gimp_image_get_active_drawable(self.img)
		
		if self.borderType == 'gaussian':
			filter = BorderTypeGaussian(self.img, draw)
		elif self.borderType == 'spread':	
			filter = BorderTypeNoiseSpread(self.img, draw)
		elif self.borderType == 'waves':	
			filter = BorderTypeWaves(self.img, draw)
		elif self.borderType == 'shift':	
			filter = BorderTypeShift(self.img, draw)
		elif self.borderType == 'ripple':	
			filter = BorderTypeRipple(self.img, draw)
		elif self.borderType == 'newsprint':	
			filter = BorderTypeNewsprint(self.img, draw)
		elif self.borderType == 'pixelize':	
			filter = BorderTypePixelize(self.img, draw)
		
		filter.main(self.borderSize)

	def hideBackground(self):
		pdb.gimp_image_set_active_layer(self.img, self.img.layers[1])
		draw = pdb.gimp_image_get_active_drawable(self.img)
		pdb.gimp_drawable_set_visible(draw, False)

def prepare_image(img, tdrawable, borderSize, borderType, bgcolor=(255, 255, 255)):
	cp = Border(img, tdrawable, borderSize, borderType)

register(
	"portal_bordas",
	"Cria bordas para a imagem",
	"Cria bordas para a imagem",
	"Fernando Michelotti",
	"Fernando Michelotti",
	"2007-2008",
	"<Image>/Filters/PORTAL/Bordas",
	"RGB*, GRAY*",
	[
		(PF_INT, "borderSize", "Tamanho da borda", 25),
		(PF_RADIO, "borderType", "Tipo", "Tipo", (("Desfoque", "gaussian"), ("Ruido", "spread"), ("Ondas","waves"),("Shift","shift"),("Ripple","ripple"),("Impressão Off-Set","newsprint"),("Pixelizar","pixelize")))
	],
	[],
	prepare_image)

main()
