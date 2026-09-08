import numpy as np
from PIL import Image
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

PASTA_ENTRADA = os.path.join(PROJECT_ROOT, "imagens", "input")
PASTA_SAIDA   = os.path.join(PROJECT_ROOT, "imagens", "output")

def convolução(img, kernel, border_mode='replicate'):
    k_altura, k_largura = kernel.shape
    altura, largura = img.shape

    if k_altura % 2 != 1 or k_largura % 2 != 1:
        raise ValueError("Kernel deve ter dimensão ímpar")

    pixel_altura = k_altura // 2
    pixel_largura = k_largura // 2
    out = np.zeros_like(img)

    if border_mode == 'replicate':
        padded = np.pad(img, ((pixel_altura, pixel_altura),(pixel_largura, pixel_largura)), mode='edge')
        for i in range(altura):
            for j in range(largura):
                regiao = padded[i:i+k_altura, j:j+k_largura]
                out[i, j] = np.sum(regiao * kernel)

    elif border_mode == 'ignore':
        for i in range(altura):
            for j in range(largura):
                if (i < pixel_altura or i >= altura - pixel_altura or j < pixel_largura or j >= largura - pixel_largura):
                    out[i, j] = img[i, j]
                else:
                    regiao = img[i-pixel_altura:i+pixel_altura+1,j-pixel_largura:j+pixel_largura+1]
                    out[i, j] = np.sum(regiao * kernel)
    else:
        raise ValueError("border_mode deve ser 'replicate' ou 'ignore'")
    return out

def filtro_identidade():
    return np.array([[0, 0, 0],[0, 1, 0],[0, 0, 0]])

def filtro_media_3x3():
    return np.ones((3, 3)) / 9.0

def filtro_media_ponderada_3x3():  
    return np.array([[1, 2, 1],[2, 4, 2], [1, 2, 1]]) / 16.0

def filtro_media_5x5():
    return np.ones((5, 5)) / 25.0

def filtro_laplaciano():
    return np.array([[0,  1, 0],[1, -4, 1],[0,  1, 0]])

def filtro_sobel_gx():
    return np.array([[-1, 0, 1],[-2, 0, 2],[-1, 0, 1]])

def filtro_sobel_gy():
    return np.array([[-1, -2, -1],[ 0,  0,  0],[ 1,  2,  1]])

# Funcao_Generica
def salvar_imagem(arr, caminho, normalizar=True):
    if normalizar:
        arr = arr.astype(np.float64)
        min_val = arr.min()
        max_val = arr.max()
        if max_val > min_val:
            arr = (arr - min_val) / (max_val - min_val) * 255.0
        else:
            arr = np.zeros_like(arr)
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    Image.fromarray(arr, mode='L').save(caminho)


def carregar_imagem(caminho):
    with Image.open(caminho) as img:
        if img.mode != 'L':
            img = img.convert('L')
        return np.array(img, dtype=np.float64)


# Testes_Minimos - Gerar a imagem
def gerar_imagem_constante(tamanho=32, valor=128):
    return np.full((tamanho, tamanho), valor, dtype=np.float64)

def gerar_impulso(tamanho=32, centro=True):
    img = np.zeros((tamanho, tamanho), dtype=np.float64)
    if centro:
        img[tamanho//2, tamanho//2] = 255.0
    else:
        img[0, 0] = 255.0
    return img

def gerar_degrau_vertical(tamanho=64, pos=None):
    if pos is None:
        pos = tamanho // 2
    img = np.zeros((tamanho, tamanho), dtype=np.float64)
    img[:, pos:] = 255.0
    return img

def gerar_degrau_horizontal(tamanho=64, pos=None):
    if pos is None:
        pos = tamanho // 2
    img = np.zeros((tamanho, tamanho), dtype=np.float64)
    img[pos:, :] = 255.0
    return img

def gerar_formas_geometricas(tamanho=128):
    img = np.zeros((tamanho, tamanho), dtype=np.float64)
    img[20:60, 30:70] = 200.0  # retângulo
    for i in range(tamanho):
        for j in range(tamanho):
            if (i-90)**2 + (j-90)**2 < 20**2:
                img[i, j] = 100.0
    return img

def gerar_conteudo_tocando_bordas(tamanho=64):
    img = np.zeros((tamanho, tamanho), dtype=np.float64)
    img[0:20, :] = 200.0   # toca a borda superior
    img[:, 0:20] = 150.0   # toca a borda esquerda
    return img


def processar_imagem_real(caminho_entrada, pasta_saida):
    img = carregar_imagem(caminho_entrada)
    nome_base = os.path.splitext(os.path.basename(caminho_entrada))[0]

    id_kernel = filtro_identidade()
    img_id = convolução(img, id_kernel, 'replicate')
    salvar_imagem(img_id, os.path.join(pasta_saida, f'{nome_base}_identidade.jpg'), normalizar=False)

    media3 = filtro_media_3x3()
    media_pond = filtro_media_ponderada_3x3()
    media5 = filtro_media_5x5()

    img_med3 = convolução(img, media3, 'replicate')
    img_med_pond = convolução(img, media_pond, 'replicate')
    img_med5 = convolução(img, media5, 'replicate')

    salvar_imagem(img_med3, os.path.join(pasta_saida, f'{nome_base}_media3.jpg'), normalizar=False)
    salvar_imagem(img_med_pond, os.path.join(pasta_saida, f'{nome_base}_media_pond3.jpg'), normalizar=False)
    salvar_imagem(img_med5, os.path.join(pasta_saida, f'{nome_base}_media5.jpg'), normalizar=False)

    lap = filtro_laplaciano()
    img_lap = convolução(img, lap, 'replicate')
    img_sharp = img - img_lap

    salvar_imagem(img_lap, os.path.join(pasta_saida, f'{nome_base}_laplaciano.jpg'), normalizar=True)
    salvar_imagem(img_sharp, os.path.join(pasta_saida, f'{nome_base}_realcado.jpg'), normalizar=True)

    gx = filtro_sobel_gx()
    gy = filtro_sobel_gy()
    Gx = convolução(img, gx, 'replicate')
    Gy = convolução(img, gy, 'replicate')
    mag_aprox = np.abs(Gx) + np.abs(Gy)
    mag_eucl = np.sqrt(Gx**2 + Gy**2)

    salvar_imagem(Gx, os.path.join(pasta_saida, f'{nome_base}_sobel_gx.jpg'), normalizar=True)
    salvar_imagem(Gy, os.path.join(pasta_saida, f'{nome_base}_sobel_gy.jpg'), normalizar=True)
    salvar_imagem(mag_aprox, os.path.join(pasta_saida, f'{nome_base}_sobel_mag_aprox.jpg'), normalizar=True)
    salvar_imagem(mag_eucl, os.path.join(pasta_saida, f'{nome_base}_sobel_mag_eucl.jpg'), normalizar=True)

    img_med3_ignore = convolução(img, media3, 'ignore')
    img_med3_replicate = convolução(img, media3, 'replicate')
    salvar_imagem(img_med3_ignore, os.path.join(pasta_saida, f'{nome_base}_media3_ignore.jpg'), normalizar=False)
    salvar_imagem(img_med3_replicate, os.path.join(pasta_saida, f'{nome_base}_media3_replicate.jpg'), normalizar=False)

    print(f"Imagem real '{nome_base}' ok")


# Testes_Sinteticos
def executar_testes_sinteticos(pasta_saida):
    pasta_testes = os.path.join(pasta_saida, 'testes_sinteticos')
    os.makedirs(pasta_testes, exist_ok=True)

    const = gerar_imagem_constante(32, 128)
    const_med3 = convolução(const, filtro_media_3x3(), 'replicate')
    salvar_imagem(const, os.path.join(pasta_testes, 'const_original.jpg'), normalizar=False)
    salvar_imagem(const_med3, os.path.join(pasta_testes, 'const_media3.jpg'), normalizar=False)

    imp = gerar_impulso(32, centro=True)
    imp_lap = convolução(imp, filtro_laplaciano(), 'replicate')
    imp_id = convolução(imp, filtro_identidade(), 'replicate')
    salvar_imagem(imp, os.path.join(pasta_testes, 'impulso_original.jpg'), normalizar=False)
    salvar_imagem(imp_lap, os.path.join(pasta_testes, 'impulso_laplaciano.jpg'), normalizar=True)
    salvar_imagem(imp_id, os.path.join(pasta_testes, 'impulso_identidade.jpg'), normalizar=False)

    deg_h = gerar_degrau_horizontal(64)
    Gx = convolução(deg_h, filtro_sobel_gx(), 'replicate')
    Gy = convolução(deg_h, filtro_sobel_gy(), 'replicate')
    mag_eucl = np.sqrt(Gx**2 + Gy**2)
    salvar_imagem(deg_h, os.path.join(pasta_testes, 'degrau_h_original.jpg'), normalizar=False)
    salvar_imagem(Gx, os.path.join(pasta_testes, 'degrau_h_sobel_gx.jpg'), normalizar=True)
    salvar_imagem(Gy, os.path.join(pasta_testes, 'degrau_h_sobel_gy.jpg'), normalizar=True)
    salvar_imagem(mag_eucl, os.path.join(pasta_testes, 'degrau_h_sobel_mag_eucl.jpg'), normalizar=True)

    deg_v = gerar_degrau_vertical(64)
    Gx_v = convolução(deg_v, filtro_sobel_gx(), 'replicate')
    Gy_v = convolução(deg_v, filtro_sobel_gy(), 'replicate')
    mag_aprox = np.abs(Gx_v) + np.abs(Gy_v)
    salvar_imagem(deg_v, os.path.join(pasta_testes, 'degrau_v_original.jpg'), normalizar=False)
    salvar_imagem(mag_aprox, os.path.join(pasta_testes, 'degrau_v_sobel_mag_aprox.jpg'), normalizar=True)

    borda = gerar_conteudo_tocando_bordas(64)
    borda_rep = convolução(borda, filtro_media_3x3(), 'replicate')
    borda_ign = convolução(borda, filtro_media_3x3(), 'ignore')
    salvar_imagem(borda, os.path.join(pasta_testes, 'borda_original.jpg'), normalizar=False)
    salvar_imagem(borda_rep, os.path.join(pasta_testes, 'borda_media_replicate.jpg'), normalizar=False)
    salvar_imagem(borda_ign, os.path.join(pasta_testes, 'borda_media_ignore.jpg'), normalizar=False)

    formas = gerar_formas_geometricas(128)
    formas_med5 = convolução(formas, filtro_media_5x5(), 'replicate')
    formas_lap = convolução(formas, filtro_laplaciano(), 'replicate')
    formas_realc = formas - formas_lap
    salvar_imagem(formas, os.path.join(pasta_testes, 'formas_original.jpg'), normalizar=False)
    salvar_imagem(formas_med5, os.path.join(pasta_testes, 'formas_media5.jpg'), normalizar=False)
    salvar_imagem(formas_realc, os.path.join(pasta_testes, 'formas_realcado.jpg'), normalizar=True)

    const_pond = convolução(const, filtro_media_ponderada_3x3(), 'replicate')
    salvar_imagem(const_pond, os.path.join(pasta_testes, 'const_media_ponderada.jpg'), normalizar=False)

    print("Testes sintéticos ok")

if __name__ == '__main__':
    os.makedirs(PASTA_ENTRADA, exist_ok=True)
    os.makedirs(PASTA_SAIDA, exist_ok=True)

    arquivos = [f for f in os.listdir(PASTA_ENTRADA) if f.lower().endswith('.jpg')]
    if arquivos:
        caminho_entrada = os.path.join(PASTA_ENTRADA, arquivos[0])
        processar_imagem_real(caminho_entrada, PASTA_SAIDA)
    else:
        print("Nenhuma imagem .jpg encontrada na pasta de entrada")

    executar_testes_sinteticos(PASTA_SAIDA)

    print(f"\nTodos os resultados salvos em '{PASTA_SAIDA}'")