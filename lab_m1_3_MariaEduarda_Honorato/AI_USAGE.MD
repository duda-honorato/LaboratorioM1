# Declaração de Uso de IA

Eu, Maria Eduarda de Melo Honorato, declaro para os devidos fins que utilizei uma ferramenta de inteligência artificial (Deepseek) como auxílio durante o desenvolvimento do presente projeto, especificamente nos seguintes contextos:

## Revisao do arquivo REPORT (Prompt 1)

Estou implementando um sistema de processamento de imagens com filtros de convolução (média, Sobel, Laplaciano, identidade e tratamento de bordas via 'replicate' e 'ignore'), preciso que formalize em txt esse pontos:

Operações implementadas (descreva a função de convolução, os kernels disponíveis e as funções auxiliares de carregamento/salvamento);

Testes realizados (detalhe as imagens sintéticas geradas e o pipeline para a imagem real);

Resultados obtidos (comportamento esperado para cada filtro, como suavização, realce e detecção de bordas);

Análise técnica (abordando complexidade computacional, influência do tratamento de bordas, normalização das saídas e interpretação dos operadores);

Limitações do sistema (como ausência de suporte a cores, desempenho com laços ingênuos, restrição de formato .jpg e falta de métricas objetivas);

## Elaboração do arquivo README (Prompt 2)

Solicitei à IA que redigisse um esboço de README para o projeto, contendo descrição geral, instruções de uso e lista de dependências. A IA forneceu uma estrutura coerente, com ênfase nas bibliotecas NumPy e Pillow, incluindo a justificativa para a escolha de cada uma. O esboço gerado serviu como base para o documento final, que foi posteriormente ajustado e complementado por mim conforme as particularidades do trabalho.

## IndexError (Prompt 3)

Estou tendo um erro IndexError: index out of bounds na minha função de convolução quando o kernel é 5x5 e a imagem é pequena (64x64). Já verifiquei o pad_h e pad_w. Parece que quando chego perto do fim da linha, o i+kh estoura. Como faço para garantir que o loop pare exatamente no limite certo quando uso o modo 'replicate'? Mostra a condição exata do range que eu devo usar.

## Pasta Output (Prompt 4)
Vou gerar umas 15 imagens de saída (média3, média5, ponderada, laplaciano, realce, sobel gx, gy, mag, etc.). Me ajuda a criar um dicionário em Python que mapeia cada nome de arquivo com uma descrição técnica curta (ex: 'media3: suavização com perda de detalhes'). Além disso, quero gerar um arquivo REPORT.MD automaticamente com uma tabela markdown listando cada filtro, o tempo de execução dele e a estratégia de borda usada. Pode me dar esse script de automação?

## Filtro Laplaciano (Prompt 4)
Minha imagem de entrada é uint8 (0 a 255). Quando aplico o Laplaciano, os valores ficam negativos. Se eu salvar direto, o Python estoura ou corta. O requisito pede para 'registrar a resposta antes da conversão final'. Como eu faço para manter esses valores negativos vivos durante o cálculo e só converter na hora de salvar o JPG? Se eu normalizar para 0-255, vou perder a informação do sinal? Como lido com isso na hora do realce (img - laplaciano)

---

Todas as sugestões fornecidas pela IA foram criteriosamente analisadas, testadas e, quando pertinentes, adaptadas à minha própria compreensão do problema e às exigências do projeto. O uso da ferramenta limitou‑se a essas orientações, não substituindo minha responsabilidade sobre a concepção, implementação e validação final do sistema.

São José, 07/09/2026.