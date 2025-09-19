import csv
from collections import defaultdict

def carregar_dados(caminho_arquivo='dados.csv'):
    dados = []
    try:
        with open(caminho_arquivo, mode='r', encoding='latin-1') as arquivo_csv:
            leitor_csv = csv.reader(arquivo_csv)
            next(leitor_csv, None)

            for i, linha in enumerate(leitor_csv):
                try:
                    data_str = linha[0]
                    partes_data = data_str.split('/')
                    dia = int(partes_data[0])
                    mes = int(partes_data[1])
                    ano = int(partes_data[2])
                    
                    dados_dia = {
                        'data': data_str,
                        'dia': dia,
                        'mes': mes,
                        'ano': ano,
                        'precipitacao': float(linha[1]),
                        'temp_max': float(linha[2]),
                        'temp_min': float(linha[3]),
                        'umidade': float(linha[6]),
                        'vento': float(linha[7])
                    }
                    dados.append(dados_dia)
                except (ValueError, IndexError) as e:
                    print(f"Aviso: Linha {i+2} do arquivo CSV ignorada por formatação inválida. Detalhes: {e}")
                    
    except FileNotFoundError:
        print(f"ERRO: O arquivo '{caminho_arquivo}' não foi encontrado. Verifique se ele está na mesma pasta que o programa.")
        return None
        
    return dados

def visualizar_dados_intervalo(dados):
    print("\n--- Visualização de Dados por Período ---")
    try:
        mes_inicio = int(input("Digite o mês inicial (1-12): "))
        ano_inicio = int(input("Digite o ano inicial: "))
        mes_fim = int(input("Digite o mês final (1-12): "))
        ano_fim = int(input("Digite o ano final: "))

        if not (1 <= mes_inicio <= 12 and 1 <= mes_fim <= 12):
            print("Erro: Mês inválido. Por favor, insira um valor entre 1 e 12.")
            return

    except ValueError:
        print("Erro: Entrada inválida. Por favor, digite apenas números.")
        return

    print("\nEscolha os dados a serem exibidos:")
    print("1 - Todos os dados")
    print("2 - Apenas Precipitação")
    print("3 - Apenas Temperaturas (Máxima e Mínima)")
    print("4 - Apenas Umidade e Vento")
    
    try:
        escolha = int(input("Opção: "))
        if escolha not in [1, 2, 3, 4]:
            print("Erro: Opção inválida.")
            return
    except ValueError:
        print("Erro: Entrada inválida.")
        return

    dados_filtrados = [
        d for d in dados 
        if (d['ano'] > ano_inicio or (d['ano'] == ano_inicio and d['mes'] >= mes_inicio)) and \
           (d['ano'] < ano_fim or (d['ano'] == ano_fim and d['mes'] <= mes_fim))
    ]

    if not dados_filtrados:
        print("\nNenhum dado encontrado para o período informado.")
        return

    if escolha == 1:
        print("\nData\t\tPrec(mm)\tTemp.Max(C)\tTemp.Min(C)\tUmidade(%)\tVento(m/s)")
    elif escolha == 2:
        print("\nData\t\tPrec(mm)")
    elif escolha == 3:
        print("\nData\t\tTemp.Max(C)\tTemp.Min(C)")
    elif escolha == 4:
        print("\nData\t\tUmidade(%)\tVento(m/s)")

    for dia in dados_filtrados:
        if escolha == 1:
            print(f"{dia['data']}\t{dia['precipitacao']}\t\t{dia['temp_max']}\t\t{dia['temp_min']}\t\t{dia['umidade']}\t\t{dia['vento']}")
        elif escolha == 2:
            print(f"{dia['data']}\t{dia['precipitacao']}")
        elif escolha == 3:
            print(f"{dia['data']}\t{dia['temp_max']}\t\t{dia['temp_min']}")
        elif escolha == 4:
            print(f"{dia['data']}\t{dia['umidade']}\t\t{dia['vento']}")

def encontrar_mes_mais_chuvoso(dados):
    print("\n--- Mês Mais Chuvoso (Todo o Período) ---")
    precipitacao_mensal = defaultdict(float)

    for dia in dados:
        chave = f"{dia['mes']:02d}/{dia['ano']}"
        precipitacao_mensal[chave] += dia['precipitacao']

    if not precipitacao_mensal:
        print("Não foi possível calcular, sem dados de precipitação.")
        return

    mes_mais_chuvoso = max(precipitacao_mensal, key=precipitacao_mensal.get)
    maior_precipitacao = precipitacao_mensal[mes_mais_chuvoso]

    print(f"O mês mais chuvoso foi {mes_mais_chuvoso} com {maior_precipitacao:.2f} mm de precipitação.")

def analisar_temperaturas_minimas(dados):
    print("\n--- Análise da Temperatura Mínima Média (2006-2016) ---")
    
    meses_map = {
        'janeiro': 1, 'fevereiro': 2, 'março': 3, 'abril': 4, 'maio': 5, 'junho': 6,
        'julho': 7, 'agosto': 8, 'setembro': 9, 'outubro': 10, 'novembro': 11, 'dezembro': 12
    }
    
    try:
        nome_mes_input = input("Digite o nome do mês a ser analisado (ex: 'Janeiro'): ").lower()
        if nome_mes_input not in meses_map:
            print("Erro: Nome do mês inválido.")
            return
        mes_escolhido = meses_map[nome_mes_input]
    except Exception as e:
        print(f"Ocorreu um erro na sua entrada: {e}")
        return

    dados_periodo = [d for d in dados if 2006 <= d['ano'] <= 2016]
    
    medias_por_ano = {}

    for ano in range(2006, 2017):
        dados_mes_ano = [
            d['temp_min'] for d in dados_periodo 
            if d['ano'] == ano and d['mes'] == mes_escolhido
        ]
        
        if dados_mes_ano:
            media_mes = sum(dados_mes_ano) / len(dados_mes_ano)
            chave = f"{nome_mes_input.capitalize()}{ano}"
            medias_por_ano[chave] = media_mes
    
    if not medias_por_ano:
        print(f"Nenhum dado encontrado para {nome_mes_input.capitalize()} entre 2006 e 2016.")
        return

    print("\n--- Médias da Temperatura Mínima por Ano ---")
    for chave, valor in medias_por_ano.items():
        print(f"{chave}: {valor:.2f}°C")

    media_geral = sum(medias_por_ano.values()) / len(medias_por_ano)
    print(f"\n--- Média Geral ---")
    print(f"A média geral da temperatura mínima para {nome_mes_input.capitalize()} entre 2006 e 2016 foi de {media_geral:.2f}°C.")

def main():
    dados_climaticos = carregar_dados()

    if dados_climaticos is None:
        print("Encerrando o programa devido a erro no carregamento dos dados.")
        return

    while True:
        print("\n===== MENU PRINCIPAL - ANÁLISE CLIMÁTICA =====")
        print("1. Visualizar dados por período")
        print("2. Encontrar o mês mais chuvoso")
        print("3. Analisar temperaturas mínimas (2006-2016)")
        print("0. Sair")
        
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            visualizar_dados_intervalo(dados_climaticos)
        elif opcao == '2':
            encontrar_mes_mais_chuvoso(dados_climaticos)
        elif opcao == '3':
            analisar_temperaturas_minimas(dados_climaticos)
        elif opcao == '0':
            print("Encerrando o programa. Até mais!")
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")

if __name__ == "__main__":
    main() 