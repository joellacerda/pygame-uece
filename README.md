# 🧠 UECE Memory Leak — Jogo da Memória

Este projeto consiste em um jogo da memória desenvolvido para a disciplina de **Computação Gráfica** da Universidade Estadual do Ceará (UECE). O principal objetivo foi a construção de um motor gráfico 2D proprietário, implementando manualmente algoritmos fundamentais de rasterização, geometria e visualização computacional.

---

# 🛠️ Implementações Técnicas

O projeto demonstra o funcionamento de um **Pipeline Gráfico** completo, desde o espaço do objeto até a rasterização final dos pixels na tela.

## 📐 1. Geometria e Transformações

As transformações de **Translação**, **Escala** e **Rotação** foram implementadas utilizando **Coordenadas Homogêneas** e matrizes $3 \times 3$.

- **Vetorização:** utilização da biblioteca **NumPy** para aplicar transformações matriciais em massa sobre os vértices dos polígonos, otimizando o processamento geométrico.
- **Pivô de Transformação:** rotações e escalas das cartas (como no efeito de *Flip*) são realizadas transladando o objeto para a origem, aplicando a transformação e retornando-o à posição original, garantindo movimentação em torno do centro da carta.

---

## 🖌️ 2. Rasterização e Preenchimento

- **Algoritmo de Bresenham:** implementação manual para o desenho de linhas e contornos do jogo.
- **Scanline Fill:** preenchimento de polígonos.
- **Gradientes:** suporte a preenchimento com gradiente linear através da interpolação de cores RGB entre vértices.
- **Flood Fill:** implementação baseada em *spans* (*scanline flood fill*) para otimização do preenchimento do fundo do menu.

---

## 🖼️ 3. Mapeamento de Texturas

- **Mapeamento UV Inverso:** aplicação das imagens dos professores nas cartas percorrendo os pixels do destino e buscando a cor correspondente na textura original.
- **Otimização com DDA:** cálculo incremental das coordenadas de textura, reduzindo operações de divisão dentro do loop principal de rasterização.

---

## 🎥 4. Sistema de Visualização e Recorte

- **Câmera Dinâmica:** implementação da transformação **Window-to-Viewport**, permitindo operações de **Pan** e **Zoom**.
- **Clipping de Cohen-Sutherland:** algoritmo de recorte de linhas para garantir que apenas elementos visíveis sejam rasterizados.
- **Minimapa:** segundo *viewport* estático exibindo o estado global do tabuleiro em tempo real.

---

## 🖱️ 5. Detecção de Colisão

- **Ray Casting:** utilizado para detectar interações do mouse com botões poligonais.
- **Broad Phase (AABB):** uso de *Bounding Boxes* para descartar rapidamente colisões impossíveis e otimizar o processamento.

---

# 🚀 Tutorial de Execução

## 📋 1. Pré-requisitos

Certifique-se de possuir o **Python 3.10** ou superior instalado.

O projeto utiliza as seguintes bibliotecas:

- `pygame` — Interface gráfica e áudio
- `numpy` — Operações matemáticas e matriciais

---

## ⚙️ 2. Instalação

Clone o repositório e instale as dependências:

```bash
git clone https://github.com/joellacerda/pygame-uece.git
cd pygame-uece
pip install pygame numpy
```

---

# 🎮 Comandos do Jogo

| Comando | Ação |
|---|---|
| Botão Esquerdo do Mouse | Virar cartas e interagir com botões e menus |
| Setas do Teclado | Movimentar a câmera pelo tabuleiro (*Pan*) |
| Teclas `+` / `-` | Ajustar o nível de aproximação (*Zoom*) |
| Mouse Hover | Aplicar destaque visual e pequena rotação na carta |

---

# 🎥 Demonstração em Vídeo

Você pode visualizar o projeto em execução e a explicação detalhada das funcionalidades técnicas através do link abaixo:

👉 https://youtu.be/iUplG8R0piE

---

# 👥 Autores

- **Joel** — Estudante de Ciência da Computação (UECE)
- **Felipe** — Estudante de Ciência da Computação (UECE)
- **Murilo** — Estudante de Ciência da Computação (UECE)
- **Vinícius** — Estudante de Ciência da Computação (UECE)