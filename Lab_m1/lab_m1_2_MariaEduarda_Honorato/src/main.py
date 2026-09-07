from PIL import Image
import numpy as np
import os

DIR_ATUAL = os.path.dirname(os.path.abspath(__file__))
RAIZ_PROJETO = os.path.dirname(DIR_ATUAL)

PASTA_ENTRADA = os.path.join(RAIZ_PROJETO, "imagens", "input")
PASTA_SAIDA = os.path.join(RAIZ_PROJETO, "imagens", "output")

# xe = caminho de entrada
# xs = caminho de saida
# ref = parametro

def ajustar_brilho(xe, ref, xs):
    img = Image.open(xe)
    img_array = np.array(img).astype(np.int16)

    if len(img_array.shape) == 3:
        altura, largura, canais = img_array.shape
        nova_img = Image.new('RGB', (largura, altura))
        nova_pixels = nova_img.load()

        for y in range(altura):
            for x in range(largura):
                r, g, b_val = img_array[y, x]

                novo_r = r + ref
                novo_g = g + ref
                novo_b = b_val + ref

                novo_r = max(0, min(255, int(novo_r)))
                novo_g = max(0, min(255, int(novo_g)))
                novo_b = max(0, min(255, int(novo_b)))

                nova_pixels[x, y] = (novo_r, novo_g, novo_b)
    else:
        altura, largura = img_array.shape
        nova_img = Image.new('L', (largura, altura))
        nova_pixels = nova_img.load()

        for y in range(altura):
            for x in range(largura):
                valor = img_array[y, x]
                novo_valor = valor + ref
                novo_valor = max(0, min(255, int(novo_valor)))
                nova_pixels[x, y] = novo_valor

    nova_img.save(xs)

def ajustar_contraste(xe, ref, xs):
    img = Image.open(xe)
    img_array = np.array(img).astype(np.int16)

    if len(img_array.shape) == 3:
        altura, largura, canais = img_array.shape
        nova_img = Image.new('RGB', (largura, altura))
        nova_pixels = nova_img.load()

        for y in range(altura):
            for x in range(largura):
                r, g, b_val = img_array[y, x]

                novo_r = ref * (r - 128) + 128
                novo_g = ref * (g - 128) + 128
                novo_b = ref * (b_val - 128) + 128

                novo_r = max(0, min(255, int(novo_r)))
                novo_g = max(0, min(255, int(novo_g)))
                novo_b = max(0, min(255, int(novo_b)))

                nova_pixels[x, y] = (novo_r, novo_g, novo_b)
    else:
        altura, largura = img_array.shape
        nova_img = Image.new('L', (largura, altura))
        nova_pixels = nova_img.load()

        for y in range(altura):
            for x in range(largura):
                valor = img_array[y, x]
                novo_valor = ref * (valor - 128) + 128
                novo_valor = max(0, min(255, int(novo_valor)))
                nova_pixels[x, y] = novo_valor

    nova_img.save(xs)

def negativo(xe, xs):
    img = Image.open(xe)
    if img.mode != 'L':
        img = img.convert('L')

    img_array = np.array(img)
    altura, largura = img_array.shape

    nova_img = Image.new('L', (largura, altura))
    nova_pixels = nova_img.load()

    for y in range(altura):
        for x in range(largura):
            valor = img_array[y, x]
            novo_valor = 255 - valor
            nova_pixels[x, y] = int(novo_valor)

    nova_img.save(xs)

def limiarizacao(xe, ref, xs):
    img = Image.open(xe)
    if img.mode != 'L':
        img = img.convert('L')

    img_array = np.array(img)
    altura, largura = img_array.shape

    nova_img = Image.new('L', (largura, altura))
    nova_pixels = nova_img.load()

    for y in range(altura):
        for x in range(largura):
            valor = img_array[y, x]
            if valor < ref:
                novo_valor = 0
            else:
                novo_valor = 255
            nova_pixels[x, y] = novo_valor

    nova_img.save(xs)

def calcular_histograma(xe, saida_csv):
    img = Image.open(xe).convert('L')
    img_array = np.array(img)
    altura, largura = img_array.shape

    histograma = [0] * 256

    for y in range(altura):
        for x in range(largura):
            intensidade = img_array[y, x]
            histograma[intensidade] += 1

    with open(saida_csv, 'w') as f:
        f.write("intensidade,quantidade\n")
        for i, qtd in enumerate(histograma):
            f.write(f"{i},{qtd}\n")

def processar_imagem(xe):
    base = os.path.splitext(os.path.basename(xe))[0]

    # brilho
    ajustar_brilho(xe, 50, os.path.join(PASTA_SAIDA, f'{base}_1_mais50.jpg'))
    ajustar_brilho(xe, -50, os.path.join(PASTA_SAIDA, f'{base}_1_menos50.jpg'))

    # contraste
    ajustar_contraste(xe, 0.5, os.path.join(PASTA_SAIDA, f'{base}_2_0.5.jpg'))
    ajustar_contraste(xe, 1.0, os.path.join(PASTA_SAIDA, f'{base}_2_1.0.jpg'))
    ajustar_contraste(xe, 1.5, os.path.join(PASTA_SAIDA, f'{base}_2_1.5.jpg'))

    # negativa
    negativo(xe, os.path.join(PASTA_SAIDA, f'{base}_3.jpg'))

    # limiarização
    limiarizacao(xe, 127, os.path.join(PASTA_SAIDA, f'{base}_4_127.jpg'))
    limiarizacao(xe, 180, os.path.join(PASTA_SAIDA, f'{base}_4_180.jpg'))

    # histogramas (originais e das imagens modificadas)
    calcular_histograma(xe, os.path.join(PASTA_SAIDA, f'hist_{base}_original.csv'))
    calcular_histograma(os.path.join(PASTA_SAIDA, f'{base}_1_mais50.jpg'),
                        os.path.join(PASTA_SAIDA, f'hist_{base}_mais50.csv'))
    calcular_histograma(os.path.join(PASTA_SAIDA, f'{base}_2_1.5.jpg'),
                        os.path.join(PASTA_SAIDA, f'hist_{base}_contraste1.5.csv'))

def main():
    os.makedirs(PASTA_SAIDA, exist_ok=True)

    if not os.path.exists(PASTA_ENTRADA):
        print(f"Erro: Pasta '{PASTA_ENTRADA}' não encontrada!")
        return

    # Lista fixa com os nomes das imagens que você quer processar
    imagens = ['test1.jpg', 'test2.jpg']

    for imagem in imagens:
        caminho_completo = os.path.join(PASTA_ENTRADA, imagem)
        if not os.path.exists(caminho_completo):
            print(f"Arquivo '{caminho_completo}' não encontrado! Pulando...")
            continue
        processar_imagem(caminho_completo)

    print("Concluído!")

if __name__ == "__main__":
    main()