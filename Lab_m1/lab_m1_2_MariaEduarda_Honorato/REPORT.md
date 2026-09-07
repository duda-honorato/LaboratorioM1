## Objetivo
Implementar um pipeline de processamento básico de imagens para aplicar transformações pontuais (brilho, contraste, negativo, limiarização) e gerar histogramas, com o intuito de demonstrar o efeito dessas operações e servir como base para análises futuras.

## Operações Implementadas
- **Ajuste de brilho**: soma/subtração de um valor constante a todos os pixels (parâmetro `ref`).
- **Ajuste de contraste**: multiplicação da distância do pixel ao centro (128) por um fator (`ref`), seguida de re-centralização.
- **Negativo**: inversão dos níveis de cinza (`novo = 255 - original`).
- **Limiarização (thresholding)**: binarização com limiar `ref` (0 ou 255).
- **Cálculo de histograma**: contagem de frequência de cada intensidade (0–255) para imagens em tons de cinza.
- **Suporte a cores e tons de cinza**: as funções tratam ambos os modos, convertendo para `'L'` quando necessário (negativo e limiarização).

## Testes Realizados
- **Imagens de entrada**: `test1.jpg` e `test2.jpg` (localizadas em `imagens/input/`).
- **Operações executadas**:
  - Brilho: +50 e -50.
  - Contraste: fatores 0.5, 1.0 e 1.5.
  - Negativo.
  - Limiarização: limiares 127 e 180.
  - Histogramas: para a original, a imagem com brilho +50 e a com contraste 1.5.
- **Saída**: todas as imagens processadas e arquivos CSV de histogramas são salvos em `imagens/output/`.

## Resultados
- As imagens geradas refletem as alterações esperadas:
  - Brilho +50 torna a imagem mais clara; -50 mais escura.
  - Contraste 0.5 reduz o contraste; 1.5 aumenta.
  - Negativo produz a imagem invertida.
  - Limiarização segmenta a imagem em preto e branco conforme o limiar.
- Os histogramas mostram deslocamentos e redistribuições de intensidade coerentes com as operações.

## Análise Técnica
- **Implementação ingênua**: os loops aninhados percorrem pixel a pixel, o que é ineficiente para imagens grandes, mas didático e de fácil compreensão.
- **Uso de `numpy` e `PIL`**: conversão para array permite manipulação direta; o código trata canais RGB e escala de cinza separadamente.
- **Clamping**: os valores são limitados entre 0 e 255 para evitar estouro.
- **Automação**: a função `processar_imagem` gera todas as variações e histogramas para cada imagem listada.

## Limitações
- **Desempenho**: loops manuais tornam o processamento lento para imagens de alta resolução (ideal usar vetorização com NumPy).
- **Parâmetros fixos**: os valores de brilho, contraste e limiares são fixos no código; não há interface para o usuário ajustá-los.
- **Formato de saída**: sempre salva como JPG, o que pode introduzir compressão e perda de qualidade; ideal oferecer opção de PNG.
- **Tratamento de cores**: as operações de negativo e limiarização convertem a imagem para escala de cinza, perdendo informação cromática.
- **Dependência de diretórios**: o código assume a existência da pasta `imagens/input` e a criação de `imagens/output`; não lida com caminhos relativos ou absolutos de forma flexível.
- **Falta de validação**: não verifica se o arquivo de entrada é realmente uma imagem válida (exceções não tratadas).

## Perguntas 
1. Qual é a diferença observada entre alteração de brilho e alteração de contraste?**  
O brilho realiza um deslocamento aditivo (soma ou subtração) de um valor fixo a todos os pixels, tornando a imagem globalmente mais clara ou mais escura, sem alterar a dispersão relativa entre os tons.  
O contraste realiza uma multiplicação da distância de cada pixel em relação ao tom médio (128), esticando (fator > 1) ou comprimindo (fator < 1) a diferença entre os tons claros e escuros, alterando a percepção de nitidez e profundidade.
2. Em quais testes ocorreu saturação e qual foi seu efeito?**  
A saturação ocorre sempre que os cálculos ultrapassam os limites de 0 ou 255 e são forçados (`max`/`min`) a esses extremos. Especificamente:
- Brilho +50: pixels com valor original > 205 saturam em 255 (branco puro).
- Brilho -50: pixels com valor original < 50 saturam em 0 (preto puro).
- Contraste 1.5: pixels distantes do 128 (valores < 43 ou > 213) saturam, respectivamente, em 0 ou 255.  
Efeito: perda de detalhes nas áreas de alto-brilho ou baixa-luz (regiões tornam-se manchas uniformes sem gradação).
3. Como o histograma se deslocou após alterar o brilho?**  
O histograma sofreu uma translação horizontal (deslocamento para a direita no brilho +50, e para a esquerda no brilho -50). A forma geral da distribuição de frequências se manteve, mas as barras que ultrapassam os limites 0 ou 255 são cortadas (acumulam-se nos extremos), causando picos artificiais nos valores 0 ou 255.
4. **Como a distribuição das intensidades mudou ao alterar o contraste?**  
- Com fator 0.5 (redução): a distribuição se **comprimiu** em direção ao centro (128), concentrando a maioria dos pixels em uma faixa estreita de tons médios, reduzindo a variância.  
- Com fator 1.5 (aumento): a distribuição se **expandiu** em direção aos extremos (0 e 255), esticando as caudas. Isso resulta em um histograma com menos valores intermediários e possíveis picos nas bordas devido à saturação.
5. **Que informação é perdida após a limiarização?**  
Toda a informação de níveis de cinza intermediários (gradação tonal) é perdida. A imagem resultante possui apenas dois valores (0 e 255), descartando completamente sombreamento, texturas, meios-tons e profundidade. Resta apenas uma silhueta binária que distingue regiões claras de escuras com base no limiar definido.