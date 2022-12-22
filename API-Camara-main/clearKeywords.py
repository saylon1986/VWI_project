#!/usr/bin/env python3
import re
import numpy as np

def limpaLista(listaKeywords):
	novaListaKeywords = []
	for keyword in listaKeywords:
		regex = r"(.\s_|._|\.\s\-|\.\-)"
		keyword = re.split(regex, keyword)
		newKeyword = []
		for s in keyword:
			st = s.lower().strip()
			if st != "" and st[0] != ("_" or ".") and len(re.findall(regex, s.lower().strip()))==0:
				var = re.search(regex, st)
				if var != None:
					st = st[:var.start()]
				newKeyword.append(st)
		
		novaListaKeywords.extend(newKeyword)
	newList = []
	for keyword in novaListaKeywords:
		if keyword[-1] == "." or keyword[-1] == ",":
			keyword = keyword[:-1]
		newList.append(keyword)
	return np.unique(newList).tolist()