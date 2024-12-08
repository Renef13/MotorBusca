from MotorBusca import MotorBusca


def main():
    arquivo_xml = 'verbetesWikipedia.xml'
    buscador = MotorBusca(arquivo_xml)
    while True:
        termo_buscado = input('Digite o termo buscado: ')
        if len(termo_buscado.strip()) < 2:
            print("\033[31mPalavra curta demaisa\033[0m\n")
            continue

        resultados = buscador.buscar(termo_buscado)
        if not resultados:
            print("\033[31mNenhum resultado encontrado para o termo\033[0m\n")
        else:
            print(f"\nResultados para '{termo_buscado}':\n")
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
