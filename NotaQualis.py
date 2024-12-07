# -*- coding: utf-8 -*-
"""
Created on Mon Mar  13 17:22:56 2023

@author: Albert dos Santos
"""

# listaBase = ['A Novel Procedure for Classification of Early Human Actions from EEG Signals',
# 			'A Model for Classification of Early Human Actions from EEG Signals',
# 			'Analyzing the benefits of the combined interaction of head and eye tracking in 3D visualization information',
# 			'Analisando os benefícios da interação combinada de rastreamento de cabeça e olhos em visualização da informação 3D',
# 			'Analisando os benefícios da interação combinada de rastreamento de cabeça e olhos em visualização da informação 3D',
# 			'Recognizing and Exploring Azulejos on Historic Buildings? Facades by Combining Computer Vision and Geolocation in Mobile Augmented Reality Applications',
# 			"Recognizing and Exploring Azulejos on Historic Buildings' Facades by Combining Computer Vision and Geolocation in Mobile Augmented Reality Applications",
# 			"Recognizing and Exploring Azulejos on Historic Buildings' Facades by Combining Computer Vision and Geolocation in Mobile Augmented Reality Applications",
# 			'Data Dissemination Based on Complex Networks? Metrics for Distributed Traffic Management Systems',
# 			"Data Dissemination Based on Complex Networks' Metrics for Distributed Traffic Management Systems",
# 			'Optimized-selection Model of Relay Nodes in Platoon-based Vehicular Ad-hoc Networks',
# 			'Optimized-selection model of relay nodes in platoon-based vehicular ad hoc networks',
# 			'Um Estudo sobre a Personalização da Interação em Jogos Adaptáveis',
# 			'A study on customizing interaction in adaptable games'
# 			]

###############################################################################

#Qualis Referência Periódicos
A1p = 1
A2p = 0.875
A3p = 0.750
A4p = 0.600
B1p = 0.300
B2p = 0.200
B3p = 0.100
B4p = 0.050
Cp = 0

def nota_qualis(tipo, qualis):
	tipo = tipo.upper()
	if tipo == 'EVENTO':
		return 0
	
	elif tipo == 'PERIODICO':
		if qualis == 'A1':
			return A1p
		elif qualis == 'A2':
			return A2p
		elif qualis == 'A3':
			return A3p
		elif qualis == 'A4':
			return A4p
		elif qualis == 'B1':
			return B1p
		elif qualis == 'B2':
			return B2p
		elif qualis == 'B3':
			return B3p
		elif qualis == 'B4':
			return B4p
		elif qualis == 'C':
			return Cp
		else:
			return 0



#Qualis Referência Conferências
# A1c = 1
# A2c = 0.875
# A3c = 0.750
# A4c = 0.625
# B1c = 0.50
# B2c = 0.200
# B3c = 0.100
# B4c = 0.050
# Cc = 0

#1.000	0.875	0.750	0.625	0.500	0.200	0.100	0.050	0.000
