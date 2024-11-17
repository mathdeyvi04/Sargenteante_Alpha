import os
from tkinter import messagebox
from tkinter import *
from tkinter import ttk
import datetime as dt
from datetime import datetime
from subfuncoes import (comparando_codigos, codigo_mes, limpeza, obtendo_hoje, obtendo_dif, serv, criando_janela,
                        pegando_info, util_ou_nao, seguinte, ordenador_escalas, informador)

limite_de_busca = 40

"""
Vamos tentar o seguinte, vamos colocar 2 subfunções essenciais. 
    Uma que se encarregada de fazer a limpeza das escalas de 15 em 15 dias. Isto é, todo dia 1 e todo dia 15, haverá a 
    limpeza do arquivo de escalas
    
    Uma que se encarrega de procurar qual o dia da escala mais longe. A da limpeza vai garantir que não precisaremos nos
    preocupar com os dias que estão no prox mes.
"""


def escalador():
    ANO = int(dt.datetime.now().year)

    # vamos fazer a limpeza das escalas antigas
    limpeza(None, 1)

    def obtendo_mais_longe():
        # Esta função vai obter o codigo da escala que está mais longe de ocorrer
        # vamos obter o ano que se passa para gerar o que vamos precisar

        esc_mais_longe = ['', 0]
        for arquivo in os.listdir('../SargenteanteAlpha/Escalas'):

            dias = obtendo_dif(arquivo)

            if dias > esc_mais_longe[1]:
                # achamos uma mais longe
                esc_mais_longe[0] = arquivo
                esc_mais_longe[1] = dias

        # verificar se não houve escala selecionada, então mandar a de hoje
        if esc_mais_longe[0] == '':
            return obtendo_hoje()

        # Com isso, obtendo escala mais antiga quanto a quanitdade de dias até ela, mas so precisamos saber qual é o
        # codigo da escala mais longe

        return esc_mais_longe[0].replace('escala', '')

    codigo_mais_longe = seguinte(obtendo_mais_longe())

    def contingente_disponivel(simulado=False):
        # essa variavel simulacao vai nos dizer se estamos numa simulação ou nao
        # vamos obter todas as pessoas que não estão no descanso e não estão baixadas.

        # Para tanto, devemos montar a lista dos incapacitados
        incapacitados = []

        # vamos ter uma variavel que funcionará apenas para a situação do grifo
        grifo_fodido = []  # ME DEU MUITO SANHA

        try:
            # adicionando as pessoas baixadas, pois elas em absolutamente nenhum momento devem entrar
            try:
                def baixados():
                    with open('../SargenteanteAlpha/SubArquivos/baixados') as bai:
                        for linha2 in bai:
                            linha1 = linha2.split("-")
                            # esta colocando nome de guerra
                            incapacitados.append(linha1[0])

                baixados()
            except:
                messagebox.showerror(message='Erro ao ler baixados')

            # Note que devemos ter em mente quem estará no descanso NA DATA QUE A ESCALA ESTA SENDO CRIADA.
            # Por exemplo, suponha um dia x em que há uma lista y de pessoas em descansos.
            # Estaremos a criar escalas para j dias na frente, onde outras pessoas estarão no descanso, compreende?
            try:
                def descansos():
                    # A função deve conseguir visualizar os descansos referente às duas escalas dos dias anteriores, certo?
                    # Sendo assim, pensemos:

                    # Suponha que estamos em um dia x e criamos a escala para esse dia!
                    # Logo, queremos o descanso promovido pelos dias x-1, x-2, x-3.
                    # Lembre-se que se estamos criando escala para o dia x, não há escala para ser executada neste dia.
                    for arq1 in os.listdir('../SargenteanteAlpha/Escalas'):
                        # Devemos fazer a comparação temporal relativamente ao dia que estamos criando a escala
                        dif = obtendo_dif(arq1, codigo_mais_longe)
                        if dif in [-1, -2]:
                            # agora que achamos as escalas
                            with open(f'Escalas/{arq1}') as esc:
                                for linha7 in esc:
                                    if '\n' in linha7:
                                        linha7 = linha7.replace('\n', '')
                                    linha3 = linha7.split('-')
                                    nome_guerra = pegando_info(linha3[0], [0, 2])
                                    if nome_guerra not in incapacitados:
                                        incapacitados.append(nome_guerra)
                                    # print(f'Incapacitei {linha3[0]}')

                if simulado:
                    # Se for uma simulação, vamos precisar de todos os nomes, então não executaremos
                    pass
                else:
                    descansos()
            except:
                messagebox.showerror(message='Erro ao ler descansados referentes à data')

            # Deveos ter uma função que vai pegar os militares isentos, em geral, serão os do grifo ou da turma de
            # comando
            try:
                def isentos():
                    T = 0 if simulado else messagebox.askyesno(message='Grifo participará?')

                    with open('../SargenteanteAlpha/SubArquivos/Isentos') as ise:
                        for linha in ise:
                            if '\n' in linha:
                                linha = linha.replace('\n', '')
                            linha = linha.split('-')
                            nome = pegando_info(linha[0], [0, 2])
                            if linha[1] == 'grifo':
                                if simulado:
                                    # como é uma simulação, o grifo deve entrar e devemos salvá-lo
                                    grifo_fodido.append(linha[0])

                                else:
                                    # Como não é simulação, vamos deixar que o Sanha reine

                                    if not T and nome not in incapacitados:
                                        incapacitados.append(nome)

                            else:
                                if nome not in incapacitados:
                                    incapacitados.append(nome)

                isentos()
            except:
                messagebox.showerror(message='Erro ao ler os isentos')

        except:
            messagebox.showerror(message='Erro ao tentar incapacitar alguns')

        contingente1 = {1: [],
                        2: [],
                        3: [],
                        4: [],
                        5: []
                        }

        try:
            def pegando_nomes():
                # Sendo assim, devemos montar o contingente de nomes completos
                for arquivo in os.listdir('../SargenteanteAlpha/Arquivos'):
                    if '.txt' in arquivo:
                        turma = 0
                        # Com isso salvamos a turma de cada um
                        for i in range(20, limite_de_busca):
                            if str(i) in arquivo:
                                turma = (dt.datetime.now().year - 2000) + 5 - i

                                if turma not in [1, 2, 3, 4, 5]:
                                    # pois note que se não for um desses numeros, nem faz sentido o Sanha
                                    pass
                                else:
                                    break

                        # Com isso salvamos o nome completo de cada

                        with open(f'Arquivos/{arquivo}') as arq:
                            for linha in arq:
                                linha = linha.split('-')
                                if linha[0] != '\n':
                                    if linha[2] not in incapacitados:
                                        contingente1[turma].append([linha[1], linha[2], linha[3], linha[0]])

            pegando_nomes()

        except:
            messagebox.showerror(message='Erro ao tentar obter contingente')

        try:
            # Agora, vamos pegar as distâncias temporais
            def registros():

                # primeiro, verificar nos registros iniciais.
                def pegando_registros_iniciais():
                    """ PARA PENSAR NA COMPLEXIDADE DO CODIGO, se tivessemos uma lista completa com todos os anos iamos
                    vasculhar cada nome do contingente em todos os nomes do registro, compreende isso?"""

                    for ano1 in contingente1.keys():
                        if len(contingente1[ano1]) != 0:
                            # quer dizer que não está vazio e podemos fazer a busca

                            # so vamos pegar as informações de uma vez, sem qualquer problema ou necessidade
                            base = open(f"Registros/registro{(ANO - 2000) + 5 - ano1}", 'r')
                            lista_completa = base.readlines()
                            base.close()

                            c = 0  # vai guardar informação do contingente
                            for militar_completo, militar_guerra, sexo, num in contingente1[ano1]:
                                for linha in lista_completa:
                                    if militar_completo in linha:
                                        # quer dizer que achamos o militar na lista
                                        data_string = linha.split(',')[1]

                                        if '\n' in data_string:
                                            # Obviamente não vai pegar
                                            data_string = data_string.replace('\n', '')

                                        if len(data_string) > 1:
                                            data_string = data_string.split('-')
                                            data_string = 'escala' + data_string[2] + codigo_mes(
                                                int(data_string[1]), True)

                                            contingente1[ano1][c] = [militar_completo,
                                                                     obtendo_dif(data_string, codigo_mais_longe),
                                                                     militar_guerra,
                                                                     sexo,
                                                                     num]
                                        else:
                                            contingente1[ano1][c] = [militar_completo,
                                                                     data_string,
                                                                     militar_guerra,
                                                                     sexo,
                                                                     num]

                                        # Se já achamos esse cara, não precisamos continuar busca por ele
                                        break

                                c += 1

                pegando_registros_iniciais()

                # Agora, vemos verificar cada uma das escalas que existem até x-2, onde x é o dia que vamos criar a escala.
                def atualizando_registros():
                    # Vamos vasculhar as escalas a fim de encontrar os guerreiros e atualizar os registros

                    # Devemos abrir cada escala e procurar as pessoas da escala no contingente,
                    # O contrário não pode ocorrer, pois é possivel que tenhamos poucas escalas
                    for arq in os.listdir('../SargenteanteAlpha/Escalas'):
                        if obtendo_dif(arq, codigo_mais_longe) not in [-1, -2]:
                            with open(f'Escalas/{arq}') as esc:
                                for linha in esc:
                                    linha = linha.split('-')
                                    # De posse do nome de um dos que estão na escala
                                    # Devemos comparar com o nome do dicionário
                                    for ano1 in contingente1.keys():
                                        if len(contingente1[ano1]) != 0:
                                            # Garantindo que não vamos perder tempo vendo as zeradas

                                            for c in range(0, len(contingente1[ano1])):
                                                if contingente1[ano1][c][2] == linha[0]:
                                                    # achamos um militar que esta na escala e no contingente, devemos
                                                    # modificar o seu correspondente
                                                    contingente1[ano1][c][1] = obtendo_dif(arq, codigo_mais_longe)

                atualizando_registros()

            registros()
        except Exception as e:
            messagebox.showerror(message=f'Erro ao verificar registro do contingente {e}')

        for ano in range(1, 6):
            if len(contingente1[ano]) != 0:
                contingente1[ano].sort()

        if simulado:
            return contingente1, grifo_fodido
        else:
            return contingente1

    def obtendo_conf(configuracoes):
        # Configuracoes vai ser [[1-12M], ...]
        # vamos guardar os serviços que existem na configuracoes
        servicos = {}

        # Quando tivermos x-0, esse zero significa que o serviço não existe

        for forma in configuracoes:
            forma = forma.split('-')
            if forma[1] != '0':
                # pense o seguinte, para cada tipo de serviço, vamos ter as determinadas caracteristicas
                if '\n' in forma[1]:
                    forma[1] = forma[1].replace('\n', '')
                servicos[serv(forma[0])] = forma[1]

        return servicos

    def filtrando_conf(conf, contingente, simulado=False):
        lista = []

        # Vamos verificar a condição de genero
        gen = []
        if conf[-1].isalpha():
            # quer dizer que há segregação de genero
            if conf[-1] == 'M':
                gen.append('M')
                conf = conf.replace('M', '')

            else:
                gen.append('F')
                conf = conf.replace('F', '')
        else:
            # quer dizer que é todos juntos
            gen.append("M")
            gen.append('F')

        if simulado:
            for ano in conf:
                # Algumas pessoas que antes eram baixadas estão chegando sem a data do último serviço RITTO
                for completo, ultimo, guerra, sexo, num in contingente[int(ano)]:
                    if sexo in gen:
                        # quer dizer que temos o grupo
                        lista.append(num)

            return lista
        else:
            # Vamos agora escollher os militares a partir do contingente
            for ano in conf:
                # Algumas pessoas que antes eram baixadas estão chegando sem a data do último serviço RITTO
                for completo, ultimo, guerra, sexo, num in contingente[int(ano)]:
                    if sexo in gen:
                        # quer dizer que temos o grupo
                        lista.append(f'{guerra}*/ {ultimo} /')

                if len(lista) != 0:
                    # Quando inserirmos um ano completo, em teoria, devemos deixar um Sanha separando
                    lista.append('-------')

            return lista

    def permitindo_selecionado(contingente, caracteristicas):

        # Vamos armazenar o nomes do sanha aqui
        escala = {}

        def obtendo_trocados():
            lista = []
            with open('../SargenteanteAlpha/SubArquivos/Trocas') as tr:
                for linha in tr:
                    if '\n' in linha:
                        linha = linha.replace('\n', '')
                    lista.append(linha)

            return lista

        def pegando_descansos():
            # Vamos pegar as pessoas que estão no descanso da última escala existente.
            # Devemos ver se existe uma última escala, caso não, devemos ir ao descanso patrão

            try:
                descanso = []
                # Em teoria, vai ocorrer naturalmente isso aqui
                p = open(f'Escalas/escala{obtendo_mais_longe()}')
                linhas = p.readlines()
                p.close()

                # Lista de [nome, tipo], com tipos repetidos.
                for linha in linhas:
                    linha = linha.split('-')
                    descanso.append(linha)

                ultimo_nome = ''
                ultimo_tipo = ''
                descanso_final = []
                for nome1, tipo1 in descanso:
                    # Se for diferente do anterior
                    if ultimo_tipo != tipo1 and ultimo_nome != '':
                        # quer dizer que se chegamos no primeiro que há a mudança, o nome anterior é o último desse tipo
                        descanso_final.append([ultimo_nome, ultimo_tipo])

                    # Vamos atualizar as sanhas
                    ultimo_tipo = tipo1
                    ultimo_nome = nome1

                return descanso_final

            except FileNotFoundError:
                # Só quando criada a primeira escala
                ultimo = ''
                with open(f'../SargenteanteAlpha/SubArquivos/Descansos') as desc:
                    for linha in desc:
                        linha = linha.split('-')
                        ultimo = linha[0]

                return ultimo

        # Vai gerar uma lista com a última pessoa que tirou cada tipo de serviço, pode ter apenas um.

        # Apenas para melhorar o código
        trocados = obtendo_trocados()

        def apagar_linha(tvw):

            # Pode ser que tenhamos mais de um selecionado, então será sanha
            sele = tvw.selection()

            for it in sele:
                item = tvw.item(it)
                for tipo in escala.keys():
                    for nome in escala[tipo]:
                        if nome == item['values'][1]:
                            escala[tipo].remove(nome)

                tvw.delete(it)

        def salvar():
            if messagebox.askokcancel(title='Certeza?', message='Deseja oficializá-los?'):
                try:
                    # Agora vamos pegar a escala e oficializá-la.
                    # Devemos deixar na ordem de grandeza do serviço

                    # vamos criar o arquivo da escala
                    p = True
                    with open(rf'Escalas/escala{codigo_mais_longe}', 'x') as esc:
                        for tipo in escala.keys():
                            for nome in escala[tipo]:
                                # Como são poucas pessoas, vale o Sanha de busca
                                numero = pegando_info(nome, [2, 0])
                                if p:
                                    esc.write(f'{numero}-{serv(tipo, True)}')
                                    p = False
                                else:
                                    esc.write(f'\n{numero}-{serv(tipo, True)}')

                    janel1.destroy()
                except:
                    messagebox.showerror(message='Erro ao tentar salvar escala')

        def criando_treeview(lista, tvw=None):
            if tvw is not None:
                tvw.destroy()

            p = Frame(janel1, bg='#dde', relief='solid', borderwidth=2)
            p.place(x=420, y=-10, width=1000, height=1000)  # isso é so para garantirmos apenas a linha vertical

            Label(p, text='Escala até agora:', bg='#dde').place(x=10, y=20)

            tv = ttk.Treeview(p, columns=['Tipo', 'Nome de Guerra'],
                              show='headings', selectmode=EXTENDED)

            # Colocando as colunas do treeview
            tv.column('Tipo', minwidth=0, width=60, anchor='center')
            tv.heading('Tipo', text='Tipo')

            tv.column('Nome de Guerra', minwidth=0, width=90, anchor='center')
            tv.heading('Nome de Guerra', text='Nome de Guerra')

            tv.place(x=10, y=57, height=270, width=250)

            # Aplicando as informações do TreeView

            try:
                for tipo in lista.keys():
                    for militar in lista[tipo]:
                        tv.insert('', 'end', values=[tipo, militar])
            except:
                pass

            Button(p, text='Retirar Militares', command=lambda: apagar_linha(tv)).place(x=100, y=350)

            Button(p, text='Efetivar', command=salvar).place(x=120, y=380)

            return tv

        def selecionar(tvw, nome, tipo, sublista1, comboboxs):
            # Devemos adicionar o nome colocado ao treeview

            # A partir do nome, vamos:
            if tipo not in escala.keys():
                escala[tipo] = []

            if nome in sublista1:

                # Teoricamente, assim conseguimos pegar o nome sem sanha do último serviço
                nome = nome.split('*')[0]

                for tipo in escala.keys():
                    if nome in escala[tipo]:
                        return messagebox.showwarning(message='Já presente na escala')

                # Vamos fazer verificações de trocas no Emergencias, pois pare para pensar que as trocas ocorrem
                # so dps que a escala é enviada.

                # Devemos fazer verificação para ver se a pessoa selecionada esta esperando uma troca de serviço!
                # Normalmente, vamos supor que a pessoa x que deveria ser é substituida por uma pessoa y.
                # O privilegiado é o x. Logo, na proxima vez que a pessoa y for selecionada para um serviço
                # o sistema deve verificar se essa pessoa y esta na prioridade para ser trocada e for
                def verificador_trocado():

                    # Devemos verificar se ele está em alguma situação de troca
                    opcao = 0
                    decisao = 0
                    for situacao in trocados:
                        if pegando_info(nome, [2, 0]) in situacao:
                            s1, s2, data = situacao.split("-")
                            # Achamos o Sanha
                            # Devemos informar ao usuário
                            msg = f"""Há um registro onde {s1} saiu e {s2} entrou substituindo-o na escala do dia {data}, deseja apagar o registro?"""

                            decisao = messagebox.askyesnocancel(message=msg)

                            if decisao is None:
                                # Vamos encerrar tudo
                                return 1
                            else:
                                break

                        opcao += 1

                    if decisao:
                        # Vamos ter que apagar o sanha
                        trocados.remove(trocados[opcao])

                        os.remove('../SargenteanteAlpha/SubArquivos/Trocas')

                        primeiro = True
                        with open('../SargenteanteAlpha/SubArquivos/Trocas', 'x') as tr:
                            for linha in trocados:
                                if primeiro:
                                    tr.write(f'{linha}')
                                else:
                                    tr.write(f'\n{linha}')

                if verificador_trocado() == 1:
                    return None

                for cb in comboboxs:
                    lista_alunos = cb['values']
                    for geral in lista_alunos:
                        if nome in geral:
                            cb.set(geral)

                            # Não há necessidade de procurar mais
                            break

                escala[tipo].append(nome)
                criando_treeview(tvw=tvw, lista=escala)
            else:
                return messagebox.showwarning(message='Esse aluno não existe')

        def escolhendo():

            tv = criando_treeview(lista=escala)
            a = 1
            b = 0
            lista_cbs = []
            desca = pegando_descansos()

            def ultima_pessoa(tip1, lista_nomes):
                if type(desca) == str:
                    return desca
                else:
                    # É uma lista onde há os nomes e os tipos de serviços
                    for nome2, tipo2 in desca:
                        if tipo2 == tip1:
                            return nome2

                    # Se chegamos aqui, quer dizer não haver sanha a ser verificado
                    return lista_nomes[0]

            for tipo in caracteristicas.keys():

                # Numa lista, devemos ter os combobox e os respectivos botões
                # Esse Sanha é a lista de alunos que podem tirar o serviço
                sanha = filtrando_conf(caracteristicas[tipo], contingente)
                if len(sanha) != 0:
                    # Os frames deverão ser guardados? Talvez não
                    p = Frame(janel1, bg='#dde', relief='solid', borderwidth=2)
                    p.place(x=10, y=b + a * 50, width=400, height=50)

                    Label(p, text=tipo, bg='#dde').place(x=10, y=13)
                    cb = ttk.Combobox(p, values=sanha)
                    cb['state'] = 'readonly'
                    cb.place(x=120, y=13, width=150)
                    cb.set(ultima_pessoa(tipo, sanha))
                    lista_cbs.append(cb)

                    bt = Button(p, text='Selecionar')
                    # VAMOS FAZER DESSE MODO, para conseguirmos garantir que o botão veja o respectivo combobox
                    bt['command'] = lambda cbb=cb, tipoo=tipo, lista0=sanha: selecionar(tv, cbb.get(), tipoo, lista0,
                                                                                        lista_cbs)
                    bt.place(x=300, y=13)
                    # Note que não coloquei nada para que a lista seja adicionada como momentanea, eu coloquei assim para que
                    # a função veja todas simultaneamente

                    a += 1
                    b += 20

        # Devemos criar uma forma mais inteligente de lidar com a altura dessa janela
        c = len(caracteristicas)
        if 50 * c > 420:
            c = 60 * c
        else:
            c = 420
        # Ótimo, pensamos em usar a altura do botão de efetivar, a qual é constante

        janel1 = criando_janela(f'Criando Escala {codigo_mais_longe}', 700, c)

        tipo_escala = ['Preta', 'Vermelha']
        global preta_vermelha
        preta_vermelha = 0  # vamos iniciar isso para termos se a escala é preta ou vermelha

        Label(janel1, text=f'Visualizando escala {tipo_escala[preta_vermelha % 2]}', bg='#dde').place(x=5, y=10,
                                                                                                      width=170)

        def alternador():
            global preta_vermelha
            preta_vermelha += 1
            Label(janel1, text=f'Visualizando escala {tipo_escala[preta_vermelha % 2]}', bg='#dde').place(x=5, y=10,
                                                                                                          width=170)
            if preta_vermelha % 2 == 0:
                # queremos escala preta, que é ordem padrao que ja esta
                ordem = False
            else:
                ordem = True

            # Devemos ordenar mudando o contingente e escrevendo por cima logo dps
            for ano in contingente.keys():
                if len(contingente[ano]) != 0:
                    contingente[ano].sort(key=lambda sublista: sublista[0], reverse=ordem)

            # agora escrevendo por cima
            escolhendo()

        escolhendo()

        Button(janel1, text='Trocar Escala', command=alternador).place(x=200, y=10)

        janel1.mainloop()

    def executando_simulacao(informacoes):
        # Informacoes é um dicionário com todos as Sanhas que precisaremos
        # informacoes = {'ID', ..., 'tipo': 'xyz...', ..., 'final', 'conf'}, é isso eu juro
        # onde xyz são as respectivas quantidades dos serviços nos dias da semana

        # Vamos obter o primeiro dia em que não há escala
        hoje_carteado = codigo_mais_longe

        # Precisamos analisar todos os descansos
        def descansos():
            # Vamos montar 2 listas de descansos, uma para dias uteis e outro para dias não uteis
            desc_total = []
            # Essa lista total é do tipo [numero, tipo servico, dia final, se tirou em dia util ou não

            escalas_gerais = os.listdir('../SargenteanteAlpha/Escalas')

            # devemos ter uma maneira de ordenar elas pelo sanha.
            escalas_gerais = ordenador_escalas(escalas_gerais)

            for arq in escalas_gerais:
                with open(f'Escalas/{arq}') as esc:
                    # print(f'Estou abrindo {arq}')
                    for linha in esc:
                        if '\n' in linha:
                            linha = linha.replace("\n", '')
                        linha = linha.split('-')
                        desc_total.append([linha[0],
                                           linha[1],
                                           seguinte(seguinte(seguinte(arq.replace('escala', '')))),
                                           util_ou_nao(arq.replace('escala', ''))
                                           ])

            desc_util = [sublista[:3] for sublista in desc_total if sublista[-1]]
            desc_nao_util = [lista_[:3] for lista_ in desc_total if not lista_[-1]]

            # Devemos fazer apenas uma verificação se ja passou do dia final do descanso para os sanhudos da escala
            # util

            return desc_util, desc_nao_util

            # Agora, devemos filtrar e usar o Sanha conosco

        # Vamos criar a logica para a escala de sentinela durante o loop mesmo, pois ela é muito carteada

        # Vamos apenas obter os iniciais, não precisamos colocar isso no loop
        descansos_util, descansos_nao_util = descansos()

        # print(f'A ordem é {descansos_util} e {descansos_nao_util}')

        # print(descansos_nao_util)
        # Precisamos das duas listas, pois o sanha é infinito
        # Estamos tendo desc = [[numero, tipo, dia_final]]

        # Devemos ter uma função capaz de saber que tipo de dia é e, além disso, informar o tipo de serviço do dia,
        # e a respectiva quantidade, note que essa função deve estar dentro do loop
        def servicos_do_dia(hj):

            def obtendo_dia_semana():
                # Ja vai nos retornar o número correspondente a semana
                # Dom - 0, Seg - 1, ...
                data = dt.date(ANO, int(codigo_mes(hj[-1], False)), int(hj.replace(hj[-1], '')))
                dia_c = data.weekday()

                if dia_c == 6:
                    dia_c = 0
                else:
                    # Para ficar no nosso referencial
                    dia_c += 1

                if util_ou_nao(hj):
                    return dia_c, True
                else:
                    return dia_c, False

            dia_semana, util1 = obtendo_dia_semana()

            def obtendo_servicos_quantidades():

                # Vamos guardar os serviços e as quantidades aqui na sanha
                serv_quant = []
                # Vamos varrer as chaves das informações e verificar o Sanha
                for chave in informacoes.keys():
                    if chave not in ['ID', 'final', 'conf']:
                        # Quer dizer que temos um tipo serviço
                        # A sua quantidade está relacionada na ‘string’ que o guarda
                        serv_quant.append([chave, int(informacoes[chave][dia_semana])])
                return serv_quant

            return obtendo_servicos_quantidades(), util1

        # Vamos obter ( [[tipo_serv, quantidade]], True se for dia util e Falso se não )

        # Com esta, obtemos um dicionário composto por listas de números ordenadas como se fosse dia util para cada
        # tipo de serviço correspondente
        def contingente_servicos():
            # Como usamos essa função no modo simulado, temos uma lista com o contingente, completo,
            # tirando os baixados
            # Para o serviço dos dias não uteis, devemos olhar nos registros a sanha, pois é assim que funciona!!

            dic_anos, grifo = contingente_disponivel(True)

            # Mas ainda precisamos lapidar esse Sanha
            """
            def ordenando_por_alfabetica():
                for ano in dic_anos.keys():
                    if len(dic_anos[ano]) != 0:
                        dic_anos[ano].sort(key=lambda sublista: sublista[0])
                        
            ordenando_por_alfabetica()
            """

            # Em teoria, mas parece que já está ordenada

            # Vamos obter as especificacoes de serviço
            def obtendo_especificacoes():
                with open('../SargenteanteAlpha/SubArquivos/ConfiguracoesServico') as ss:
                    for linha in ss:
                        if informacoes['conf'] in linha:
                            if '\n' in linha:
                                linha = linha.replace("\n", '')
                            linha = linha.split(":")
                            linha = linha[1].split(';')
                            lista = list(linha)
                            break

                c = 0
                # Separando ainda mais
                for sublista in lista:
                    lista[c] = sublista.split('-')
                    c += 1

                return lista

            especificacoes = obtendo_especificacoes()

            def organizando_escalas():
                conting_final = {}
                for tipo, especificacoes_do_tipo in especificacoes:
                    if tipo in informacoes.keys():
                        # Se queremos um tipo de serviço
                        # vamos mexer nele
                        conting_final[tipo] = filtrando_conf(especificacoes_do_tipo, dic_anos, True)

                return conting_final

            return organizando_escalas(), grifo

        # Vamos pegar os alunos aqui
        contingente_total_serv, grifo1 = contingente_servicos()

        # Obtemos {tipo: [numeros ordenados como se fossem ordenados em dia util]}

        def limpeza_servico(lista1, hj):
            # Como a lista de descanso é pequena, não precisaremos nos preocupar com tanto Sanha

            def ultima_do_serv(sv, numero):
                # deve retornar se há apenas um desse tipo de serviço e se o militar é o último dele
                quant = 0
                num = 0
                for sub in lista1:
                    if sub[1] == sv:
                        quant += 1
                        num = sub[0]

                if quant > 1:
                    # Há mais de uma pessoa nesse serviço
                    # Devemos verificar se é o último
                    if num == numero:
                        # Não é o único, e é o último
                        return False, True
                    else:
                        # Não é o único, e não é o último
                        return False, False
                else:
                    # quer dizer que é o único e é o último tbm, obvio
                    return True, True

            # Verificando
            a_serem_apagados = []
            for sublista in lista1:
                # vamos varrer a lista de descanso
                # print(f'Para {sublista[0]}, estou a obter {ultima_do_serv(sublista[1], sublista[0])}')
                if sublista[2] == hj or comparando_codigos(sublista[2], hj):
                    # Estamos a fazer assim, pois o comparando_codigos(x, x) vai retornar falso, logo com esse primeiro
                    # pegamos o caso de x=y e o outro todos os outros casos
                    # print(f'Devo verificar {sublista[0]}')

                    resultados = ultima_do_serv(sublista[1], sublista[0])

                    if resultados[0]:
                        # quer dizer é o único e o último, logo não devemos fazer nada
                        # print(f'{sublista[0]} é o unico e o último')
                        pass
                    else:
                        if resultados[1]:
                            # Não é o único, mas é o último, logo não devemos fazer nada apenas seguir
                            # print(f'{sublista[0]} não é unico, mas é o último')
                            pass
                        else:
                            # Não é o único nem o último
                            # print(f'{sublista[0]} não é o unico e não é o último, logo, vou retirá-lo')
                            a_serem_apagados.append(sublista)

            # Apagando
            # print(a_serem_apagados)
            for elemento in a_serem_apagados:
                lista1.remove(elemento)

                # Vamos limpar todos os que já chegaram no descanso, menos quando é o último de cada respectivo tipo de serviço

        quero_ver = False

        # Agora, devemos o iniciar o sanha para calcular as pessoas das escalas simuladas
        def formando_escala(dia, tipo_dia, serv_quant, lista_descanso, total_para_servico, outra_lista_descanso):
            # Devemos receber um dicionário de cada tipo de serviço e a quantidade respectiva para este serviço
            # Além disso, devemos receber que tipo de dia é, útil ou não.

            # for tipo, quantidade in serv_quant:

            # Aqui, construimos o Sanha para cada tipo de serviço
            def simulada_do_serv(tipo, quantidade):
                # vamos considerar que ela já está ordenada corretamente
                # deve retornar o indice do aluno que vai ser o primeiro a ser escolhido

                # vamos obter a última pessoa que tirou esse tipo de serviço
                def ultimo():
                    # vamos obter a última pessoa que tirou esse tipo de serviço
                    numero = 0
                    for sublista in lista_descanso:
                        if sublista[1] == tipo:
                            # achamos alguem com o mesmo tipo de serviço, vamos salvar o seu número
                            numero = sublista[0]

                    # Em teoria, note que se não houver ninguém que tirou esse serviço ainda, devemos pegar o primeiro
                    # número antisafo
                    if numero == 0:
                        # O PRIMEIRO DA LISTA DE NÚMEROS, NÃO O PRIMEIRO DA LISTA DE DESCANSO, ANIMAL
                        # Pense um pouco, se retornarmos o número da posição 0, é como se o primeiro já tivesse tirado
                        # Logo, precisamos informar o Sanha para a próxima função
                        pass
                    else:
                        # Necessariamente, ele será o último
                        pass
                    return numero

                ultimo_sanhudo = ultimo()

                # print(f'O último que tirou {tipo} foi {ultimo_sanhudo}')

                # De posse do último, devemos obter a posição dele
                def obtendo_indice(pessoa):
                    if pessoa == 0:
                        # Quer dizer que não há uma última pessoa nesse tipo, logo
                        return -1
                    else:
                        # vamos varrer o contingente do serviço e obter o indice da sua posição na lista
                        indice = 0
                        for numero in total_para_servico[tipo]:
                            # print(f'Comparando {numero} com {ultimo_sanhudo}')
                            if numero == pessoa:
                                # achamos ele
                                return indice

                            indice += 1

                indice_ultimo_sanhudo = obtendo_indice(ultimo_sanhudo)

                # Ele é o último desse serviço no descanso
                # Devemos conseguir obter os próximos nomes das pessoas seguintes que não estão no descanso também
                def obtendo_pessoas(pos):

                    try:
                        def verificacao_se_pode_tirar_servi(num):

                            # Em teoria, isso deve resolver.

                            # LEMBRA DO GRIFO, SENTINELA
                            def nao_esta_descanso_1():

                                for sublista in lista_descanso:
                                    # Procurando ele na lista
                                    if sublista[0] == num:
                                        # print(f'---Apesar de tudo, {numero} está na lista de descanso normal', end='')
                                        # print(f'E o resultado da sua comparação com {hoje_carteado} é {comparando_codigos(sublista[-1], hoje_carteado)}')
                                        if comparando_codigos(sublista[-1], hoje_carteado) or sublista[
                                            -1] == hoje_carteado:
                                            # Ele não está no descanso
                                            return True
                                        else:
                                            # Quer dizer que ele ainda está no descanso
                                            return False

                                # Como não foi achado, ele não está nem lá
                                return True

                            if nao_esta_descanso_1():
                                # Se não está nesse descanso, devemos continuar
                                pass
                            else:
                                # Como está presente, nem adianta procurar o resto
                                return False

                            def nao_esta_descanso_2():

                                for sublista in outra_lista_descanso:
                                    # Procurando ele na lista
                                    if sublista[0] == num:
                                        # print(f'---Apesar de tudo, {numero} está na lista de descanso contrária', end='')
                                        # print(f'E o resultado da comparação de {sublista[-1]} com {hoje_carteado} é {comparando_codigos(sublista[-1], hoje_carteado)}')
                                        if comparando_codigos(sublista[-1], hoje_carteado) or sublista[
                                            -1] == hoje_carteado:
                                            # Ele não está no descanso
                                            return True
                                        else:
                                            # Quer dizer que ele ainda está no descanso
                                            return False

                                # Como não foi achado, ele não está nem lá
                                return True

                            if nao_esta_descanso_2():
                                # Se não está nesse descanso, devemos continuar
                                pass
                            else:
                                # Como está presente, nem adianta procurar o resto
                                return False

                            # Como passou das duas verificacoes, ele teoricamente pode tirar o serviço
                            # Mas falta verificar se ele é do grifo
                            def grifou():

                                if num in grifo1:
                                    # se pertence ao grifo

                                    if tipo_dia:
                                        # Se for dia útil, o grifo não pode tirar
                                        return False
                                    else:
                                        # Caso não seja dia útil, ele pode tirar
                                        return True

                                else:
                                    # Caso não, pode tirar
                                    return True

                            return grifou()

                        escaladas = []
                        # Varrer a lista usando isso
                        var = 1  # Deve começar com 1, pois o último que tirou não deve ser considerado
                        # tam = len(escaladas) Isso obviamente está errado, pois pegamos o len de forma estática, ou seja,
                        # esse valor não vai mudar
                        tam = 0
                        ja_procurei_muito_mas_nao_tem = 0
                        while True:

                            try:

                                if tam == quantidade or len(total_para_servico[tipo]) == 0:
                                    # se ja chegamos ao limite desejado
                                    break

                                if quero_ver:
                                    print(f'O index que estou procurando é {pos + var}')

                                numero = total_para_servico[tipo][pos + var]

                                if verificacao_se_pode_tirar_servi(numero):
                                    # não estiver no descanso
                                    # vamos adicionar ele na escala
                                    escaladas.append(numero)
                                    tam += 1
                                    if quero_ver:
                                        print(
                                            f'Vou adicionar {numero} em {tipo}, pois não achei o achei em {lista_descanso} nem em {outra_lista_descanso}')

                                else:
                                    if quero_ver:
                                        print(f'Não posso adicionar {numero}, pois está em algum descanso')
                                    pass

                                var += 1
                            except IndexError:
                                # quer dizer que chegamos ao final, portanto, devemos voltar ao Sanha inicial
                                var = - pos

                                ja_procurei_muito_mas_nao_tem += 1

                                if ja_procurei_muito_mas_nao_tem == 3:
                                    return messagebox.showerror(title='ERRO CRÍTICO',
                                                                message='NÃO HÁ CONTINGENTE SUFICIENTE PARA A SIMULAÇÃO OCORRER')

                        return escaladas
                    except TypeError:
                        return messagebox.showerror(message=f'Não há contingente SUFICIENTE para o serviço {serv(tipo, False)}')

                # Devemos retornar uma lista tal que [tipo, numeros escalados]
                return obtendo_pessoas(indice_ultimo_sanhudo)

            # Vamos receber uma lista de números para esse tipo específico de serviço

            # Agora, devemos construir o Sanha para cada dia
            def simulada_do_dia():

                escala = []

                for tipo, quantidade in serv_quant:
                    subescala = simulada_do_serv(tipo, quantidade)
                    for pessoa in subescala:
                        escala.append(pessoa)
                        lista_descanso.append([pessoa, tipo, seguinte(seguinte(seguinte(dia)))])

                return [dia, escala]

            return simulada_do_dia()

        def configurando(util_ou_nao1, const_ordenadacao, total):

            if util_ou_nao1:
                if const_ordenadacao:
                    # Se for dia útil, e já estiver ordenada como tal, não precisamos fazer nada
                    pass
                else:
                    # Se for dia útil e não estiver ordenada como tal,
                    # Vai deixar ordenada como se fosse dia util
                    for chave in total.keys():
                        # Tenho que colocar essa parte do sentinela aqui também
                        if len(total[chave]) != 0 and chave != '2':
                            total[chave] = total[chave][::-1]

                    const_ordenadacao = True
            else:
                if const_ordenadacao:
                    # Se não for dia útil e não estiver ordenada como dia não útil
                    # Vai deixar ordenada como se fosse dia não útil
                    for chave in total.keys():
                        # Colocamos essa verificação, pois se for Sentinela, não queremos nada seja feito, deve ser sempre
                        # ordenada como dia útil
                        if len(total[chave]) != 0 and chave != '2':
                            total[chave] = total[chave][::-1]

                    const_ordenadacao = False
                else:
                    # Se não for dia útil e estiver ordenada como tal
                    pass

            return total, const_ordenadacao

        # Devemos perguntar ao usuário se ele deseja salvar as escalas sanhudas
        decisao_salvamento = False
        if messagebox.askyesno(message='Deseja salvar as escalas de forma oficial?'):
            decisao_salvamento = True

        def salvando(dia_escala, sv_qu, quer_salvar):
            # Vamos receber uma lista do tipo [dia, [numeros escalados]
            # E outra lista [tipo_serv, quantidade_respectiva]

            if quer_salvar:
                primeira_linha = True
                with open(f'Escalas/escala{dia_escala[0]}', 'x') as esc_criada:
                    de_qual_tipo = 0
                    quantidade = 0

                    for pessoa in dia_escala[1]:

                        # Se essa pessoa está na escala desse dia, seria interessante avisar ao usuário em quais dias ele está
                        # Segundo essa simulação
                        # O ponto é que isso só vai ser executado caso o usuário queira salvar
                        if informacoes['ID'] == pessoa:
                            messagebox.showinfo(
                                message=f'Encontrei a pessoa procurada na escala do dia {dia_escala[0]}')
                        # Sendo assim, devemos ter algo fora também

                        # Vamos ver as pessoas que estão na escala
                        if quantidade == sv_qu[de_qual_tipo][1]:
                            # quer dizer que já adicionamos as pessoas suficientes para o tipo
                            # Logo, precisamos fazer a quantidade voltar a zero
                            quantidade = 0
                            # E mudar o tipo que estamos vendo
                            de_qual_tipo += 1

                        if primeira_linha:

                            esc_criada.write(f'{pessoa}-{sv_qu[de_qual_tipo][0]}')

                            primeira_linha = False
                        else:

                            esc_criada.write(f'\n{pessoa}-{sv_qu[de_qual_tipo][0]}')

                        # Sabendo que independe de qualquer coisa estamos adicionando uma pessoa
                        quantidade += 1
            else:
                if informacoes['ID'] != '0':
                    for numero in dia_escala[1]:
                        if informacoes['ID'] == numero:
                            messagebox.showinfo(
                                message=f'Encontrei a pessoa procurada na escala do dia {dia_escala[0]}')

        # Este é o loop da simulação
        ordenada_como_util = True
        while True:

            if seguinte(informacoes['final']) == hoje_carteado:
                # ja finalizamos a simulação
                break

            # Vamos obter as informações do dia
            servicos_quantidades, dia_util_ou = servicos_do_dia(hoje_carteado)

            limpeza_servico(descansos_util if dia_util_ou else descansos_nao_util, hoje_carteado)

            # Configurando a lista total para escala preta ou vermelha
            lista_total, ordenada_como_util = configurando(dia_util_ou, ordenada_como_util, contingente_total_serv)

            # print(f'\nHoje é {hoje_carteado}')
            # print(f'Pegando as pessoas de: {lista_total}')
            # print(f'Criando a partir do descanso {dia_util_ou}: {descansos_util if dia_util_ou else descansos_nao_util}')
            # print(f'Preciso para "hoje" {servicos_quantidades}')
            # Por que não podemos fazer:
            # lista = descansos_util if dia_util_ou else descansos_nao_util
            # Porque alterariamos o valor de lista e não do descanso exatamente
            def mostrando():
                if quero_ver:
                    print(f'\nHoje é {hoje_carteado}')
                    print(f'Pegando as pessoas de: {lista_total}')
                    print(
                        f'Criando a partir do descanso {dia_util_ou}: {descansos_util if dia_util_ou else descansos_nao_util}')
                    print(f'Preciso para "hoje" {servicos_quantidades}')

            mostrando()

            """DEVEMOS VER A SITUAÇÃO DO SENTINELA"""
            # Vamos montar a escala do dia aqui
            escala_simulada = formando_escala(hoje_carteado,
                                              dia_util_ou,
                                              servicos_quantidades,
                                              descansos_util if dia_util_ou else descansos_nao_util,
                                              lista_total,
                                              descansos_nao_util if dia_util_ou else descansos_util)

            if quero_ver:
                print(f'Montei {escala_simulada}')  # Já mostra o dia também

            salvando(escala_simulada, servicos_quantidades, decisao_salvamento)

            # Vamos para o próximo dia
            hoje_carteado = seguinte(hoje_carteado)

            # Vamos fazer a limpeza
            limpeza_servico(descansos_util, hoje_carteado)
            limpeza_servico(descansos_nao_util, hoje_carteado)

            if quero_ver:
                print(f'Fiz a limpeza do descanso {dia_util_ou}')

    # Funções responsáveis pelo Front End

    def FrontEnd():

        janela = criando_janela('Escalador', 300, 400)

        b = 25

        def Criando_Escala():
            janela.destroy()

            # Aqui vamos criar a sanha, devemos criar uma nova janela já mostrando as coisas que iremos fazer
            def pegando_config():
                # Vai guardar as possiveis configurações
                possibilidades = []

                # Vamos pegar as informações gerais
                with open('../SargenteanteAlpha/SubArquivos/ConfiguracoesServico') as ss:
                    for linha in ss:
                        if linha[-1] == '\n':
                            linha = linha.replace('\n', '')

                        possibilidades.append(linha.split(':'))

                # vamos criar a janela a depender da quantidade
                a = len(possibilidades)

                jan1 = criando_janela('', 200, 100 + a * 50)

                fra = Frame(jan1, relief='solid', borderwidth=2, bg='#dde')
                fra.place(x=5, y=5, width=190, height=100 + a * 50 - 10)

                Label(fra, text='Decida a situação do dia:', bg='#dde').place(x=10, y=10)

                opcao = IntVar(fra)

                k = 1
                for possib, conf in possibilidades:
                    Radiobutton(fra, text=possib, variable=opcao, value=k - 1, bg='#dde').place(x=10, y=10 + k * 30)
                    k += 1

                return jan1, opcao, a, possibilidades

            if messagebox.askokcancel(message=f'Você estará criando a escala do dia {codigo_mais_longe}'):
                # Devemos ter a situação do dia que vamos criar, se ele vai ser safo ou carteado

                # Vamos criar uma janela, a opcao de config, o tamanho regulado da tela e as configuracoes, respectivamente
                jan, opc, b1, config1 = pegando_config()

                def mostrar():
                    especificacoes_selecionadas = config1[opc.get()][1]
                    config_selecionada = config1[opc.get()][0]
                    jan.destroy()

                    if config_selecionada == 'Emergencias':

                        # Devemos montar uma nova janela pedindo que o usuário insira cada uma de suas necessidades

                        sanha = criando_janela('Emergenciando', 200, 400)
                        sanha.update_idletasks()

                        # Vai devolver a correlação de cada tipo de serviço
                        tipos = {
                            "1": 'PtSegMasc',
                            "1.2": 'PtSegFem',
                            "1.4": '3° Piso',
                            "1.8": 'Cabo',
                            "2": 'Sentinela',
                            "3": 'Cabo da Guarda',
                            "3.5": 'Cdt da Guarda',
                            "4": 'Sgt',
                            "5": 'Aux Of'
                        }

                        # Vamos guardar os valores inseridos pelo usuário aqui
                        valores = []
                        posy = 20
                        for objeto in tipos.values():
                            # Para cada um vamos criar um combobox e mostrar ao usuário
                            Label(sanha, text=objeto, bg='#dde').place(x=10, y=posy)
                            resp = Entry(sanha)
                            resp.place(x=100, y=posy, width=50)
                            posy += 30
                            valores.append(resp)

                        def pegando():
                            # Vamos varrer as entradas e pegar os valores que estão nelas
                            index = 0
                            lista_tipos = list(tipos.keys())
                            especificacoes_de_emergencia = ''
                            primeiro = True
                            for entrada in valores:
                                entrada = entrada.get()

                                # Verificando
                                if entrada.isnumeric():
                                    if primeiro:
                                        especificacoes_de_emergencia = especificacoes_de_emergencia + f'{lista_tipos[index]}-{entrada}'
                                        primeiro = False
                                    else:
                                        especificacoes_de_emergencia = especificacoes_de_emergencia + f';{lista_tipos[index]}-{entrada}'

                                else:
                                    # impede e pede que corriga
                                    return messagebox.showwarning(message='Apenas números serão permitidos')

                                index += 1

                            sanha.destroy()
                            print(especificacoes_de_emergencia)
                            criando_escala(especificacoes_de_emergencia)

                        Button(sanha, text='Pegar', command=pegando).place(x=10, y=posy)

                        messagebox.showinfo(message='Você deve preencher que anos participarão de cada serviço.')

                        sanha.mainloop()
                    else:
                        criando_escala(especificacoes_selecionadas)

                Button(jan, text='Escolher', command=mostrar).place(x=120, y=50 + b1 * 50)
                informador(jan, 90, 50 + b1 * 50,
                           'Essas opções definem quais anos irão pegar os respectivos serviços.')

                def criando_escala(configuracoes):

                    if configuracoes == '':
                        # ESSE IF SO VAI SER EXECUTADO SE FOR UMA EMERGENCIA
                        pass
                    else:
                        # vamos ter que separar os tipos de serviço
                        configuracoes = configuracoes.split(';')

                        servicos1 = obtendo_conf(configuracoes)

                        # Se o último caractere for M ou F, quer dizer que é contingente mac ou fem. Se não tem nada, são ambos
                        # Os números indicarão os anos que participam do Sanha

                        # Vamos fazer tudo aqui
                        permitindo_selecionado(contingente_disponivel(), servicos1)

        Button(janela, text='Criando Escala', command=Criando_Escala, borderwidth=5).place(x=10, y=b, width=280,
                                                                                           height=100)

        def Criando_Simulacoes():
            janela.destroy()

            # Vamos fazer as Sanhas reais

            infos = {}

            def recebendo_info():
                tela = criando_janela('Condiçoes Iniciais', 630, 460)

                Label(tela, text='Insira o número da pessoa: ', bg='#dde').place(x=10, y=10)
                nu = Entry(tela)
                nu.place(x=160, y=10, width=60)
                Label(tela,
                      text='Caso coloque, sistema mostrará para você em quais escalas está presente.').place(
                    x=230, y=10)

                tipos_serv = ['PtSegMasc', '3° Piso', 'PtSegFem', 'Sentinela',
                              'Cabo', 'Cabo da Guarda', 'Cdt da Guarda',
                              'Sgt',
                              'Aux Of']

                def pegando_quantidades_postos():
                    Label(tela, text='Informe as configurações de simulação: # Não clique em nenhuma para padronizar',
                          bg='#dde').place(x=10, y=40)

                    informador(tela, 470, 40, 'Esses números indicam quantos postos de cada serviço teremos.',
                               'clique em mim')

                    informador(tela, 580, 40,
                               'Caso você não selecione nada nenhum botão, o sistema setará uma configuração de serviços e de postos. Você deverá escolher entre duas opções.')

                    # vamos criar vários botões de check para inserir quais serviços serão considerados no período
                    # e a quantidade de cada um.

                    # Vamos salvar os nossos dados com isso
                    variaveis = []
                    spin_boxs = []

                    # Vamos ter as variaveis de cada um
                    # Vamos ter os spin_boxs de cada checkbutton que foi clicado, logo precisamos saber o indice do respectivo
                    # sendo assim no spinbox, teremos [[indice, [sbs]]

                    def spinbox(y, i):
                        # Vai criar um spinbox quando necessário e ainda vai permitir
                        dias_semana = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sab']

                        # Vamos salvar o indice correspondente ao sanha e o valor dos spins
                        spin_boxs.append([i, []])

                        posx = 130
                        for dia in dias_semana:
                            Label(tela, text=dia, bg='#dde').place(x=posx, y=y + 2)
                            sb = Spinbox(tela, from_=1, to=9)
                            sb.place(x=posx + 30, y=y, width=30)
                            posx += 70

                            # Assim vamos sempre pegar a última lista e ainda a sua segunda posição, que é uma lista
                            spin_boxs[-1][1].append(sb)

                    pos_x = 10
                    pos_y = 70
                    for c in range(0, len(tipos_serv)):
                        # Vamos criar os meios para obter as informações
                        var = IntVar(tela)  # tela dentro dos parenthesis colocou-me NUM JANGAU ABSOLUTO
                        cb = Checkbutton(tela, text=tipos_serv[c], bg='#dde',
                                         variable=var, onvalue=1, offvalue=0,
                                         command=lambda psy=pos_y, ind=c: spinbox(psy, ind))
                        cb.place(x=pos_x, y=pos_y)
                        variaveis.append(var)

                        pos_y += 30

                    return variaveis, spin_boxs

                variaveis1, spin_boxs1 = pegando_quantidades_postos()

                Label(tela, text='Insira a data final desejada: ', bg='#dde').place(x=10, y=340)
                dt_f = Entry(tela)
                dt_f.place(x=170, y=340)

                possi = []
                Label(tela, text='Informe a configuração desejada: ', bg='#dde').place(x=10, y=370)
                informador(tela, 300, 370, 'Se trata de quais anos vão concorrer a cada serviço.')

                with open('../SargenteanteAlpha/SubArquivos/ConfiguracoesServico') as ss:
                    for linha in ss:
                        possi.append(linha.split(':')[0])
                cb1 = ttk.Combobox(tela, values=possi)
                cb1['state'] = 'readonly'
                cb1.set(possi[0])
                cb1.place(x=200, y=370, width=80)

                def salvando():
                    # Salvar o número
                    num = nu.get()
                    if num.isnumeric() and 10000 < int(num) < 99999:
                        infos['ID'] = num
                    elif num == '':
                        infos['ID'] = '0'
                    else:
                        # Não precisa ter um clear aqui, pois se o if não foi executado, nem haverá nada no infos
                        return messagebox.showwarning(message='O número está incorretamente digitado')

                    # Vamos salvar as variaveis e as respectivas quantidades de cada um escolhido pelo usuário.
                    # Vamos precisar varrer todas as unidades de checkbutton e criar classes nos infos.
                    # Para cada classe que salvarmos, vamos precisar o indice correspondente ao tipo de serviço e tam-
                    # bem a quantidade.

                    def quantidades():

                        def obtendo_spins_correspondentes(indice):
                            for ind, lista_sbs in spin_boxs1:
                                if ind == indice:
                                    lista_valores = ''
                                    for sb in lista_sbs:
                                        lista_valores = lista_valores + str(sb.get())
                                    return lista_valores

                        h = 0
                        quer_personalizado = True
                        for variavel in variaveis1:
                            if variavel.get() == 1:
                                # quer dizer que esta selecionada
                                infos[serv(tipos_serv[h], True)] = obtendo_spins_correspondentes(h)
                                quer_personalizado = False

                            h += 1

                        if quer_personalizado:
                            # Quer dizer que não houve nada adicionado e devemos perguntar ao usuário qual o padrão que
                            # ele deseja

                            decisao = messagebox.askyesnocancel(
                                message='Você deseja então a configuração de S1 completa(SIM) ou a de S2(NÃO)?')
                            if decisao is None:
                                return 0
                            else:
                                if decisao:
                                    decisao = 0
                                else:
                                    decisao = 1

                            """['PtSegMasc', '3° Piso', 'PtSegFem', 'Sentinela',
                             'Cabo', 'Cabo da Guarda', 'Cdt da Guarda',
                             'Sgt',
                             'Aux Of']"""
                            # Vamos criar as duas strings que simbolizaram as duas opções
                            s1 = [
                                '6666666',
                                '3333333',
                                '3111311',
                                '0000006',
                                '1111111',
                                '0000001',
                                '0000001',
                                '1111111',
                                '1111111'
                            ]
                            s2 = [
                                '6666666',
                                '0000000',
                                '1111111',
                                '0000006',
                                '1111111',
                                '0000001',
                                '0000001',
                                '1111111',
                                '1111111'
                            ]
                            possiveis = [s1, s2]

                            c = 0
                            for quantidades1 in possiveis[decisao]:
                                # Para estar criptografado e seja mais simples nos ‘loops’
                                infos[serv(tipos_serv[c], True)] = quantidades1

                                c += 1

                    quantidades()

                    # Vamos salvar o dia final da simulação
                    data = dt_f.get()
                    if '/' in data:
                        data = data.split('/')

                        try:

                            infos['final'] = data[0] + codigo_mes(data[1], True)

                        except:
                            return messagebox.showwarning(message='Data Invalida')

                    else:
                        return messagebox.showwarning(message='Data Inválida')

                    # Falta a configuração desejada de serviços
                    infos['conf'] = cb1.get()
                    if infos['conf'] == 'Emergencias':
                        return messagebox.showwarning(message='Essa configuração não é aceita nesse módulo.')

                    if messagebox.askokcancel(message='Confirme as informações.'):
                        tela.destroy()
                        executando_simulacao(infos)
                    else:
                        infos.clear()

                Button(tela, text='Salvar Configurações', command=salvando).place(x=150, y=410)

                tela.mainloop()

            recebendo_info()

        Button(janela, text='Criando Simulações', command=Criando_Simulacoes, borderwidth=5).place(x=10, y=120 + b,
                                                                                                   width=280,
                                                                                                   height=100)

        def Trocas():

            janela.destroy()

            # Aqui vamos selecionar eventos de trocas em escalas
            # Como será algo simples, vou criar as funções aqui mesmo
            # Basicamente devemos criar uma janela e mostrar as escalas que podem ser alteradas em um combobx
            jan = criando_janela('Trocador', 300, 400)

            def criacaotv(escala):
                tv = ttk.Treeview(jan, columns=['Tipo', 'Nome de Guerra'],
                                  show='headings', selectmode=EXTENDED)

                # Colocando as colunas do treeview
                tv.column('Tipo', minwidth=0, width=60, anchor='center')
                tv.heading('Tipo', text='Tipo')

                tv.column('Nome de Guerra', minwidth=0, width=90, anchor='center')
                tv.heading('Nome de Guerra', text='Nome de Guerra')

                tv.place(x=10, y=60, height=270, width=280)

                for tipo, nome in escala:
                    tv.insert('', 'end', values=[tipo, nome])

                return tv

            def efetivar(escala, arq, de_saida, de_entrada):
                def procurando_existencia():
                    # Se não vamos gravar, é bom que pelo menos avisemos em quais escalas os sanhudos estão
                    p = False
                    for esc2 in os.listdir('../SargenteanteAlpha/Escalas'):
                        if esc2 != arq:
                            with open(f'Escalas/{esc2}') as esc1:
                                for linha in esc1:
                                    if de_entrada in linha:
                                        p = True
                                        messagebox.showinfo(title='Oportunidade',
                                                            message=f'{pegando_info(de_entrada, [0, 2])}(ENTRANDO) foi encontrado em {esc2.replace("escala", "")}')

                    if p:
                        messagebox.showinfo(
                            message='Pode ser uma chance para o Senhor(a) substituir e evitar sanhas futuros')

                # o que devemos fazer é
                decisao = messagebox.askyesnocancel(
                    message='Deseja gravar as informações para que o software o lembre dps?')

                if decisao is True:
                    # Devemos anotar essa entrada e saida para lembrar o usuário deste Sanha
                    # Vamos guardar quem sai da escala, quem entrou e em que dia essa troca ocorreu
                    with open('../SargenteanteAlpha/SubArquivos/Trocas', 'a') as tr:
                        tr.write(f'{de_saida}-{de_entrada}-{arq.replace("escala", "")}\n')
                        # isso mesmo, foda-se o \n
                elif decisao is False:
                    pass

                if decisao is None:
                    # Não salvamos e nem vamos efetivar
                    pass
                else:

                    # apagar o existe
                    os.remove(f'Escalas/{arq}')

                    # criá-lo com a diferença
                    c = True
                    with open(f'Escalas/{arq}', 'x') as esc:
                        for tipo, nome in escala:
                            if c:
                                esc.write(f'{pegando_info(nome, [2, 0])}-{serv(tipo, True)}')
                                c = False
                            else:
                                esc.write(f'\n{pegando_info(nome, [2, 0])}-{serv(tipo, True)}')

                    # É bizu informar também ao usuário quando o guerreiro que sai, o privilegiado, pode entrar

                    procurando_existencia()

            # Vamos ver o sanha
            cb_lista = os.listdir('../SargenteanteAlpha/Escalas')
            cb = ttk.Combobox(jan, values=cb_lista)
            cb['state'] = 'readonly'
            try:
                cb.set(cb_lista[0])
            except IndexError:
                return messagebox.showerror(message='Não há escalas prontas')
            cb.place(x=80, y=10, width=100, height=27)

            def Abrir():
                # Aqui vamos exibir um treeview da escala

                escala = []

                arquivo = cb.get()
                with open(f'Escalas/{arquivo}') as esc:
                    for linha in esc:
                        if '\n' in linha:
                            linha = linha.replace('\n', '')

                        linha = linha.split("-")
                        linha[0] = pegando_info(linha[0], [0, 2])
                        linha[1] = serv(linha[1])

                        # Vamos ordenar ela de forma diferente também
                        escala.append(linha[::-1])

                tv = criacaotv(escala)

                # O botão so deve existir dps que termos uma escala, lembra?

                def trocar():
                    pessoa1 = tv.selection()
                    # noinspection PyTypeChecker
                    sair = tv.item(pessoa1)['values']

                    # [tipo, nome]

                    # Entretanto, so poderemos deletar essa pessoa conseguirmos-se outra no lugar, como faremos isso?
                    # Vamos criar uma janela perguntar trocar com quem, compreende?

                    def pegando_trocado():
                        jan1 = criando_janela('Quem trocado:', 300, 100)

                        Label(jan1, text='Informe o numero do que irá substituir(entrar):', bg='#dde').place(x=10, y=10)

                        antisafo = Entry(jan1)
                        antisafo.place(x=10, y=30, width=150)

                        def tentar():
                            guerreiro = antisafo.get()

                            # Devemos confirmar se ele existe de fato
                            # Como? Verificando o sanha do ime completo? NÃO
                            # Devemos verificar qual é o ano da pessoa que esta saindo ai modificar o sanha
                            nome_guerreiro = pegando_info(guerreiro, [0, 2])

                            if nome_guerreiro not in [None, False]:
                                # confirmamos que existe, devemos fazer algo

                                # vamos alterar o valor da escala
                                c = 0
                                for tipo, nome in escala:
                                    if nome == sair[1]:
                                        escala[c][1] = nome_guerreiro

                                    c += 1

                                # vamos mudar o treeview tbm
                                # noinspection PyTypeChecker
                                tv.delete(pessoa1)
                                tv.insert('', 'end', values=[sair[0], nome_guerreiro])

                                jan1.destroy()

                                # Agora, vamos dispor um novo botão para efetivar a troca
                                Button(jan, text='Efetivar',
                                       command=lambda: efetivar(escala, arquivo, pegando_info(sair[1], [2, 0]),
                                                                guerreiro)).place(x=40, y=350)

                            else:
                                return messagebox.showerror(message='Esse militar não esta registrado')

                        Button(jan1, text='Trocar', command=tentar).place(x=10, y=60)

                        jan1.mainloop()

                    pegando_trocado()

                    # Note que o privilegiado é o que esta saindo

                Button(jan, text='Trocar', command=trocar).place(x=130, y=350)

            Button(jan, text='Selecionar', command=Abrir).place(x=200, y=10)

            jan.mainloop()

        Button(janela, text='Trocas', command=Trocas, borderwidth=5).place(x=10, y=240 + b,
                                                                           width=280,
                                                                           height=100)

        def executando_sanha():
            janela.mainloop()

        executando_sanha()

    FrontEnd()


if __name__ == '__main__':
    escalador()
