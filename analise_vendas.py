# -*- coding: utf-8 -*-
import pandas as pd
from datetime import datetime
import sys
import os

def safe_print(text):
    """Função para imprimir com fallback para encoding"""
    try:
        print(text)
    except UnicodeEncodeError:
        # Fallback: remover emojis e caracteres especiais
        import re
        text_safe = re.sub(r'[^\x00-\x7F]+', '', text)
        print(text_safe)

# Configurar o pandas para exibir todas as colunas
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

def carregar_dados():
    """Carrega e prepara os dados de vendas"""
    df = pd.read_csv('datasets/vendas.csv')
    
    # Converter a coluna Data para datetime
    df['Data'] = pd.to_datetime(df['Data'])
    
    # Extrair ano e mês
    df['Ano'] = df['Data'].dt.year
    df['Mes'] = df['Data'].dt.month
    df['Ano_Mes'] = df['Data'].dt.to_period('M')
    
    return df

def produto_mais_vendido_geral(df):
    """Encontra o produto que mais vendeu no geral (por quantidade)"""
    print("=" * 60)
    print("PRODUTO QUE MAIS VENDEU - GERAL (Por Quantidade)")
    print("=" * 60)
    
    produto_qtd = df.groupby('Produto')['Qtd_Vendida'].sum().sort_values(ascending=False)
    print("Ranking dos produtos por quantidade vendida:")
    for i, (produto, qtd) in enumerate(produto_qtd.head(10).items(), 1):
        print(f"{i}. {produto}: {qtd:,} unidades")
    
    print(f"\nCAMPEAO: {produto_qtd.index[0]} com {produto_qtd.iloc[0]:,} unidades vendidas")
    
    return produto_qtd

def produto_mais_vendido_por_receita(df):
    """Encontra o produto que mais vendeu por receita"""
    print("\n" + "=" * 60)
    print("PRODUTO QUE MAIS VENDEU - GERAL (Por Receita)")
    print("=" * 60)
    
    produto_receita = df.groupby('Produto')['Receita'].sum().sort_values(ascending=False)
    print("Ranking dos produtos por receita:")
    for i, (produto, receita) in enumerate(produto_receita.head(10).items(), 1):
        print(f"{i}. {produto}: R$ {receita:,.2f}")
    
    print(f"\nCAMPEAO: {produto_receita.index[0]} com R$ {produto_receita.iloc[0]:,.2f}")
    
    return produto_receita

def vendedor_mais_vendeu_geral(df):
    """Encontra o vendedor que mais vendeu no geral"""
    print("\n" + "=" * 60)
    print("VENDEDOR QUE MAIS VENDEU - GERAL")
    print("=" * 60)
    
    # Por quantidade
    vendedor_qtd = df.groupby('Vendedor')['Qtd_Vendida'].sum().sort_values(ascending=False)
    print("Ranking por quantidade vendida:")
    for i, (vendedor, qtd) in enumerate(vendedor_qtd.items(), 1):
        print(f"{i}. {vendedor}: {qtd:,} unidades")
    
    # Por receita
    vendedor_receita = df.groupby('Vendedor')['Receita'].sum().sort_values(ascending=False)
    print("\nRanking por receita:")
    for i, (vendedor, receita) in enumerate(vendedor_receita.items(), 1):
        print(f"{i}. {vendedor}: R$ {receita:,.2f}")
    
    print(f"\nCAMPEAO (Quantidade): {vendedor_qtd.index[0]} com {vendedor_qtd.iloc[0]:,} unidades")
    print(f"CAMPEAO (Receita): {vendedor_receita.index[0]} com R$ {vendedor_receita.iloc[0]:,.2f}")
    
    return vendedor_qtd, vendedor_receita

def analise_por_ano(df):
    """Análise de produtos e vendedores por ano"""
    print("\n" + "=" * 60)
    print("ANÁLISE POR ANO")
    print("=" * 60)
    
    anos = sorted(df['Ano'].unique())
    
    for ano in anos:
        print(f"\nANO {ano}")
        print("-" * 40)
        
        df_ano = df[df['Ano'] == ano]
        
        # Produto mais vendido do ano (quantidade)
        produto_ano_qtd = df_ano.groupby('Produto')['Qtd_Vendida'].sum().sort_values(ascending=False)
        print(f"Produto mais vendido (qtd): {produto_ano_qtd.index[0]} - {produto_ano_qtd.iloc[0]:,} unidades")
        
        # Produto mais vendido do ano (receita)
        produto_ano_receita = df_ano.groupby('Produto')['Receita'].sum().sort_values(ascending=False)
        print(f"Produto maior receita: {produto_ano_receita.index[0]} - R$ {produto_ano_receita.iloc[0]:,.2f}")
        
        # Vendedor que mais vendeu no ano (quantidade)
        vendedor_ano_qtd = df_ano.groupby('Vendedor')['Qtd_Vendida'].sum().sort_values(ascending=False)
        print(f"Vendedor mais vendeu (qtd): {vendedor_ano_qtd.index[0]} - {vendedor_ano_qtd.iloc[0]:,} unidades")
        
        # Vendedor que mais vendeu no ano (receita)
        vendedor_ano_receita = df_ano.groupby('Vendedor')['Receita'].sum().sort_values(ascending=False)
        print(f"Vendedor maior receita: {vendedor_ano_receita.index[0]} - R$ {vendedor_ano_receita.iloc[0]:,.2f}")

def analise_por_mes(df):
    """Análise de produtos e vendedores por mês"""
    print("\n" + "=" * 60)
    print("ANÁLISE POR MÊS (Top 3 meses com maiores vendas)")
    print("=" * 60)
    
    # Encontrar os meses com maiores vendas
    vendas_por_mes = df.groupby('Ano_Mes')['Receita'].sum().sort_values(ascending=False)
    top_meses = vendas_por_mes.head(12)  # Top 12 meses
    
    for mes_periodo in top_meses.index:
        print(f"\n{mes_periodo} - Receita Total: R$ {top_meses[mes_periodo]:,.2f}")
        print("-" * 50)
        
        df_mes = df[df['Ano_Mes'] == mes_periodo]
        
        # Produto mais vendido do mês
        produto_mes_qtd = df_mes.groupby('Produto')['Qtd_Vendida'].sum().sort_values(ascending=False)
        produto_mes_receita = df_mes.groupby('Produto')['Receita'].sum().sort_values(ascending=False)
        
        print(f"Produto mais vendido (qtd): {produto_mes_qtd.index[0]} - {produto_mes_qtd.iloc[0]:,} unidades")
        print(f"Produto maior receita: {produto_mes_receita.index[0]} - R$ {produto_mes_receita.iloc[0]:,.2f}")
        
        # Vendedor que mais vendeu no mês
        vendedor_mes_qtd = df_mes.groupby('Vendedor')['Qtd_Vendida'].sum().sort_values(ascending=False)
        vendedor_mes_receita = df_mes.groupby('Vendedor')['Receita'].sum().sort_values(ascending=False)
        
        print(f"Vendedor mais vendeu (qtd): {vendedor_mes_qtd.index[0]} - {vendedor_mes_qtd.iloc[0]:,} unidades")
        print(f"Vendedor maior receita: {vendedor_mes_receita.index[0]} - R$ {vendedor_mes_receita.iloc[0]:,.2f}")

def gerar_resumo_estatisticas(df):
    """Gera um resumo geral das estatísticas dos dados"""
    safe_print("\n" + "=" * 60)
    safe_print("RESUMO ESTATISTICAS GERAIS")
    safe_print("=" * 60)
    
    safe_print(f"Periodo analisado: {df['Data'].min().strftime('%d/%m/%Y')} a {df['Data'].max().strftime('%d/%m/%Y')}")
    safe_print(f"Total de registros: {len(df):,}")
    safe_print(f"Total de produtos vendidos: {df['Qtd_Vendida'].sum():,} unidades")
    safe_print(f"Receita total: R$ {df['Receita'].sum():,.2f}")
    safe_print(f"Lucro total: R$ {df['Lucro'].sum():,.2f}")
    safe_print(f"Numero de produtos diferentes: {df['Produto'].nunique()}")
    safe_print(f"Numero de vendedores: {df['Vendedor'].nunique()}")
    safe_print(f"Numero de regioes: {df['Regiao'].nunique()}")
    
    safe_print(f"\nProdutos disponiveis: {', '.join(df['Produto'].unique())}")
    safe_print(f"Vendedores: {', '.join(df['Vendedor'].unique())}")
    safe_print(f"Regioes: {', '.join(df['Regiao'].unique())}")

def main():
    """Função principal"""
    safe_print("ANALISE DE VENDAS - RELATORIO COMPLETO")
    safe_print("=" * 60)
    
    # Carregar dados
    df = carregar_dados()
    
    # Executar todas as análises
    gerar_resumo_estatisticas(df)
    produto_mais_vendido_geral(df)
    produto_mais_vendido_por_receita(df)
    vendedor_mais_vendeu_geral(df)
    analise_por_ano(df)
    analise_por_mes(df)
    
    safe_print("\n" + "=" * 60)
    safe_print("ANALISE CONCLUIDA!")
    safe_print("=" * 60)

if __name__ == "__main__":
    main()