# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
import sys
import os

# Configurar encoding UTF-8 para Windows
if sys.platform == "win32":
    os.system("chcp 65001 > nul")

warnings.filterwarnings('ignore')

# Configurar estilo dos gráficos
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def garantir_diretorio(caminho_arquivo):
    """Garante que o diretório do arquivo existe, criando se necessário"""
    diretorio = os.path.dirname(caminho_arquivo)
    if diretorio and not os.path.exists(diretorio):
        os.makedirs(diretorio, exist_ok=True)
        print(f"📁 Diretório criado: {diretorio}")

# Configurar fontes para português
plt.rcParams['font.size'] = 10
plt.rcParams['figure.figsize'] = (12, 8)

class VisualizacaoVendas:
    def __init__(self, df):
        self.df = df.copy()
        self.preparar_dados()
    
    def preparar_dados(self):
        """Prepara os dados para visualização"""
        self.df['Data'] = pd.to_datetime(self.df['Data'])
        self.df['Ano'] = self.df['Data'].dt.year
        self.df['Mes'] = self.df['Data'].dt.month
        self.df['Ano_Mes'] = self.df['Data'].dt.to_period('M')
        self.df['Trimestre'] = self.df['Data'].dt.quarter
        
        # Criar nomes de meses em português
        meses_pt = {1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun',
                   7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'}
        self.df['Mes_Nome'] = self.df['Mes'].map(meses_pt)
    
    def grafico_produtos_mais_vendidos(self):
        """Gráfico de produtos mais vendidos"""
        plt.figure(figsize=(14, 8))
        
        # Dados por quantidade
        produto_qtd = self.df.groupby('Produto')['Qtd_Vendida'].sum().sort_values(ascending=True)
        
        # Subplot 1: Quantidade
        plt.subplot(2, 1, 1)
        bars1 = plt.barh(produto_qtd.index, produto_qtd.values, color='skyblue', alpha=0.8)
        plt.title('🏆 Produtos Mais Vendidos - Por Quantidade', fontsize=14, fontweight='bold')
        plt.xlabel('Quantidade Vendida (unidades)')
        
        # Adicionar valores nas barras
        for bar in bars1:
            width = bar.get_width()
            plt.text(width + width*0.01, bar.get_y() + bar.get_height()/2, 
                    f'{int(width):,}', ha='left', va='center')
        
        # Dados por receita
        produto_receita = self.df.groupby('Produto')['Receita'].sum().sort_values(ascending=True)
        
        # Subplot 2: Receita
        plt.subplot(2, 1, 2)
        bars2 = plt.barh(produto_receita.index, produto_receita.values, color='lightcoral', alpha=0.8)
        plt.title('💰 Produtos Mais Vendidos - Por Receita', fontsize=14, fontweight='bold')
        plt.xlabel('Receita (R$)')
        
        # Adicionar valores nas barras
        for bar in bars2:
            width = bar.get_width()
            plt.text(width + width*0.01, bar.get_y() + bar.get_height()/2, 
                    f'R$ {width:,.0f}', ha='left', va='center')
        
        plt.tight_layout()
        
        # Garantir que o diretório existe antes de salvar
        caminho_arquivo = 'output/imagens/produtos_mais_vendidos.png'
        garantir_diretorio(caminho_arquivo)
        plt.savefig(caminho_arquivo, dpi=300, bbox_inches='tight')
        plt.show()
    
    def grafico_vendedores_performance(self):
        """Gráfico de performance dos vendedores"""
        plt.figure(figsize=(15, 10))
        
        # Subplot 1: Quantidade por vendedor
        plt.subplot(2, 2, 1)
        vendedor_qtd = self.df.groupby('Vendedor')['Qtd_Vendida'].sum().sort_values(ascending=False)
        bars = plt.bar(vendedor_qtd.index, vendedor_qtd.values, color='lightgreen', alpha=0.8)
        plt.title('👥 Vendedores - Quantidade Vendida', fontsize=12, fontweight='bold')
        plt.ylabel('Quantidade (unidades)')
        plt.xticks(rotation=45)
        
        # Adicionar valores nas barras
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                    f'{int(height):,}', ha='center', va='bottom')
        
        # Subplot 2: Receita por vendedor
        plt.subplot(2, 2, 2)
        vendedor_receita = self.df.groupby('Vendedor')['Receita'].sum().sort_values(ascending=False)
        bars = plt.bar(vendedor_receita.index, vendedor_receita.values, color='gold', alpha=0.8)
        plt.title('👥 Vendedores - Receita', fontsize=12, fontweight='bold')
        plt.ylabel('Receita (R$)')
        plt.xticks(rotation=45)
        
        # Adicionar valores nas barras
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                    f'R$ {height:,.0f}', ha='center', va='bottom', fontsize=9)
        
        # Subplot 3: Vendas por região
        plt.subplot(2, 2, 3)
        regiao_vendas = self.df.groupby('Regiao')['Qtd_Vendida'].sum()
        plt.pie(regiao_vendas.values, labels=regiao_vendas.index, autopct='%1.1f%%', 
                startangle=90, colors=['lightblue', 'lightcoral', 'lightgreen', 'gold'])
        plt.title('🗺️ Distribuição por Região', fontsize=12, fontweight='bold')
        
        # Subplot 4: Evolução temporal geral
        plt.subplot(2, 2, 4)
        vendas_mensais = self.df.groupby('Ano_Mes')['Qtd_Vendida'].sum()
        plt.plot(range(len(vendas_mensais)), vendas_mensais.values, marker='o', linewidth=2, markersize=6)
        plt.title('📈 Evolução Temporal das Vendas', fontsize=12, fontweight='bold')
        plt.ylabel('Quantidade Vendida')
        plt.xlabel('Período')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Garantir que o diretório existe antes de salvar
        caminho_arquivo = 'output/imagens/vendedores_performance.png'
        garantir_diretorio(caminho_arquivo)
        plt.savefig(caminho_arquivo, dpi=300, bbox_inches='tight')
        plt.show()
    
    def grafico_evolucao_temporal(self):
        """Gráfico detalhado da evolução temporal"""
        plt.figure(figsize=(16, 12))
        
        # Subplot 1: Vendas por mês (todos os anos)
        plt.subplot(3, 2, 1)
        vendas_mensais = self.df.groupby('Ano_Mes').agg({
            'Qtd_Vendida': 'sum',
            'Receita': 'sum'
        })
        
        plt.plot(range(len(vendas_mensais)), vendas_mensais['Qtd_Vendida'], 
                marker='o', linewidth=2, markersize=6, color='blue', label='Quantidade')
        plt.title('📅 Evolução Mensal - Quantidade', fontsize=12, fontweight='bold')
        plt.ylabel('Quantidade Vendida')
        plt.grid(True, alpha=0.3)
        
        # Subplot 2: Receita por mês
        plt.subplot(3, 2, 2)
        plt.plot(range(len(vendas_mensais)), vendas_mensais['Receita'], 
                marker='s', linewidth=2, markersize=6, color='red', label='Receita')
        plt.title('💰 Evolução Mensal - Receita', fontsize=12, fontweight='bold')
        plt.ylabel('Receita (R$)')
        plt.grid(True, alpha=0.3)
        
        # Subplot 3: Vendas por ano
        plt.subplot(3, 2, 3)
        vendas_anuais = self.df.groupby('Ano')['Qtd_Vendida'].sum()
        bars = plt.bar(vendas_anuais.index.astype(str), vendas_anuais.values, 
                      color='lightblue', alpha=0.8, width=0.6)
        plt.title('📊 Vendas Anuais', fontsize=12, fontweight='bold')
        plt.ylabel('Quantidade Vendida')
        
        # Adicionar valores nas barras
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                    f'{int(height):,}', ha='center', va='bottom')
        
        # Subplot 4: Sazonalidade por mês
        plt.subplot(3, 2, 4)
        sazonalidade = self.df.groupby('Mes')['Qtd_Vendida'].sum()
        meses_nomes = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
                      'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        
        plt.bar(meses_nomes, sazonalidade.values, color='orange', alpha=0.8)
        plt.title('🌡️ Sazonalidade (Vendas por Mês)', fontsize=12, fontweight='bold')
        plt.ylabel('Quantidade Total')
        plt.xticks(rotation=45)
        
        # Subplot 5: Heatmap de vendas por vendedor e produto
        plt.subplot(3, 2, 5)
        heatmap_data = self.df.groupby(['Vendedor', 'Produto'])['Qtd_Vendida'].sum().unstack(fill_value=0)
        sns.heatmap(heatmap_data, annot=True, fmt='g', cmap='YlOrRd', cbar_kws={'label': 'Quantidade'})
        plt.title('🔥 Heatmap: Vendedor × Produto', fontsize=12, fontweight='bold')
        plt.ylabel('Vendedor')
        plt.xlabel('Produto')
        
        # Subplot 6: Boxplot de vendas por trimestre
        plt.subplot(3, 2, 6)
        vendas_trimestre = self.df.groupby(['Ano', 'Trimestre'])['Qtd_Vendida'].sum().reset_index()
        
        # Criar dados para boxplot
        dados_boxplot = []
        for trim in [1, 2, 3, 4]:
            dados_trim = vendas_trimestre[vendas_trimestre['Trimestre'] == trim]['Qtd_Vendida'].values
            dados_boxplot.append(dados_trim)
        
        plt.boxplot(dados_boxplot, labels=['Q1', 'Q2', 'Q3', 'Q4'])
        plt.title('📦 Distribuição por Trimestre', fontsize=12, fontweight='bold')
        plt.ylabel('Quantidade Vendida')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Garantir que o diretório existe antes de salvar
        caminho_arquivo = 'output/imagens/evolucao_temporal.png'
        garantir_diretorio(caminho_arquivo)
        plt.savefig(caminho_arquivo, dpi=300, bbox_inches='tight')
        plt.show()
    
    def grafico_analise_produtos_detalhada(self):
        """Análise detalhada por produto"""
        produtos = self.df['Produto'].unique()
        n_produtos = len(produtos)
        
        plt.figure(figsize=(16, 4*n_produtos))
        
        for i, produto in enumerate(produtos):
            df_produto = self.df[self.df['Produto'] == produto]
            
            # Vendas mensais do produto
            plt.subplot(n_produtos, 3, i*3 + 1)
            vendas_mensais = df_produto.groupby('Ano_Mes')['Qtd_Vendida'].sum()
            plt.plot(range(len(vendas_mensais)), vendas_mensais.values, 
                    marker='o', linewidth=2, markersize=4)
            plt.title(f'📈 {produto} - Evolução Mensal', fontsize=11, fontweight='bold')
            plt.ylabel('Quantidade')
            plt.grid(True, alpha=0.3)
            
            # Vendas por vendedor para este produto
            plt.subplot(n_produtos, 3, i*3 + 2)
            vendas_vendedor = df_produto.groupby('Vendedor')['Qtd_Vendida'].sum().sort_values(ascending=True)
            plt.barh(vendas_vendedor.index, vendas_vendedor.values, alpha=0.8)
            plt.title(f'👥 {produto} - Por Vendedor', fontsize=11, fontweight='bold')
            plt.xlabel('Quantidade')
            
            # Distribuição por região
            plt.subplot(n_produtos, 3, i*3 + 3)
            vendas_regiao = df_produto.groupby('Regiao')['Qtd_Vendida'].sum()
            if len(vendas_regiao) > 1:
                plt.pie(vendas_regiao.values, labels=vendas_regiao.index, autopct='%1.1f%%', startangle=90)
            else:
                plt.bar(vendas_regiao.index, vendas_regiao.values, alpha=0.8)
            plt.title(f'🗺️ {produto} - Por Região', fontsize=11, fontweight='bold')
        
        plt.tight_layout()
        
        # Garantir que o diretório existe antes de salvar
        caminho_arquivo = 'output/imagens/analise_produtos_detalhada.png'
        garantir_diretorio(caminho_arquivo)
        plt.savefig(caminho_arquivo, dpi=300, bbox_inches='tight')
        plt.show()
    
    def grafico_previsoes_2025(self):
        """Gráfico das previsões para 2025"""
        from analise_predicao_vendas import AnalisePredicaoVendas
        
        # Criar análise preditiva
        analise = AnalisePredicaoVendas(self.df)
        
        # Obter previsões
        produtos_tendencia = analise.previsao_inteligente_produto()
        vendedores_analise = analise.previsao_inteligente_vendedores()
        previsoes_2025 = analise.media_vendas_2025_inteligente()
        
        plt.figure(figsize=(16, 12))
        
        # Subplot 1: Previsões de produtos para 2025
        plt.subplot(2, 3, 1)
        produtos_nomes = list(produtos_tendencia.keys())
        produtos_previsoes = [dados['previsao_2025'] for dados in produtos_tendencia.values()]
        produtos_cores = ['green' if dados['tendencia'] == 'CRESCIMENTO' 
                         else 'red' if dados['tendencia'] == 'QUEDA' 
                         else 'orange' for dados in produtos_tendencia.values()]
        
        bars = plt.bar(produtos_nomes, produtos_previsoes, color=produtos_cores, alpha=0.7)
        plt.title('🔮 Previsão Produtos 2025\n(unidades/mês)', fontsize=12, fontweight='bold')
        plt.ylabel('Quantidade Prevista')
        plt.xticks(rotation=45)
        
        # Adicionar valores
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                    f'{int(height)}', ha='center', va='bottom', fontsize=9)
        
        # Subplot 2: Tendências dos produtos
        plt.subplot(2, 3, 2)
        tendencias_count = {}
        for dados in produtos_tendencia.values():
            tend = dados['tendencia']
            tendencias_count[tend] = tendencias_count.get(tend, 0) + 1
        
        cores_tendencia = {'CRESCIMENTO': 'green', 'QUEDA': 'red', 'ESTÁVEL': 'orange'}
        cores = [cores_tendencia.get(tend, 'gray') for tend in tendencias_count.keys()]
        
        plt.pie(tendencias_count.values(), labels=tendencias_count.keys(), 
                autopct='%1.0f%%', startangle=90, colors=cores)
        plt.title('📊 Distribuição de Tendências\nProdutos', fontsize=12, fontweight='bold')
        
        # Subplot 3: Previsões dos vendedores
        plt.subplot(2, 3, 3)
        vendedores_nomes = list(vendedores_analise.keys())
        vendedores_previsoes = [dados['previsao_2025'] for dados in vendedores_analise.values()]
        vendedores_cores = []
        
        for dados in vendedores_analise.values():
            if 'CRESCIMENTO' in dados['tendencia']:
                vendedores_cores.append('green')
            elif 'QUEDA' in dados['tendencia']:
                vendedores_cores.append('red')
            else:
                vendedores_cores.append('orange')
        
        bars = plt.bar(vendedores_nomes, vendedores_previsoes, color=vendedores_cores, alpha=0.7)
        plt.title('🚀 Previsão Vendedores 2025\n(unidades/trimestre)', fontsize=12, fontweight='bold')
        plt.ylabel('Quantidade Prevista')
        plt.xticks(rotation=45)
        
        # Adicionar valores
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                    f'{int(height)}', ha='center', va='bottom', fontsize=9)
        
        # Subplot 4: Comparação histórico vs previsão
        plt.subplot(2, 3, 4)
        # Calcular médias históricas por vendedor
        historico_vendedores = self.df.groupby('Vendedor')['Qtd_Vendida'].sum() / len(self.df['Ano'].unique())
        previsao_vendedores = [previsoes_2025[vend]['previsao'] for vend in historico_vendedores.index]
        
        x = np.arange(len(historico_vendedores))
        width = 0.35
        
        plt.bar(x - width/2, historico_vendedores.values, width, label='Histórico', alpha=0.8, color='lightblue')
        plt.bar(x + width/2, previsao_vendedores, width, label='Previsão 2025', alpha=0.8, color='orange')
        
        plt.xlabel('Vendedores')
        plt.ylabel('Vendas Anuais')
        plt.title('📊 Histórico vs Previsão 2025', fontsize=12, fontweight='bold')
        plt.xticks(x, historico_vendedores.index, rotation=45)
        plt.legend()
        
        # Subplot 5: Intervalos de confiança
        plt.subplot(2, 3, 5)
        vendedores_order = list(previsoes_2025.keys())
        previsoes_values = [previsoes_2025[v]['previsao'] for v in vendedores_order]
        limite_inf = [previsoes_2025[v]['limite_inferior'] for v in vendedores_order]
        limite_sup = [previsoes_2025[v]['limite_superior'] for v in vendedores_order]
        
        x_pos = range(len(vendedores_order))
        plt.errorbar(x_pos, previsoes_values, 
                    yerr=[np.array(previsoes_values) - np.array(limite_inf),
                          np.array(limite_sup) - np.array(previsoes_values)],
                    fmt='o', capsize=5, capthick=2, markersize=8)
        
        plt.xlabel('Vendedores')
        plt.ylabel('Previsão 2025')
        plt.title('🎯 Intervalos de Confiança\n(95%)', fontsize=12, fontweight='bold')
        plt.xticks(x_pos, vendedores_order, rotation=45)
        plt.grid(True, alpha=0.3)
        
        # Subplot 6: Share de mercado previsto
        plt.subplot(2, 3, 6)
        total_previsto = sum([dados['previsao'] for dados in previsoes_2025.values()])
        shares = [(dados['previsao']/total_previsto)*100 for dados in previsoes_2025.values()]
        
        plt.pie(shares, labels=vendedores_order, autopct='%1.1f%%', startangle=90)
        plt.title('🥧 Share de Mercado\nPrevisto 2025', fontsize=12, fontweight='bold')
        
        plt.tight_layout()
        
        # Garantir que o diretório existe antes de salvar
        caminho_arquivo = 'output/imagens/previsoes_2025.png'
        garantir_diretorio(caminho_arquivo)
        plt.savefig(caminho_arquivo, dpi=300, bbox_inches='tight')
        plt.show()
    
    def analise_lucros_custos(self):
        """Análise detalhada de lucros e custos"""
        plt.figure(figsize=(16, 12))
        
        # Calcular custos
        self.df['Custo'] = self.df['Receita'] - self.df['Lucro']
        self.df['Margem_%'] = (self.df['Lucro'] / self.df['Receita']) * 100
        
        # Dados por produto
        dados_produto = self.df.groupby('Produto').agg({
            'Receita': 'sum',
            'Lucro': 'sum',
            'Custo': 'sum',
            'Qtd_Vendida': 'sum'
        }).reset_index()
        dados_produto['Margem_%'] = (dados_produto['Lucro'] / dados_produto['Receita']) * 100
        dados_produto['Lucro_Unitario'] = dados_produto['Lucro'] / dados_produto['Qtd_Vendida']
        dados_produto['Custo_Unitario'] = dados_produto['Custo'] / dados_produto['Qtd_Vendida']
        
        # 1. Receita vs Lucro vs Custo por produto
        plt.subplot(2, 3, 1)
        x = range(len(dados_produto))
        width = 0.25
        
        plt.bar([i - width for i in x], dados_produto['Receita'], width, label='Receita', alpha=0.8, color='blue')
        plt.bar(x, dados_produto['Custo'], width, label='Custo', alpha=0.8, color='red')
        plt.bar([i + width for i in x], dados_produto['Lucro'], width, label='Lucro', alpha=0.8, color='green')
        
        plt.title('💰 Análise Financeira por Produto', fontweight='bold')
        plt.xlabel('Produtos')
        plt.ylabel('Valor (R$)')
        plt.xticks(x, dados_produto['Produto'], rotation=45)
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # 2. Margem de lucro por produto
        plt.subplot(2, 3, 2)
        cores_margem = ['green' if m >= 30 else 'orange' if m >= 20 else 'red' for m in dados_produto['Margem_%']]
        bars = plt.bar(dados_produto['Produto'], dados_produto['Margem_%'], color=cores_margem, alpha=0.8)
        plt.title('📊 Margem de Lucro (%)', fontweight='bold')
        plt.ylabel('Margem (%)')
        plt.xticks(rotation=45)
        plt.axhline(y=30, color='green', linestyle='--', alpha=0.7, label='Meta 30%')
        plt.axhline(y=20, color='orange', linestyle='--', alpha=0.7, label='Mínimo 20%')
        plt.legend()
        
        # Adicionar valores
        for bar, valor in zip(bars, dados_produto['Margem_%']):
            plt.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.5,
                    f'{valor:.1f}%', ha='center', va='bottom', fontsize=9)
        
        # 3. Lucro vs Custo unitário
        plt.subplot(2, 3, 3)
        x = range(len(dados_produto))
        
        plt.bar([i - 0.2 for i in x], dados_produto['Lucro_Unitario'], 0.4, label='Lucro Unit.', alpha=0.8, color='green')
        plt.bar([i + 0.2 for i in x], dados_produto['Custo_Unitario'], 0.4, label='Custo Unit.', alpha=0.8, color='red')
        
        plt.title('🔢 Análise Unitária', fontweight='bold')
        plt.xlabel('Produtos')
        plt.ylabel('Valor Unitário (R$)')
        plt.xticks(x, dados_produto['Produto'], rotation=45)
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # 4. Evolução temporal dos custos
        plt.subplot(2, 3, 4)
        evolucao_mensal = self.df.groupby('Ano_Mes').agg({
            'Receita': 'sum',
            'Lucro': 'sum',
            'Custo': 'sum'
        })
        
        x_tempo = range(len(evolucao_mensal))
        plt.plot(x_tempo, evolucao_mensal['Receita'], marker='o', label='Receita', linewidth=2)
        plt.plot(x_tempo, evolucao_mensal['Custo'], marker='s', label='Custo', linewidth=2)
        plt.plot(x_tempo, evolucao_mensal['Lucro'], marker='^', label='Lucro', linewidth=2)
        
        plt.title('📈 Evolução Financeira Mensal', fontweight='bold')
        plt.ylabel('Valor (R$)')
        plt.xlabel('Período')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # 5. ROI por produto
        plt.subplot(2, 3, 5)
        dados_produto['ROI_%'] = (dados_produto['Lucro'] / dados_produto['Custo']) * 100
        cores_roi = ['green' if roi >= 50 else 'orange' if roi >= 25 else 'red' for roi in dados_produto['ROI_%']]
        bars = plt.bar(dados_produto['Produto'], dados_produto['ROI_%'], color=cores_roi, alpha=0.8)
        
        plt.title('📈 ROI por Produto', fontweight='bold')
        plt.ylabel('ROI (%)')
        plt.xticks(rotation=45)
        plt.axhline(y=50, color='green', linestyle='--', alpha=0.7, label='Excelente 50%+')
        plt.axhline(y=25, color='orange', linestyle='--', alpha=0.7, label='Bom 25%+')
        plt.legend()
        
        # Adicionar valores
        for bar, valor in zip(bars, dados_produto['ROI_%']):
            plt.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1,
                    f'{valor:.1f}%', ha='center', va='bottom', fontsize=9)
        
        # 6. Scatter: Volume vs Lucratividade
        plt.subplot(2, 3, 6)
        plt.scatter(dados_produto['Qtd_Vendida'], dados_produto['Lucro'], 
                   s=dados_produto['Margem_%']*10, alpha=0.7, 
                   c=dados_produto['Margem_%'], cmap='RdYlGn')
        
        plt.title('🎯 Volume vs Lucratividade\n(tamanho/cor = margem)', fontweight='bold')
        plt.xlabel('Quantidade Vendida')
        plt.ylabel('Lucro Total (R$)')
        
        # Adicionar labels
        for i, row in dados_produto.iterrows():
            plt.annotate(f'{row["Produto"]}\n{row["Margem_%"]:.1f}%', 
                        (row['Qtd_Vendida'], row['Lucro']),
                        xytext=(5, 5), textcoords='offset points', fontsize=8)
        
        plt.colorbar(label='Margem (%)')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Garantir que o diretório existe antes de salvar
        caminho_arquivo = 'output/imagens/analise_lucros_custos.png'
        garantir_diretorio(caminho_arquivo)
        plt.savefig(caminho_arquivo, dpi=300, bbox_inches='tight')
        plt.show()
    
    def dashboard_completo(self):
        """Cria um dashboard completo com todos os gráficos"""
        print("🎨 Gerando Dashboard Completo de Vendas...")
        print("=" * 60)
        
        print("📊 1. Gráficos de Produtos Mais Vendidos...")
        self.grafico_produtos_mais_vendidos()
        
        print("👥 2. Gráficos de Performance dos Vendedores...")
        self.grafico_vendedores_performance()
        
        print("📈 3. Gráficos de Evolução Temporal...")
        self.grafico_evolucao_temporal()
        
        print("🔍 4. Análise Detalhada por Produto...")
        self.grafico_analise_produtos_detalhada()
        
        print("🔮 5. Análise de Lucros e Custos...")
        self.analise_lucros_custos()
        
        print("🔮 6. Gráficos de Previsões 2025...")
        self.grafico_previsoes_2025()
        
        print("\n✅ Dashboard completo gerado!")
        print("📁 Arquivos salvos:")
        print("   - output/imagens/produtos_mais_vendidos.png")
        print("   - output/imagens/vendedores_performance.png") 
        print("   - output/imagens/evolucao_temporal.png")
        print("   - output/imagens/analise_produtos_detalhada.png")
        print("   - output/imagens/analise_lucros_custos.png")
        print("   - output/imagens/previsoes_2025.png")

def main():
    """Função principal"""
    print("🎨 SISTEMA DE VISUALIZAÇÃO DE VENDAS")
    print("=" * 60)
    
    # Carregar dados
    df = pd.read_csv('datasets/vendas.csv')
    
    # Criar instância da visualização
    viz = VisualizacaoVendas(df)
    
    # Gerar dashboard completo
    viz.dashboard_completo()

if __name__ == "__main__":
    main()