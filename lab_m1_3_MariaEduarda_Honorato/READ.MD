# qual laboratório está sendo entregue

- m1.3

# linguagem utilizada

- **Python 3.8+**

# dependências

As bibliotecas necessárias estão listadas abaixo. Todas são facilmente instaláveis via pip.
- [Pillow] – para manipulação de imagens.
- [NumPy] – para operações matriciais eficientes.
Bibliotecas padrão utilizadas:
- [Pillow] - manipulação de caminhos e diretórios.

# como preparar o ambiente

- Clone ou baixe este repositório para sua máquina.
- Instale as dependências: pip install numpy Pillow

# como executar

- Execute o script a partir do diretório raiz do projeto: python main.py
- Resultados: 
As imagens processadas serão salvas em imagens/output/ com nomes descritivos (ex: nome_identidade.jpg, nome_media3.jpg, etc.).
Uma subpasta testes_sinteticos/ também será criada em output/ contendo imagens geradas artificialmente para validação dos filtros.

# exemplos de comandos

- **Executar o processamento padrão:**: python processamento.py
- **Se quiser especificar manualmente a imagem de entrada**: O script atual processa automaticamente o primeiro .jpg encontrado em input/. Para processar uma imagem específica, você pode modificar o código ou renomear a imagem desejada para que seja a única na pasta.
- **Limpeza dos resultados**: Para reiniciar os testes, apague o conteúdo da pasta output/ ou exclua-a e execute o script novamente.