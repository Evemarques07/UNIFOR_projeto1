# Passo a Passo - Projeto 1

Este guia mostra como baixar e executar o projeto do GitHub.

---

## Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- **Git** - [Download Git](https://git-scm.com/downloads)
- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **Jupyter Notebook** ou **JupyterLab** (opcional, para notebooks)

---

## Passo 1: Clonar o Repositório

Abra o terminal (ou Git Bash no Windows) e execute:

```bash
git clone https://github.com/Cassiopo7/mba_ia_unifor_projeto1.git
```

---

## Passo 2: Navegar até o Diretório do Projeto

```bash
cd mba_ia_unifor_projeto1
```

---

## Passo 3: Instalar Dependências

Instale as bibliotecas Python necessárias:

```bash
pip install pandas numpy jupyter
```

Ou, se houver um arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## Passo 4: Executar os Scripts

### 4.1. Gerar o Hello World HTML

```bash
python gerar_hello_world.py
```

Isso criará o arquivo `hello_world.html` no diretório do projeto. Abra-o no navegador para visualizar.

---

### 4.2. Gerar os Datasets

```bash
python 2_gerar_datasets.py
```

Isso criará a pasta `datasets/` com 5 arquivos CSV:
- `titanic.csv`
- `vendas.csv`
- `ibge_populacao.csv`
- `covid.csv`
- `filmes.csv`

---

### 4.3. Visualizar os Dados (Jupyter Notebook)

Inicie o Jupyter Notebook:

```bash
jupyter notebook
```

Ou JupyterLab:

```bash
jupyter lab
```

No navegador que abrir automaticamente:
1. Navegue até o arquivo `3_leitura_dos_dados.ipynb`
2. Clique para abrir
3. Execute todas as células: **Cell > Run All** ou use `Shift + Enter` em cada célula

---

## Estrutura do Projeto

Após executar todos os scripts, a estrutura ficará assim:

```
mba_ia_unifor_projeto1/
├── gerar_hello_world.py
├── 2_gerar_datasets.py
├── 3_leitura_dos_dados.ipynb
├── passo_passo.md
├── hello_world.html (gerado)
└── datasets/ (gerado)
    ├── titanic.csv
    ├── vendas.csv
    ├── ibge_populacao.csv
    ├── covid.csv
    └── filmes.csv
```

---

## Solução de Problemas

### Erro: "git não é reconhecido como comando"
- Instale o Git: https://git-scm.com/downloads
- Reinicie o terminal após a instalação

### Erro: "python não é reconhecido como comando"
- Instale o Python: https://www.python.org/downloads/
- Durante a instalação, marque a opção "Add Python to PATH"

### Erro: "ModuleNotFoundError: No module named 'pandas'"
- Execute: `pip install pandas numpy`

### Erro ao abrir Jupyter Notebook
- Execute: `pip install jupyter`
- Tente novamente: `jupyter notebook`

---

## Contato e Suporte

Para dúvidas ou problemas:
- Abra uma issue no GitHub: https://github.com/Cassiopo7/mba_ia_unifor_projeto1/issues
- Entre em contato com o desenvolvedor

---

**Projeto desenvolvido para o MBA em Inteligência Artificial - UNIFOR**
