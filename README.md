# 📊 Sistema de Análise de Vendas com Previsões Financeiras

## 📋 Visão Geral do Projeto

Este sistema realiza análise completa de dados de vendas, incluindo previsões financeiras avançadas para apoio à tomada de decisões estratégicas. O projeto foi desenvolvido para fornecer insights acionáveis sobre performance de produtos, vendedores e projeções futuras.

## 🗂️ Estrutura do Projeto

```
mba_ia_unifor_projeto1/
├── 📊 DADOS
│   └── datasets/
│       ├── vendas.csv              # Dataset principal de vendas
│       ├── covid.csv               # Dados auxiliares
│       ├── filmes.csv              # Dados auxiliares
│       ├── ibge_populacao.csv      # Dados auxiliares
│       └── titanic.csv             # Dados auxiliares
│
├── 📈 ANÁLISES PRINCIPAIS
│   ├── analise_vendas.py           # Análise básica de vendas
│   ├── analise_predicao_vendas.py  # Análise preditiva avançada
│   └── resumo_previsoes_financeiras.py # Resumo executivo
│
├── 🎨 VISUALIZAÇÕES
│   ├── visualizacao_vendas.py      # Gráficos estáticos (PNG)
│   ├── visualizacao_interativa.py  # Gráficos interativos (HTML)
│   └── dashboard_completo.py       # Dashboard unificado
│
├──  RESULTADOS
│   └── output/
│       ├── imagens/                # Gráficos PNG
│       ├── html_interativos/       # Dashboards HTML
│       └── index_dashboard.html    # Página principal
│
├── 📋 CONFIGURAÇÃO
│   ├── requirements.txt           # Dependências
│   └── README.md                  # Esta documentação
```

## 🛠️ Instalação e Configuração

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalação das Dependências

```bash
# Clone o repositório (se aplicável)
git clone [url-do-repositorio]
cd mba_ia_unifor_projeto1

# Instale as dependências
pip install -r requirements.txt
```

### Verificação da Instalação

```bash
python -c "import pandas, numpy, matplotlib, seaborn, plotly, scipy; print('✅ Todas as dependências instaladas!')"
```

## 📚 Bibliotecas Utilizadas

### 🔧 Manipulação de Dados

- **pandas (>=2.0.0)**: Manipulação e análise de DataFrames
- **numpy (>=1.24.0)**: Operações matemáticas e arrays

### 📊 Visualizações Estáticas

- **matplotlib (>=3.7.0)**: Criação de gráficos estáticos
- **seaborn (>=0.12.0)**: Visualizações estatísticas elegantes

### 🌐 Visualizações Interativas

- **plotly (>=5.14.0)**: Gráficos interativos e dashboards
- **kaleido (>=0.2.1)**: Exportação de gráficos plotly

### 📈 Análise Estatística

- **scipy (>=1.10.0)**: Análises estatísticas e previsões

## 🚀 Como Executar

### ⚠️ Importante: Verificação de Dependências

Antes de executar qualquer análise, certifique-se de que todas as dependências estão instaladas:

```bash
# Instalar todas as dependências
pip install -r requirements.txt

# Ou instalar individualmente se necessário
pip install pandas numpy matplotlib seaborn plotly scipy kaleido
```

### Execução Completa (Recomendada)

Para executar todas as análises na sequência correta, execute os scripts na seguinte ordem:

```bash
# 1. Análise básica de vendas
python analise_vendas.py

# 2. Análise preditiva avançada
python analise_predicao_vendas.py

# 3. Visualizações estáticas (gráficos PNG)
python visualizacao_vendas.py

# 4. Visualizações interativas (dashboards HTML)
python visualizacao_interativa.py

# 5. Dashboard completo unificado
python dashboard_completo.py

# 6. Resumo executivo financeiro
python resumo_previsoes_financeiras.py
```

### Execução Individual

Você também pode executar qualquer análise individualmente:

```bash
# Análise básica
python analise_vendas.py

# Análise preditiva
python analise_predicao_vendas.py

# Visualizações estáticas
python visualizacao_vendas.py

# Visualizações interativas
python visualizacao_interativa.py

# Dashboard completo
python dashboard_completo.py

# Resumo executivo
python resumo_previsoes_financeiras.py
```

### 📁 Verificando os Resultados

Após a execução, os resultados serão gerados na pasta `output/`:

- `output/imagens/` - Gráficos estáticos em PNG
- `output/html_interativos/` - Dashboards interativos em HTML

Para visualizar os dashboards interativos, abra os arquivos HTML em qualquer navegador.

## 📊 Estrutura dos Dados

### Dataset Principal (vendas.csv)

```
Campos obrigatórios:
- Data: Data da venda (formato: YYYY-MM-DD)
- Produto: Nome do produto
- Vendedor: Nome do vendedor
- Regiao: Região de venda
- Qtd_Vendida: Quantidade vendida (inteiro)
- Receita: Receita total (float)
- Lucro: Lucro total (float)
```

## 📈 Indicadores e KPIs Explicados

### 🎯 KPIs Básicos

#### **Quantidade Vendida**

- **Definição**: Total de unidades vendidas
- **Cálculo**: Soma de `Qtd_Vendida`
- **Uso**: Medir volume de vendas

#### **Receita Total**

- **Definição**: Valor total faturado
- **Cálculo**: Soma de `Receita`
- **Uso**: Avaliar performance financeira

#### **Lucro Total**

- **Definição**: Valor total de lucro
- **Cálculo**: Soma de `Lucro`
- **Uso**: Medir rentabilidade

#### **Custo Total**

- **Definição**: Custo total dos produtos vendidos
- **Cálculo**: `Receita - Lucro`
- **Uso**: Controle de custos

### 💰 KPIs Financeiros Avançados

#### **Margem de Lucro (%)**

- **Definição**: Percentual de lucro sobre a receita
- **Cálculo**: `(Lucro / Receita) × 100`
- **Interpretação**:
  - 🟢 ≥30%: Excelente
  - 🟡 20-29%: Bom
  - 🔴 <20%: Atenção necessária

#### **ROI - Retorno sobre Investimento (%)**

- **Definição**: Retorno do lucro em relação ao custo
- **Cálculo**: `(Lucro / Custo) × 100`
- **Interpretação**:
  - 🟢 ≥50%: Excelente
  - 🟡 25-49%: Bom
  - 🔴 <25%: Revisar estratégia

#### **Receita Unitária**

- **Definição**: Receita média por unidade vendida
- **Cálculo**: `Receita Total / Qtd_Vendida`
- **Uso**: Análise de pricing

#### **Lucro Unitário**

- **Definição**: Lucro médio por unidade vendida
- **Cálculo**: `Lucro Total / Qtd_Vendida`
- **Uso**: Rentabilidade por item

#### **Custo Unitário**

- **Definição**: Custo médio por unidade vendida
- **Cálculo**: `Custo Total / Qtd_Vendida`
- **Uso**: Controle de custos unitários

### 🔮 KPIs Preditivos

#### **Tendência de Crescimento**

- **Definição**: Direção da evolução das vendas
- **Valores**:
  - 📈 **CRESCIMENTO**: Tendência positiva
  - 📊 **ESTÁVEL**: Sem variação significativa
  - 📉 **QUEDA**: Tendência negativa

#### **Confiança da Previsão (%)**

- **Definição**: Nível de certeza da previsão
- **Interpretação**:
  - 🟢 ≥70%: Alta confiança
  - 🟡 30-69%: Confiança moderada
  - 🔴 <30%: Baixa confiança

#### **Previsão 2025**

- **Definição**: Quantidade/valor previsto para 2025
- **Base**: Análise de tendências históricas
- **Uso**: Planejamento estratégico

## 📊 Tipos de Gráficos e Interpretações

### 📈 Gráficos de Linha (Evolução Temporal)

- **Propósito**: Mostrar tendências ao longo do tempo
- **Interpretação**:
  - Linha ascendente = crescimento
  - Linha descendente = declínio
  - Linha horizontal = estabilidade

### 📊 Gráficos de Barras

- **Propósito**: Comparar valores entre categorias
- **Interpretação**: Altura da barra = valor da métrica
- **Cores**: Indicam performance (verde = bom, vermelho = atenção)

### 🥧 Gráficos de Pizza

- **Propósito**: Mostrar proporções do total
- **Interpretação**: Tamanho da fatia = participação percentual
- **Uso**: Share de mercado, distribuição por região

### 🔥 Heatmaps (Mapas de Calor)

- **Propósito**: Mostrar intensidade em matriz 2D
- **Interpretação**:
  - 🔴 Cores quentes = valores altos
  - 🔵 Cores frias = valores baixos
- **Uso**: Performance vendedor × produto

### 🎯 Gráficos de Dispersão (Scatter)

- **Propósito**: Mostrar relação entre duas variáveis
- **Interpretação**:
  - Pontos no alto à direita = alta performance
  - Tamanho/cor = terceira dimensão (ex: margem)

### 📊 Gráficos de Bubble (Bolhas)

- **Propósito**: Mostrar 3 dimensões simultaneamente
- **Interpretação**:
  - Posição X/Y = duas métricas
  - Tamanho da bolha = terceira métrica
  - Cor = quarta dimensão

## 🎨 Sistema de Cores e Significados

### 🚦 Semáforo de Performance

- 🟢 **Verde**: Excelente performance (meta atingida)
- 🟡 **Amarelo/Laranja**: Performance moderada (atenção)
- 🔴 **Vermelho**: Performance baixa (ação necessária)

### 📈 Tendências

- 🔵 **Azul**: Dados históricos
- 🟠 **Laranja**: Previsões
- 🟢 **Verde**: Crescimento/positivo
- 🔴 **Vermelho**: Declínio/negativo

## 📊 Dashboards Disponíveis

### 1. 📈 Dashboard Geral de Vendas

- **Arquivo**: `output/imagens/dashboard_vendas_gerais.png`
- **Conteúdo**:
  - Top produtos por quantidade
  - Performance de vendedores
  - Distribuição por região
  - Evolução temporal
  - Sazonalidade
  - Análise receita vs lucro vs custo

### 2. 🔥 Heatmap de Performance

- **Arquivo**: `output/imagens/heatmap_performance.png`
- **Conteúdo**: Matriz vendedor × produto mostrando intensidade de vendas

### 3. 💰 Análise Financeira Detalhada

- **Arquivo**: `output/imagens/analise_financeira_detalhada.png`
- **Conteúdo**:
  - Receita/custo/lucro por produto
  - Margem de lucro por produto
  - Evolução financeira temporal
  - Análise unitária
  - ROI por produto
  - Volume vs lucratividade

### 4. 🔮 Previsões Financeiras Inteligentes

- **Arquivo**: `output/imagens/previsoes_financeiras_inteligentes.png`
- **Conteúdo**:
  - Previsão de receita
  - Previsão lucro vs custo
  - Evolução da margem
  - Cenários (otimista/realista/pessimista)
  - ROI projetado
  - Resumo das previsões

### 5. 💰 Previsões Financeiras por Produto 2025

- **Arquivo**: `output/imagens/previsoes_financeiras_produtos_2025.png`
- **Conteúdo**:
  - Comparação atual vs previsto
  - Variações percentuais
  - Margens previstas
  - Lucratividade absoluta

### 6. 🔮 Previsões 2025

- **Arquivo**: `output/imagens/previsoes_2025.png`
- **Conteúdo**:
  - Previsão por produto
  - Previsão por vendedor
  - Histórico vs previsão
  - Share de mercado previsto

### 7. 💡 Análise de Lucros e Custos

- **Arquivo**: `output/imagens/analise_lucros_custos.png`
- **Conteúdo**:
  - Análise financeira por produto
  - Margem de lucro
  - Análise unitária
  - Evolução temporal
  - ROI por produto
  - Volume vs lucratividade

## 🌐 Dashboards Interativos

### 📱 Como Acessar

1. Execute `python dashboard_completo.py`
2. Abra `output/index_dashboard.html` no navegador
3. Navegue pelos links para dashboards específicos

### 🎮 Funcionalidades Interativas

- **Zoom**: Clique e arraste para ampliar áreas
- **Hover**: Passe o mouse para ver detalhes
- **Filtros**: Use controles para filtrar dados
- **Download**: Botão para salvar gráficos
- **Fullscreen**: Modo tela cheia

## 📋 Interpretação dos Resultados

### ✅ Indicadores Positivos

- Margem de lucro crescente
- ROI acima de 50%
- Tendência de crescimento
- Receita em alta
- Custo controlado

### ⚠️ Pontos de Atenção

- Margem abaixo de 20%
- ROI em declínio
- Custo crescendo mais que receita
- Produtos com tendência de queda
- Concentração excessiva em poucos produtos

### 🚨 Sinais de Alerta

- Margem negativa
- ROI abaixo de 10%
- Queda consistente de receita
- Aumento descontrolado de custos
- Perda de market share

## 🎯 Como Usar para Tomada de Decisão

### 📊 Análise de Produtos

1. **Identifique** produtos com maior margem
2. **Invista** em produtos em crescimento
3. **Revise** estratégia para produtos em queda
4. **Otimize** custos de produtos com baixa margem

### 👥 Análise de Vendedores

1. **Reconheça** top performers
2. **Treine** vendedores com baixa performance
3. **Redistribua** territories conforme necessário
4. **Incentive** baseado em dados

### 🗺️ Análise Regional

1. **Expanda** regiões com potencial
2. **Investiga** regiões com baixa performance
3. **Adapte** produtos por região
4. **Otimize** logística e distribuição

### 🔮 Planejamento Estratégico

1. **Use previsões** para orçamento 2025
2. **Prepare-se** para mudanças de mercado
3. **Aloque recursos** baseado em projeções
4. **Defina metas** realistas e alcançáveis

## 🛠️ Customização e Extensões

### 📊 Adicionando Novos KPIs

1. Edite `analise_vendas.py` para KPIs básicos
2. Modifique `analise_predicao_vendas.py` para previsões
3. Atualize visualizações conforme necessário

### 🎨 Personalizando Visualizações

- **Cores**: Modifique paletas nos arquivos de visualização
- **Títulos**: Ajuste textos e labels
- **Formatos**: Altere tipos de gráficos conforme necessidade

### 📁 Novos Datasets

1. Mantenha a estrutura de colunas obrigatórias
2. Coloque arquivo em `datasets/`
3. Atualize caminho nos scripts

## 🐛 Solução de Problemas

### ❌ Erro: Módulo não encontrado

```bash
pip install -r requirements.txt
```

### ❌ Erro: Arquivo não encontrado

Verifique se `datasets/vendas.csv` existe e tem a estrutura correta

### ❌ Gráficos não aparecem

- Instale: `pip install kaleido`
- Execute em ambiente com interface gráfica

### ❌ Performance lenta

- Reduza tamanho do dataset para testes
- Use filtros de data para análises específicas

## 📞 Suporte e Contribuições

### 🆘 Obtendo Ajuda

1. Verifique esta documentação
2. Execute `python -c "import sys; print(sys.version)"` para verificar Python
3. Teste dependências individualmente

### 🤝 Contribuindo

1. Fork o repositório
2. Crie branch para feature: `git checkout -b nova-feature`
3. Commit mudanças: `git commit -m "Add nova feature"`
4. Push para branch: `git push origin nova-feature`
5. Abra Pull Request

## 📄 Licença

Este projeto é desenvolvido para fins educacionais e de análise de dados empresariais.

---

📊 **Sistema de Análise de Vendas** - Transformando dados em insights acionáveis para decisões estratégicas.
# UNIFOR_projeto1
