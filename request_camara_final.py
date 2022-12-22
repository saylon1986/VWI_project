import requests
from bs4 import BeautifulSoup
import re
import pandas as pd





list_cg = ['https://www.camara.leg.br/deputados/204534/votacoes-nominais-plenario/','https://www.camara.leg.br/deputados/141488/votacoes-nominais-plenario/','https://www.camara.leg.br/deputados/204526/votacoes-nominais-plenario/','https://www.camara.leg.br/deputados/73788/votacoes-nominais-plenario/','https://www.camara.leg.br/deputados/178975/votacoes-nominais-plenario/']

anos = ["2019"]#,"2020","2021","2022"]

list_deput = ["Tabata Amaral","Paulo Teixeira","Orleans e Bragança","Ricardo Barros","Baleia Rossi"]

df_final =pd.DataFrame()



for ano in anos:
	for l in range(len(list_cg)):
		# j=0
		cg_lk_ano = str(list_cg[l])+str(ano)
		print(list_deput[l],ano)



		x = requests.get(cg_lk_ano)



		html_page = x.text

		soup = BeautifulSoup(html_page, 'html.parser')

		# print(soup.prettify())


		dados_lp= []
		dados_p = []
		for link in soup.find_all('td'):
			# print(link)
			# z = input("")
			if "<a" in str(link):	
				if len(dados_p) > 0:
					dados_lp.append(dados_p)
					dados_p = []
					# print(dados_lp)
					# z = input("")
				nome = re.findall("Sigla=(.+?)&",str(link))
				# print(nome)
				numero = re.findall("Numero=(.+?)&",str(link))
				# print(numero)
				link_text = link.text
				
				try:
					nome_f = nome[0].strip()+" "+numero[0].strip()
					# print(nome_f)
					nome_fl = nome[0].strip()+numero[0].strip()+link_text.strip()
					nome_fl = re.sub(" ","",nome_fl)
					dados_p.append(nome_f)
					dados_p.append(nome_fl)
				except:
					print(link)
					z = input("")
			else:
				# print(link.text)
				dados_p.append(link.text)


		deput = list_deput[l]
		nome_pl = []
		nome_ajust=[]
		voto = []
		for dt in dados_lp:
			nome_pl.append(dt[0])
			nome_ajust.append(dt[1])
			voto.append(dt[2])

		votacoes = pd.DataFrame(columns =["PLs"])
		votacoes["PLs"] = nome_pl
		votacoes["Nm_ajust"] = nome_ajust
		votacoes[deput] = voto

		# print(votacoes)
		if l == 0:
			df_final = votacoes

		else:	
			df_final = pd.merge(df_final,votacoes, how = "inner", on = ["Nm_ajust","PLs"])
			df_final.drop_duplicates(inplace = True)
		print(df_final)

		

df_final.to_excel("Votacoes_nominais.xlsx", index= False)



dict_dep ={}
ids = []
pos = []
for n in range(len(list_deput)):
	dict_dep[list_deput[n]] = n
	ids.append(n)
	pos.append("Political")




source =[]
target = []
for nm in list_deput:
	list_votos = df_final[nm].to_list()
	idx = list_deput.index(nm)
	if idx+1 != len(list_deput):
		for z in range(idx+1, len(list_deput)):
			list_votos_2 = df_final[list_deput[z]].to_list()
			for v1,v2 in zip(list_votos,list_votos_2):
				if v1 == v2 and str(v1) != "---" and str(v2) != "---":
					# print(v1,v2)
					# ç= input("")
					source.append(dict_dep[nm])
					target.append(dict_dep[list_deput[z]])
					





df_relacoes_ext = pd.read_excel("dados_redes.xlsx")

dfs = [df_relacoes_ext["Econômica"], df_relacoes_ext["Social"],df_relacoes_ext["Institucional"], df_relacoes_ext["Familiar"]]

rgx = re.compile("\[|\]")
for d in range(len(dfs)):
	for k in range(len(dfs[d])):
		# print(dfs[d])
		# print(type(dfs[d]))
		# z= input("")
		try:
			sb = dfs[d][k]
			sb = re.sub(rgx,"",sb)
			sb = sb.split(",")
			# print(sb)
			# print(type(sb))
			# z= input("")
			for nm in sb:
				try:
					a = dict_dep[nm.strip()]
				except:
					n = n+1
					dict_dep[nm.strip()] = n
					ids.append(n)
					list_deput.append(nm.strip())
					if d == 0:
						pos.append("Economic")
					elif d == 1:
						pos.append("Social")
					elif d == 2:
						pos.append("Institutional")
					elif d == 3:
						pos.append("Family")
		except:
			pass			

print(dict_dep)
z = input("")


for p in range(len(df_relacoes_ext["Parlamentar"])):
	pl = df_relacoes_ext.loc[p,"Parlamentar"]
	for d in range(len(dfs)):
		try:
			sb = dfs[d][p]
			sb = re.sub(rgx,"",sb)
			sb = sb.split(",")
			for nm in sb:
				source.append(dict_dep[pl])
				target.append(dict_dep[nm.strip()])
		except:
			pass		




lista_nos = pd.DataFrame()
lista_nos["Label"] = list_deput
lista_nos["Id"] = ids
lista_nos["tipo"] = pos


relacoes = pd.DataFrame()
relacoes["Source"] = source
relacoes["Target"] = target
relacoes["Type"] = "Directed"



lista_nos.to_csv("nos_parlamentares.csv", index= False)
relacoes.to_csv("relacoes_parlamentares.csv", index= False)