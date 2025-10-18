#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para gerar um arquivo HTML com texto destacado "HELLO WORLD!"
"""

import os

def gerar_html():
    # Obter o diretório onde o script está localizado
    script_dir = os.path.dirname(os.path.abspath(__file__))

    html_content = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hello World</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            font-family: Arial, sans-serif;
        }

        .container {
            text-align: center;
            animation: fadeIn 1.5s ease-in;
        }

        h1 {
            font-size: 6rem;
            font-weight: bold;
            color: #ffffff;
            text-shadow:
                0 0 10px rgba(255, 255, 255, 0.8),
                0 0 20px rgba(255, 255, 255, 0.6),
                0 0 30px rgba(255, 255, 255, 0.4),
                5px 5px 10px rgba(0, 0, 0, 0.3);
            margin: 0;
            padding: 20px;
            letter-spacing: 0.1em;
            animation: pulse 2s ease-in-out infinite;
        }

        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: scale(0.8);
            }
            to {
                opacity: 1;
                transform: scale(1);
            }
        }

        @keyframes pulse {
            0%, 100% {
                transform: scale(1);
            }
            50% {
                transform: scale(1.05);
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>HELLO WORLD!</h1>
    </div>
</body>
</html>
"""

    # Salvar o arquivo HTML no mesmo diretório do script
    output_path = os.path.join(script_dir, 'hello_world.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"Arquivo 'hello_world.html' gerado com sucesso em: {output_path}")
    print("Abra o arquivo no seu navegador para visualizar.")


if __name__ == "__main__":
    gerar_html()
