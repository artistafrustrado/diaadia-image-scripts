#!/usr/bin/python
# -*- coding: utf8 -*-

import os, sys, re, math
from gimpfu import *
import portaltvmm

register(
	"portal_resize_one",
	"Conversão individual de imagens para a utilizacao na TV Multimidia",
	"Conversão individual de imagens para a utilizacao na TV Multimidia",
	"Fernando Michelotti, Lúcio de Araújo, Silvia Regina Alcântara, Ailton Lopes, Marcia Girola, Andreas Piekarz",
	"Fernando Michelotti, Lúcio de Araújo, Silvia Regina Alcântara, Ailton Lopes, Marcia Girola, Andreas Piekarz",
	"2008",
	"<Image>/Filters/PORTAL/Conversao individual",
	"RGB*, GRAY*",
	[
		(PF_STRING, "textoTitulo",  "Titulo",  ""),
		(PF_STRING, "textoFonte",  "Fonte do arquivo",  ""),
		(PF_COLOR, "corFundo",  "Cor da borda", (255,255,255)),
		(PF_COLOR, "corFrente",  "Cor do texto", (0,0,0)),
	],
	[],
	portaltvmm.redimensionar_individial)

main()
