# 📸 Double Checker

Aplicativo desenvolvido para permitir a re-classificação de uma determinada base de dados e comparar a nova classificação com a anterior, foi projetado especialmente para auxiliar pesquisadores na produção de um padrão ouro mais robusto e confiável (ground-truth). Importante salientar que o sistema está ajustado para as especificações do meu projeto de mestrado, não sendo uma solução genérica para múltiplas bases.

---

## 🔎 Descrição Geral

O **Double Checker** tem como objetivo:
- Classificar imagens extraídas de um conjunto de imagens nas seguintes categorias:
  - `Indolor`  
  - `Pouca dor`  
  - `Muita dor`  
  - `Incerto`
- Comparar a nova classificação com a classificação do dataset original de modo automatizado (identificando possíveis outliers);

Destina-se principalmente a **pesquisadores em medicina veterinária**, na criação de 'ground-truths' mas pode ser utilizado em outros contextos que exijam uma reclassificação de bases de dados (especificamente no contexto da análise de presença de dor por meio de atributos visuais)

---

## 🖥️ Interface e Funcionalidades

### 📂 Janela Inicial
- Contém uma área à esquerda dedicada à exibição das imagens provenientes da base de dados;
- Contém uma área à direita dedicada às funcionalidades do sistema, sendo:
  - **Selecionar diretório de imagens** – Permite selecionar a pasta contendo a base de dados a ser reclassificada. Importante salientar que a base deve conter apenas arquivos de imagens (sem haver a presença de subpastas que representem as diferentes classes das imagens);  
  - **Classificar como 'Indolor'** – Move a imagem exibida na janela para um o diretório 'Reclassificados/Indolor' localizado na pasta raiz do executável;  
  - **Classificar como 'Pouca Dor'** – Move a imagem exibida na janela para um o diretório 'Reclassificados/Pouca Dor' localizado na pasta raiz do executável;  
  - **Classificar como 'Muita Dor'** – Move a imagem exibida na janela para um o diretório 'Reclassificados/Muita Dor' localizado na pasta raiz do executável;  
  - **Classificar como 'Incerto'** – Move a imagem exibida na janela para um o diretório 'Reclassificados/Incerto' localizado na pasta raiz do executável;  
  - **Desfazer última operação** – Permite desfazer a última operação de classificação, devolvendo a imagem para seu diretório original;  
  - **Comparar datasets (Projeto-ratos)** – Compara o dataset re-classificado com o dataset original, evidenciando as divergências e possíveis outliers;  
  - **Fechar programa** – encerra a aplicação.  

---

> 🔎 **Observações Importantes**  
> - Ao comparar os datasets é importante nunca inverter a ordem de qual é o original e qual é o re-classificado (os resultados continuam consistentes, porém ocorre uma inversão dos rótulos das classes originais e re-classificadas);
> - Ao selecionar um diretório para re-classificar, é importante ele contenha apenas os arquivos de imagem. Neste caso, as imagens de todas as classes devem ser reunidas em um único diretório (se possível, preservar a estrutura original para fazer uma comparação futura)

---

## ⚙️ Pré-requisitos e Instalação

- Sistema Operacional: **Windows**  
- Python **3.9** (recomendado)   

---

## ▶️ Modo de Uso

1. Abrir uma IDE python de sua preferência e criar um novo ambiente virtual
2. Instalar os pacotes utilizados pela aplicação (Em especial: PyQt5, shutil, os, sys e tkinter)
3. Executar o arquivo main.py
4. Carregar um diretório contendo uma base de dados com imagens
5. Escolher uma opção de classificação para a imagem exibida à esqueda da janela de execução

OBSERVAÇÃO -> Os arquivos re-classificados são armazenados em um novo diretório denominado 'Reclassificados', o qual se localiza na pasta raiz do arquivo executável

---

## ⚠️ Erros Comuns

| Erro | Causa provável | Solução |
|------|----------------|---------|
| ❌ Diretório não retorna arquivos | Extensão inválida | Verifique se os arquivos estão em formato ".png", ".jpg", ".jpeg", ".bmp" |
| ❌ Aplicativo não abre | Python ou dependências ausentes | Reinstale dependências |
| ❌ Lista de divergências vazia | Estrutura equivocada da base | Certifique-se que ao comparar bases, elas apresentem a mesma estrutura interna |
| ❌ Travamento ou fechamento inesperado | Instabilidade de código | Contatar desenvolvedor |

---

## 🆕 Atualizações / Changelog

- **v1.0.0**
  - Adicionado a função de comparar bases de dados

- **v0.5.0**
  - Adicionado elementos gráficos

- **v0.1.0**
  - Primeira iteração do programa
  - Permite a classificação das imagens

---

## 👨‍💻 Autores / Contribuidores

- Marcio Salmazo Ramos – **Desenvolvedor principal**  
  📧 marcio.salmazo19@gmail.com  
- Daniel Duarte Abdala   

---
