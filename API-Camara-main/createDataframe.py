#!/usr/bin/env python3
import re
import pandas as pd
from bs4 import BeautifulSoup
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE

def createDataframeProposicao(idProposicao, htmlSoup):
	h3selector = htmlSoup.select('h3[class="inteiroTeor"]')
	h3Soup = BeautifulSoup(str(h3selector[0]), 'html.parser')
	nomeProposicao = h3Soup.select('span[class="nomeProposicao"]')[0].text.strip() 
	# print(nomeProposicao)
	tipoProposicao = h3Soup.select('span[class="tipoProposicao"]')[0].text.strip()
	# print(tipoProposicao)

	divselector = htmlSoup.select('div[id="subSecaoSituacaoOrigemAcessoria"] > p')[0]
	# print(divselector)
	spanSoupSituacao = BeautifulSoup(str(divselector), 'html.parser')
	situacaoSpan = spanSoupSituacao.select('span')#[0].text.strip()
	if len(situacaoSpan) == 0:
		situacaoSpan = spanSoupSituacao.select('a')
	# print(situacaoSpan)
	situacao = str(situacaoSpan[0].text).strip()
	# print(situacao)
	
	autorHtml = htmlSoup.select('div[id="identificacaoProposicao"] > div > div[class="row"] > div[class="col-md-9"] > p > a')#[0].text.strip()
	if len(autorHtml) == 0:
		autorHtml = htmlSoup.select('div[id="identificacaoProposicao"] > div > div[class="row"] > div[class="col-md-9"] > p > span')#[0].text.strip()
	autor = autorHtml[0].text.strip()
	# print(autor)
	apresentacao = htmlSoup.select('div[id="identificacaoProposicao"] > div > div[class="row"] > div[class="col-md-3"] > p')[0].text.strip().split("Apresentação")[1].strip()
	# print(apresentacao)
	dataframe = {'id': [idProposicao], 'nome da lei': [nomeProposicao],
				 'tipo de projeto': [tipoProposicao], 'situacao': [situacao],
				 'autor': [autor], 'apresentacao': [apresentacao]}
	paragraphs = htmlSoup.select('div[id="identificacaoProposicao"] > p')
	for p in paragraphs:
		pSoup = BeautifulSoup(str(p), 'html.parser')
		nomeCampo = pSoup.strong.text.strip()
		dadosCampo = pSoup.span.text.strip()
		nomeCampo = [nomeCampo[:-1] if nomeCampo[-1] == ":" else nomeCampo]
		dadosCampo = ILLEGAL_CHARACTERS_RE.sub(r'', str(dadosCampo))
		dataframe[str(nomeCampo[0])] = [dadosCampo]
		# print(str(nomeCampo[0]))
		# print(dadosCampo)
	
	indexacaoSoup = htmlSoup.select('div[id="identificacaoProposicao"] > div[class="naoVisivelNaImpressao"] > div[id="textoIndexacao"]')
	if indexacaoSoup != []:
		indexacaoSoup = indexacaoSoup[0].text.strip()
	else:
		indexacaoSoup = ""
	dataframe["indexacao"] = [indexacaoSoup]

	return pd.DataFrame(dataframe)

def createDataframeKeywords(keywords):
	dataframe = {'termos': keywords}
	df = pd.DataFrame(data=dataframe)
	df['selecionado'] = pd.Series(dtype=int)
	return df