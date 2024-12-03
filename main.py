from MotorBusca import MotorBusca


def main():
    arquivo_xml = 'verbetesWikipedia.xml'
    buscador = MotorBusca(arquivo_xml)
    while True:
        termo_buscado = input('Digite o termo buscado: ')
        resultados = buscador.buscar(termo_buscado)
        if resultados is None:
            print("Palavra curta demais\n")
        else:
            for artigo_id, (artigo_titulo, relevancia) in resultados.items():
                print(f'Id: {artigo_id},Titulo: {artigo_titulo}, Relevancia: {(relevancia * 10):.2f}\n')
                print('-' * 40)
        sair = input('\nDeseja continuar [S/N]?  ')

        if sair.lower() == 'n':
            print('\nSaindo...')
            break


if __name__ == '__main__':
    main()
