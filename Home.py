import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import copy
import itertools
from io import BytesIO
from PIL import Image

# Funções auxiliares de otimização
def euclideanDistances(x1, y1, x2, y2):
    return (((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5) * 120

def matrizDistancias(coord):
    X = []
    Y = []
    for i in coord:
        X.append(i[0])
        Y.append(i[1])
    distMatrix = np.zeros((len(X), len(Y)))
    for i in range(len(X)):
        for j in range(len(Y)):
            distMatrix[i][j] = float(euclideanDistances(X[i], Y[i], X[j], Y[j]))
    custo = distMatrix
    return custo

def calCusto(solucao):
    dist = 0
    for i in range(len(solucao) - 1):
        dist += float(Mcusto[solucao[i]][solucao[i + 1]])
    distTotal = dist
    return distTotal

# Defina aqui as funções metodoOrOpt1, metodoSwapp, metodo2opt, listaDeVizinhança, graspContrutiva, buscaTabu, etc.

#Or-Opt1 — Um cliente é removido da rota e inserido em outra posição.
#
def metodoOrOpt1(solução):
    candidatosOrOpt1 = list(itertools.combinations(range(1, len(solução) - 1), 2))
    #print('candidatosOrOpt1',candidatosOrOpt1)
    vizinhosOrOpt1 = []
    for i in range(0, len(candidatosOrOpt1)):
        novoVizinho = copy.deepcopy(solução)
        #print("i:",candidatosOrOpt1[i], novoVizinho[candidatosOrOpt1[i][0]])
        novoVizinho.insert(candidatosOrOpt1[i][1]+1,novoVizinho[candidatosOrOpt1[i][0]])
        del(novoVizinho[candidatosOrOpt1[i][0]])
        #print(novoVizinho)
        #if ValidaçãoRota(novoVizinho):
        vizinhosOrOpt1.append(novoVizinho)
           #print(novoVizinho)
    #print(len(vizinhosOrOpt1))
    return vizinhosOrOpt1


#Or-Opt2 — Dois clientes adjacentes são removidos da rota e inseridos em outra posição.
#

def metodoOrOpt2(solução):
    list1=range(1,len(solução)-2)
    list2=(range(1, len(solução)))
    candidatosOrOpt2 = list(itertools.product(list1,list2))
    #print(candidatosOrOpt2)
    vizinhosOrOpt2 = []
    for i in candidatosOrOpt2:
        if i[1] != i[0] and i[1] != i[0]+1 and i[1] != i[0]+2 :
            novoVizinho = copy.deepcopy(solução)
            #print("i:",i, novoVizinho[i[0]],novoVizinho[i[0]+1])
            aux= novoVizinho[i[0]+1]
            novoVizinho.insert(i[1],novoVizinho[i[0]])
            novoVizinho.insert(i[1]+1,aux)   
            if i[1] > i[0]:
                del(novoVizinho[i[0]])
                del(novoVizinho[i[0]])
            else:
                del(novoVizinho[i[0]+2])
                del(novoVizinho[i[0]+2])
            #print(novoVizinho)
            vizinhosOrOpt2.append(novoVizinho)
    #print(len(vizinhosOrOpt2))
    return vizinhosOrOpt2

#Or-Opt3 — Três clientes adjacentes são removidos da rota e inseridos em outra posição.
#
def metodoOrOpt3(solução):
    list1=range(1,len(solução)-3)
    list2=(range(1, len(solução)))
    candidatosOrOpt3 = list(itertools.product(list1,list2))
    #print(candidatosOrOpt3)
    vizinhosOrOpt3 = []
    for i in candidatosOrOpt3:
        if i[1] != i[0] and i[1] != i[0]+1 and i[1] != i[0]+2 and i[1] != i[0]+3:
            novoVizinho = copy.deepcopy(solução)
            #print("i:",i, novoVizinho[i[0]],novoVizinho[i[0]+1])
            aux1= novoVizinho[i[0]+1]
            aux2= novoVizinho[i[0]+2]
            novoVizinho.insert(i[1],novoVizinho[i[0]])
            novoVizinho.insert(i[1]+1,aux1)
            novoVizinho.insert(i[1]+2,aux2)
            if i[1] > i[0]:
                del(novoVizinho[i[0]])
                del(novoVizinho[i[0]])
                del(novoVizinho[i[0]])
            else:
                del(novoVizinho[i[0]+3])
                del(novoVizinho[i[0]+3])
                del(novoVizinho[i[0]+3])
            #print(novoVizinho)
            vizinhosOrOpt3.append(novoVizinho)
    #print(len(vizinhosOrOpt3))        
    return vizinhosOrOpt3

#Swap — Troca entre dois clientes não adjacentes.
#
def metodoSwapp(solução):
    candidatosSwapp = list(itertools.combinations(range(1, len(solução) - 1), 2))
    #print('candidatosSwapp',candidatosSwapp)
    vizinhosSwapp = []
    for i in range(0, len(candidatosSwapp)):
        novoVizinho = copy.deepcopy(solução)
        aux = novoVizinho[candidatosSwapp[i][0]]
        novoVizinho[candidatosSwapp[i][0]] = novoVizinho[candidatosSwapp[i][1]]
        novoVizinho[candidatosSwapp[i][1]] = aux
        #if ValidaçãoRota(novoVizinho):
        vizinhosSwapp.append(novoVizinho)
           #print(novoVizinho)
    #print(len(vizinhosSwapp))
    return vizinhosSwapp


#2-opt — Remove dois arcos de uma rota e insere dois novos arcos à mesma rota.
#
def metodo2opt(solução):
    candidatos2opt = list(itertools.combinations(range(1, len(solução) - 1), 2))
    vizinhos2opt=[]
    for k in candidatos2opt:
        if len(solução) > 3 :
            novaRota = copy.deepcopy(solução)
            i= k[0]
            j= k[1]
            if (i > j):
                i, j = j, i
            novaRota[i:j+1] = list(reversed(novaRota[i:j+1]))
            vizinhos2opt.append(novaRota)            
        else:
            vizinhos2opt=[]
    #print(len(vizinhos2opt))
    return vizinhos2opt

def plotarGrafi(R,p):
    sol = []
    for i in R:
        sol.append(p[i])
    data = np.array(p)
    data2= np.array(sol)
    plt.plot(data2[:, 0], data2[:, 1])
    plt.scatter(data[:, 0], data[:, 1], c="r")
    plt.show()   
    
def buscaTabu(alpha,Mcusto):
    
    MelhorResultado = (999999999999,[])
    for rod in range(0,1): 
        listaRotas = []
        ## SOLUÇÃO INICIAL ALEATÓRIA ##
        solução = graspContrutiva(alpha,Mcusto)
        s = solução
        listaRotas.append(s)
        print("s ",s)
        ## BUSCA TABU ##
        k = 0
        melhorIter = k
        BTmax = 4
        
        listaTabu = []
        listaViz = []
        listaVizOrd = listaDeVizinhança(s,listaViz)
        s = listaVizOrd[0]
        listaTabu.insert(0,listaVizOrd[0][1])
        mS = s
        while (k - melhorIter <= BTmax):
            print(k,"-",melhorIter,"<=",BTmax)
            k += 1
            listaVizOrd = listaDeVizinhança(s[1],listaViz)
            #print([x[0] for x in listaVizOrd][:5])
            for j in listaVizOrd:
                if j[1] not in listaTabu:
                    #print(j)
                    s = j
                    listaTabu.insert(0,j[1])
                    listaTabu = listaTabu[:5]
                    break
                else:
                    pass
            if s <= mS:
                listaRotas.append(s[1])
                mS = s
                melhorIter = k
            else:
                pass
        print(mS, melhorIter)
        if mS[0] <= MelhorResultado[0]:
            MelhorResultado = mS
    return MelhorResultado,listaRotas



def listaDeVizinhança(s,listaViz):
    #[metodoOrOpt1,metodoOrOpt2 ,metodoOrOpt3 ,metodoSwapp ,metodo2opt]
    operadores = [metodoOrOpt1,metodoSwapp ,metodo2opt]
    for i in operadores:
        viz = i(s)
        for j in viz:
            if j in listaViz:
                pass
            else:
                listaViz.append(j)
    l=[]
    for i in listaViz:
        g= (calCusto(i),i)
        l.append(g)
    listaVizOrd = sorted(l)
    return listaVizOrd


def graspContrutiva(alpha,Mcusto):
    solucao = []
    locais = range(1,len(Mcusto))
    n = len(locais)
    solucao.append(0)
    for i in range(n):
        CidadesN = [x for x in locais if x not in solucao]
        #print(CidadesN)
        conj_ord = []
        conj = []
        if len(CidadesN) == 0:
            break
        else:
            
            for i in CidadesN:
                Vec = [Mcusto[solucao[-1]][i],i]
                conj.append(Vec)
            conj_ord = sorted(conj)
            #print('conj_ord ',conj_ord)
            RCL = []
            custoMax = conj_ord[0][0]
            custoMin = conj_ord[-1][0] 
            for i in range(0 , len(conj_ord)):
                if(conj_ord[i][0] <= (custoMin + alpha * (custoMax-custoMin))):
                    RCL.append(conj_ord[i])
            #print('RCL ',RCL)
            elemento = random.choice(RCL)
            sol=[elemento[1]]  
            #print('sol ',sol[0])
            solucao.append(sol[0])
    solucao.append(0)
    return solucao

# Configurações da página
st.set_page_config(page_title="Sistema de Otimização de Rotas", page_icon="🚚", layout="wide")

st.title("🚚 Sistema de Otimização de Rotas")
st.write("Otimize rotas de entrega de forma eficiente e profissional.")

# CSS personalizado para melhorar o visual
st.markdown("""
    <style>
    /* Estilos gerais */
    body {
        background-color: #f0f2f6;
    }
    /* Títulos */
    h1, h2, h3, h4, h5, h6 {
        color: #2E4053;
        font-family: 'Arial', sans-serif;
    }
    /* Botões */
    .stButton button {
        background-color: #28a745;
        color: white;
        font-size: 18px;
        padding: 10px 20px;
        border-radius: 10px;
    }
    /* Inputs */
    .stTextInput>div>div>input {
        border: 1px solid #ced4da;
        border-radius: 5px;
    }
    /* Seções */
    .section {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Inicializar variáveis no session_state, se ainda não existirem
if 'pontos' not in st.session_state:
    st.session_state['pontos'] = None
if 'can_optimize' not in st.session_state:
    st.session_state['can_optimize'] = False
if 'NCoord' not in st.session_state:
    st.session_state['NCoord'] = 3

# Organizar a entrada de dados
st.header("📍 Inserir Dados")

# Entrada do ponto de origem
st.subheader("Ponto de Origem")
origem_input = st.text_input(
    "Coordenadas (formato: -11.431479662163595, -61.45796459717541)",
    value="",
    help="Copie e cole as coordenadas do Google Maps no formato indicado."
)

# Entrada do número de pontos de entrega
st.subheader("Pontos de Entrega")
NCoord = st.number_input("Número de Pontos de Entrega", min_value=1, value=int(st.session_state['NCoord']), step=1)
st.session_state['NCoord'] = NCoord

# Coleta das coordenadas dos pontos de entrega
st.write("Insira as coordenadas para cada ponto de entrega:")

Coordenadas_input = []
for i in range(int(NCoord)):
    coord_input = st.text_input(
        f"Ponto {i+1} (formato: lat, lon)",
        key=f"coord{i}",
        value="",
        help="Copie e cole as coordenadas do Google Maps no formato indicado."
    )
    Coordenadas_input.append(coord_input)

# Botão para confirmar os dados
if st.button('🚀 Confirmar Dados'):
    origem = None
    Coordenadas = []
    error_flag = False

    # Validar coordenadas do ponto de origem
    if origem_input.strip() != "":
        try:
            origem = [float(coord.strip()) for coord in origem_input.strip("() ").split(",")]
            if len(origem) != 2:
                raise ValueError
        except:
            st.error("Por favor, insira as coordenadas do ponto de origem no formato correto.")
            error_flag = True
    else:
        st.error("Por favor, insira as coordenadas do ponto de origem.")
        error_flag = True

    # Validar coordenadas dos pontos de entrega
    for idx, coord_input in enumerate(Coordenadas_input):
        if coord_input.strip() != "":
            try:
                coord = [float(coord.strip()) for coord in coord_input.strip("() ").split(",")]
                if len(coord) != 2:
                    raise ValueError
                Coordenadas.append(coord)
            except:
                st.error(f"Por favor, insira as coordenadas do ponto {idx+1} no formato correto.")
                error_flag = True
        else:
            st.error(f"Por favor, insira as coordenadas do ponto {idx+1}.")
            error_flag = True

    if not error_flag:
        st.session_state['pontos'] = [origem] + Coordenadas
        st.session_state['can_optimize'] = True
        st.success("✅ Dados inseridos com sucesso! Pronto para otimizar a rota.")
    else:
        st.session_state['can_optimize'] = False
        st.error("Corrija os erros acima para continuar.")

# Botão para otimizar a rota
if st.session_state['can_optimize']:
    if st.button("🛣️ Otimizar Rota"):
        with st.spinner('Otimizando a rota, por favor aguarde...'):
            pontos = st.session_state['pontos']
            # Definir o parâmetro alpha para o GRASP
            alpha = 0.3

            # Gerar a matriz de custos
            Mcusto = matrizDistancias(pontos)

            # Executar a otimização com Busca Tabu
            R = buscaTabu(alpha, Mcusto)

            # Plotar a rota otimizada
            fig, ax = plt.subplots()
            sol = [pontos[i] for i in R[0][1]]
            data = np.array(pontos)
            data2 = np.array(sol)
            ax.plot(data2[:, 0], data2[:, 1], marker='o', c='b', label='Rota')
            ax.scatter(data[1:, 0], data[1:, 1], c="red", label='Pontos de Entrega')
            ax.scatter(data[0, 0], data[0, 1], c="green", marker="D", s=100, label='Origem')
            ax.set_xlabel('Longitude')
            ax.set_ylabel('Latitude')
            ax.set_title('Rota Otimizada')
            ax.legend()
            st.pyplot(fig)

            # Criar animação do processo de otimização
            Rotas = R[1]
            fig_anim, ax_anim = plt.subplots()
            data = np.array(pontos)

            def animate(i):
                ax_anim.clear()
                rota = Rotas[i]
                sol = [pontos[j] for j in rota]
                sol_array = np.array(sol)
                ax_anim.plot(sol_array[:, 0], sol_array[:, 1], marker='o', c='b')
                ax_anim.scatter(data[1:, 0], data[1:, 1], c="red")
                ax_anim.scatter(data[0, 0], data[0, 1], c="green", marker="D", s=100)
                ax_anim.set_xlabel('Longitude')
                ax_anim.set_ylabel('Latitude')
                ax_anim.set_title('Iteração {}'.format(i+1))

            ani = animation.FuncAnimation(fig_anim, animate, frames=len(Rotas), interval=1000, repeat=False)

            # Salvar a animação como GIF
            ani.save('otimizacao.gif', writer='pillow')

            # Exibir o GIF
            st.header("Animação do Processo de Otimização")
            gif = open('otimizacao.gif', 'rb').read()
            st.image(gif)

            st.success('✅ Rota otimizada com sucesso!')