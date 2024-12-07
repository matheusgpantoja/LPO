import glob
import os
import sys
import xml.etree.ElementTree as et
import zipfile

anos_validos = ["2021", "2022", "2023", "2024"]

def get_curriculos(caminho):
    cont = 0
    curriculos = []
    for f in glob.glob(caminho):
        curriculos.append(f)
        cont = cont+1 
        curriculos.sort()
    return curriculos

def unzip_file(path_to_zip_file, directory_to_extract_to):
    with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
        zip_ref.extractall(directory_to_extract_to)

def unzip_and_rename(path_to_zip_file, directory_to_extract_to):
    with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
        zip_ref.extractall(directory_to_extract_to)
    # Renomeia o arquivo XML extraído para 'curriculo.xml'
    for file in os.listdir(directory_to_extract_to):
        if file.endswith(".xml"):
            os.rename(os.path.join(directory_to_extract_to, file), os.path.join(directory_to_extract_to, "curriculo.xml"))
            break
        
def redirect_output(file_name):
    # Redireciona a saída para um arquivo de texto
    return open(file_name, 'a')  # 'a' para append (acrescentar)

i = 1
coord = ""

def read_lattes(path):
    # Lista e filtra somente os arquivos que tenham extensão .zip
    name_of_all_zip_files = [f for f in os.listdir(path) if f.endswith(".zip")]
    #print(name_of_all_zip_files)
    cont = 0
    dono_lattes = ""
    
    
    # Cria dois arquivos para armazenar as dissertações e teses separadamente
    with redirect_output('saidas/dissertacoes.txt') as f_dissertacoes, \
        redirect_output('saidas/teses.txt') as f_teses, \
        redirect_output('saidas/projetos.txt') as f_projetos, \
        redirect_output('saidas/patentes.txt') as f_patentes, \
        redirect_output('saidas/premios.txt') as f_premios, \
        redirect_output('saidas/projetos_financiados.txt') as f_projetos_financiados, \
        redirect_output('saidas/produtos.txt') as f_produtos, \
        redirect_output('saidas/softwares.txt') as f_softwares:
    
            
            
         
         for file in name_of_all_zip_files:
            #print(file)
            cont += 1
            file_path = path + '/curriculo.xml'
            #unzip_file(path + '/' + file, path)  # unzip file
            unzip_and_rename(path + '/' + file, path)  # descompacta e renomeia para curriculo.xml
            xml = et.parse(file_path).getroot()  # load file
            for t in xml.iter('DADOS-GERAIS'):
                #print("\n"+str(cont)+"#" + t.attrib['NOME-COMPLETO'])
                dono_lattes = t.attrib['NOME-COMPLETO']
    
            #dissertações de mestrado em andamento
            linha_dissertacao = ""
            trabalhos = []
            for t in xml.iter('ORIENTACAO-EM-ANDAMENTO-DE-MESTRADO'):
                for j in t.iter('DETALHAMENTO-DA-ORIENTACAO-EM-ANDAMENTO-DE-MESTRADO'):
                    linha_dissertacao = j.attrib['NOME-CURSO'] +"\t"+ j.attrib['NOME-DO-ORIENTANDO']
                for i in t.iter('DADOS-BASICOS-DA-ORIENTACAO-EM-ANDAMENTO-DE-MESTRADO'):
                    ano = i.attrib['ANO']
                    if ano in anos_validos:
                        linha_dissertacao = linha_dissertacao +"\t"+ i.attrib['NATUREZA'] +"\t"+ i.attrib['ANO'] +"\t"+ i.attrib['TITULO-DO-TRABALHO']
                #print(linha_dissertacao)
                        f_dissertacoes.write(linha_dissertacao + "\n")  # Escreve no arquivo .txt
              
            #os.remove(file_path)      
        
            # teses de doutorado em andamento
            linha_tese = ""
            for t in xml.iter('ORIENTACAO-EM-ANDAMENTO-DE-DOUTORADO'):
                for j in t.iter('DETALHAMENTO-DA-ORIENTACAO-EM-ANDAMENTO-DE-DOUTORADO'):
                    linha_tese = j.attrib['NOME-CURSO']+ "\t" + j.attrib['NOME-DO-ORIENTANDO']
                for i in t.iter('DADOS-BASICOS-DA-ORIENTACAO-EM-ANDAMENTO-DE-DOUTORADO'):
                    linha_tese = linha_tese + "\t" + i.attrib['NATUREZA'] + "\t" + i.attrib['ANO'] + "\t" + i.attrib['TITULO-DO-TRABALHO']
                    ano = i.attrib['ANO']
                    if ano in anos_validos:
                        linha_tese = linha_tese +"\t"+ i.attrib['NATUREZA'] +"\t"+ i.attrib['ANO'] +"\t"+ i.attrib['TITULO-DO-TRABALHO']
                #print(linha_dissertacao)
                        f_teses.write(linha_tese + "\n")  # Escreve no arquivo .txt
            
            #os.remove(file_path)  
                #print(linha_tese)
                  
            #projetos de pesquisa
            for t in xml.iter('PARTICIPACAO-EM-PROJETO'):
                # print(t)
                entra = False
                for v in t.iter():
                    if v.tag == 'PROJETO-DE-PESQUISA':
                        projeto = v.attrib['NOME-DO-PROJETO']
                        ano_inicio = v.attrib['ANO-INICIO']
                        ano_fim = v.attrib['ANO-FIM'] or "Atual"
                        natureza = v.attrib['NATUREZA']
            
            
                        if ano_fim == "Atual":
                            linha_projeto = f"{dono_lattes}\t{natureza}\t{projeto}\t{ano_inicio}\t{ano_fim}"
                            f_projetos.write(linha_projeto + "\n")  # Escreve no arquivo de projetos

                            #print(dono_lattes,"\t", natureza,"\t", projeto,"\t",ano_inicio,"\t",ano_fim)

            # # Patentes
            for t in xml.iter('PATENTE'):
                for j in t.iter('DADOS-BASICOS-DA-PATENTE'):
                    ano_desenvolvimento = j.attrib["ANO-DESENVOLVIMENTO"]
                    if ano_desenvolvimento in anos_validos:
                        titulo_patente = j.attrib["TITULO"]
                        linha_patente = f"{dono_lattes} ; {titulo_patente} ; {ano_desenvolvimento}"
                        f_patentes.write(linha_patente + "\n")  # Escreve no arquivo de patentes

           
        # Prêmios e Títulos
            for t in xml.iter('PREMIO-TITULO'):
                ano = t.attrib['ANO-DA-PREMIACAO']
                if ano in anos_validos:
                    nome_premio = t.attrib['NOME-DO-PREMIO-OU-TITULO']
                    entidade = t.attrib['NOME-DA-ENTIDADE-PROMOTORA']
                    linha_premio = f"{dono_lattes}\t{ano}\t{nome_premio}\t{entidade}"
                    f_premios.write(linha_premio + "\n")  # Escreve no arquivo de prêmios

            # Projetos de Pesquisa com Financiamento
            for t in xml.iter('PARTICIPACAO-EM-PROJETO'):
                projeto = ""
                financiamento = ""
                entra = False
                for v in t.iter():
                    if v.tag == 'PROJETO-DE-PESQUISA':
                        if not v.attrib['ANO-FIM'] or v.attrib['ANO-FIM'] in anos_validos:
                            projeto = f"{dono_lattes}\t{v.attrib['NOME-DO-PROJETO']}\t{v.attrib['ANO-INICIO']}\t{(v.attrib['ANO-FIM'] or 'Atual')}"
                            entra = True
                    if entra and v.tag == 'FINANCIADOR-DO-PROJETO':
                        financiamento = f"\t{v.attrib['NATUREZA']}\t{v.attrib['NOME-INSTITUICAO']}"
                if projeto and financiamento:
                    f_projetos_financiados.write(projeto + financiamento + "\n")

            # Produtos Tecnológicos
            for t in xml.iter('PRODUTO-TECNOLOGICO'):
                for j in t.iter('DADOS-BASICOS-DO-PRODUTO-TECNOLOGICO'):
                    ano = j.attrib["ANO"]
                    if ano in anos_validos:
                        titulo_produto = j.attrib['TITULO-DO-PRODUTO']
                        linha_produto = f"{dono_lattes}\tPRODUTO\t{ano}\t{titulo_produto}"
                        f_produtos.write(linha_produto + "\n")

            # Software
            for t in xml.iter('SOFTWARE'):
                for j in t.iter('DADOS-BASICOS-DO-SOFTWARE'):
                    ano = j.attrib["ANO"]
                    if ano in anos_validos:
                        titulo_software = j.attrib['TITULO-DO-SOFTWARE']
                        linha_software = f"{dono_lattes}\tSOFTWARE\t{ano}\t{titulo_software}"
                        f_softwares.write(linha_software + "\n")


            os.remove(file_path)  # remove unzip file

#file_path = 'projetosfinanciados.txt'
#sys.stdout = open(file_path, "w")

#read_lattes("LattesPPGCC")
path = os.path.join("curriculos", "todos")
read_lattes(path)