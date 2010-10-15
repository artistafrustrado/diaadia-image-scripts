#!/usr/bin/python
# -*- coding: utf8 -*-

import os, sys, re, math
from gimpfu import *
import portaltvmm

register(
	"portal_resize_tb",
	"Conversão em lote de imagens para a utilizacao na TV Multimidia",
	"Conversão em lote de imagens para a utilizacao na TV Multimidia",
	"Fernando Michelotti, Lúcio de Araújo, Silvia Regina Alcântara, Ailton Lopes, Marcia Girola, Andreas Piekarz",
	"Fernando Michelotti, Lúcio de Araújo, Silvia Regina Alcântara, Ailton Lopes, Marcia Girola, Andreas Piekarz",
	"2008",
	"<Image>/Filters/PORTAL/Conversao em lote",
#	"<Toolbox>/Xtns/PORTAL/Conversão em lote",
#	"RGB*, GRAY*",
	"",
	[
		(PF_STRING, "textoTitulo",  "Titulo",  ""),
		(PF_STRING, "textoFonte",  "Fonte do arquivo",  ""),
		(PF_STRING, "caminhoOrigem",  "Pasta origem",  "%s/Desktop/entrada" % os.environ['HOME']),
		(PF_STRING, "caminhoDestino",  "Pasta destino",  "%s/Desktop/saida" % os.environ['HOME']),
		(PF_COLOR, "corFundo",  "Cor da borda", (255,255,255)),
		(PF_COLOR, "corFrente",  "Cor do texto", (0,0,0)),
	],
	[],
	portaltvmm.redimensionar_lote)

main()
