import LZW_Fixo
import argparse
import time

def contar_caracteres(arquivo):
    with open(arquivo, 'r') as file:
        conteudo = file.read()
    return len(conteudo)

def calcular_taxa_compressao(tam_original, tam_comprimido):
    tam_comprimido = -(-tam_comprimido // 8)
    taxa_compressao = round(100-100*tam_comprimido/tam_original, 2)
    return taxa_compressao

def main():
    #Analisando os argumentos passados
    parser = argparse.ArgumentParser()
    parser.add_argument('arquivo_entrada', type=str)
    parser.add_argument('arquivo_comprimido', type=str)
    parser.add_argument('arquivo_descomprimido', type=str)
    parser.add_argument('--tam_dic', type=int, default=12)
    parser.add_argument('--stat', action='store_true')
    
    args = parser.parse_args()

    #Lendo o arquivo de entrada como bytes
    with open(args.arquivo_entrada, 'rb') as file:
        dados_entrada = file.read()
    tam_entrada = len(dados_entrada)

    #Comprimindo os dados
    tempo_inicial_compressao = time.time()
    codigos_compressao = LZW_Fixo.lzw_compressor(dados_entrada, args.tam_dic)
    tempo_final_compressao = time.time()
    
    #Convertendo os códigos de compressão para binário e concatenando tudo em uma única string binária
    string_bin_comp = LZW_Fixo.converter_para_string_binaria(codigos_compressao, args.tam_dic)
    
    #Convertendo a string binária para bytes e salvando em um arquivo
    LZW_Fixo.salvar_bits_em_arquivo(args.arquivo_comprimido, string_bin_comp)
    
    #Transformando os bytes do arquivo comprimido em uma string binária
    string_bin_descomp = LZW_Fixo.ler_bytes_de_arquivo(args.arquivo_comprimido)

    #Convertendo a string binária de volta para códigos de compressão
    codigos_descompressao = LZW_Fixo.converter_string_binaria_para_codigos(string_bin_descomp, args.tam_dic)
    
    #Descomprimindo os códigos de compressão
    tempo_inicial_descompressao = time.time()
    arquivo_descomprimido = LZW_Fixo.lzw_descompressor(codigos_descompressao, args.tam_dic)
    tempo_final_descompressao = time.time()
    
    # Salvando o arquivo descomprimido como uma imagem bitmap
    with open(args.arquivo_descomprimido, 'wb') as file:
        file.write(arquivo_descomprimido)

    #Calculando a taxa de compressão
    taxa_compressao = calcular_taxa_compressao(tam_entrada, len(string_bin_comp))
    print(f'Taxa de compressão = {taxa_compressao}%')
    print(f'Tempo de compressão = {1000*(tempo_final_compressao - tempo_inicial_compressao):.2f} ms')
    print(f'Tempo de descompressão = {1000*(tempo_final_descompressao - tempo_inicial_descompressao):.2f} ms')


    
if __name__ == "__main__":
    tempo_inicial = time.time()
    main()
    tempo_final = time.time()
    print(f'Tempo total de execução = {1000*(tempo_final - tempo_inicial):.2f} ms')
