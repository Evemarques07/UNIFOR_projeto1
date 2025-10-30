# -*- coding: utf-8 -*-
"""
💰 RESUMO EXECUTIVO - PREVISÕES FINANCEIRAS 2025
============================================

Este script gera um relatório executivo focado nas previsões
de receita, custo e lucro por produto para 2025.

Autor: Sistema de Análise de Vendas
Data: 30/10/2025
"""

import pandas as pd
from analise_predicao_vendas import AnalisePredicaoVendas
from datetime import datetime
import sys
import os

# Configurar encoding UTF-8 para Windows
if sys.platform == "win32":
    os.system("chcp 65001 > nul")

def gerar_resumo_executivo_financeiro():
    """Gera resumo executivo das previsões financeiras"""
    print("=" * 80)
    print("💰 RESUMO EXECUTIVO - PREVISÕES FINANCEIRAS 2025")
    print("=" * 80)
    print(f"📅 Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print()
    
    # Carregar dados
    df = pd.read_csv('datasets/vendas.csv')
    analise = AnalisePredicaoVendas(df)
    
    # Executar análise (silencioso)
    import sys
    from io import StringIO
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    try:
        previsoes_financeiras = analise.previsoes_financeiras_produtos()
    finally:
        sys.stdout = old_stdout
    
    # Dados históricos para comparação
    historico_total = df.groupby('Produto').agg({
        'Receita': 'sum',
        'Lucro': 'sum',
        'Qtd_Vendida': 'sum'
    })
    historico_total['Custo'] = historico_total['Receita'] - historico_total['Lucro']
    historico_total['Margem_%'] = (historico_total['Lucro'] / historico_total['Receita']) * 100
    
    print("📊 VISÃO GERAL DO NEGÓCIO")
    print("-" * 50)
    print(f"📈 Período analisado: {df['Data'].min()} a {df['Data'].max()}")
    print(f"🏷️  Total de produtos: {df['Produto'].nunique()}")
    print(f"👥 Total de vendedores: {df['Vendedor'].nunique()}")
    print(f"📦 Total vendido histórico: {df['Qtd_Vendida'].sum():,} unidades")
    print(f"💰 Receita histórica total: R$ {df['Receita'].sum():,.2f}")
    print(f"💚 Lucro histórico total: R$ {df['Lucro'].sum():,.2f}")
    margem_historica = (df['Lucro'].sum() / df['Receita'].sum()) * 100
    print(f"📊 Margem histórica média: {margem_historica:.1f}%")
    print()
    
    print("🎯 PRINCIPAIS INSIGHTS FINANCEIROS 2025")
    print("-" * 50)
    
    # Calcular totais previstos
    total_receita_prevista = sum([p['receita_prevista'] for p in previsoes_financeiras.values()])
    total_custo_previsto = sum([p['custo_previsto'] for p in previsoes_financeiras.values()])
    total_lucro_previsto = sum([p['lucro_previsto'] for p in previsoes_financeiras.values()])
    margem_prevista = (total_lucro_previsto / total_receita_prevista) * 100
    
    # Variações
    receita_historica = df['Receita'].sum()
    lucro_historico = df['Lucro'].sum()
    custo_historico = receita_historica - lucro_historico
    
    var_receita = ((total_receita_prevista - receita_historica) / receita_historica) * 100
    var_lucro = ((total_lucro_previsto - lucro_historico) / lucro_historico) * 100
    var_custo = ((total_custo_previsto - custo_historico) / custo_historico) * 100
    
    print(f"💰 Receita prevista 2025: R$ {total_receita_prevista:,.2f} ({var_receita:+.1f}%)")
    print(f"💸 Custo previsto 2025: R$ {total_custo_previsto:,.2f} ({var_custo:+.1f}%)")
    print(f"💚 Lucro previsto 2025: R$ {total_lucro_previsto:,.2f} ({var_lucro:+.1f}%)")
    print(f"📊 Margem prevista 2025: {margem_prevista:.1f}% (atual: {margem_historica:.1f}%)")
    print()
    
    print("🏆 RANKING DE PRODUTOS POR LUCRATIVIDADE 2025")
    print("-" * 50)
    
    # Ordenar produtos por lucro previsto
    produtos_ordenados = sorted(previsoes_financeiras.items(), 
                               key=lambda x: x[1]['lucro_previsto'], reverse=True)
    
    for i, (produto, dados) in enumerate(produtos_ordenados, 1):
        trend_icon = "📈" if dados['tendencia'] == 'CRESCIMENTO' else "📊" if dados['tendencia'] == 'ESTÁVEL' else "📉"
        
        print(f"{i}. {produto.upper()} {trend_icon}")
        print(f"   💚 Lucro previsto: R$ {dados['lucro_previsto']:,.2f}")
        print(f"   📊 Margem prevista: {dados['margem_prevista_%']:.1f}%")
        print(f"   📈 Qtd prevista: {dados['qtd_prevista']:,.0f} unidades")
        print(f"   💰 Receita prevista: R$ {dados['receita_prevista']:,.2f}")
        print(f"   📋 Variação lucro: {dados['variacao_lucro_%']:+.1f}%")
        print()
    
    print("🎖️  DESTAQUES E RECOMENDAÇÕES")
    print("-" * 50)
    
    # Produto mais lucrativo
    produto_top = produtos_ordenados[0]
    print(f"🥇 Produto mais lucrativo: {produto_top[0]}")
    print(f"   💡 Representa {(produto_top[1]['lucro_previsto']/total_lucro_previsto)*100:.1f}% do lucro total previsto")
    
    # Produto com melhor margem
    produto_melhor_margem = max(previsoes_financeiras.items(), 
                               key=lambda x: x[1]['margem_prevista_%'])
    print(f"📊 Melhor margem prevista: {produto_melhor_margem[0]} ({produto_melhor_margem[1]['margem_prevista_%']:.1f}%)")
    
    # Produto em maior crescimento
    produtos_crescimento = [p for p in previsoes_financeiras.items() 
                           if p[1]['tendencia'] == 'CRESCIMENTO']
    if produtos_crescimento:
        produto_crescimento = max(produtos_crescimento, 
                                 key=lambda x: x[1]['variacao_lucro_%'])
        print(f"🚀 Maior crescimento previsto: {produto_crescimento[0]} (+{produto_crescimento[1]['variacao_lucro_%']:.1f}%)")
    
    print()
    print("⚠️  PONTOS DE ATENÇÃO")
    print("-" * 50)
    
    # Produtos com margem baixa
    produtos_margem_baixa = [p for p in previsoes_financeiras.items() 
                            if p[1]['margem_prevista_%'] < 30]
    if produtos_margem_baixa:
        print("📉 Produtos com margem abaixo de 30%:")
        for produto, dados in produtos_margem_baixa:
            print(f"   • {produto}: {dados['margem_prevista_%']:.1f}%")
    
    # Produtos em queda
    produtos_queda = [p for p in previsoes_financeiras.items() 
                     if p[1]['variacao_lucro_%'] < 0]
    if produtos_queda:
        print("⚠️  Produtos com queda no lucro prevista:")
        for produto, dados in produtos_queda:
            print(f"   • {produto}: {dados['variacao_lucro_%']:+.1f}%")
    
    print()
    print("💡 RECOMENDAÇÕES ESTRATÉGICAS")
    print("-" * 50)
    print("1. 🎯 Focar recursos nos produtos com maior margem e crescimento")
    print("2. 🔍 Revisar estratégia de preços dos produtos com margem baixa")
    print("3. 📈 Investir em marketing para produtos em crescimento")
    print("4. 🛠️  Otimizar custos dos produtos com margem abaixo de 30%")
    print("5. 📊 Monitorar tendências mensalmente para ajustes")
    
    print()
    print("=" * 80)
    print("📋 Relatório gerado pelo Sistema de Análise Preditiva de Vendas")
    print("💾 Para visualizações completas, execute: python dashboard_completo.py")
    print("=" * 80)

if __name__ == "__main__":
    gerar_resumo_executivo_financeiro()