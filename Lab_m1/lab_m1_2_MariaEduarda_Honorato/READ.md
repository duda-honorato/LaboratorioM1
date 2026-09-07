# Laboratório de Processamento de Imagens – Operações Básicas

Este projeto implementa um conjunto de operações fundamentais de processamento de imagens digitais, utilizando a linguagem Python e as bibliotecas Pillow e NumPy. O programa lê imagens de entrada, aplica transformações (brilho, contraste, negativo, limiarização) e gera histogramas das imagens originais e modificadas.

## Funcionalidades implementadas

- **Ajuste de brilho**: adição ou subtração de um valor constante a todos os pixels.
- **Ajuste de contraste**: multiplicação da diferença de cada pixel em relação ao valor médio (128) por um fator.
- **Negativo**: inversão dos níveis de cinza (255 – valor original).
- **Limiarização**: binarização da imagem com base em um valor de corte (threshold).
- **Cálculo de histograma**: geração de arquivo CSV com a distribuição de intensidades (0 a 255).

## Linguagem utilizada

- **Python 3.8+**

## Dependências

As seguintes bibliotecas são necessárias:

- [Pillow](https://python-pillow.org/) – para manipulação de imagens.
- [NumPy](https://numpy.org/) – para operações matriciais eficientes.

## Instalacao de dependências

- pip install pillow numpy

## Exemplos de comando

- **Executar o processamento padrão:**: python src.py
- **Alterar as imagens de entrada**: edite a lista imagens dentro da função main() no arquivo .py: imagens = ['foto1.png', 'foto2.png', 'minha_imagem.jpg']
- **Modificar parâmetros de brilho/contraste:**: ajuste os valores passados nas chamadas das funções dentro de processar_imagem()

## Estrutura do código

- **ajustar_brilho(xe, ref, xs)**: aplica brilho (ref pode ser positivo ou negativo)
- **ajustar_contraste(xe, ref, xs)**: aplica contraste (ref é o fator multiplicador)
- **negativo(xe, xs)**: gera o negativo da imagem
- **limiarizacao(xe, ref, xs)**: binariza com o limiar ref
- **calcular_histograma(xe, saida_csv)**: gera histograma em CSV
- **processar_imagem(xe)**: orquestra todas as operações para uma imagem de entrada
- **main**: cria pastas, verifica arquivos e processa a lista de imagens

## Resultados esperados

Para cada imagem de entrada, serão gerados:
- 2 variações de brilho
- 3 variações de contraste
- 1 negativo
- 2 versões limiarizadas
- 3 arquivos de histograma (original, com brilho +50 e com contraste 1.5)
Todos os arquivos são salvos na pasta imagens/output/