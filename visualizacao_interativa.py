# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.io as pio
from datetime import datetime
import warnings
import sys
import os

# Configurar encoding UTF-8 para Windows
if sys.platform == "win32":
    os.system("chcp 65001 > nul")

warnings.filterwarnings('ignore')

# Configurar tema
pio.templates.default = "plotly_white"

def garantir_diretorio(caminho_arquivo):
    """Garante que o diretório do arquivo existe, criando se necessário"""
    diretorio = os.path.dirname(caminho_arquivo)
    if diretorio and not os.path.exists(diretorio):
        os.makedirs(diretorio, exist_ok=True)
        print(f"📁 Diretório criado: {diretorio}")

class VisualizacaoInterativa:
    def __init__(self, df):
        self.df = df.copy()
        self.preparar_dados()
        
        # Configurar cores personalizadas
        self.cores_produtos = px.colors.qualitative.Set3
        self.cores_vendedores = px.colors.qualitative.Pastel
        self.cores_regioes = px.colors.qualitative.Safe
    
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
        self.df['Data_Str'] = self.df['Ano_Mes'].astype(str)
    
    def grafico_produtos_interativo(self):
        """Gráfico interativo de produtos"""
        # Dados
        produto_dados = self.df.groupby('Produto').agg({
            'Qtd_Vendida': 'sum',
            'Receita': 'sum',
            'Lucro': 'sum'
        }).reset_index()
        
        # Criar subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=['📊 Quantidade Vendida', '💰 Receita Total', '💸 Lucro Total', '📈 Receita vs Quantidade'],
            specs=[[{"type": "bar"}, {"type": "bar"}],
                   [{"type": "bar"}, {"type": "scatter"}]]
        )
        
        # Gráfico 1: Quantidade
        fig.add_trace(
            go.Bar(x=produto_dados['Produto'], y=produto_dados['Qtd_Vendida'],
                  name='Quantidade', marker_color=self.cores_produtos[0],
                  text=produto_dados['Qtd_Vendida'], textposition='outside'),
            row=1, col=1
        )
        
        # Gráfico 2: Receita
        fig.add_trace(
            go.Bar(x=produto_dados['Produto'], y=produto_dados['Receita'],
                  name='Receita', marker_color=self.cores_produtos[1],
                  text=[f'R$ {x:,.0f}' for x in produto_dados['Receita']], textposition='outside'),
            row=1, col=2
        )
        
        # Gráfico 3: Lucro
        fig.add_trace(
            go.Bar(x=produto_dados['Produto'], y=produto_dados['Lucro'],
                  name='Lucro', marker_color=self.cores_produtos[2],
                  text=[f'R$ {x:,.0f}' for x in produto_dados['Lucro']], textposition='outside'),
            row=2, col=1
        )
        
        # Gráfico 4: Scatter Receita vs Quantidade
        fig.add_trace(
            go.Scatter(x=produto_dados['Qtd_Vendida'], y=produto_dados['Receita'],
                      mode='markers+text', text=produto_dados['Produto'],
                      textposition='top center', marker=dict(size=15, color=self.cores_produtos[3]),
                      name='Produtos'),
            row=2, col=2
        )
        
        # Layout
        fig.update_layout(
            title_text="🏆 ANÁLISE COMPLETA DE PRODUTOS",
            title_x=0.5,
            showlegend=False,
            height=800,
            font=dict(size=12)
        )
        
        # Salvar
        caminho_arquivo = "output/html_interativos/produtos_interativo.html"
        garantir_diretorio(caminho_arquivo)
        fig.write_html(caminho_arquivo)
        fig.show()
        
        return fig
    
    def grafico_vendedores_interativo(self):
        """Gráfico interativo de vendedores"""
        # Dados por vendedor
        vendedor_dados = self.df.groupby('Vendedor').agg({
            'Qtd_Vendida': 'sum',
            'Receita': 'sum',
            'Lucro': 'sum'
        }).reset_index()
        
        # Dados mensais por vendedor para linha do tempo
        vendas_mensais = self.df.groupby(['Data_Str', 'Vendedor'])['Qtd_Vendida'].sum().reset_index()
        
        # Criar subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=['👥 Performance por Vendedor', '📈 Evolução Temporal', '🥧 Share de Vendas', '💰 Receita por Vendedor'],
            specs=[[{"type": "bar"}, {"type": "scatter"}],
                   [{"type": "pie"}, {"type": "bar"}]]
        )
        
        # Gráfico 1: Barras vendedor
        fig.add_trace(
            go.Bar(x=vendedor_dados['Vendedor'], y=vendedor_dados['Qtd_Vendida'],
                  name='Quantidade', marker_color=self.cores_vendedores,
                  text=vendedor_dados['Qtd_Vendida'], textposition='outside'),
            row=1, col=1
        )
        
        # Gráfico 2: Linha temporal por vendedor
        for i, vendedor in enumerate(self.df['Vendedor'].unique()):
            dados_vendedor = vendas_mensais[vendas_mensais['Vendedor'] == vendedor]
            fig.add_trace(
                go.Scatter(x=dados_vendedor['Data_Str'], y=dados_vendedor['Qtd_Vendida'],
                          mode='lines+markers', name=vendedor, 
                          line=dict(color=self.cores_vendedores[i % len(self.cores_vendedores)])),
                row=1, col=2
            )
        
        # Gráfico 3: Pizza share
        fig.add_trace(
            go.Pie(values=vendedor_dados['Qtd_Vendida'], labels=vendedor_dados['Vendedor'],
                   name="Share", marker=dict(colors=self.cores_vendedores)),
            row=2, col=1
        )
        
        # Gráfico 4: Receita por vendedor
        fig.add_trace(
            go.Bar(x=vendedor_dados['Vendedor'], y=vendedor_dados['Receita'],
                  name='Receita', marker_color=self.cores_vendedores,
                  text=[f'R$ {x:,.0f}' for x in vendedor_dados['Receita']], textposition='outside'),
            row=2, col=2
        )
        
        # Layout
        fig.update_layout(
            title_text="👥 ANÁLISE COMPLETA DE VENDEDORES",
            title_x=0.5,
            height=800,
            font=dict(size=12)
        )
        
        # Remover eixo x do gráfico de linha para melhor visualização
        fig.update_xaxes(tickangle=45, row=1, col=2)
        
        # Salvar
        caminho_arquivo = "output/html_interativos/vendedores_interativo.html"
        garantir_diretorio(caminho_arquivo)
        fig.write_html(caminho_arquivo)
        fig.show()
        
        return fig
    
    def dashboard_temporal_interativo(self):
        """Dashboard temporal interativo"""
        # Dados temporais
        dados_temporais = self.df.groupby('Data_Str').agg({
            'Qtd_Vendida': 'sum',
            'Receita': 'sum',
            'Lucro': 'sum'
        }).reset_index()
        
        # Dados anuais
        dados_anuais = self.df.groupby('Ano').agg({
            'Qtd_Vendida': 'sum',
            'Receita': 'sum'
        }).reset_index()
        
        # Sazonalidade
        sazonalidade = self.df.groupby('Mes_Nome')['Qtd_Vendida'].sum().reset_index()
        ordem_meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
                      'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        sazonalidade['Mes_Nome'] = pd.Categorical(sazonalidade['Mes_Nome'], categories=ordem_meses, ordered=True)
        sazonalidade = sazonalidade.sort_values('Mes_Nome')
        
        # Criar subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=['📅 Evolução Mensal', '📊 Vendas Anuais', '🌡️ Sazonalidade', '💰 Receita vs Lucro'],
            specs=[[{"secondary_y": True}, {"type": "bar"}],
                   [{"type": "bar"}, {"type": "scatter"}]]
        )
        
        # Gráfico 1: Evolução mensal (com eixo duplo)
        fig.add_trace(
            go.Scatter(x=dados_temporais['Data_Str'], y=dados_temporais['Qtd_Vendida'],
                      mode='lines+markers', name='Quantidade', line=dict(color='blue')),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(x=dados_temporais['Data_Str'], y=dados_temporais['Receita'],
                      mode='lines+markers', name='Receita', line=dict(color='red'),
                      yaxis='y2'),
            row=1, col=1
        )
        
        # Gráfico 2: Vendas anuais
        fig.add_trace(
            go.Bar(x=dados_anuais['Ano'].astype(str), y=dados_anuais['Qtd_Vendida'],
                  name='Vendas Anuais', marker_color='lightblue',
                  text=dados_anuais['Qtd_Vendida'], textposition='outside'),
            row=1, col=2
        )
        
        # Gráfico 3: Sazonalidade
        fig.add_trace(
            go.Bar(x=sazonalidade['Mes_Nome'], y=sazonalidade['Qtd_Vendida'],
                  name='Sazonalidade', marker_color='orange',
                  text=sazonalidade['Qtd_Vendida'], textposition='outside'),
            row=2, col=1
        )
        
        # Gráfico 4: Receita vs Lucro por período
        fig.add_trace(
            go.Scatter(x=dados_temporais['Receita'], y=dados_temporais['Lucro'],
                      mode='markers', name='Períodos',
                      marker=dict(size=10, color='green'),
                      text=dados_temporais['Data_Str']),
            row=2, col=2
        )
        
        # Layout
        fig.update_layout(
            title_text="📈 DASHBOARD TEMPORAL INTERATIVO",
            title_x=0.5,
            height=800,
            font=dict(size=12)
        )
        
        # Configurar eixo duplo
        fig.update_yaxes(title_text="Quantidade", row=1, col=1)
        fig.update_yaxes(title_text="Receita (R$)", secondary_y=True, row=1, col=1)
        
        # Salvar
        caminho_arquivo = "output/html_interativos/dashboard_temporal.html"
        garantir_diretorio(caminho_arquivo)
        fig.write_html(caminho_arquivo)
        fig.show()
        
        return fig
    
    def heatmap_vendedor_produto_interativo(self):
        """Heatmap interativo vendedor vs produto"""
        # Dados para heatmap
        heatmap_data = self.df.groupby(['Vendedor', 'Produto'])['Qtd_Vendida'].sum().reset_index()
        heatmap_pivot = heatmap_data.pivot(index='Vendedor', columns='Produto', values='Qtd_Vendida').fillna(0)
        
        # Criar heatmap
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_pivot.values,
            x=heatmap_pivot.columns,
            y=heatmap_pivot.index,
            colorscale='Viridis',
            text=heatmap_pivot.values,
            texttemplate="%{text}",
            textfont={"size": 12},
            hoverongaps=False
        ))
        
        fig.update_layout(
            title="🔥 HEATMAP: VENDEDOR × PRODUTO",
            title_x=0.5,
            xaxis_title="Produtos",
            yaxis_title="Vendedores",
            font=dict(size=12),
            height=500
        )
        
        # Salvar
        caminho_arquivo = "output/html_interativos/heatmap_vendedor_produto.html"
        garantir_diretorio(caminho_arquivo)
        fig.write_html(caminho_arquivo)
        fig.show()
        
        return fig
    
    def grafico_previsoes_interativo(self):
        """Gráfico interativo das previsões"""
        from analise_predicao_vendas import AnalisePredicaoVendas
        
        # Obter previsões
        analise = AnalisePredicaoVendas(self.df)
        produtos_tendencia = analise.previsao_inteligente_produto()
        vendedores_analise = analise.previsao_inteligente_vendedores()
        previsoes_2025 = analise.media_vendas_2025_inteligente()
        
        # Criar subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=['🔮 Previsão Produtos 2025', '🚀 Previsão Vendedores 2025', 
                           '📊 Histórico vs Previsão', '🎯 Intervalos de Confiança'],
            specs=[[{"type": "bar"}, {"type": "bar"}],
                   [{"type": "bar"}, {"type": "scatter"}]]
        )
        
        # Dados dos produtos
        produtos_nomes = list(produtos_tendencia.keys())
        produtos_previsoes = [dados['previsao_2025'] for dados in produtos_tendencia.values()]
        produtos_cores_tend = []
        for dados in produtos_tendencia.values():
            if dados['tendencia'] == 'CRESCIMENTO':
                produtos_cores_tend.append('green')
            elif dados['tendencia'] == 'QUEDA':
                produtos_cores_tend.append('red')
            else:
                produtos_cores_tend.append('orange')
        
        # Gráfico 1: Previsão produtos
        fig.add_trace(
            go.Bar(x=produtos_nomes, y=produtos_previsoes,
                  name='Previsão Produtos', marker_color=produtos_cores_tend,
                  text=[f'{int(x)}' for x in produtos_previsoes], textposition='outside'),
            row=1, col=1
        )
        
        # Dados dos vendedores
        vendedores_nomes = list(vendedores_analise.keys())
        vendedores_previsoes = [dados['previsao_2025'] for dados in vendedores_analise.values()]
        vendedores_cores_tend = []
        for dados in vendedores_analise.values():
            if 'CRESCIMENTO' in dados['tendencia']:
                vendedores_cores_tend.append('green')
            elif 'QUEDA' in dados['tendencia']:
                vendedores_cores_tend.append('red')
            else:
                vendedores_cores_tend.append('orange')
        
        # Gráfico 2: Previsão vendedores
        fig.add_trace(
            go.Bar(x=vendedores_nomes, y=vendedores_previsoes,
                  name='Previsão Vendedores', marker_color=vendedores_cores_tend,
                  text=[f'{int(x)}' for x in vendedores_previsoes], textposition='outside'),
            row=1, col=2
        )
        
        # Dados histórico vs previsão
        historico_vendedores = self.df.groupby('Vendedor')['Qtd_Vendida'].sum() / len(self.df['Ano'].unique())
        previsao_vendedores_valores = [previsoes_2025[vend]['previsao'] for vend in historico_vendedores.index]
        
        # Gráfico 3: Histórico vs Previsão
        x = list(range(len(historico_vendedores)))
        fig.add_trace(
            go.Bar(x=historico_vendedores.index, y=historico_vendedores.values,
                  name='Histórico', marker_color='lightblue', opacity=0.8),
            row=2, col=1
        )
        fig.add_trace(
            go.Bar(x=historico_vendedores.index, y=previsao_vendedores_valores,
                  name='Previsão 2025', marker_color='orange', opacity=0.8),
            row=2, col=1
        )
        
        # Gráfico 4: Intervalos de confiança
        vendedores_order = list(previsoes_2025.keys())
        previsoes_values = [previsoes_2025[v]['previsao'] for v in vendedores_order]
        limite_inf = [previsoes_2025[v]['limite_inferior'] for v in vendedores_order]
        limite_sup = [previsoes_2025[v]['limite_superior'] for v in vendedores_order]
        
        fig.add_trace(
            go.Scatter(x=vendedores_order, y=previsoes_values,
                      error_y=dict(
                          type='data',
                          symmetric=False,
                          array=[sup - prev for sup, prev in zip(limite_sup, previsoes_values)],
                          arrayminus=[prev - inf for prev, inf in zip(previsoes_values, limite_inf)]
                      ),
                      mode='markers', name='Intervalos 95%', marker=dict(size=10)),
            row=2, col=2
        )
        
        # Layout
        fig.update_layout(
            title_text="🔮 PREVISÕES INTELIGENTES 2025",
            title_x=0.5,
            height=800,
            font=dict(size=12)
        )
        
        # Salvar
        caminho_arquivo = "output/html_interativos/previsoes_interativo.html"
        garantir_diretorio(caminho_arquivo)
        fig.write_html(caminho_arquivo)
        fig.show()
        
        return fig
    
    def analise_financeira_interativa(self):
        """Dashboard interativo de análise financeira"""
        print("💰 Gerando análise financeira interativa...")
        
        # Calcular dados financeiros
        self.df['Custo'] = self.df['Receita'] - self.df['Lucro']
        self.df['Margem_%'] = (self.df['Lucro'] / self.df['Receita']) * 100
        self.df['ROI_%'] = (self.df['Lucro'] / self.df['Custo']) * 100
        
        # Dados agregados por produto
        dados_produto = self.df.groupby('Produto').agg({
            'Receita': 'sum',
            'Lucro': 'sum',
            'Custo': 'sum',
            'Qtd_Vendida': 'sum'
        }).reset_index()
        dados_produto['Margem_%'] = (dados_produto['Lucro'] / dados_produto['Receita']) * 100
        dados_produto['ROI_%'] = (dados_produto['Lucro'] / dados_produto['Custo']) * 100
        dados_produto['Lucro_Unitario'] = dados_produto['Lucro'] / dados_produto['Qtd_Vendida']
        dados_produto['Custo_Unitario'] = dados_produto['Custo'] / dados_produto['Qtd_Vendida']
        
        # Dados temporais
        evolucao_temporal = self.df.groupby('Data_Str').agg({
            'Receita': 'sum',
            'Lucro': 'sum',
            'Custo': 'sum'
        }).reset_index()
        evolucao_temporal['Margem_%'] = (evolucao_temporal['Lucro'] / evolucao_temporal['Receita']) * 100
        
        # Criar dashboard
        fig = make_subplots(
            rows=3, cols=2,
            subplot_titles=[
                '💰 Receita vs Lucro vs Custo por Produto',
                '📊 Margem de Lucro por Produto (%)',
                '📈 Evolução Financeira Temporal',
                '🎯 ROI por Produto (%)',
                '🔢 Análise Unitária',
                '💡 Volume vs Lucratividade'
            ],
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # 1. Receita vs Lucro vs Custo
        fig.add_trace(go.Bar(
            name='Receita',
            x=dados_produto['Produto'],
            y=dados_produto['Receita'],
            marker_color='blue',
            opacity=0.8,
            hovertemplate='<b>%{x}</b><br>Receita: R$ %{y:,.0f}<extra></extra>'
        ), row=1, col=1)
        
        fig.add_trace(go.Bar(
            name='Custo',
            x=dados_produto['Produto'],
            y=dados_produto['Custo'],
            marker_color='red',
            opacity=0.8,
            hovertemplate='<b>%{x}</b><br>Custo: R$ %{y:,.0f}<extra></extra>'
        ), row=1, col=1)
        
        fig.add_trace(go.Bar(
            name='Lucro',
            x=dados_produto['Produto'],
            y=dados_produto['Lucro'],
            marker_color='green',
            opacity=0.8,
            hovertemplate='<b>%{x}</b><br>Lucro: R$ %{y:,.0f}<extra></extra>'
        ), row=1, col=1)
        
        # 2. Margem de lucro
        cores_margem = ['green' if m >= 30 else 'orange' if m >= 20 else 'red' for m in dados_produto['Margem_%']]
        fig.add_trace(go.Bar(
            name='Margem (%)',
            x=dados_produto['Produto'],
            y=dados_produto['Margem_%'],
            marker_color=cores_margem,
            opacity=0.8,
            hovertemplate='<b>%{x}</b><br>Margem: %{y:.1f}%<extra></extra>',
            showlegend=False
        ), row=1, col=2)
        
        # Linha de meta
        fig.add_hline(y=30, line_dash="dash", line_color="green", 
                     annotation_text="Meta 30%", row=1, col=2)
        fig.add_hline(y=20, line_dash="dash", line_color="orange", 
                     annotation_text="Mínimo 20%", row=1, col=2)
        
        # 3. Evolução temporal
        fig.add_trace(go.Scatter(
            name='Receita Temporal',
            x=evolucao_temporal['Data_Str'],
            y=evolucao_temporal['Receita'],
            mode='lines+markers',
            line=dict(color='blue', width=3),
            hovertemplate='<b>%{x}</b><br>Receita: R$ %{y:,.0f}<extra></extra>'
        ), row=2, col=1)
        
        fig.add_trace(go.Scatter(
            name='Custo Temporal',
            x=evolucao_temporal['Data_Str'],
            y=evolucao_temporal['Custo'],
            mode='lines+markers',
            line=dict(color='red', width=3),
            hovertemplate='<b>%{x}</b><br>Custo: R$ %{y:,.0f}<extra></extra>'
        ), row=2, col=1)
        
        fig.add_trace(go.Scatter(
            name='Lucro Temporal',
            x=evolucao_temporal['Data_Str'],
            y=evolucao_temporal['Lucro'],
            mode='lines+markers',
            line=dict(color='green', width=3),
            hovertemplate='<b>%{x}</b><br>Lucro: R$ %{y:,.0f}<extra></extra>'
        ), row=2, col=1)
        
        # 4. ROI por produto
        cores_roi = ['green' if roi >= 50 else 'orange' if roi >= 25 else 'red' for roi in dados_produto['ROI_%']]
        fig.add_trace(go.Bar(
            name='ROI (%)',
            x=dados_produto['Produto'],
            y=dados_produto['ROI_%'],
            marker_color=cores_roi,
            opacity=0.8,
            hovertemplate='<b>%{x}</b><br>ROI: %{y:.1f}%<extra></extra>',
            showlegend=False
        ), row=2, col=2)
        
        # Linhas de referência ROI
        fig.add_hline(y=50, line_dash="dash", line_color="green", 
                     annotation_text="Excelente 50%+", row=2, col=2)
        fig.add_hline(y=25, line_dash="dash", line_color="orange", 
                     annotation_text="Bom 25%+", row=2, col=2)
        
        # 5. Análise unitária
        fig.add_trace(go.Bar(
            name='Lucro Unitário',
            x=dados_produto['Produto'],
            y=dados_produto['Lucro_Unitario'],
            marker_color='green',
            opacity=0.8,
            hovertemplate='<b>%{x}</b><br>Lucro Unit.: R$ %{y:.2f}<extra></extra>'
        ), row=3, col=1)
        
        fig.add_trace(go.Bar(
            name='Custo Unitário',
            x=dados_produto['Produto'],
            y=dados_produto['Custo_Unitario'],
            marker_color='red',
            opacity=0.8,
            hovertemplate='<b>%{x}</b><br>Custo Unit.: R$ %{y:.2f}<extra></extra>'
        ), row=3, col=1)
        
        # 6. Volume vs Lucratividade
        fig.add_trace(go.Scatter(
            name='Volume vs Lucro',
            x=dados_produto['Qtd_Vendida'],
            y=dados_produto['Lucro'],
            mode='markers',
            marker=dict(
                size=dados_produto['Margem_%'] * 2,
                color=dados_produto['Margem_%'],
                colorscale='RdYlGn',
                showscale=True,
                colorbar=dict(title="Margem (%)", x=1.02)
            ),
            text=dados_produto['Produto'],
            hovertemplate='<b>%{text}</b><br>' +
                         'Quantidade: %{x}<br>' +
                         'Lucro: R$ %{y:,.0f}<br>' +
                         'Margem: %{marker.color:.1f}%<extra></extra>',
            showlegend=False
        ), row=3, col=2)
        
        # Configurar layout
        fig.update_layout(
            title={
                'text': '💰 DASHBOARD FINANCEIRO INTERATIVO',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24, 'color': 'darkblue'}
            },
            height=1200,
            showlegend=True,
            hovermode='closest',
            plot_bgcolor='rgba(240,240,240,0.3)'
        )
        
        # Atualizar eixos
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
        
        # Salvar
        caminho_arquivo = 'output/html_interativos/analise_financeira_interativa.html'
        garantir_diretorio(caminho_arquivo)
        fig.write_html(caminho_arquivo)
        print("   ✅ output/html_interativos/analise_financeira_interativa.html")
        
        return fig
    
    def dashboard_completo_interativo(self):
        """Cria dashboard completo interativo"""
        print("🎨 Gerando Dashboard Interativo Completo...")
        print("=" * 60)
        
        # Gerar todos os gráficos
        print("📊 1. Análise de Produtos Interativa...")
        self.grafico_produtos_interativo()
        
        print("👥 2. Análise de Vendedores Interativa...")
        self.grafico_vendedores_interativo()
        
        print("📈 3. Dashboard Temporal Interativo...")
        self.dashboard_temporal_interativo()
        
        print("🔥 4. Heatmap Vendedor × Produto...")
        self.heatmap_vendedor_produto_interativo()
        
        print("🔮 5. Análise Financeira Interativa...")
        self.analise_financeira_interativa()
        
        print("🔮 6. Previsões Interativas 2025...")
        self.grafico_previsoes_interativo()
        
        print("\n✅ Dashboard interativo completo gerado!")
        print("🌐 Arquivos HTML criados:")
        print("   - output/html_interativos/produtos_interativo.html")
        print("   - output/html_interativos/vendedores_interativo.html")
        print("   - output/html_interativos/dashboard_temporal.html")
        print("   - output/html_interativos/heatmap_vendedor_produto.html")
        print("   - output/html_interativos/analise_financeira_interativa.html")
        print("   - output/html_interativos/previsoes_interativo.html")
        print("\n💡 Abra os arquivos .html no navegador para interagir com os gráficos!")

def main():
    """Função principal"""
    print("🌐 SISTEMA DE VISUALIZAÇÃO INTERATIVA")
    print("=" * 60)
    
    # Carregar dados
    df = pd.read_csv('datasets/vendas.csv')
    
    # Criar instância da visualização
    viz = VisualizacaoInterativa(df)
    
    # Gerar dashboard completo
    viz.dashboard_completo_interativo()

if __name__ == "__main__":
    main()