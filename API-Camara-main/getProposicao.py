#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning

warnings.simplefilter('ignore', InsecureRequestWarning)

def getFichaProposicao(idProposicao):
	urlDefault = "https://www.camara.leg.br/proposicoesWeb"
	query = "?idProposicao={}".format(idProposicao) # &ord=1&tp=completa
	headers = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13F69 Safari/601.1'}

	req = requests.get(urlDefault+query, headers=headers, verify=False)
	htmlSoup = BeautifulSoup(req.content, 'html.parser')
	
	return htmlSoup