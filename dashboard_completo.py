# -*- coding: utf-8 -*-
"""
🎨 SISTEMA COMPLETO DE VISUALIZAÇÃO DE VENDAS
============================================

Este arquivo integra todas as funcionalidades de visualização:
- Gráficos estáticos (PNG) com matplotlib/seaborn
- Gráficos interativos (HTML) com plotly
- Dashboard completo para análise de vendas

Autor: Sistema de Análise de Vendas
Data: 30/10/2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.io as pio
from datetime import datetime
import warnings
import os
import sys

# Configurar encoding UTF-8 para Windows
if sys.platform == "win32":
    os.system("chcp 65001 > nul")

def garantir_diretorio(caminho_arquivo):
    """Garante que o diretório do arquivo existe, criando se necessário"""
    diretorio = os.path.dirname(caminho_arquivo)
    if diretorio and not os.path.exists(diretorio):
        os.makedirs(diretorio, exist_ok=True)
        print(f"📁 Diretório criado: {diretorio}")

warnings.filterwarnings('ignore')

# Configurações visuais
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")
pio.templates.default = "plotly_white"

class DashboardCompleto:
    def __init__(self, df):
        self.df = df.copy()
        self.preparar_dados()
        self.criar_diretorios()
        
        # Configurar cores
        self.cores_produtos = px.colors.qualitative.Set3
        self.cores_vendedores = px.colors.qualitative.Pastel
        
    def preparar_dados(self):
        """Prepara os dados para visualização"""
        self.df['Data'] = pd.to_datetime(self.df['Data'])
        self.df['Ano'] = self.df['Data'].dt.year
        self.df['Mes'] = self.df['Data'].dt.month
        self.df['Ano_Mes'] = self.df['Data'].dt.to_period('M')
        self.df['Trimestre'] = self.df['Data'].dt.quarter
        
        # Nomes em português
        meses_pt = {1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun',
                   7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'}
        self.df['Mes_Nome'] = self.df['Mes'].map(meses_pt)
        self.df['Data_Str'] = self.df['Ano_Mes'].astype(str)
        
    def criar_diretorios(self):
        """Cria diretórios para organizar os gráficos"""
        # Estrutura principal de output
        if not os.path.exists('output'):
            os.makedirs('output')
        if not os.path.exists('output/imagens'):
            os.makedirs('output/imagens')
        if not os.path.exists('output/html_interativos'):
            os.makedirs('output/html_interativos')
    
    def dashboard_vendas_gerais(self):
        """Dashboard geral de vendas - Estático"""
        print("📊 Gerando Dashboard Geral de Vendas...")
        
        fig, axes = plt.subplots(2, 3, figsize=(20, 12))
        fig.suptitle('📊 DASHBOARD GERAL DE VENDAS', fontsize=16, fontweight='bold')
        
        # 1. Top produtos (quantidade)
        produto_qtd = self.df.groupby('Produto')['Qtd_Vendida'].sum().sort_values(ascending=True)
        axes[0,0].barh(produto_qtd.index, produto_qtd.values, color='skyblue', alpha=0.8)
        axes[0,0].set_title('🏆 Top Produtos - Quantidade', fontweight='bold')
        axes[0,0].set_xlabel('Unidades Vendidas')
        
        # Adicionar valores
        for i, v in enumerate(produto_qtd.values):
            axes[0,0].text(v + v*0.01, i, f'{v:,}', va='center', ha='left')
        
        # 2. Top vendedores
        vendedor_qtd = self.df.groupby('Vendedor')['Qtd_Vendida'].sum().sort_values(ascending=False)
        axes[0,1].bar(vendedor_qtd.index, vendedor_qtd.values, color='lightgreen', alpha=0.8)
        axes[0,1].set_title('👥 Top Vendedores', fontweight='bold')
        axes[0,1].set_ylabel('Unidades Vendidas')
        axes[0,1].tick_params(axis='x', rotation=45)
        
        # Adicionar valores
        for i, v in enumerate(vendedor_qtd.values):
            axes[0,1].text(i, v + v*0.01, f'{v:,}', ha='center', va='bottom')
        
        # 3. Distribuição por região
        regiao_vendas = self.df.groupby('Regiao')['Qtd_Vendida'].sum()
        axes[0,2].pie(regiao_vendas.values, labels=regiao_vendas.index, autopct='%1.1f%%', 
                     startangle=90, colors=['lightblue', 'lightcoral', 'lightgreen', 'gold'])
        axes[0,2].set_title('🗺️ Vendas por Região', fontweight='bold')
        
        # 4. Evolução temporal
        vendas_mensais = self.df.groupby('Ano_Mes')['Qtd_Vendida'].sum()
        axes[1,0].plot(range(len(vendas_mensais)), vendas_mensais.values, 
                      marker='o', linewidth=2, markersize=6, color='blue')
        axes[1,0].set_title('📈 Evolução Temporal', fontweight='bold')
        axes[1,0].set_ylabel('Unidades Vendidas')
        axes[1,0].grid(True, alpha=0.3)
        
        # 5. Sazonalidade
        sazonalidade = self.df.groupby('Mes')['Qtd_Vendida'].sum()
        meses_nomes = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
                      'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        axes[1,1].bar(meses_nomes, sazonalidade.values, color='orange', alpha=0.8)
        axes[1,1].set_title('🌡️ Sazonalidade', fontweight='bold')
        axes[1,1].set_ylabel('Unidades Vendidas')
        axes[1,1].tick_params(axis='x', rotation=45)
        
        # 6. Receita vs Lucro vs Custo
        dados_financeiros = self.df.groupby('Produto').agg({'Receita': 'sum', 'Lucro': 'sum'})
        # Calcular custo (Receita - Lucro)
        dados_financeiros['Custo'] = dados_financeiros['Receita'] - dados_financeiros['Lucro']
        
        axes[1,2].scatter(dados_financeiros['Receita'], dados_financeiros['Lucro'], 
                         s=dados_financeiros['Custo']/1000, alpha=0.7, color='purple', 
                         label='Produtos (tamanho = custo)')
        axes[1,2].set_title('💰 Receita vs Lucro vs Custo', fontweight='bold')
        axes[1,2].set_xlabel('Receita (R$)')
        axes[1,2].set_ylabel('Lucro (R$)')
        
        # Adicionar linha de margem de 30%
        x_max = dados_financeiros['Receita'].max()
        x_line = np.linspace(0, x_max, 100)
        y_line = x_line * 0.3  # 30% de margem
        axes[1,2].plot(x_line, y_line, 'r--', alpha=0.5, label='Margem 30%')
        axes[1,2].legend()
        
        # Adicionar labels nos pontos
        for i, (produto, dados) in enumerate(dados_financeiros.iterrows()):
            axes[1,2].annotate(f'{produto}\nM:{(dados["Lucro"]/dados["Receita"]*100):.1f}%', 
                              (dados['Receita'], dados['Lucro']), 
                              xytext=(5, 5), textcoords='offset points', fontsize=8)
        
        plt.tight_layout()
        plt.savefig('output/imagens/dashboard_vendas_gerais.png', dpi=300, bbox_inches='tight')
        plt.show()
        
    def heatmap_performance(self):
        """Heatmap de performance - Estático"""
        print("🔥 Gerando Heatmap de Performance...")
        
        plt.figure(figsize=(14, 8))
        
        # Dados para heatmap
        heatmap_data = self.df.groupby(['Vendedor', 'Produto'])['Qtd_Vendida'].sum().unstack(fill_value=0)
        
        # Criar heatmap
        sns.heatmap(heatmap_data, annot=True, fmt='g', cmap='YlOrRd', 
                   cbar_kws={'label': 'Quantidade Vendida'})
        
        plt.title('🔥 HEATMAP: PERFORMANCE VENDEDOR × PRODUTO', fontsize=14, fontweight='bold')
        plt.ylabel('Vendedores')
        plt.xlabel('Produtos')
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        plt.savefig('output/imagens/heatmap_performance.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def analise_financeira_detalhada(self):
        """Análise financeira detalhada - Estático"""
        print("💰 Gerando Análise Financeira Detalhada...")
        
        plt.figure(figsize=(18, 12))
        
        # Dados financeiros por produto
        dados_produto = self.df.groupby('Produto').agg({
            'Receita': 'sum',
            'Lucro': 'sum',
            'Qtd_Vendida': 'sum'
        }).reset_index()
        dados_produto['Custo'] = dados_produto['Receita'] - dados_produto['Lucro']
        dados_produto['Margem_%'] = (dados_produto['Lucro'] / dados_produto['Receita']) * 100
        dados_produto['Receita_Unitaria'] = dados_produto['Receita'] / dados_produto['Qtd_Vendida']
        dados_produto['Lucro_Unitario'] = dados_produto['Lucro'] / dados_produto['Qtd_Vendida']
        dados_produto['Custo_Unitario'] = dados_produto['Custo'] / dados_produto['Qtd_Vendida']
        
        # 1. Receita, Custo e Lucro por produto
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
        plt.title('📊 Margem de Lucro por Produto', fontweight='bold')
        plt.ylabel('Margem (%)')
        plt.xticks(rotation=45)
        plt.axhline(y=30, color='green', linestyle='--', alpha=0.7, label='Meta 30%')
        plt.axhline(y=20, color='orange', linestyle='--', alpha=0.7, label='Mínimo 20%')
        plt.legend()
        
        # Adicionar valores nas barras
        for bar, valor in zip(bars, dados_produto['Margem_%']):
            plt.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.5,
                    f'{valor:.1f}%', ha='center', va='bottom', fontsize=9)
        
        # 3. Evolução financeira temporal
        plt.subplot(2, 3, 3)
        evolucao_financeira = self.df.groupby('Data_Str').agg({
            'Receita': 'sum',
            'Lucro': 'sum'
        })
        evolucao_financeira['Custo'] = evolucao_financeira['Receita'] - evolucao_financeira['Lucro']
        evolucao_financeira['Margem_%'] = (evolucao_financeira['Lucro'] / evolucao_financeira['Receita']) * 100
        
        x_temp = range(len(evolucao_financeira))
        plt.plot(x_temp, evolucao_financeira['Receita'], marker='o', label='Receita', linewidth=2)
        plt.plot(x_temp, evolucao_financeira['Custo'], marker='s', label='Custo', linewidth=2)
        plt.plot(x_temp, evolucao_financeira['Lucro'], marker='^', label='Lucro', linewidth=2)
        
        plt.title('📈 Evolução Financeira Temporal', fontweight='bold')
        plt.ylabel('Valor (R$)')
        plt.xlabel('Período')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # 4. Análise unitária
        plt.subplot(2, 3, 4)
        x = range(len(dados_produto))
        width = 0.25
        
        plt.bar([i - width for i in x], dados_produto['Receita_Unitaria'], width, label='Receita Unit.', alpha=0.8)
        plt.bar(x, dados_produto['Custo_Unitario'], width, label='Custo Unit.', alpha=0.8)
        plt.bar([i + width for i in x], dados_produto['Lucro_Unitario'], width, label='Lucro Unit.', alpha=0.8)
        
        plt.title('🔢 Análise Unitária por Produto', fontweight='bold')
        plt.xlabel('Produtos')
        plt.ylabel('Valor Unitário (R$)')
        plt.xticks(x, dados_produto['Produto'], rotation=45)
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # 5. ROI por produto (Retorno sobre Investimento)
        plt.subplot(2, 3, 5)
        dados_produto['ROI_%'] = (dados_produto['Lucro'] / dados_produto['Custo']) * 100
        cores_roi = ['green' if roi >= 50 else 'orange' if roi >= 25 else 'red' for roi in dados_produto['ROI_%']]
        bars = plt.bar(dados_produto['Produto'], dados_produto['ROI_%'], color=cores_roi, alpha=0.8)
        plt.title('📈 ROI por Produto (Retorno/Custo)', fontweight='bold')
        plt.ylabel('ROI (%)')
        plt.xticks(rotation=45)
        plt.axhline(y=50, color='green', linestyle='--', alpha=0.7, label='Excelente 50%+')
        plt.axhline(y=25, color='orange', linestyle='--', alpha=0.7, label='Bom 25%+')
        plt.legend()
        
        # Adicionar valores
        for bar, valor in zip(bars, dados_produto['ROI_%']):
            plt.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1,
                    f'{valor:.1f}%', ha='center', va='bottom', fontsize=9)
        
        # 6. Análise de contribuição (Lucro vs Volume)
        plt.subplot(2, 3, 6)
        plt.scatter(dados_produto['Qtd_Vendida'], dados_produto['Lucro'], 
                   s=dados_produto['Margem_%']*10, alpha=0.7, 
                   c=dados_produto['Margem_%'], cmap='RdYlGn')
        
        plt.title('🎯 Contribuição: Volume vs Lucro\n(tamanho/cor = margem)', fontweight='bold')
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
        plt.savefig('output/imagens/analise_financeira_detalhada.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def previsoes_financeiras_inteligentes(self):
        """Previsões financeiras usando análise inteligente - Estático"""
        print("🔮 Gerando Previsões Financeiras Inteligentes...")
        
        plt.figure(figsize=(18, 12))
        
        # Preparar dados históricos financeiros
        historico_mensal = self.df.groupby(self.df['Data'].dt.to_period('M')).agg({
            'Receita': 'sum',
            'Lucro': 'sum',
            'Qtd_Vendida': 'sum'
        })
        historico_mensal['Custo'] = historico_mensal['Receita'] - historico_mensal['Lucro']
        historico_mensal['Margem_%'] = (historico_mensal['Lucro'] / historico_mensal['Receita']) * 100
        
        # Gerar previsões usando tendência linear simples
        import numpy as np
        
        # Preparar dados para previsão (método simplificado sem sklearn)
        x_hist = np.arange(len(historico_mensal))
        
        # Função simples de regressão linear
        def calcular_tendencia(x, y):
            n = len(x)
            x_mean = np.mean(x)
            y_mean = np.mean(y)
            
            # Calcular coeficientes
            numerador = np.sum((x - x_mean) * (y - y_mean))
            denominador = np.sum((x - x_mean) ** 2)
            
            if denominador == 0:
                slope = 0
            else:
                slope = numerador / denominador
            
            intercept = y_mean - slope * x_mean
            return slope, intercept
        
        # Calcular tendências
        slope_receita, intercept_receita = calcular_tendencia(x_hist, historico_mensal['Receita'].values)
        slope_lucro, intercept_lucro = calcular_tendencia(x_hist, historico_mensal['Lucro'].values)
        slope_custo, intercept_custo = calcular_tendencia(x_hist, historico_mensal['Custo'].values)
        slope_margem, intercept_margem = calcular_tendencia(x_hist, historico_mensal['Margem_%'].values)
        
        # Próximos 6 meses
        x_futuro = np.arange(len(historico_mensal), len(historico_mensal) + 6)
        
        # Previsões usando as tendências calculadas
        prev_receita = slope_receita * x_futuro + intercept_receita
        prev_lucro = slope_lucro * x_futuro + intercept_lucro
        prev_custo = slope_custo * x_futuro + intercept_custo
        prev_margem = slope_margem * x_futuro + intercept_margem
        
        # Garantir valores positivos
        prev_receita = np.maximum(prev_receita, 0)
        prev_lucro = np.maximum(prev_lucro, 0)
        prev_custo = np.maximum(prev_custo, 0)
        
        # 1. Previsão de Receita
        plt.subplot(2, 3, 1)
        plt.plot(x_hist, historico_mensal['Receita'], 'o-', label='Histórico', linewidth=2, markersize=6)
        plt.plot(x_futuro, prev_receita, 's--', label='Previsão', linewidth=2, markersize=6, color='orange')
        plt.title('💰 Previsão de Receita', fontweight='bold')
        plt.ylabel('Receita (R$)')
        plt.xlabel('Período (meses)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Adicionar valores de previsão
        for i, val in enumerate(prev_receita):
            plt.annotate(f'R$ {val:,.0f}', 
                        (x_futuro[i], val),
                        xytext=(5, 5), textcoords='offset points', fontsize=8)
        
        # 2. Previsão de Lucro vs Custo
        plt.subplot(2, 3, 2)
        plt.plot(x_hist, historico_mensal['Lucro'], 'o-', label='Lucro Histórico', linewidth=2, color='green')
        plt.plot(x_hist, historico_mensal['Custo'], 'o-', label='Custo Histórico', linewidth=2, color='red')
        plt.plot(x_futuro, prev_lucro, 's--', label='Lucro Previsto', linewidth=2, color='lightgreen')
        plt.plot(x_futuro, prev_custo, 's--', label='Custo Previsto', linewidth=2, color='lightcoral')
        plt.title('📊 Previsão: Lucro vs Custo', fontweight='bold')
        plt.ylabel('Valor (R$)')
        plt.xlabel('Período (meses)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # 3. Evolução da Margem de Lucro
        plt.subplot(2, 3, 3)
        plt.plot(x_hist, historico_mensal['Margem_%'], 'o-', label='Margem Histórica', linewidth=2)
        plt.plot(x_futuro, prev_margem, 's--', label='Margem Prevista', linewidth=2, color='purple')
        plt.axhline(y=30, color='green', linestyle=':', alpha=0.7, label='Meta 30%')
        plt.title('📈 Evolução da Margem de Lucro', fontweight='bold')
        plt.ylabel('Margem (%)')
        plt.xlabel('Período (meses)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # 4. Cenários de Previsão (Otimista, Realista, Pessimista)
        plt.subplot(2, 3, 4)
        
        # Calcular cenários baseados no desvio padrão histórico
        std_receita = historico_mensal['Receita'].std()
        cenario_otimista = prev_receita + std_receita
        cenario_pessimista = prev_receita - std_receita
        
        plt.fill_between(x_futuro, cenario_pessimista, cenario_otimista, 
                        alpha=0.3, color='blue', label='Faixa de Previsão')
        plt.plot(x_futuro, prev_receita, 'o-', label='Cenário Realista', linewidth=2, color='blue')
        plt.plot(x_futuro, cenario_otimista, '--', label='Cenário Otimista', color='green')
        plt.plot(x_futuro, cenario_pessimista, '--', label='Cenário Pessimista', color='red')
        
        plt.title('🎯 Cenários de Receita Futura', fontweight='bold')
        plt.ylabel('Receita (R$)')
        plt.xlabel('Período (meses)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # 5. ROI Projetado
        plt.subplot(2, 3, 5)
        roi_historico = (historico_mensal['Lucro'] / historico_mensal['Custo']) * 100
        
        # Evitar divisão por zero
        roi_previsto = np.where(prev_custo > 0, (prev_lucro / prev_custo) * 100, 0)
        
        plt.plot(x_hist, roi_historico, 'o-', label='ROI Histórico', linewidth=2)
        plt.plot(x_futuro, roi_previsto, 's--', label='ROI Previsto', linewidth=2, color='orange')
        plt.axhline(y=50, color='green', linestyle=':', alpha=0.7, label='Meta 50%')
        plt.title('📊 ROI Projetado', fontweight='bold')
        plt.ylabel('ROI (%)')
        plt.xlabel('Período (meses)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # 6. Resumo das Previsões
        plt.subplot(2, 3, 6)
        
        # Criar tabela de resumo
        resumo_dados = {
            'Métrica': ['Receita Média', 'Lucro Médio', 'Custo Médio', 'Margem Média', 'ROI Médio'],
            'Próx. 6 Meses': [
                f'R$ {np.mean(prev_receita):,.0f}',
                f'R$ {np.mean(prev_lucro):,.0f}',
                f'R$ {np.mean(prev_custo):,.0f}',
                f'{np.mean(prev_margem):.1f}%',
                f'{np.mean(roi_previsto):.1f}%'
            ]
        }
        
        # Criar tabela visual
        plt.axis('off')
        table_data = list(zip(resumo_dados['Métrica'], resumo_dados['Próx. 6 Meses']))
        table = plt.table(cellText=table_data,
                         colLabels=['Métrica', 'Previsão (6 meses)'],
                         cellLoc='center',
                         loc='center',
                         bbox=[0, 0, 1, 1])
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 2)
        
        # Colorir header
        for i in range(len(resumo_dados['Métrica'])):
            table[(i+1, 0)].set_facecolor('#E8F4F8')
            table[(i+1, 1)].set_facecolor('#F0F8E8')
        
        table[(0, 0)].set_facecolor('#4CAF50')
        table[(0, 1)].set_facecolor('#4CAF50')
        
        plt.title('📋 Resumo das Previsões Financeiras', fontweight='bold', pad=20)
        
        plt.tight_layout()
        plt.savefig('output/imagens/previsoes_financeiras_inteligentes.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def previsoes_financeiras_produtos_2025(self):
        """Gráfico específico das previsões financeiras por produto"""
        print("💰 Gerando Previsões Financeiras por Produto 2025...")
        
        # Importar e executar análise preditiva financeira
        from analise_predicao_vendas import AnalisePredicaoVendas
        analise = AnalisePredicaoVendas(self.df)
        
        # Executar análises silenciosamente
        import sys
        from io import StringIO
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        try:
            previsoes_financeiras = analise.previsoes_financeiras_produtos()
        finally:
            sys.stdout = old_stdout
        
        # Criar figura com subplots
        fig, axes = plt.subplots(2, 3, figsize=(20, 12))
        fig.suptitle('💰 PREVISÕES FINANCEIRAS POR PRODUTO 2025', fontsize=16, fontweight='bold')
        
        # Preparar dados
        produtos = list(previsoes_financeiras.keys())
        receitas_previstas = [previsoes_financeiras[p]['receita_prevista'] for p in produtos]
        custos_previstos = [previsoes_financeiras[p]['custo_previsto'] for p in produtos]
        lucros_previstos = [previsoes_financeiras[p]['lucro_previsto'] for p in produtos]
        margens_previstas = [previsoes_financeiras[p]['margem_prevista_%'] for p in produtos]
        
        # Dados históricos para comparação
        receitas_atuais = [previsoes_financeiras[p]['historico']['receita_atual'] for p in produtos]
        lucros_atuais = [previsoes_financeiras[p]['historico']['lucro_atual'] for p in produtos]
        custos_atuais = [previsoes_financeiras[p]['historico']['custo_atual'] for p in produtos]
        
        # 1. Comparação Receita: Atual vs Prevista
        axes[0,0].bar(np.arange(len(produtos)) - 0.2, receitas_atuais, 0.4, 
                     label='Receita Atual', alpha=0.8, color='lightblue')
        axes[0,0].bar(np.arange(len(produtos)) + 0.2, receitas_previstas, 0.4, 
                     label='Receita Prevista 2025', alpha=0.8, color='blue')
        axes[0,0].set_title('💰 Receita: Atual vs Prevista 2025', fontweight='bold')
        axes[0,0].set_ylabel('Receita (R$)')
        axes[0,0].set_xticks(range(len(produtos)))
        axes[0,0].set_xticklabels(produtos, rotation=45)
        axes[0,0].legend()
        axes[0,0].grid(True, alpha=0.3)
        
        # 2. Comparação Lucro: Atual vs Previsto
        axes[0,1].bar(np.arange(len(produtos)) - 0.2, lucros_atuais, 0.4, 
                     label='Lucro Atual', alpha=0.8, color='lightgreen')
        axes[0,1].bar(np.arange(len(produtos)) + 0.2, lucros_previstos, 0.4, 
                     label='Lucro Previsto 2025', alpha=0.8, color='green')
        axes[0,1].set_title('💚 Lucro: Atual vs Previsto 2025', fontweight='bold')
        axes[0,1].set_ylabel('Lucro (R$)')
        axes[0,1].set_xticks(range(len(produtos)))
        axes[0,1].set_xticklabels(produtos, rotation=45)
        axes[0,1].legend()
        axes[0,1].grid(True, alpha=0.3)
        
        # 3. Comparação Custo: Atual vs Previsto
        axes[0,2].bar(np.arange(len(produtos)) - 0.2, custos_atuais, 0.4, 
                     label='Custo Atual', alpha=0.8, color='lightcoral')
        axes[0,2].bar(np.arange(len(produtos)) + 0.2, custos_previstos, 0.4, 
                     label='Custo Previsto 2025', alpha=0.8, color='red')
        axes[0,2].set_title('💸 Custo: Atual vs Previsto 2025', fontweight='bold')
        axes[0,2].set_ylabel('Custo (R$)')
        axes[0,2].set_xticks(range(len(produtos)))
        axes[0,2].set_xticklabels(produtos, rotation=45)
        axes[0,2].legend()
        axes[0,2].grid(True, alpha=0.3)
        
        # 4. Variações percentuais
        variacoes_receita = [previsoes_financeiras[p]['variacao_receita_%'] for p in produtos]
        variacoes_lucro = [previsoes_financeiras[p]['variacao_lucro_%'] for p in produtos]
        variacoes_custo = [previsoes_financeiras[p]['variacao_custo_%'] for p in produtos]
        
        x = np.arange(len(produtos))
        width = 0.25
        
        axes[1,0].bar(x - width, variacoes_receita, width, label='Var. Receita (%)', alpha=0.8, color='blue')
        axes[1,0].bar(x, variacoes_lucro, width, label='Var. Lucro (%)', alpha=0.8, color='green')
        axes[1,0].bar(x + width, variacoes_custo, width, label='Var. Custo (%)', alpha=0.8, color='red')
        
        axes[1,0].set_title('📈 Variações Previstas (%)', fontweight='bold')
        axes[1,0].set_ylabel('Variação (%)')
        axes[1,0].set_xticks(x)
        axes[1,0].set_xticklabels(produtos, rotation=45)
        axes[1,0].legend()
        axes[1,0].grid(True, alpha=0.3)
        axes[1,0].axhline(y=0, color='black', linestyle='-', alpha=0.5)
        
        # 5. Margem de lucro prevista
        cores_margem = ['green' if m >= 30 else 'orange' if m >= 20 else 'red' for m in margens_previstas]
        bars = axes[1,1].bar(produtos, margens_previstas, color=cores_margem, alpha=0.8)
        axes[1,1].set_title('📊 Margens de Lucro Previstas 2025', fontweight='bold')
        axes[1,1].set_ylabel('Margem (%)')
        axes[1,1].set_xticklabels(produtos, rotation=45)
        axes[1,1].axhline(y=30, color='green', linestyle='--', alpha=0.7, label='Meta 30%')
        axes[1,1].axhline(y=20, color='orange', linestyle='--', alpha=0.7, label='Mínimo 20%')
        axes[1,1].legend()
        axes[1,1].grid(True, alpha=0.3)
        
        # Adicionar valores nas barras
        for bar, valor in zip(bars, margens_previstas):
            axes[1,1].text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.5,
                          f'{valor:.1f}%', ha='center', va='bottom', fontsize=9)
        
        # 6. Lucratividade absoluta prevista (bubble chart)
        qtds_previstas = [previsoes_financeiras[p]['qtd_prevista'] for p in produtos]
        
        scatter = axes[1,2].scatter(qtds_previstas, lucros_previstos, 
                                   s=[m*10 for m in margens_previstas], 
                                   c=margens_previstas, cmap='RdYlGn', 
                                   alpha=0.7, edgecolors='black')
        
        axes[1,2].set_title('🎯 Lucratividade 2025\n(tamanho/cor = margem)', fontweight='bold')
        axes[1,2].set_xlabel('Quantidade Prevista')
        axes[1,2].set_ylabel('Lucro Previsto (R$)')
        axes[1,2].grid(True, alpha=0.3)
        
        # Adicionar labels
        for i, produto in enumerate(produtos):
            axes[1,2].annotate(f'{produto}\n{margens_previstas[i]:.1f}%', 
                              (qtds_previstas[i], lucros_previstos[i]),
                              xytext=(5, 5), textcoords='offset points', fontsize=8)
        
        # Colorbar
        cbar = plt.colorbar(scatter, ax=axes[1,2])
        cbar.set_label('Margem (%)')
        
        plt.tight_layout()
        plt.savefig('output/imagens/previsoes_financeiras_produtos_2025.png', dpi=300, bbox_inches='tight')
        plt.show()
        
    def grafico_previsoes_estatico(self):
        """Gráfico de previsões 2025 - Estático"""
        print("🔮 Gerando Gráfico de Previsões 2025...")
        
        # Importar e executar análise preditiva
        from analise_predicao_vendas import AnalisePredicaoVendas
        analise = AnalisePredicaoVendas(self.df)
        
        # Executar análises silenciosamente (capturar saída)
        import sys
        from io import StringIO
        
        # Capturar saída das análises
        old_stdout = sys.stdout
        sys.stdout = buffer = StringIO()
        
        try:
            produtos_tendencia = analise.previsao_inteligente_produto()
            vendedores_analise = analise.previsao_inteligente_vendedores()  
            previsoes_2025 = analise.media_vendas_2025_inteligente()
        finally:
            sys.stdout = old_stdout
        
        # Criar gráficos
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('🔮 PREVISÕES INTELIGENTES 2025', fontsize=16, fontweight='bold')
        
        # 1. Previsão produtos
        produtos_nomes = list(produtos_tendencia.keys())
        produtos_previsoes = [dados['previsao_2025'] for dados in produtos_tendencia.values()]
        produtos_cores = []
        
        for dados in produtos_tendencia.values():
            if dados['tendencia'] == 'CRESCIMENTO':
                produtos_cores.append('green')
            elif dados['tendencia'] == 'QUEDA':
                produtos_cores.append('red')
            else:
                produtos_cores.append('orange')
        
        bars1 = axes[0,0].bar(produtos_nomes, produtos_previsoes, color=produtos_cores, alpha=0.7)
        axes[0,0].set_title('📈 Previsão Produtos 2025\n(unidades/mês)', fontweight='bold')
        axes[0,0].set_ylabel('Quantidade Prevista')
        axes[0,0].tick_params(axis='x', rotation=45)
        
        # Adicionar valores
        for bar in bars1:
            height = bar.get_height()
            axes[0,0].text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                          f'{int(height)}', ha='center', va='bottom')
        
        # 2. Previsão vendedores
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
        
        bars2 = axes[0,1].bar(vendedores_nomes, vendedores_previsoes, color=vendedores_cores, alpha=0.7)
        axes[0,1].set_title('🚀 Previsão Vendedores 2025\n(unidades/trimestre)', fontweight='bold')
        axes[0,1].set_ylabel('Quantidade Prevista')
        axes[0,1].tick_params(axis='x', rotation=45)
        
        # Adicionar valores
        for bar in bars2:
            height = bar.get_height()
            axes[0,1].text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                          f'{int(height)}', ha='center', va='bottom')
        
        # 3. Histórico vs Previsão
        historico_vendedores = self.df.groupby('Vendedor')['Qtd_Vendida'].sum() / len(self.df['Ano'].unique())
        previsao_vendedores_valores = [previsoes_2025[vend]['previsao'] for vend in historico_vendedores.index]
        
        x = np.arange(len(historico_vendedores))
        width = 0.35
        
        axes[1,0].bar(x - width/2, historico_vendedores.values, width, 
                     label='Histórico', alpha=0.8, color='lightblue')
        axes[1,0].bar(x + width/2, previsao_vendedores_valores, width, 
                     label='Previsão 2025', alpha=0.8, color='orange')
        
        axes[1,0].set_xlabel('Vendedores')
        axes[1,0].set_ylabel('Vendas Anuais')
        axes[1,0].set_title('📊 Histórico vs Previsão 2025', fontweight='bold')
        axes[1,0].set_xticks(x)
        axes[1,0].set_xticklabels(historico_vendedores.index, rotation=45)
        axes[1,0].legend()
        
        # 4. Share de mercado previsto
        total_previsto = sum([dados['previsao'] for dados in previsoes_2025.values()])
        shares = [(dados['previsao']/total_previsto)*100 for dados in previsoes_2025.values()]
        vendedores_order = list(previsoes_2025.keys())
        
        axes[1,1].pie(shares, labels=vendedores_order, autopct='%1.1f%%', startangle=90)
        axes[1,1].set_title('🥧 Share de Mercado\nPrevisto 2025', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('output/imagens/previsoes_2025.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def dashboard_interativo_completo(self):
        """Dashboard interativo completo"""
        print("🌐 Gerando Dashboard Interativo...")
        
        # Dashboard principal
        fig = make_subplots(
            rows=3, cols=3,
            subplot_titles=['📊 Top Produtos', '👥 Performance Vendedores', '🗺️ Vendas por Região',
                           '📈 Evolução Temporal', '🌡️ Sazonalidade', '💰 Receita vs Lucro',
                           '🔮 Previsão Produtos 2025', '🚀 Previsão Vendedores 2025', '📋 Resumo Financeiro'],
            specs=[[{"type": "bar"}, {"type": "bar"}, {"type": "pie"}],
                   [{"secondary_y": True}, {"type": "bar"}, {"type": "scatter"}],
                   [{"type": "bar"}, {"type": "bar"}, {"type": "indicator"}]]
        )
        
        # 1. Top produtos
        produto_qtd = self.df.groupby('Produto')['Qtd_Vendida'].sum().sort_values(ascending=False)
        fig.add_trace(
            go.Bar(x=produto_qtd.index, y=produto_qtd.values, name='Produtos',
                  marker_color=self.cores_produtos[0]),
            row=1, col=1
        )
        
        # 2. Performance vendedores
        vendedor_qtd = self.df.groupby('Vendedor')['Qtd_Vendida'].sum().sort_values(ascending=False)
        fig.add_trace(
            go.Bar(x=vendedor_qtd.index, y=vendedor_qtd.values, name='Vendedores',
                  marker_color=self.cores_vendedores[0]),
            row=1, col=2
        )
        
        # 3. Vendas por região
        regiao_vendas = self.df.groupby('Regiao')['Qtd_Vendida'].sum()
        fig.add_trace(
            go.Pie(values=regiao_vendas.values, labels=regiao_vendas.index, name="Regiões"),
            row=1, col=3
        )
        
        # 4. Evolução temporal
        dados_temporais = self.df.groupby('Data_Str').agg({
            'Qtd_Vendida': 'sum',
            'Receita': 'sum'
        }).reset_index()
        
        fig.add_trace(
            go.Scatter(x=dados_temporais['Data_Str'], y=dados_temporais['Qtd_Vendida'],
                      mode='lines+markers', name='Quantidade', line=dict(color='blue')),
            row=2, col=1
        )
        
        # 5. Sazonalidade
        sazonalidade = self.df.groupby('Mes_Nome')['Qtd_Vendida'].sum().reindex(
            ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        )
        fig.add_trace(
            go.Bar(x=sazonalidade.index, y=sazonalidade.values, name='Sazonalidade',
                  marker_color='orange'),
            row=2, col=2
        )
        
        # 6. Receita vs Lucro
        dados_financeiros = self.df.groupby('Produto').agg({'Receita': 'sum', 'Lucro': 'sum'}).reset_index()
        fig.add_trace(
            go.Scatter(x=dados_financeiros['Receita'], y=dados_financeiros['Lucro'],
                      mode='markers+text', text=dados_financeiros['Produto'],
                      textposition='top center', name='Produtos'),
            row=2, col=3
        )
        
        # Análise preditiva (silenciosa)
        from analise_predicao_vendas import AnalisePredicaoVendas
        analise = AnalisePredicaoVendas(self.df)
        
        import sys
        from io import StringIO
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        try:
            produtos_tendencia = analise.previsao_inteligente_produto()
            vendedores_analise = analise.previsao_inteligente_vendedores()
        finally:
            sys.stdout = old_stdout
        
        # 7. Previsão produtos 2025
        produtos_nomes = list(produtos_tendencia.keys())
        produtos_previsoes = [dados['previsao_2025'] for dados in produtos_tendencia.values()]
        fig.add_trace(
            go.Bar(x=produtos_nomes, y=produtos_previsoes, name='Previsão Produtos',
                  marker_color='green'),
            row=3, col=1
        )
        
        # 8. Previsão vendedores 2025
        vendedores_nomes = list(vendedores_analise.keys())
        vendedores_previsoes = [dados['previsao_2025'] for dados in vendedores_analise.values()]
        fig.add_trace(
            go.Bar(x=vendedores_nomes, y=vendedores_previsoes, name='Previsão Vendedores',
                  marker_color='purple'),
            row=3, col=2
        )
        
        # 9. Resumo financeiro
        receita_total = self.df['Receita'].sum()
        fig.add_trace(
            go.Indicator(
                mode = "number",
                value = receita_total,
                title = {"text": "Receita Total (R$)"},
                number = {'prefix': "R$ ", 'valueformat': ',.0f'}
            ),
            row=3, col=3
        )
        
        # Layout
        fig.update_layout(
            title_text="🎨 DASHBOARD COMPLETO DE VENDAS",
            title_x=0.5,
            height=1200,
            showlegend=False,
            font=dict(size=10)
        )
        
        # Salvar
        caminho_arquivo = "output/html_interativos/dashboard_completo.html"
        garantir_diretorio(caminho_arquivo)
        fig.write_html(caminho_arquivo)
        fig.show()
    
    def relatorio_visual_completo(self):
        """Gera relatório visual completo"""
        print("📈 GERANDO RELATÓRIO VISUAL COMPLETO")
        print("=" * 60)
        
        # Estatísticas gerais
        print(f"📊 Período: {self.df['Data'].min().strftime('%d/%m/%Y')} a {self.df['Data'].max().strftime('%d/%m/%Y')}")
        print(f"📊 Total vendido: {self.df['Qtd_Vendida'].sum():,} unidades")
        print(f"📊 Receita total: R$ {self.df['Receita'].sum():,.2f}")
        print(f"📊 Lucro total: R$ {self.df['Lucro'].sum():,.2f}")
        print()
        
        # Gerar todos os gráficos
        print("1️⃣ Dashboard Geral de Vendas...")
        self.dashboard_vendas_gerais()
        
        print("2️⃣ Heatmap de Performance...")
        self.heatmap_performance()
        
        print("3️⃣ Análise Financeira Detalhada...")
        self.analise_financeira_detalhada()
        
        print("4️⃣ Previsões Financeiras Inteligentes...")
        self.previsoes_financeiras_inteligentes()
        
        print("5️⃣ Previsões Financeiras por Produto 2025...")
        self.previsoes_financeiras_produtos_2025()
        
        print("6️⃣ Previsões 2025...")
        self.grafico_previsoes_estatico()
        
        print("7️⃣ Dashboard Interativo...")
        self.dashboard_interativo_completo()
        
        # Criar índice HTML
        self.criar_indice_html()
        
        print("\n✅ RELATÓRIO VISUAL COMPLETO GERADO!")
        print("📁 Arquivos criados:")
        print("   �️  Imagens (PNG): output/imagens/")
        print("   📄 HTML Estáticos: output/html_estaticos/")
        print("   🌐 HTML Interativos: output/html_interativos/")
        print("   📋 Índice principal: output/index_dashboard.html")
        print("\n💡 Abra output/index_dashboard.html no navegador para acessar tudo!")
    
    def criar_indice_html(self):
        """Cria página HTML principal com links para todos os gráficos"""
        html_content = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📊 Dashboard de Vendas - Análise Completa</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.1);
            padding: 30px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }
        h1 {
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }
        .card {
            background: rgba(255, 255, 255, 0.2);
            padding: 25px;
            border-radius: 10px;
            text-align: center;
            transition: transform 0.3s ease;
            border: 1px solid rgba(255, 255, 255, 0.3);
        }
        .card:hover {
            transform: translateY(-5px);
            background: rgba(255, 255, 255, 0.3);
        }
        .card h3 {
            margin-top: 0;
            font-size: 1.5em;
        }
        .btn {
            display: inline-block;
            padding: 12px 25px;
            background: rgba(255, 255, 255, 0.2);
            color: white;
            text-decoration: none;
            border-radius: 25px;
            margin: 10px;
            transition: all 0.3s ease;
            border: 2px solid rgba(255, 255, 255, 0.3);
        }
        .btn:hover {
            background: rgba(255, 255, 255, 0.4);
            transform: scale(1.05);
        }
        .stats {
            background: rgba(255, 255, 255, 0.15);
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            text-align: center;
        }
        .stat-item {
            display: inline-block;
            margin: 0 20px;
            padding: 10px;
        }
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            display: block;
        }
        .footer {
            text-align: center;
            margin-top: 40px;
            opacity: 0.8;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Dashboard de Vendas - Análise Completa</h1>
        
        <div class="stats">
            <div class="stat-item">
                <span class="stat-number">""" + f"{self.df['Qtd_Vendida'].sum():,}" + """</span>
                <span>Unidades Vendidas</span>
            </div>
            <div class="stat-item">
                <span class="stat-number">R$ """ + f"{self.df['Receita'].sum():,.0f}" + """</span>
                <span>Receita Total</span>
            </div>
            <div class="stat-item">
                <span class="stat-number">""" + f"{self.df['Produto'].nunique()}" + """</span>
                <span>Produtos</span>
            </div>
            <div class="stat-item">
                <span class="stat-number">""" + f"{self.df['Vendedor'].nunique()}" + """</span>
                <span>Vendedores</span>
            </div>
        </div>

        <div class="grid">
            <div class="card">
                <h3>📊 Dashboard Geral</h3>
                <p>Visão geral de produtos, vendedores e performance</p>
                <a href="imagens/dashboard_vendas_gerais.png" class="btn" target="_blank">Ver Gráfico</a>
            </div>

            <div class="card">
                <h3>🔥 Heatmap Performance</h3>
                <p>Análise de performance vendedor × produto</p>
                <a href="imagens/heatmap_performance.png" class="btn" target="_blank">Ver Heatmap</a>
            </div>

            <div class="card">
                <h3>🔮 Previsões 2025</h3>
                <p>Análise preditiva para produtos e vendedores</p>
                <a href="imagens/previsoes_2025.png" class="btn" target="_blank">Ver Previsões</a>
            </div>

            <div class="card">
                <h3>🌐 Dashboard Interativo</h3>
                <p>Dashboard completo com gráficos interativos</p>
                <a href="html_interativos/dashboard_completo.html" class="btn" target="_blank">Abrir Dashboard</a>
            </div>

            <div class="card">
                <h3>📈 Análise Básica</h3>
                <p>Execute análise básica de vendas</p>
                <a href="#" onclick="alert('Execute: python analise_vendas.py')" class="btn">Ver Código</a>
            </div>

            <div class="card">
                <h3>🧠 Análise Preditiva</h3>
                <p>Execute análise preditiva avançada</p>
                <a href="#" onclick="alert('Execute: python analise_predicao_vendas.py')" class="btn">Ver Código</a>
            </div>
        </div>

        <div class="footer">
            <p>🎨 Gerado automaticamente pelo Sistema de Análise de Vendas</p>
            <p>📅 """ + datetime.now().strftime('%d/%m/%Y %H:%M') + """</p>
        </div>
    </div>
</body>
</html>
        """
        
        with open('output/index_dashboard.html', 'w', encoding='utf-8') as f:
            f.write(html_content)

def main():
    """Função principal"""
    print("🎨 SISTEMA COMPLETO DE VISUALIZAÇÃO DE VENDAS")
    print("=" * 60)
    
    # Carregar dados
    try:
        df = pd.read_csv('datasets/vendas.csv')
        print(f"✅ Dados carregados: {len(df)} registros")
    except FileNotFoundError:
        print("❌ Erro: Arquivo datasets/vendas.csv não encontrado!")
        return
    
    # Criar dashboard
    dashboard = DashboardCompleto(df)
    
    # Gerar relatório completo
    dashboard.relatorio_visual_completo()

if __name__ == "__main__":
    main()