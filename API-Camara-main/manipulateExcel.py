#!/usr/bin/env python3
import pandas as pd
from datetime import datetime
import xlsxwriter

def createExcel(dataframe):
	df = pd.DataFrame(dataframe)
	# print(df)
	date_hour = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
	writer = pd.ExcelWriter('files/output_{}.xlsx'.format(date_hour), engine='xlsxwriter')
	df.to_excel(writer, index=False)
	writer.save()
	print("Arquivo gerado com sucesso: files/output_{}.xlsx".format(date_hour))
	return "output_{}.xlsx".format(date_hour)

def extractFromExcel(excelName):
	df = pd.read_excel('files/'+excelName)
	# sim_upper = "Sim"
	# sim_lower = "sim"
	termos = []
	if 'selecionado' in df.columns:
		df = df.query("selecionado == 'Sim' or selecionado == 'sim' or selecionado == 1")['termos']
		# df_lower = df.query("selecionado == @sim_lower")['termos']
		termos.extend(list(df.iloc))
	else:
		termos.extend(list(df['termos']))
	# termos.extend(list(df_lower.iloc))
	return termos

# def dataframeToExcel(dataframe):
# 	# dataframe = {'termos': keywords}
# 	# df = pd.DataFrame(data=dataframe)
# 	date_hour = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
# 	dataframe.to_excel("files/output_termos_{}.xlsx".format(date_hour), index=False)
# 	print("Arquivo gerado com sucesso: files/output_termos_{}.xlsx".format(date_hour))
# 	return

if __name__ == "__main__":
	print(extractFromExcel("output_new_termos_com_aspas_revisado.xlsx"))