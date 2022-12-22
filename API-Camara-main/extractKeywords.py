#!/usr/bin/env python3
import re
import requests
import json
import numpy as np
import pandas as pd
from urllib.parse import parse_qs
from getIds import getAllIds
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning


warnings.simplefilter('ignore', InsecureRequestWarning)

def getKeywords(idProposicao):
	req = requests.get("https://dadosabertos.camara.leg.br/api/v2/proposicoes/"+str(idProposicao))
	responseJson = json.loads(req.content)
	if responseJson['dados']['keywords'] is not None:
		return responseJson['dados']['keywords'].split(', ')
	else: return []

def getAllKeywords(anoInicial, anoFinal, keywordInicial=""):
	list_ids = getAllIds(anoInicial, anoFinal, keywordInicial)

	keywords = []
	for idx in list_ids:
		keywords.extend(getKeywords(idx))

	return keywords

if __name__ == "__main__":
	ids = getIDsApiv2(2005, 2020, "lei de falências")
	print(obtemKeywords(ids[0]))