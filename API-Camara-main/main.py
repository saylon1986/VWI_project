#!/usr/bin/env python3
import argparse
import os
import numpy as np
import pandas as pd
from extractKeywords import getAllKeywords
from getIds import getAllIds
from getProposicao import getFichaProposicao
from createDataframe import createDataframeProposicao, createDataframeKeywords
from manipulateExcel import createExcel, extractFromExcel
from clearKeywords import limpaLista

parser = argparse.ArgumentParser()
# parser.add_argument("--keyword", help="Keyword de partida", required="True")
parser.add_argument("--extract-keywords", help="Extrai todas as keywords", action="store_true")
parser.add_argument("--extract-proposicoes", help="Extrai todas as proposições", action="store_true")
args = parser.parse_args()

if args.extract_keywords:
	keyword = input("Digite a palavra-chave de partida: ")
	anoInicial = input("Digite o ano de início: ")
	anoFinal = input("Digite o ano final: ")
	allKeywords = getAllKeywords(int(anoInicial), int(anoFinal), keyword)
	keywordsCleaned = limpaLista(limpaLista(allKeywords))
	dataframe = createDataframeKeywords(keywordsCleaned)
	createExcel(dataframe)
elif args.extract_proposicoes:
	resposta = input("Ler um arquivo excel? [SIM/ NÃO] ")
	if resposta.upper() == "SIM":
		filename = input("Digite o nome do arquivo excel: ")
		if os.path.isfile('files/'+filename) is False:
			print("O arquivo excel não existe.")
			exit()
		keywordsSelected = extractFromExcel(filename)
		keywordsCleaned = limpaLista(limpaLista(keywordsSelected))
		anoInicial = input("Digite o ano de início: ")
		anoFinal = input("Digite o ano final: ")
		allIds = []
		for keyword in keywordsCleaned:
			allIds.extend(getAllIds(int(anoInicial), int(anoFinal), keyword))
		allIds = np.unique(allIds).tolist()
		allDf = pd.DataFrame({})
		for idx in allIds:
			texts = getFichaProposicao(idx)
			df = createDataframeProposicao(idx, texts)
			allDf = pd.concat([allDf, df])
		createExcel(allDf)
	else:
		keyword = input("Digite a palavra-chave de partida: ")
		anoInicial = input("Digite o ano de início: ")
		anoFinal = input("Digite o ano final: ")
		allKeywords = getAllKeywords(int(anoInicial), int(anoFinal), keyword)
		keywordsCleaned = limpaLista(limpaLista(allKeywords))
		dataframe = createDataframeKeywords(keywordsCleaned)
		filename = createExcel(dataframe)
		input("Dê enter após ter selecionado os termos... ")
		keywordsSelected = extractFromExcel(filename)
		keywordsCleaned = limpaLista(limpaLista(keywordsSelected))
		allIds = []
		for keyword in keywordsCleaned:
			allIds.extend(getAllIds(int(anoInicial), int(anoFinal), keyword))
		allIds = np.unique(allIds).tolist()
		allDf = pd.DataFrame({})
		for idx in allIds:
			texts = getFichaProposicao(idx)
			df = createDataframeProposicao(idx, texts)
			allDf = pd.concat([allDf, df])
		createExcel(allDf)