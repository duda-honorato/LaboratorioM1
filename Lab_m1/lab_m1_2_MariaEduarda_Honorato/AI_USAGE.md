# Declaração de Uso de IA

Eu, Maria Eduarda de Melo Honorato, declaro para os devidos fins que utilizei uma ferramenta de inteligência artificial (Deepseek) como auxílio durante o desenvolvimento do presente projeto, especificamente nos seguintes contextos:

## Diagnóstico e correção de erro de overflow (Prompt 1)

Durante a implementação da função de ajuste de brilho, deparei‑me com o erro `OverflowError: Python integer -50 out of bounds for uint8`. Submeti à IA a mensagem de exceção e o trecho de código relevante. A IA identificou que o problema decorria da tentativa de realizar operações aritméticas diretamente sobre arrays do tipo `np.uint8`, que não suportam valores negativos. A solução proposta – converter a imagem para um tipo com sinal (`np.int16`) antes das operações, aplicar o ajuste e depois limitar o resultado ao intervalo [0, 255] – foi adotada e integrada ao código final, resolvendo o erro de forma eficaz.

## Elaboração do arquivo README (Prompt 2)

Solicitei à IA que redigisse um esboço de README para o projeto, contendo descrição geral, instruções de uso e lista de dependências. A IA forneceu uma estrutura coerente, com ênfase nas bibliotecas NumPy e Pillow (substituto do PIL), incluindo a justificativa para a escolha de cada uma. O esboço gerado serviu como base para o documento final, que foi posteriormente ajustado e complementado por mim conforme as particularidades do trabalho.

## Caminho de saída (Prompt 3)

Eu iniciei o projeto de processamento de imagens, todos os arquivos gerados (imagens e CSVs) eram salvos em `resultados/` com caminhos fixos. Mas como o projeto solicita que tudo esteja em `report`, decidi mover a pasta para `report/resultados`. Questionei a IA sobre o impacto dessa mudança.  
A solução dada e adotada foi parametrizar o diretório de saída com uma constante e usar `os.path.join` para garantir portabilidade. O código foi reescrito com essas alterações, mantendo a lógica intacta.

---

Todas as sugestões fornecidas pela IA foram criteriosamente analisadas, testadas e, quando pertinentes, adaptadas à minha própria compreensão do problema e às exigências do projeto. O uso da ferramenta limitou‑se a essas orientações, não substituindo minha responsabilidade sobre a concepção, implementação e validação final do sistema.

São José, 07/09/2026.