# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from scipy import stats
from collections import defaultdict
import warnings
import sys
import os
import io

# Configurar encoding UTF-8 para saída no Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

warnings.filterwarnings('ignore')

def safe_print(*args, **kwargs):
    """Função para print seguro em sistemas Windows com problemas de encoding"""
    import re
    try:
        # Tentar print normal primeiro
        print(*args, **kwargs)
    except UnicodeEncodeError:
        # Se falhar, remover caracteres problemáticos e tentar novamente
        safe_args = []
        for arg in args:
            if isinstance(arg, str):
                # Remover emojis e caracteres Unicode especiais
                clean_arg = re.sub(r'[^\x00-\x7F]+', '', str(arg))
                safe_args.append(clean_arg)
            else:
                safe_args.append(arg)
        print(*safe_args, **kwargs)

class AnalisePredicaoVendas:
    def __init__(self, df):
        self.df = df.copy()
        self.preparar_dados()
    
    def preparar_dados(self):
        """Prepara os dados para análise preditiva inteligente"""
        # Converter data
        self.df['Data'] = pd.to_datetime(self.df['Data'])
        self.df['Ano'] = self.df['Data'].dt.year
        self.df['Mes'] = self.df['Data'].dt.month
        self.df['Trimestre'] = self.df['Data'].dt.quarter
        
        # Criar features para análise
        self.df['Ano_Mes'] = self.df['Data'].dt.to_period('M')
        self.df['Data_Ordinal'] = self.df['Data'].map(lambda x: x.toordinal())
        
        # Normalizar valores para melhor análise
        self.df['Qtd_Norm'] = (self.df['Qtd_Vendida'] - self.df['Qtd_Vendida'].mean()) / self.df['Qtd_Vendida'].std()
        self.df['Receita_Norm'] = (self.df['Receita'] - self.df['Receita'].mean()) / self.df['Receita'].std()
    
    def calcular_conhecimento_historico(self, grupo, metrica='Qtd_Vendida'):
        """Calcula a distribuição histórica para um grupo"""
        dados_grupo = self.df.groupby(grupo)[metrica].sum()
        
        # Parâmetros da distribuição histórica (assumindo distribuição normal)
        media_historica = dados_grupo.mean()
        desvio_historico = dados_grupo.std()
        
        return media_historica, desvio_historico, dados_grupo
    
    def previsao_inteligente_produto(self):
        """Prevê qual produto venderá mais/menos usando análise preditiva inteligente"""
        safe_print("=" * 70)
        safe_print("🔮 PREVISÃO INTELIGENTE - PRODUTOS 2025")
        safe_print("=" * 70)
        
        # Calcular tendências por produto ao longo do tempo
        produtos_tendencia = {}
        
        for produto in self.df['Produto'].unique():
            df_produto = self.df[self.df['Produto'] == produto]
            
            # Agrupar por ano-mês para ver tendência
            vendas_mensais = df_produto.groupby('Ano_Mes')['Qtd_Vendida'].sum().reset_index()
            vendas_mensais['Periodo_Num'] = range(len(vendas_mensais))
            
            # Calcular correlação com tempo (tendência)
            if len(vendas_mensais) > 1:
                correlacao = np.corrcoef(vendas_mensais['Periodo_Num'], vendas_mensais['Qtd_Vendida'])[0,1]
                
                # Análise inteligente para média futura
                media_historica = vendas_mensais['Qtd_Vendida'].mean()
                desvio_historico = vendas_mensais['Qtd_Vendida'].std()
                
                # Usando distribuição normal como conhecimento base
                # Resultado final = evidência atual * conhecimento histórico
                n_observacoes = len(vendas_mensais)
                
                # Atualizando conhecimento com evidência (últimos meses têm mais peso)
                pesos_recentes = np.exp(np.linspace(-1, 0, len(vendas_mensais)))
                media_ponderada = np.average(vendas_mensais['Qtd_Vendida'], weights=pesos_recentes)
                
                # Previsão inteligente
                peso_historico = 0.3  # Peso do conhecimento histórico
                previsao_2025 = (peso_historico * media_historica + (1 - peso_historico) * media_ponderada)
                
                produtos_tendencia[produto] = {
                    'correlacao_temporal': correlacao,
                    'media_historica': media_historica,
                    'previsao_2025': previsao_2025,
                    'tendencia': 'CRESCIMENTO' if correlacao > 0.1 else 'QUEDA' if correlacao < -0.1 else 'ESTÁVEL',
                    'confianca': abs(correlacao)
                }
        
        # Ordenar por previsão de vendas
        produtos_ordenados = sorted(produtos_tendencia.items(), 
                                  key=lambda x: x[1]['previsao_2025'], reverse=True)
        
        safe_print("📈 RANKING DE PRODUTOS PARA 2025 (Previsão Inteligente):")
        safe_print("-" * 70)
        
        for i, (produto, dados) in enumerate(produtos_ordenados, 1):
            tendencia_emoji = "📈" if dados['tendencia'] == 'CRESCIMENTO' else "📉" if dados['tendencia'] == 'QUEDA' else "➡️"
            confianca_pct = dados['confianca'] * 100
            
            safe_print(f"{i}. {produto}")
            safe_print(f"   {tendencia_emoji} Tendência: {dados['tendencia']} (Confiança: {confianca_pct:.1f}%)")
            safe_print(f"   🎯 Previsão 2025: {dados['previsao_2025']:.0f} unidades/mês")
            safe_print(f"   📊 Média histórica: {dados['media_historica']:.0f} unidades/mês")
            safe_print()
        
        # Probabilidades estatísticas
        safe_print("🎲 PROBABILIDADES ESTATÍSTICAS:")
        safe_print("-" * 70)
        
        total_previsao = sum([dados['previsao_2025'] for _, dados in produtos_ordenados])
        
        for produto, dados in produtos_ordenados:
            probabilidade = (dados['previsao_2025'] / total_previsao) * 100
            safe_print(f"P({produto} ser o mais vendido) = {probabilidade:.1f}%")
        
        return produtos_tendencia
    
    def previsao_inteligente_vendedores(self):
        """Analisa tendências de crescimento/queda dos vendedores"""
        safe_print("\n" + "=" * 70)
        safe_print("👥 ANÁLISE INTELIGENTE - VENDEDORES 2025")
        safe_print("=" * 70)
        
        vendedores_analise = {}
        
        for vendedor in self.df['Vendedor'].unique():
            df_vendedor = self.df[self.df['Vendedor'] == vendedor]
            
            # Agrupar por trimestre para análise de tendência
            vendas_trimestrais = df_vendedor.groupby(['Ano', 'Trimestre']).agg({
                'Qtd_Vendida': 'sum',
                'Receita': 'sum'
            }).reset_index()
            
            vendas_trimestrais['Periodo'] = range(len(vendas_trimestrais))
            
            # Análise inteligente de tendência
            if len(vendas_trimestrais) > 2:
                # Correlação temporal
                corr_qtd = np.corrcoef(vendas_trimestrais['Periodo'], vendas_trimestrais['Qtd_Vendida'])[0,1]
                corr_receita = np.corrcoef(vendas_trimestrais['Periodo'], vendas_trimestrais['Receita'])[0,1]
                
                # Análise de aceleração (segunda derivada)
                if len(vendas_trimestrais) > 3:
                    vendas_diff = np.diff(vendas_trimestrais['Qtd_Vendida'])
                    aceleracao = np.mean(np.diff(vendas_diff))
                else:
                    aceleracao = 0
                
                # Análise inteligente para performance futura
                # Conhecimento base: performance histórica média
                media_qtd = vendas_trimestrais['Qtd_Vendida'].mean()
                desvio_qtd = vendas_trimestrais['Qtd_Vendida'].std()
                
                # Evidência atual: tendência recente (últimos 4 trimestres)
                ultimos_periodos = vendas_trimestrais.tail(4)
                if len(ultimos_periodos) > 1:
                    tendencia_recente = np.polyfit(range(len(ultimos_periodos)), 
                                                 ultimos_periodos['Qtd_Vendida'], 1)[0]
                else:
                    tendencia_recente = 0
                
                # Previsão final: combinação de conhecimento base e evidência atual
                peso_tendencia = 0.7  # Peso da tendência recente
                previsao_qtd_2025 = media_qtd + (peso_tendencia * tendencia_recente * 4)  # 4 trimestres
                
                # Classificação de tendência
                score_tendencia = (corr_qtd * 0.4) + (tendencia_recente/media_qtd * 0.6)
                
                if score_tendencia > 0.1:
                    tendencia = "FORTE CRESCIMENTO"
                    emoji = "🚀"
                elif score_tendencia > 0.05:
                    tendencia = "CRESCIMENTO"
                    emoji = "📈"
                elif score_tendencia > -0.05:
                    tendencia = "ESTÁVEL"
                    emoji = "➡️"
                elif score_tendencia > -0.1:
                    tendencia = "QUEDA"
                    emoji = "📉"
                else:
                    tendencia = "FORTE QUEDA"
                    emoji = "💥"
                
                vendedores_analise[vendedor] = {
                    'correlacao_qtd': corr_qtd,
                    'correlacao_receita': corr_receita,
                    'tendencia_recente': tendencia_recente,
                    'aceleracao': aceleracao,
                    'media_historica': media_qtd,
                    'previsao_2025': max(0, previsao_qtd_2025),  # Não pode ser negativo
                    'tendencia': tendencia,
                    'emoji': emoji,
                    'score_tendencia': score_tendencia,
                    'confianca': min(abs(score_tendencia) * 10, 1.0)
                }
        
        # Ordenar por previsão de performance
        vendedores_ordenados = sorted(vendedores_analise.items(), 
                                    key=lambda x: x[1]['previsao_2025'], reverse=True)
        
        safe_print("🏆 RANKING DE VENDEDORES PARA 2025:")
        safe_print("-" * 70)
        
        for i, (vendedor, dados) in enumerate(vendedores_ordenados, 1):
            safe_print(f"{i}. {vendedor}")
            safe_print(f"   {dados['emoji']} Tendência: {dados['tendencia']}")
            safe_print(f"   🎯 Previsão 2025: {dados['previsao_2025']:.0f} unidades/trimestre")
            safe_print(f"   📊 Média histórica: {dados['media_historica']:.0f} unidades/trimestre")
            safe_print(f"   🎲 Confiança: {dados['confianca']*100:.1f}%")
            safe_print()
        
        return vendedores_analise
    
    def media_vendas_2025_inteligente(self):
        """Calcula a média de vendas por vendedor para 2025 usando análise preditiva inteligente"""
        safe_print("\n" + "=" * 70)
        safe_print("📊 PREVISÃO DE MÉDIA DE VENDAS POR VENDEDOR - 2025")
        safe_print("=" * 70)
        
        # Análise geral do mercado
        vendas_anuais = self.df.groupby('Ano')['Qtd_Vendida'].sum()
        
        # Tendência geral do mercado
        anos = vendas_anuais.index.values
        vendas = vendas_anuais.values
        
        if len(anos) > 1:
            # Regressão linear para tendência geral
            tendencia_mercado = np.polyfit(anos, vendas, 1)[0]
            
            # Projeção para 2025
            vendas_total_2025 = vendas_anuais.iloc[-1] + tendencia_mercado * (2025 - anos[-1])
        else:
            vendas_total_2025 = vendas_anuais.iloc[-1]
            tendencia_mercado = 0
        
        safe_print(f"📈 Tendência do mercado: {tendencia_mercado:+.0f} unidades/ano")
        safe_print(f"🎯 Previsão total mercado 2025: {vendas_total_2025:,.0f} unidades")
        
        # Análise inteligente por vendedor
        num_vendedores = self.df['Vendedor'].nunique()
        
        # Conhecimento base: distribuição uniforme entre vendedores
        media_base = vendas_total_2025 / num_vendedores
        
        safe_print(f"\n🧮 ANÁLISE INTELIGENTE POR VENDEDOR:")
        safe_print("-" * 70)
        
        previsoes_vendedores = {}
        
        for vendedor in self.df['Vendedor'].unique():
            df_vendedor = self.df[self.df['Vendedor'] == vendedor]
            
            # Performance histórica do vendedor
            vendas_vendedor_anual = df_vendedor.groupby('Ano')['Qtd_Vendida'].sum()
            
            # Calcular share histórico do vendedor
            share_historico = vendas_vendedor_anual.sum() / self.df['Qtd_Vendida'].sum()
            
            # Tendência específica do vendedor
            if len(vendas_vendedor_anual) > 1:
                anos_vendedor = vendas_vendedor_anual.index.values
                vendas_vendedor = vendas_vendedor_anual.values
                tendencia_vendedor = np.polyfit(anos_vendedor, vendas_vendedor, 1)[0]
            else:
                tendencia_vendedor = 0
            
            # Combinação inteligente de informações
            # Conhecimento histórico: share histórico * previsão total
            conhecimento_historico = share_historico * vendas_total_2025
            
            # Evidência atual: tendência específica do vendedor
            ultimo_ano_vendedor = vendas_vendedor_anual.iloc[-1]
            ajuste_tendencia = tendencia_vendedor * (2025 - anos_vendedor[-1])
            evidencia_atual = ultimo_ano_vendedor + ajuste_tendencia
            
            # Previsão final (combinação do conhecimento histórico e evidência atual)
            peso_historico = 0.6  # Peso da performance histórica
            peso_tendencia = 0.4  # Peso da tendência recente
            
            previsao_vendedor = (peso_historico * conhecimento_historico + 
                               peso_tendencia * evidencia_atual)
            
            # Garantir que seja positivo
            previsao_vendedor = max(0, previsao_vendedor)
            
            # Calcular intervalos de confiança estatísticos
            desvio_historico = vendas_vendedor_anual.std() if len(vendas_vendedor_anual) > 1 else vendas_vendedor_anual.iloc[0] * 0.2
            
            # Intervalo de confiança 95%
            margem_erro = 1.96 * desvio_historico
            limite_inferior = max(0, previsao_vendedor - margem_erro)
            limite_superior = previsao_vendedor + margem_erro
            
            previsoes_vendedores[vendedor] = {
                'previsao': previsao_vendedor,
                'share_historico': share_historico,
                'tendencia': tendencia_vendedor,
                'limite_inferior': limite_inferior,
                'limite_superior': limite_superior,
                'media_mensal': previsao_vendedor / 12,
                'media_trimestral': previsao_vendedor / 4
            }
            
            safe_print(f"👤 {vendedor}:")
            safe_print(f"   🎯 Previsão 2025: {previsao_vendedor:,.0f} unidades/ano")
            safe_print(f"   📅 Média mensal: {previsao_vendedor/12:,.0f} unidades")
            safe_print(f"   📅 Média trimestral: {previsao_vendedor/4:,.0f} unidades")
            safe_print(f"   📊 Share previsto: {(previsao_vendedor/vendas_total_2025)*100:.1f}%")
            safe_print(f"   🎲 Intervalo 95%: [{limite_inferior:,.0f} - {limite_superior:,.0f}]")
            safe_print()
        
        return previsoes_vendedores
    
    def analise_probabilidades_produtos(self):
        """Análise de probabilidades condicionais para produtos"""
        safe_print("\n" + "=" * 70)
        safe_print("🎲 ANÁLISE DE PROBABILIDADES CONDICIONAIS - PRODUTOS")
        safe_print("=" * 70)
        
        # P(Produto | Região)
        safe_print("📍 P(Produto | Região):")
        safe_print("-" * 40)
        
        for regiao in self.df['Regiao'].unique():
            df_regiao = self.df[self.df['Regiao'] == regiao]
            vendas_por_produto = df_regiao.groupby('Produto')['Qtd_Vendida'].sum()
            total_regiao = vendas_por_produto.sum()
            
            safe_print(f"\n🗺️  {regiao}:")
            for produto in vendas_por_produto.index:
                prob = (vendas_por_produto[produto] / total_regiao) * 100
                safe_print(f"   {produto}: {prob:.1f}%")
        
        # P(Produto | Vendedor)
        safe_print("\n👥 P(Produto | Vendedor):")
        safe_print("-" * 40)
        
        for vendedor in self.df['Vendedor'].unique():
            df_vendedor = self.df[self.df['Vendedor'] == vendedor]
            vendas_por_produto = df_vendedor.groupby('Produto')['Qtd_Vendida'].sum()
            total_vendedor = vendas_por_produto.sum()
            
            produto_preferido = vendas_por_produto.idxmax()
            prob_max = (vendas_por_produto.max() / total_vendedor) * 100
            
            safe_print(f"👤 {vendedor}: Especialista em {produto_preferido} ({prob_max:.1f}%)")
    
    def gerar_relatorio_completo(self):
        """Gera o relatório completo de análise preditiva inteligente"""
        safe_print("🔬 ANÁLISE PREDITIVA DE VENDAS - RELATÓRIO COMPLETO")
        safe_print("=" * 70)
        safe_print(f"📅 Data da análise: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        safe_print(f"📊 Período dos dados: {self.df['Data'].min().strftime('%d/%m/%Y')} a {self.df['Data'].max().strftime('%d/%m/%Y')}")
        safe_print()
        
        # Executar todas as análises
        produtos_tendencia = self.previsao_inteligente_produto()
        vendedores_analise = self.previsao_inteligente_vendedores()
        previsoes_2025 = self.media_vendas_2025_inteligente()
        previsoes_financeiras = self.previsoes_financeiras_produtos()
        self.analise_probabilidades_produtos()
        
        # Resumo executivo
        safe_print("\n" + "=" * 70)
        safe_print("📋 RESUMO EXECUTIVO - INSIGHTS PREDITIVOS")
        safe_print("=" * 70)
        
        # Produto com maior probabilidade de crescimento
        melhor_produto = max(produtos_tendencia.items(), key=lambda x: x[1]['previsao_2025'])
        safe_print(f"🏆 Produto mais promissor 2025: {melhor_produto[0]}")
        safe_print(f"   Previsão: {melhor_produto[1]['previsao_2025']:.0f} unidades/mês")
        
        # Vendedor com melhor tendência
        melhor_vendedor = max(vendedores_analise.items(), key=lambda x: x[1]['score_tendencia'])
        safe_print(f"🚀 Vendedor em maior crescimento: {melhor_vendedor[0]}")
        safe_print(f"   Tendência: {melhor_vendedor[1]['tendencia']}")
        
        # Total previsto para 2025
        total_previsto = sum([dados['previsao'] for dados in previsoes_2025.values()])
        safe_print(f"🎯 Previsão total 2025: {total_previsto:,.0f} unidades")
        
        safe_print("\n✅ Análise preditiva concluída!")
        
        return {
            'produtos': produtos_tendencia,
            'vendedores': vendedores_analise,
            'previsoes_2025': previsoes_2025,
            'previsoes_financeiras': previsoes_financeiras
        }
    
    def previsoes_financeiras_produtos(self):
        """Prevê custos e lucros baseados nas previsões de vendas por produto"""
        safe_print("=" * 70)
        safe_print("💰 PREVISÕES FINANCEIRAS POR PRODUTO 2025")
        safe_print("=" * 70)
        
        # Primeiro, obter previsões de vendas por produto
        produtos_tendencia = self.previsao_inteligente_produto()
        
        # Calcular médias históricas financeiras por produto
        financeiro_historico = self.df.groupby('Produto').agg({
            'Qtd_Vendida': 'sum',
            'Receita': 'sum',
            'Lucro': 'sum'
        }).reset_index()
        
        # Calcular valores unitários médios históricos
        financeiro_historico['Receita_Unitaria'] = financeiro_historico['Receita'] / financeiro_historico['Qtd_Vendida']
        financeiro_historico['Lucro_Unitario'] = financeiro_historico['Lucro'] / financeiro_historico['Qtd_Vendida']
        financeiro_historico['Custo_Unitario'] = financeiro_historico['Receita_Unitaria'] - financeiro_historico['Lucro_Unitario']
        financeiro_historico['Margem_%'] = (financeiro_historico['Lucro'] / financeiro_historico['Receita']) * 100
        
        previsoes_financeiras = {}
        
        safe_print("📊 ANÁLISE FINANCEIRA POR PRODUTO:")
        safe_print("=" * 50)
        
        for produto in financeiro_historico['Produto']:
            dados_produto = financeiro_historico[financeiro_historico['Produto'] == produto].iloc[0]
            
            # Obter previsão de vendas
            if produto in produtos_tendencia:
                qtd_prevista_2025 = produtos_tendencia[produto]['previsao_2025']
                tendencia_vendas = produtos_tendencia[produto]['tendencia']
            else:
                qtd_prevista_2025 = dados_produto['Qtd_Vendida'] * 1.1  # Crescimento padrão de 10%
                tendencia_vendas = 'ESTÁVEL'
            
            # Calcular valores unitários com ajustes baseados na tendência
            receita_unit_base = dados_produto['Receita_Unitaria']
            lucro_unit_base = dados_produto['Lucro_Unitario']
            custo_unit_base = dados_produto['Custo_Unitario']
            
            # Ajustar valores unitários baseados na tendência e inflação
            if tendencia_vendas == 'CRESCIMENTO':
                # Produtos em crescimento podem ter melhor margem
                fator_ajuste_receita = 1.08  # 8% aumento na receita unitária
                fator_ajuste_custo = 1.05    # 5% aumento no custo (menor que receita)
            elif tendencia_vendas == 'QUEDA':
                # Produtos em queda podem precisar reduzir preços
                fator_ajuste_receita = 0.95  # 5% redução na receita unitária
                fator_ajuste_custo = 1.03    # 3% aumento no custo (inflação)
            else:
                # Produtos estáveis seguem inflação padrão
                fator_ajuste_receita = 1.04  # 4% inflação
                fator_ajuste_custo = 1.04    # 4% inflação
            
            receita_unit_2025 = receita_unit_base * fator_ajuste_receita
            custo_unit_2025 = custo_unit_base * fator_ajuste_custo
            lucro_unit_2025 = receita_unit_2025 - custo_unit_2025
            
            # Calcular totais previstos
            receita_prevista = qtd_prevista_2025 * receita_unit_2025
            custo_previsto = qtd_prevista_2025 * custo_unit_2025
            lucro_previsto = qtd_prevista_2025 * lucro_unit_2025
            margem_prevista = (lucro_previsto / receita_prevista) * 100 if receita_prevista > 0 else 0
            
            # Calcular variações em relação ao histórico
            receita_atual = dados_produto['Receita']
            lucro_atual = dados_produto['Lucro']
            custo_atual = receita_atual - lucro_atual
            
            variacao_receita = ((receita_prevista - receita_atual) / receita_atual) * 100
            variacao_lucro = ((lucro_previsto - lucro_atual) / lucro_atual) * 100
            variacao_custo = ((custo_previsto - custo_atual) / custo_atual) * 100
            
            # Armazenar previsões
            previsoes_financeiras[produto] = {
                'qtd_prevista': qtd_prevista_2025,
                'receita_prevista': receita_prevista,
                'custo_previsto': custo_previsto,
                'lucro_previsto': lucro_previsto,
                'margem_prevista_%': margem_prevista,
                'receita_unitaria_2025': receita_unit_2025,
                'custo_unitario_2025': custo_unit_2025,
                'lucro_unitario_2025': lucro_unit_2025,
                'variacao_receita_%': variacao_receita,
                'variacao_lucro_%': variacao_lucro,
                'variacao_custo_%': variacao_custo,
                'tendencia': tendencia_vendas,
                'historico': {
                    'receita_atual': receita_atual,
                    'lucro_atual': lucro_atual,
                    'custo_atual': custo_atual,
                    'margem_atual_%': dados_produto['Margem_%']
                }
            }
            
            # Exibir análise
            safe_print(f"🏷️  {produto.upper()}")
            safe_print(f"   📈 Quantidade prevista: {qtd_prevista_2025:,.0f} unidades")
            safe_print(f"   💰 Receita prevista: R$ {receita_prevista:,.2f} ({variacao_receita:+.1f}%)")
            safe_print(f"   💸 Custo previsto: R$ {custo_previsto:,.2f} ({variacao_custo:+.1f}%)")
            safe_print(f"   💚 Lucro previsto: R$ {lucro_previsto:,.2f} ({variacao_lucro:+.1f}%)")
            safe_print(f"   📊 Margem prevista: {margem_prevista:.1f}% (atual: {dados_produto['Margem_%']:.1f}%)")
            safe_print(f"   📋 Tendência: {tendencia_vendas}")
            safe_print()
        
        # Análise consolidada
        total_receita_prevista = sum([p['receita_prevista'] for p in previsoes_financeiras.values()])
        total_custo_previsto = sum([p['custo_previsto'] for p in previsoes_financeiras.values()])
        total_lucro_previsto = sum([p['lucro_previsto'] for p in previsoes_financeiras.values()])
        margem_total_prevista = (total_lucro_previsto / total_receita_prevista) * 100
        
        # Histórico total
        total_receita_atual = self.df['Receita'].sum()
        total_lucro_atual = self.df['Lucro'].sum()
        total_custo_atual = total_receita_atual - total_lucro_atual
        
        safe_print("🎯 RESUMO FINANCEIRO CONSOLIDADO 2025:")
        safe_print("=" * 50)
        safe_print(f"💰 Receita total prevista: R$ {total_receita_prevista:,.2f}")
        safe_print(f"💸 Custo total previsto: R$ {total_custo_previsto:,.2f}")
        safe_print(f"💚 Lucro total previsto: R$ {total_lucro_previsto:,.2f}")
        safe_print(f"📊 Margem total prevista: {margem_total_prevista:.1f}%")
        safe_print()
        safe_print("📈 VARIAÇÕES EM RELAÇÃO AO HISTÓRICO:")
        variacao_receita_total = ((total_receita_prevista - total_receita_atual) / total_receita_atual) * 100
        variacao_lucro_total = ((total_lucro_previsto - total_lucro_atual) / total_lucro_atual) * 100
        variacao_custo_total = ((total_custo_previsto - total_custo_atual) / total_custo_atual) * 100
        
        safe_print(f"💰 Receita: {variacao_receita_total:+.1f}%")
        safe_print(f"💸 Custo: {variacao_custo_total:+.1f}%")
        safe_print(f"💚 Lucro: {variacao_lucro_total:+.1f}%")
        
        # Produto mais lucrativo previsto
        produto_mais_lucrativo = max(previsoes_financeiras.items(), key=lambda x: x[1]['lucro_previsto'])
        safe_print(f"\n🏆 Produto mais lucrativo previsto: {produto_mais_lucrativo[0]}")
        safe_print(f"   💚 Lucro: R$ {produto_mais_lucrativo[1]['lucro_previsto']:,.2f}")
        safe_print(f"   📊 Margem: {produto_mais_lucrativo[1]['margem_prevista_%']:.1f}%")
        
        # Produto com melhor margem prevista
        produto_melhor_margem = max(previsoes_financeiras.items(), key=lambda x: x[1]['margem_prevista_%'])
        safe_print(f"\n📊 Produto com melhor margem prevista: {produto_melhor_margem[0]}")
        safe_print(f"   📊 Margem: {produto_melhor_margem[1]['margem_prevista_%']:.1f}%")
        safe_print(f"   💚 Lucro: R$ {produto_melhor_margem[1]['lucro_previsto']:,.2f}")
        
        safe_print("\n✅ Previsões financeiras concluídas!")
        
        return previsoes_financeiras

def main():
    """Função principal"""
    # Carregar dados
    df = pd.read_csv('datasets/vendas.csv')
    
    # Criar instância da análise
    analise = AnalisePredicaoVendas(df)
    
    # Executar análise completa
    resultados = analise.gerar_relatorio_completo()
    
    return resultados

if __name__ == "__main__":
    resultados = main()