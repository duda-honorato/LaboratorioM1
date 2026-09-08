## objetivo
Implementar operações de vizinhança e convolução no domínio espacial, tratando explicitamente kernels, bordas, tipos numéricos e saturação

## operações implementadas
Sistema é composto pelos seguintes módulos:

1. **Convolução genérica** – função `convolução(img, kernel, border_mode)` que realiza a soma de produtos entre a imagem e o kernel, suportando dois modos de borda:
   - `replicate`: estende a imagem replicando os pixels das bordas.
   - `ignore`: mantém os pixels originais nas bordas (sem filtragem).

2. **Filtros disponíveis**:
   - Identidade (kernel delta).
   - Média 3×3 e 5×5 (suavização uniforme).
   - Média ponderada 3×3 (pesos Gaussiano simples).
   - Laplaciano 3×3 (detecção de bordas de segunda ordem).
   - Sobel horizontal (Gx) e vertical (Gy) (gradientes de primeira ordem).
   - Magnitude do gradiente (aproximada por |Gx|+|Gy| e euclidiana √(Gx²+Gy²)).

3. **Funções auxiliares**:
   - Carregamento e salvamento de imagens (formato `.jpg`, conversão para escala de cinza).
   - Geração de imagens sintéticas: constante, impulso, degraus horizontal/vertical, formas geométricas e conteúdo tocando bordas.

4. **Pipeline de execução**:
   - Processa a primeira imagem `.jpg` encontrada na pasta `imagens/input`.
   - Executa bateria de testes sintéticos, salvando todos os resultados em `imagens/output/testes_sinteticos`.

## testes
1. **Imagem_Constante (32×32)** – Média 3×3 e média ponderada 3×3.
2. **Imagem_Impulso Central** -  Laplaciano e identidade.
3. **Imagem_Degrau horizontal** -  Sobel Gx, Gy e magnitude euclidiana.   
4. **Imagem_Degrau Vertical** -  Sobel Gx, Gy e magnitude aproximada.
5. **Imagem_Formas Geométricas** -  Média 5×5 e realce (original − Laplaciano).   
5. **Imagem_Bordas tocadas** -  Média 3×3 com modos *replicate* e *ignore*.    

## Resultados Obtidos (Comportamento Esperado)
- **Filtro identidade**: reproduz a imagem original (diferença nula).
- **Médias**: suavizam a imagem, reduzindo ruído e borrando bordas. Quanto maior o kernel, maior o borramento.
- **Laplaciano**: realça variações abruptas de intensidade (bordas). As regiões homogêneas tornam-se escuras (próximas de zero).
- **Realce**: a subtração do Laplaciano enfatiza contornos e detalhes finos.
- **Sobel Gx**: destaca bordas verticais; **Gy** destaca bordas horizontais. A magnitude do gradiente fornece um mapa de bordas independente da orientação.
- **Tratamento de bordas**:
  - `replicate`: evita perda de informação nas bordas, mas pode introduzir artefatos.
  - `ignore`: mantém as bordas originais, mas pode criar descontinuidades visuais.

Nos testes sintéticos, os resultados confirmam a teoria:
- Impulso com Laplaciano produz uma cruz com valores positivos/negativos.
- Degrau horizontal com Sobel gera resposta forte em Gx e fraca em Gy.
- Formas geométricas com realce evidenciam contornos nítidos.

## Análise Técnica
### Tratamento de Bordas
A escolha do modo de borda afeta diretamente a qualidade do resultado:
- `replicate` é mais adequado para aplicações que exigem continuidade, como realce e detecção de bordas.
- `ignore` preserva a fidelidade nos pixels marginais, útil quando a região de interesse não inclui as bordas.

### Normalização
As imagens de saída de filtros como Laplaciano ou Sobel (que produzem valores negativos) são normalizadas para o intervalo [0,255] antes de salvar, garantindo visualização adequada. Já as imagens de média ou identidade são salvas sem normalização, mantendo a escala original.

### Interpretação dos Filtros
- **Média ponderada** (Gaussiana) suaviza com menor perda de contorno comparada à média uniforme.
- **Sobel** é um operador derivativo discreto, sensível a ruído, mas eficaz para detecção de bordas.
- O **realce** via Laplaciano amplifica ruído de alta frequência, sendo recomendado apenas para imagens com baixo ruído.

## limitações
1. **Escala de cinza**: o sistema não suporta imagens coloridas (RGB), convertendo-as automaticamente para tons de cinza.
2. **Formato de entrada**: apenas arquivos `.jpg` são processados.
3. **Desempenho**: a convolução não utiliza aceleração vetorial nem FFT, limitando a aplicação a imagens pequenas ou médias.
4. **Normalização forçada**: para filtros que geram valores fora do intervalo [0,255], a normalização pode comprimir o contraste de forma indesejada.
5. **Kernels fixos**: não há suporte a kernels personalizados ou ajuste de parâmetros (ex.: desvio padrão para Gaussiano).

## Perguntas 
1. **Qual é a diferença entre uma operação pontual e uma operação de vizinhança?**: Cada pixel da imagem de saída depende exclusivamente do valor do pixel correspondente na imagem de entrada.
2. **Por que kernels normalmente possuem dimensões ímpares**: Para garantir a existência de um pixel central exato.
3. **Qual é o efeito de aumentar o tamanho do kernel de média?**: Aumenta o efeito de suavização (borramento)..
4. **Como a estratégia de tratamento de bordas interfere no resultado?**: A estratégia de tratamento de bordas interfere diretamente nos pixels próximos aos limites da imagem, criando dois efeitos visuais e matemáticos completamente distintos: replicate e ignore.
5. **Por que a resposta bruta do Laplaciano pode conter valores negativos?**: Porque o Laplaciano calcula a segunda derivada (curvatura) da intensidade dos pixels, e a operação matemática do kernel [[0,1,0],[1,-4,1],[0,1,0]] resulta na subtração do valor do pixel central multiplicado por 4 da soma de seus vizinhos.
6. **Qual é a diferença entre `Gx` e `Gy` no Sobel?**: Gx (Sobel horizontal): Detecta bordas verticais (coluna x coluna), e Gy (Sobel vertical) detecta bordas horizontais (linha x linha).
7. **Que diferenças são observadas entre `|Gx| + |Gy|` e `sqrt(Gx² + Gy²)`?**: 
- |Gx| + |Gy|
Resultado: A imagem resultante tende a ter picos mais pronunciados e descontinuidades angulares.
- sqrt(Gx² + Gy²)
Resultado: A imagem tem transições mais suaves, com bordas diagonais exibindo a mesma intensidade que bordas horizontais/verticais, resultando em um mapa de bordas mais uniforme e contínuo.