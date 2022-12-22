# API-Camara

## Configuração do ambiente
Execute para instalar todas as bibliotecas necessária:
Ambiente Linux/OSX:
```
pip3 install -r requirements.txt
```
Ambiente Windows:
```
python3 -m pip3 install -r requirements.txt
```

## Modo de uso
No projeto existe dois parâmetros a serem passados
```
usage: main.py [-h] [--extract-keywords] [--extract-proposicoes]
options:
  -h, --help            show this help message and exit
  --extract-keywords    Extrai todas as keywords
  --extract-proposicoes
                        Extrai todas as proposições
```
Para extrair todas as keywords, utiliza-se --extract-keywords
```
$ python3 main.py --extract-keywords
Digite a palavra-chave de partida: <keyword inicial>
Digite o ano de início: <ano de início>
Digite o ano final: <ano final>
Arquivo gerado com sucesso: files/output_aaaa_MM_dd-HH_mm_ss_a.xlsx
```
Ao gerar o arquivo, o programa irá gerar o nome dele composto por "output_" + horário atual, esse horário segue o formato ```aaaa_MM_dd-HH_mm_ss_a``` (vide: https://www.ibm.com/docs/pt-br/tap/3.5.3?topic=time-custom-date-formats)

Para extrair todas as proposições, utiliza-se --extract-proposicoes
```
python3 main.py --extract-proposicoes
Ler um arquivo excel? [SIM/ NÃO] não
Digite a palavra-chave de partida: <keyword inicial>
Digite o ano de início: <ano de início>
Digite o ano final: <ano final>
Arquivo gerado com sucesso: files/output_aaaa_MM_dd-HH_mm_ss_a.xlsx
Dê enter após ter selecionado os termos... 
```
Ao responder NÃO, será gerado um arquivo com todas as keywords (igual ao processo anterior de extrair as keywords) e logo depois o programa ficará pausado esperando a avaliação das keywords. Essa avaliacação deverá ser feita no próprio arquivo gerado e as modificações devem ser salvas nele também. A tal verificação funciona da seguinte forma: digite ```sim``` na coluna de nome ```selecionado``` ao escolher um termo. Após feita a avaliação, volte ao programa e pressione enter.
Por fim, o programa extrairá todas as proposições com os termos selecionados:
```
$ python3 main.py --extract-proposicoes
Ler um arquivo excel? [SIM/ NÃO] não
Digite a palavra-chave de partida: lei de falências
Digite o ano de início: 2005
Digite o ano final: 2006
Arquivo gerado com sucesso: files/output_aaaa_MM_dd-HH_mm_ss_a.xlsx
Dê enter após ter selecionado os termos... 
Arquivo gerado com sucesso: files/output_aaaa_MM_dd-HH_mm_ss_a.xlsx
```
Pode-se notar que, após a escolha dos termos, o programa voltou a execução normal e extraiu todas informações de todas as proposições relacionadas aos termos. No final, salvou todas essas informações em um novo arquivo Excel.

E, no caso em que a resposta é SIM, tem-se:
```
$ python3 main.py --extract-proposicoes
Ler um arquivo excel? [SIM/ NÃO] sim
Digite o nome do arquivo excel: <arquivo_excel.xlsx>
Digite o ano de início: <ano de início>
Digite o ano final: <ano final>
```
Nesse modo, o programa irá ler um arquivo Excel. Nesse caso, é necessário que o arquivo Excel esteja no seguinte formato: uma coluna de nome ```termos```, que contenha os termos, e uma coluna de nome ```selecionado```, que contenha ```sim``` para os termos selecionados. O programa irá pegar todas os termos marcados com a palavra ```sim``` e extrairá as informações das proposições.
E, por fim, o programa vai gerar um arquivo com todas as proposições:
```
$ python3 main.py --extract-proposicoes
Ler um arquivo excel? [SIM/ NÃO] sim
Digite o nome do arquivo excel: <arquivo_excel.xlsx>
Digite o ano de início: <ano de início>
Digite o ano final: <ano final>
Arquivo gerado com sucesso: files/output_aaaa_MM_dd-HH_mm_ss_a.xlsx
```

### Informações sobre o código
O programa utiliza as duas versões da API da Câmara:
* v1 - versão 1, encontrada em: ```https://www.camara.leg.br/api/v1/```
* v2 - versão 2, encontrada em: ```https://dadosabertos.camara.leg.br/api/v2/```

Observação: utiliza-se as duas versões, porque aparentemente a versão 2, apesar de ser mais simples de usar, não está totalmente completa.

E para a extração completa das proposições, utiliza-se o próprio site da Câmara:
```https://www.camara.leg.br/proposicoesWeb/fichadetramitacao?idProposicao=<id da Proposição>```
