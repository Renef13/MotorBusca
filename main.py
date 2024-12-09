from MotorBusca import MotorBusca

def main():
    arquivo_xml = 'verbetesWikipedia.xml'
    buscador = MotorBusca(arquivo_xml)

    while True:
        termos_buscados = input('Digite os termos buscados (separados por espaço): ')
        
        if len(termos_buscados.strip()) < 2:
            print("\033[31mEntrada muito curta. Digite pelo menos um termo válido.\033[0m\n")
            continue

        resultados = buscador.buscar(termos_buscados)
        
        if not resultados:
            print("\033[31mNenhum resultado encontrado para os termos\033[0m\n")
        else:
            print(f"\nResultados para '{termos_buscados}':\n")
            for artigo_titulo, relevancia in resultados.items():
                print(f'Título: {artigo_titulo}')
                print(f'Relevância: {(relevancia * 10):.2f}')
                print('-' * 40)

        sair = input('\nDeseja continuar [S/N]? ').strip().lower()
        if sair == 'n':
            print('\nSaindo...')
            break

if __name__ == '__main__':
    main()