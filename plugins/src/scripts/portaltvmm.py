#!/usr/bin/python
# -*- coding: utf8 -*-

import os, sys, re, math, rsvg, time
from gimpfu import *
	
fonteNome = "Liberation Sans"
fonteTamanho = 18
imagemLargura = 640
imagemAltura  = 420
telaLargura = 720
telaAltura  = 480 

comentarioImagem = "dia a dia educacao"
images = []
logFile = "%s/portal_plug-in.log" % os.environ['HOME']

# define lista de formatos aceitos
formats = 'jpg|jpeg|jpe|gif|tiff|tif|tga|eps|ps|psd|png|bmp|ico|xcf|xpm|pcx|svg'

def log_to_desktop(msg):
	fd = open(logFile,'a')
	fd.write(msg)
	fd.close()

def novas_dimensoes(width, height):
	# testa proporcao da imagem e calcula regra de 3 de acordo
	proporcao = float(width) / float(height)

	if proporcao > 1.5:
		nl = imagemLargura
		na = (nl * int(height)) / int(width)

	else:
		na = imagemAltura
		nl = (na * int(width)) / int(height)
	
	return (nl, na)


#def prepare_image(img, textoTitulo, textoFonte, imageName, caminhoDestino):
def prepare_image(img, textoTitulo, textoFonte):
	draw = pdb.gimp_image_get_active_drawable(img)
	
	# confere se o modo da imagem e indexado ou tons de cinza - caso sim converter para RGB
	index = pdb.gimp_drawable_is_indexed(draw)
	gray  = pdb.gimp_drawable_is_gray(draw)
	if (index) or (gray):
		pdb.gimp_image_convert_rgb(img)

	nl, na = novas_dimensoes(img.width, img.height)
	#redimensiona imagem
	pdb.gimp_image_scale(img, nl, na)
	
	#calcula posicionamento da imagem na tela
	posicaoX = (telaLargura - nl) / 2
	posicaoY = (telaAltura - na) / 2
	
	#redimensiona a tela e posiciona a imagem de acordo com as mediadas previamente calculadas
	pdb.gimp_image_resize(img, telaLargura, telaAltura, posicaoX, posicaoY)

	# calcula posição do texto para fonte da imagem
	fonteX = posicaoX  
	fonteY = posicaoY + na + 5

	# cria texto e transforma seleção flutuante em camada
	camadaFonte = pdb.gimp_text_fontname(img, draw, fonteX, fonteY, "Fonte: %s" % textoFonte, 0, True, fonteTamanho, PIXELS, fonteNome)
	pdb.gimp_floating_sel_to_layer(camadaFonte)

	# caso texto titulo nao seja vazio criar camada para texto titulo
	if len(textoTitulo) > 0:
		# calcula tamanho do texto em pixels
		font_data = pdb.gimp_text_get_extents_fontname(textoTitulo, fonteTamanho, PIXELS, fonteNome)
		tamanhoTexto = font_data[0]
		# calcula posicao do texto titulo
		fonteX = (telaLargura - tamanhoTexto) / 2
		fonteY = posicaoY - 23

		# cria texto e transforma seleção flutuante em camada
		camadaFonte = pdb.gimp_text_fontname(img, draw, fonteX, fonteY, "%s" % textoTitulo, 0, True, fonteTamanho, PIXELS, fonteNome)
		pdb.gimp_floating_sel_to_layer(camadaFonte)

	# achata imagem
	pdb.gimp_image_flatten(img)
	return img

def abrir_imagem(file):
	print file
	# extrai extencao do nome do arquivo e converte para minusculo
	file_extension = os.path.splitext(file)[1].lower()

	# de acordo com a extensao do arquivo abrir a imagem com o procedimento correto
	
	try:

		if file_extension == '.jpg' or file_extension == '.jpeg' or file_extension == '.jpe':			
			img = pdb.file_jpeg_load(file, file)
		elif file_extension == '.png':
			img = pdb.file_png_load(file, file)
		elif file_extension == '.gif':
			img = pdb.file_gif_load(file, file)
		elif file_extension == '.bmp':
			img = pdb.file_bmp_load(file, file)
		elif file_extension == '.xcf':
			img = pdb.gimp_xcf_load(0,file, file)
		if file_extension == '.tiff' or file_extension == '.tif':			
			img = pdb.file_tiff_load(file, file)
		elif file_extension == '.tga':
			img = pdb.file_tga_load(file, file)
		elif file_extension == '.eps':
			img = pdb.file_eps_load(file, file)
		elif file_extension == '.ps':
			img = pdb.file_ps_load(file, file)
		elif file_extension == '.psd':
			img = pdb.file_psd_load(file, file)
		elif file_extension == '.pcx':
			img = pdb.file_pcx_load(file, file)
		elif file_extension == '.xpm':
			img = pdb.file_xpm_load(file, file)
		elif file_extension == '.svg':
			svg = rsvg.Handle(file)
			if svg.props.width < 640 and svg.props.height < 420:
				nl, na = novas_dimensoes(width, height)
				img = pdb.file_svg_load(file, file, 90, nl, na, 0)
			else:
				img = pdb.file_svg_load(file, file, 90, 0, 0, 0)
	except:
		e = sys.exc_info()[1]
   		print "Error: %s" % e 
		log_to_desktop("%s : Erro :: Nao foi possivel converter imagem\n" % file)
		return None
	else:
		log_to_desktop("%s : OK :: Imagem convertida com sucesso\n" % file)
		return img

def clean_up_and_queue(path, dirs, files):
        test = re.compile("\.(%s)$" % formats, re.IGNORECASE)
        files = filter(test.search, files)
        if len(files) > 0:
                for file in files:
                        fpath = "%s/%s" % (path, file)
                        images.append(fpath)

def redimensionar_lote_recursivo(img, draw, textoTitulo, textoFonte, caminhoOrigem, caminhoDestino, corFundo, corFrente):
	print pdb.gimp_version()
	
	log_to_desktop("%s\nLOTE RECURSIVO\nConvertendo imagens do diretório %s para o diretório %s\n" % (time.strftime("INÍCIO DE CONVERSÂO: %Y-%m-%d %H:%M:%S"),caminhoOrigem, caminhoDestino))

	# seta as cores de frente e fundo para as fornecidas na caixa de dialogo
	pdb.gimp_context_set_background(corFundo)
	pdb.gimp_context_set_foreground(corFrente)

	# lista o diretorio caminhoOrigem e executa um filtro deixando apenas os formatos aceitos
	for resource in os.walk(caminhoOrigem):
        	clean_up_and_queue(resource[0], resource[1], resource[2])
	
	test = re.compile("\.(%s)$" % formats, re.IGNORECASE)
	files = filter(test.search, images)  

	# itera sobre os nomes de arquivo no diretorio
	for file in files:

		# efetua as transformacoes e sala a imagem
		img = abrir_imagem(file)
		if img is not None:
			img = prepare_image(img, textoTitulo, textoFonte)
			
			draw = pdb.gimp_image_get_active_drawable(img)
			# nome da nova imagem -> saida	
			filename = file.replace(caminhoOrigem, caminhoDestino)
			(fpath, fname) = os.path.split(filename)

			if not os.path.isdir(fpath):
				os.makedirs(fpath)
			
			# substitui a extensao do arquivo para jpg para que o nome do arquivo final (saida) esteja correto
			pattern = '\.(%s|%s)$' % (formats, formats.upper())
			filename = re.sub(pattern, '.jpg', filename)

			# salava como JPG
			pdb.file_jpeg_save(img, draw, filename, filename, 0.85, 0, 0, 0, comentarioImagem, 0, 0, 0, 1 )
		
			# Libera a memoria ocupada pela imagem
			gimp.delete(img)
	
	log_to_desktop("%s\n" % time.strftime("TÉRMINO DE CONVERSÃO: %Y-%m-%d"))
	

def redimensionar_lote(img, draw, textoTitulo, textoFonte, caminhoOrigem, caminhoDestino, corFundo, corFrente):
	print pdb.gimp_version()

	log_to_desktop("%s\nLOTE\nConvertendo imagens do diretório %s para o diretório %s\n" % (time.strftime("INÍCIO DE CONVERSÂO: %Y-%m-%d %H:%M:%S"),caminhoOrigem, caminhoDestino))
	# seta as cores de frente e fundo para as fornecidas na caixa de dialogo
	pdb.gimp_context_set_background(corFundo)
	pdb.gimp_context_set_foreground(corFrente)

	# lista o diretorio caminhoOrigem e executa um filtro deixando apenas os formatos aceitos
	files = os.listdir(caminhoOrigem)    
	test = re.compile("\.(%s)$" % formats, re.IGNORECASE)
	files = filter(test.search, files)  

	# itera sobre os nomes de arquivo no diretorio
	for file in files:
		print "FILE " + file
		filepath = caminhoOrigem + '/' + file
		print "FILEPATH " + filepath
	
		img = abrir_imagem(filepath)	
		if img is not None:
			# substitui a extensao do arquivo para jpg para que o nome do arquivo final (saida) esteja correto
			pattern = '.(%s|%s)' % (formats, formats.upper())
			file = re.sub(pattern, '.jpg', file)
			
			img = prepare_image(img, textoTitulo, textoFonte)
			draw = pdb.gimp_image_get_active_drawable(img)
			# nome da nova imagem -> saida	
			filename = "%s/%s" % (caminhoDestino, file)
			# salava como JPG
			pdb.file_jpeg_save(img, draw, filename, filename, 0.85, 0, 0, 0, comentarioImagem, 0, 0, 0, 1 )
			
			# Libera a memoria ocupada pela imagem
			gimp.delete(img)

	log_to_desktop("%s\n" % time.strftime("TÉRMINO DE CONVERSÃO: %Y-%m-%d"))

def redimensionar_individial(img, draw, textoTitulo, textoFonte, corFundo, corFrente):
	# seta as cores de frente e fundo para as fornecidas na caixa de dialogo
	pdb.gimp_context_set_background(corFundo)
	pdb.gimp_context_set_foreground(corFrente)

	# efetua as transformacoes e sala a imagem
	img = prepare_image(img, textoTitulo, textoFonte)
	draw = pdb.gimp_image_get_active_drawable(img)
	# Libera a memoria ocupada pela imagem
	gimp.delete(img)

