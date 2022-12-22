#!/usr/bin/env python3
import re
import requests
import json
import numpy as np
from urllib.parse import parse_qs
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning

warnings.simplefilter('ignore', InsecureRequestWarning)

def getIDsApiv1(anoInicial=2005, anoFinal=2020, keyword=""):
	urlDefault = "https://www.camara.leg.br/api/v1"
	proposicaoEndpoint = "/busca/proposicoes/_search"
	ids = []
	for ano in range(anoInicial, anoFinal+1):
		dictQuery = {"order": "relevancia", "pagina": 1, "ano": ano, "q": "\"{}\"".format(keyword)}
		query = json.dumps(dictQuery)
		headers = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13F69 Safari/601.1',
				   'Accept': 'application/json',
				   'Content-Type': 'application/json'}

		req = requests.post(urlDefault+proposicaoEndpoint, data=query, headers=headers)
		responseJson = json.loads(req.content)

		totProposicoes = responseJson['hits']['total'] 
		for proposicao in responseJson['hits']['hits']:
			ids.append(proposicao['_id'])

		pagina = 2
		while len(ids) < totProposicoes:
			dictQuery = {"order": "relevancia", "pagina": pagina, "q": "\"{}\"".format(keyword)}
			query = json.dumps(dictQuery)
			req = requests.post(urlDefault+proposicaoEndpoint, data=query, headers=headers)
			responseJson = json.loads(req.content)
			for proposicao in responseJson['hits']['hits']:
				ids.append(proposicao['_id'])
			pagina += 1

	return ids

def getIDsApiv2(anoInicial=2005, anoFinal=2020, keywordInicial=""):
	try:
		urlDefault = "https://dadosabertos.camara.leg.br/api/v2"
		proposicaoEndpoint = "/proposicoes"
		query = "?keywords={}&dataApresentacaoInicio={}-01-01&dataApresentacaoFim={}-12-31&ordem=ASC&ordenarPor=id&itens=100".format(keywordInicial, anoInicial, anoFinal)
		headers = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13F69 Safari/601.1',
				   'Accept': 'application/json'}

		req = requests.get(urlDefault+proposicaoEndpoint+query, headers=headers, verify=False)
		responseJson = json.loads(req.content)

		if len(responseJson['links']) > 1 and responseJson['links'][-2]['href'] != responseJson['links'][-1]['href']:
			lastPage = parse_qs(responseJson['links'][-1]['href'])['pagina'][0]
			for numPagina in range(2, int(lastPage)+1):
				query = "?keywords={}&dataApresentacaoInicio=2005-01-01&ordem=ASC&ordenarPor=id&pagina={}&itens=100".format(keywordInicial, numPagina)
				req = requests.get(urlDefault+proposicaoEndpoint+query, headers=headers, verify=False)
				auxJson = json.loads(req.content)
				if auxJson['dados'] == []: break
				responseJson['dados'].extend(auxJson['dados'])

		ids = [idx['id'] for idx in responseJson['dados']]
		return ids
	except:
		print(responseJson)

def getAllIds(anoInicial, anoFinal, keywordInicial):
	ids_api_v1 = getIDsApiv1(anoInicial, anoFinal, keywordInicial)
	ids_api_v2 = getIDsApiv2(anoInicial, anoFinal, keywordInicial)

	list_ids = np.unique(ids_api_v1+ids_api_v2).tolist()
	return list_ids