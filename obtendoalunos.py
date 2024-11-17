import pandas as pd
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import os
import openpyxl as xl
from openpyxl.styles import Font, PatternFill
from subfuncoes import informador, criador_planilha_assistente


def importador():
    App = Tk()
    App.title("Importando Dados")
    App.geometry("250x320")
    App.configure(background="#dde")
    App.resizable(False, False)

    """
    Reestruturando o código... sempre muito complicado.


    Como funcionará o sistema de numeração:

    Ativa; são numerados a partir de uma ordem alfabética, não contendo os reservas.

    Reserva; são numerados a partir de uma ordem alfabética só entre eles.

    Remates; deverão ser colocados na frente, tbm em ordem alfabetica. Só entre eles.

    Para facilitar, vamos criar um novo estilo de planilha. Uma só nossa.

    Sanha dos Remats:
        E se o remat vier de um ano diferente do anterior, que nem o da rocha??? Mais um sanha
        Como são casos extremamente especiais, vamos deixar para que isso seja alterado individualmente!!
        MANO OS REMATS NÃO NECESSARIAMENTE ESTÃO UM LOGO ABAIXO DO OUTRO, POIS VINHERAM NO SANHA!

        Como os remats são sempre uma excessão muito grande, vamos deixar para inserir o 'número de cada um individualmente'


    VAMOS FIXAR:
    1° 0: Quant. Serv



    Optamos por deixar à mostrar o que haviamos feito em uma versão mais antiga para mostrar a evolução do código e como 
    foi possível fazê-lo de forma mais inteligente




    """

    def importando_coletivo():
        """Com essa função, a intenção é receber uma planilha de alunos completa, sem qualquer erro.
        Deixando-a zerada e preparada."""

        App.destroy()

        def importar(bases, decisao, mestre):

            if messagebox.askyesnocancel("Certeza?", message='Confirme as informações antes de continuar!'):
                # Pegando as informações
                base = bases.get()
                nome = decisao.get() + '.txt'

                # Abrindo a base que importaremos
                def verificando_existencia_criando(deseja_destruir=False):
                    global planilha, base_dados1
                    try:
                        planilha = pd.read_excel(base)

                    except FileNotFoundError:
                        messagebox.showerror("ERROR", 'Erro ao tentar importar base de dados')

                    # Criando os arquivos que usaremos
                    try:
                        # É possível que a pasta arquivos não exista também
                        try:
                            if os.path.isdir('../SargenteanteAlpha/Arquivos'):
                                # Vai ter o Sanha
                                if deseja_destruir:
                                    if nome in os.listdir('../SargenteanteAlpha/Arquivos'):
                                        os.remove(f'Arquivos/{nome}')

                            else:
                                os.mkdir('../SargenteanteAlpha/Arquivos')

                            if deseja_destruir:
                                pass
                            else:
                                base_dados1 = open(rf'Arquivos/{nome}', "x")

                        except Exception as e:
                            print(e)
                            messagebox.showerror(message='Erro ao criar pasta de arquivos principais.')

                        def criando_pastas():
                            try:
                                pastas = ['Escalas', 'Punicoes', 'SubArquivos', 'Registros', 'Lixeira',
                                          'ServicosGerais']

                                for pasta in pastas:
                                    if os.path.isdir(pasta):
                                        pass
                                    else:
                                        os.mkdir(pasta)
                            except Exception as e:
                                print(e)
                                messagebox.showerror(
                                    message='Erro ao tentar criar pastas adjacentes, necessária intervenção manual')

                        if deseja_destruir:
                            pass
                        else:
                            criando_pastas()

                        def criando_subarquivos():
                            try:
                                subarquivos = ['baixados', 'Descansos',
                                               'historicobaixados', 'Trocas',
                                               'Isentos', 'ConfiguracoesServico',
                                               'HistoricoVisual'
                                               ]

                                for subarquivo in subarquivos:
                                    try:
                                        # Verificação se existe o Sanha
                                        p = open(rf'SubArquivos/{subarquivo}', 'r')
                                        p.close()
                                    except FileNotFoundError:
                                        # Caso não exista, vamos criar
                                        p = open(rf'SubArquivos/{subarquivo}', 'x')
                                        p.close()
                            except Exception as e:
                                print(e)
                                messagebox.showerror(
                                    message='Erro ao tentar criar subarquivos, necessária intervenção manual')

                        if deseja_destruir:
                            pass
                        else:
                            criando_subarquivos()

                        return base_dados1
                    except Exception as e:
                        print(e)
                        messagebox.showerror("ERROR", 'Erro ao tentar criar base de alunos')

                base_dados = verificando_existencia_criando()

                mestre.destroy()

                try:
                    # Devemos salvar os nomes completos aqui
                    para_registro = []

                    diferentes = [['Ã', 'A'], ['Õ', 'O'], ['Á', 'A'], ['É', 'E'], ['Ó', 'O'],
                                  ['Ú', 'U'], ['Ç', 'C'], ['À', 'A']]

                    if not messagebox.askyesno(message='Será uma planilha com número?'):
                        try:
                            def construindo_base():

                                messagebox.showinfo(title='ATENÇÃO',
                                                    message='Você deve colocar o número de cada um dos remats, já que eles não possuem um lógica consistente e não é possível prevê-los.')

                                # Há 3 tipos de alunos, REMATS, ATIVAS, RESERVAS, sendo nessa ordem a necessidade de inscrição
                                classes = [['REMATS', 'REMATS-NOMEDEGUERRA'],
                                           ['ATIVAS', 'ATIVAS-NOMEDEGUERRA'],
                                           ['RESERVAS', 'RESERVAS-NOMEDEGUERRA']]

                                # Com isso, vamos fazer as verificações, lembrando que cada coluna tem o mesmo número de linhas
                                # que a sua correspondente

                                """Dava um erro serio sobre se chegamos ao final ou não
                                Essa função é para conseguirmos colocar a última linha sem o pulo"""

                                def chegou_final(p, string):

                                    try:
                                        teste = planilha[string][p + 1].split('-')

                                        return False

                                    except AttributeError:
                                        return True

                                """
                                ESTA(va) DANDO UM JANGAU ABSOLUTO

                                Note que quando clicamos no botão queremos fazer a função retornar o valor para a variavel numero lá
                                So que para pensar: a função relativa ao botão esta dentro de uma função e não da para referenciar 
                                esse return da função do botão na função de escopo maior, logo não consigo resolver esse problema.                    
                                """
                                verificacao_de_numeros = []
                                for titulo_coluna, nomeguerrasexo in classes:
                                    # Vamos fazer as 3 obtenções em um ‘loop’
                                    for c in range(0, len(planilha[titulo_coluna])):

                                        # obtendo as informações
                                        try:

                                            # pegando o nome completo correspondente
                                            nomes_completos = planilha[titulo_coluna][c]

                                            # pegando uma lista do nome de guerra e o sexo
                                            nomeguerrasexo_ = planilha[nomeguerrasexo][c].split('-')
                                            """print(planilha[nomeguerrasexo][c]) aqui estava dando um erro muito insano, 
                                            havia mudado o nome da coluna no arquivo .xlsx e o programa não conseguia achar.

                                            Outro erro que estava tendo é que o número de elemente é definido pela primeira coluna!
                                            Por exemplo, pense em uma matriz 3x3 onde a primeira col tem de fato 3 linhas ocupadas,
                                            mas a 3 col tem só uma, logo a 2° e a 3° ficam com Nan e nada pode ser feito
                                            """

                                            # separando-os
                                            nomes_guerra = nomeguerrasexo_[0]
                                            sexo = nomeguerrasexo_[1]

                                            # fazendo verificações de nomes com acento para não dar erro
                                            for diferen, normal in diferentes:
                                                if diferen in nomes_completos:
                                                    nomes_completos = nomes_completos.replace(diferen, normal)

                                                if diferen in nomes_guerra:
                                                    nomes_guerra = nomes_guerra.replace(diferen, normal)

                                                if diferen in sexo:
                                                    sexo = sexo.replace(diferen, normal)

                                            para_registro.append(nomes_completos.upper())

                                            # Devemos obter o número de cada um também
                                            global numero
                                            numero = 0

                                            if titulo_coluna == 'REMATS':
                                                # Para remats, tudo muda diferente

                                                pegando = Tk()
                                                pegando.title("Numeração")
                                                pegando.geometry("200x130+300+300")
                                                pegando.configure(bg='#dde')
                                                pegando.resizable(False, False)

                                                pegando.update_idletasks()

                                                Label(pegando, text=f'AL:   {nomes_guerra}', bg='#dde').place(x=10,
                                                                                                              y=10)

                                                num = Entry(pegando)
                                                num.update_idletasks()
                                                num.place(x=10, y=40)
                                                Label(pegando, text='Pressione Enter', bg='#dde').place(x=10, y=70)
                                                num.focus()

                                                def teste(event):
                                                    # para conseguirmos fazer as modificações nessa variavel
                                                    global numero

                                                    try:
                                                        numero = int(num.get())
                                                        if 10000 < numero < 99999:
                                                            # É válido
                                                            if numero in verificacao_de_numeros:
                                                                return messagebox.showwarning(
                                                                    message='Esse número já foi digitado')
                                                            else:
                                                                verificacao_de_numeros.append(numero)
                                                                return pegando.destroy()
                                                        else:
                                                            return messagebox.showerror(title='ERROR',
                                                                                        message='Tente verificar se você realmente digitou um número válido')

                                                    except (ValueError, TypeError):
                                                        return messagebox.showerror(title='ERROR',
                                                                                    message='Tente verificar se você realmente digitou um número válido')

                                                num.bind('<Return>', teste)
                                                pegando.mainloop()

                                                """
                                                ESTA(va) DANDO UM JANGAU ABSOLUTO

                                                Note que quando clicamos no botão queremos fazer a função retornar o valor para a 
                                                variavel numero lá So que para pensar: a função relativa ao botão esta dentro de 
                                                uma função e não da para referenciar esse return da função do botão na função de 
                                                escopo maior, logo não consigo resolver esse problema."""

                                            elif titulo_coluna == 'ATIVAS':
                                                # vamos precisar do ano que esta adentrando!
                                                for i in range(20, 40):
                                                    if f'{i}' in nome:
                                                        numero = (c + 1) + (i - 4) * 1000

                                            elif titulo_coluna == 'RESERVAS':
                                                for i in range(20, 40):
                                                    if f'{i}' in nome:
                                                        numero = (c + 1) + (i - 4) * 1000 + 400

                                            # print(f'{nomes_guerra} salvo como {numero}')
                                            # De posse das informações, vamos inseri-las, ainda nesse 'loop'

                                            if titulo_coluna == 'RESERVAS' and chegou_final(c, nomeguerrasexo):

                                                # Esta é a ÚLTIMA linha mesmo linha
                                                # print("Executando ultima linha")

                                                # Note que vamos usar pulos de linha para identificar as classes, logo não faz
                                                # muito sentido usá-las para impedir aquela última linha, vamos cuidar disso
                                                # exatamente quando ela estiver imediatamente a ser digitada
                                                """Note que se tivessemos colocado apenas len(planilha['RESERVAS']-1), poderiamos 
                                                ter um erro, dado que imagine a primeira tendo 20 linhas e a dos reservas tendo 
                                                15. Quando c fosse igual a 14, ela seria ativada, independente da coluna que 
                                                estivessemos, sendo assim, é necessário uma segunda condição no sistema
                                                """

                                                base_dados.write(
                                                    f'{numero}-{nomes_completos.upper()}-{nomes_guerra.upper()}-{sexo.capitalize()}-0')

                                            else:
                                                # Demais Linhas

                                                base_dados.write(
                                                    f'{numero}-{nomes_completos.upper()}-{nomes_guerra.upper()}-{sexo.capitalize()}-0\n')

                                        except AttributeError:
                                            # Chegamos no fim quando há esse erro, teoricamente
                                            """
                                            Estava dando um erro sério, pois note que: Como o programa sabe que chegamos ao final de
                                            uma classe? 
                                            Não podemos confiar no len pois ele esta dando erro aqui.

                                            O final só ocorre quando há aquele erro ou se chega na primeira coluna.

                                            """
                                            break

                                    if titulo_coluna != 'RESERVAS':
                                        base_dados.write('\n')

                            construindo_base()
                        except:
                            messagebox.showerror(message='Talvez a planilha não esteja adequadamente formatada')
                            base_dados.close()
                            return verificando_existencia_criando(True)
                    else:

                        try:
                            # Aqui, vamos criar a forma de obtenção que já vem com os números de cada.

                            def construindo_base_numerizada():
                                # Em teoria, vamos ter uma coluna simplesmente escrito aos caralho tudo junto
                                # Vai se basear em 2 funções básicas,
                                # Construir a base de alunos
                                # Montar outra planilha safinha e organizada.

                                # Vamos guardar tudo aqui
                                base_informacoes = {'REMAT': [],
                                                    'ATIVA': [],
                                                    'RESERVA': [],
                                                    }

                                def construtor():
                                    # Vamos pegar a planilha e montar a base
                                    global planilha
                                    from datetime import datetime

                                    def extraindo():
                                        # Vamos pegar só uma coluna, então, vamos bradar, com isso temos todas as informações que precisamos
                                        coluna = list(planilha[list(planilha.columns)[0]])
                                        # Com isso, nem precisamos mais da planilha
                                        ano = int(datetime.now().year) - 2000

                                        # Lembre-se que estaremos pegando a partir da segunda linha
                                        for linha in coluna:
                                            infos = linha.split('-')

                                            # Temos:
                                            # 0 - numero
                                            # 1 - nome completo
                                            # 2 - nome de guerra
                                            # 3 - sexo

                                            # Em teoria, conseguimos criar a base bem rapido, vamos devemos descobrir a classe do Sanha também

                                            def pegando_classe(num):
                                                # Exemplo 23054
                                                num = str(num)

                                                if num[2] == '4':
                                                    # quer dizer que é reserva
                                                    return 'RESERVA'

                                                elif int(num[:2]) == ano:
                                                    return 'ATIVA'

                                                else:
                                                    # remat com certeza
                                                    return 'REMAT'

                                            # Vamos salvar as informações de uma vez no dicionário
                                            base_informacoes[pegando_classe(infos[0])].append(str(linha))

                                    extraindo()

                                    def preenchendo():
                                        # Vamos colocar no texto

                                        primeira = True
                                        with open(f'Arquivos/{nome}', 'w') as basew:
                                            for chave in base_informacoes.keys():
                                                # Separadora de classes
                                                if not primeira:
                                                    basew.write('\n')

                                                for pessoa in base_informacoes[chave]:
                                                    pessoa = pessoa + '-0'
                                                    # Em teoria, vai ser o Sanha só do remat
                                                    if primeira:
                                                        basew.write(pessoa)
                                                        primeira = False

                                                    else:
                                                        basew.write(f'\n{pessoa}')

                                    preenchendo()

                                construtor()

                                return base_informacoes

                            b = construindo_base_numerizada()

                        except:
                            messagebox.showinfo(message='Talvez a planilha colocada não está adequadamente formatada.')
                            base_dados.close()
                            return verificando_existencia_criando(True)

                    base_dados.close()

                    if messagebox.askyesno(
                            message='Deseja criar uma planilha assistente, isto é, criar uma planilha com todos os alunos de forma organizada?'):
                        criador_planilha_assistente(nome)

                    def inicializando_sanhas():
                        def colocando_registro():
                            # a pasta de registro esta zerada, so nos resta então
                            i = 0
                            for f in range(20, 40):
                                if str(f) in nome:
                                    i = f
                                    # assim não precisaremos continuar
                                    break

                            # vamos criar o respectivo arquivo na pasta
                            try:
                                p = open(f'Registros/registro{i}', 'x')
                                p.close()

                                with open(f'Registros/registro{i}', 'w') as reg:
                                    c = True
                                    for pessoa in para_registro:
                                        if c:
                                            reg.write(f'{pessoa},')
                                            c = False
                                        else:
                                            reg.write(f'\n{pessoa},')

                            except FileExistsError:
                                pass

                        colocando_registro()

                        def servicando_geral():
                            i = 0
                            for f in range(20, 40):
                                if str(f) in nome:
                                    i = f
                                    # assim não precisaremos continuar
                                    break

                            # vamos criar o respectivo arquivo na pasta
                            try:
                                p = open(f'ServicosGerais/servicos{i}', 'x')
                                p.close()

                                with open(f'ServicosGerais/servicos{i}', 'w') as reg:
                                    c = True
                                    for pessoa in para_registro:
                                        if c:
                                            reg.write(f'{pessoa}=1-0;1.2-0;1.4-0;1.8-0;2-0;3-0;3.5-0;4-0;5-0')
                                            c = False
                                        else:
                                            reg.write(f'\n{pessoa}=1-0;1.2-0;1.4-0;1.8-0;2-0;3-0;3.5-0;4-0;5-0')

                            except FileExistsError:
                                pass

                        servicando_geral()

                        def colocando_configuracoes():
                            """Note que mesmo que estejamos iniciando outra turma, esse arquivo não deve ser preechido de novo."""

                            # Em teoria, só vai passar do try se ele conseguir

                            try:
                                # Vamos tentar abrir, por que criado já foi anteriormente
                                p = open('../SargenteanteAlpha/SubArquivos/ConfiguracoesServico', 'r')

                                if len(p.readlines()) == 0:
                                    # quer dizer que está vazio
                                    # Nada deve se fazer e a função deve prosseguir.
                                    p.close()
                                else:
                                    # Caso já haja alguma escrita, não devemos fazer nada em teoria.
                                    return p.close()

                            except FileNotFoundError:
                                # Se o arquivo não existe, devemos criar ele
                                p = open('../SargenteanteAlpha/SubArquivos/ConfiguracoesServico', 'x')
                                p.close()
                                # E dai, ele com certeza estará vazio.

                            configu = ["Padrao(S1):1-12M;1.2-12F;1.4-1M;1.8-2;2-1;3-2;3.5-3;4-4;5-5",
                                       "Padrao(S2):1-1M;1.2-12F;1.4-0;1.8-2;2-1;3-2;3.5-2;4-2",
                                       "Semana Provas:1-12M;1.2-12F;1.4-0;1.8-0;2-0;3-0;3.5-0;4-0;5-0",
                                       "Emergencias:"]

                            primeiralinha = True
                            with open('../SargenteanteAlpha/SubArquivos/ConfiguracoesServico', 'w') as cs:
                                for linha in configu:
                                    if primeiralinha:
                                        cs.write(linha)
                                        primeiralinha = False
                                    else:
                                        cs.write(f'\n{linha}')

                        colocando_configuracoes()

                        def colocando_historico_visualizacao():

                            try:
                                p = open('../SargenteanteAlpha/SubArquivos/HistoricoVisual', 'r')

                                if len(p.readlines()) == 0:
                                    # quer dizer que está vazio
                                    p.close()
                                else:
                                    # já está preenchido
                                    return p.close()

                            except FileNotFoundError:
                                # Estará vazio com certeza, pois será criado
                                p = open('../SargenteanteAlpha/SubArquivos/HistoricoVisual', 'x')
                                p.close()

                            infos = ['85996238611', 'deyvissongamerpinto@gmail.com',
                                     'mathdeyvisson@gmail.com;axaw txcw hekp ypqr']

                            primeira = True
                            with open('../SargenteanteAlpha/SubArquivos/HistoricoVisual', 'w') as hv:
                                for linha in infos:
                                    if primeira:
                                        hv.write(f'{linha}')
                                        primeira = False
                                    else:
                                        hv.write(f'\n{linha}')

                        colocando_historico_visualizacao()

                    inicializando_sanhas()

                    messagebox.showinfo(message='Base de Alunos Criada, você deve reiniciar.')

                except AttributeError:
                    messagebox.showerror('ERROR', message='Houve um erro ao tentar importar as informações\n' +
                                                          'Talvez seja um erro no nome das colunas, deve haver um padrão')

            else:
                pass

        def criando_ambiente():
            App1 = Tk()
            App1.title("Importar Coletivo")
            App1.geometry("400x200")
            App1.configure(background="#dde")
            App1.resizable(False, False)

            def procurando_planilhas_e_mostrando():
                try:
                    # Devemos ter um combobox com os possiveis arquivos que se fará a importação
                    possivel_base = []
                    for arq in os.listdir(os.getcwd()):
                        # print(arq)
                        if '.xlsx' in arq:
                            possivel_base.append(arq)

                    Label(App1, text='Selecione de qual base deseja importar:').place(x=10, y=20)
                    informador(App1, 10, 45,
                               'Há duas formas de importação das planilhas, o que depende de como a planilha está formatada.',
                               'clique em mim')
                    bases1 = ttk.Combobox(App1, values=possivel_base)
                    bases1['state'] = 'readonly'
                    bases1.place(x=230, y=20)
                    bases1.set(possivel_base[0])

                    return bases1
                except IndexError:
                    messagebox.showerror(message='Não foi encontrado nenhuma planilha xlsx na mesma pasta.')

            bases2 = procurando_planilhas_e_mostrando()

            # Devemos ter um entry perguntando o nome do arquivo final que sera criado

            # Esse update aqui faz com que a interface não fique travada devido à destruição da janela passada.
            App1.update_idletasks()

            Label(App1, text='Digite o nome final da base:').place(x=10, y=100)
            Label(App1, text='Ex: CFG-27', bg="#dde").place(x=170, y=130)
            decisao2 = Entry(App1)
            decisao2.place(x=170, y=100)

            Button(App1, text='Importar', command=lambda: importar(bases2, decisao2, App1)).place(x=180, y=160)

            texto = 'Você está prestes a colocar o nome do banco de informações de alunos, você deve colocar um nome com o padrão: CFG-(ano_final_de_formação). Não é necessário adicionar .txt'

            # Ensinando ao usuário como fazer
            messagebox.showinfo(title='INFO',
                                message=texto)

            App1.mainloop()

        criando_ambiente()

    Button(App, text='Criar\nBase\nZerada', command=importando_coletivo, relief='solid').place(x=10, y=10, width=230,
                                                                                               height=300)

    App.mainloop()


if __name__ == '__main__':
    importador()
