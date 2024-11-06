import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import copy
import itertools
from io import BytesIO
from PIL import Image
import folium
from streamlit_folium import st_folium

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

def calCusto(solucao, Mcusto):
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
    
# Implementação da Busca Tabu com parâmetros personalizáveis
def buscaTabu(alpha, Mcusto, iteracoes=50, tabu_tenure=5):
    MelhorResultado = (float('inf'), [])
    listaCustos = []
    listaRotas = []
    # Solução inicial aleatória
    n = len(Mcusto)
    s = list(range(1, n))
    random.shuffle(s)
    s = [0] + s + [0]
    custo_s = calCusto(s, Mcusto)
    MelhorResultado = (custo_s, s)
    custo_inicial = custo_s
    listaCustos.append(custo_s)
    listaRotas.append(s)
    listaTabu = []

    melhor_custo = custo_s
    melhor_solucao = s

    for k in range(iteracoes):
        vizinhos = []
        for i in range(1, n - 1):
            for j in range(i + 1, n):
                vizinho = s[:]
                vizinho[i], vizinho[j] = vizinho[j], vizinho[i]
                movimento = (s[i], s[j])
                if movimento not in listaTabu:
                    custo_vizinho = calCusto(vizinho, Mcusto)
                    vizinhos.append((custo_vizinho, vizinho, movimento))
        if not vizinhos:
            break
        vizinhos.sort()
        custo_s, s, movimento = vizinhos[0]
        listaTabu.append(movimento)
        if len(listaTabu) > tabu_tenure:
            listaTabu.pop(0)
        listaCustos.append(custo_s)
        listaRotas.append(s)
        if custo_s < MelhorResultado[0]:
            MelhorResultado = (custo_s, s)
            melhor_custo = custo_s
            melhor_solucao = s

    return MelhorResultado, listaRotas, listaCustos, custo_inicial




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
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
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
    /* Métricas */
    .metric-container {
        display: flex;
        justify-content: space-around;
        margin-bottom: 20px;
    }
    .metric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        width: 30%;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .metric h3 {
        margin: 5px 0;
    }
    .metric p {
        margin: 0;
        font-size: 24px;
        font-weight: bold;
    }
    .metric.initial-cost h3 {
        color: #ff4d4d;  /* Vermelho claro */
    }
    .metric.optimized-cost h3 {
        color: #66cc66;  /* Verde claro */
    }
    .metric.gain h3 {
        color: #4da6ff;  /* Azul claro */
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
if 'optimization_done' not in st.session_state:
    st.session_state['optimization_done'] = False
if 'results' not in st.session_state:
    st.session_state['results'] = {}

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

# Parâmetros personalizáveis
st.header("⚙️ Parâmetros do Algoritmo")
col_param1, col_param2 = st.columns(2)
with col_param1:
    iteracoes = st.number_input("Número de Iterações", min_value=10, max_value=1000, value=50, step=10)
with col_param2:
    tabu_tenure = st.number_input("Tamanho da Lista Tabu", min_value=1, max_value=100, value=5, step=1)

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
        st.session_state['optimization_done'] = False  # Resetar o estado de otimização
        st.success("✅ Dados inseridos com sucesso! Pronto para otimizar a rota.")
    else:
        st.session_state['can_optimize'] = False
        st.session_state['optimization_done'] = False
        st.error("Corrija os erros acima para continuar.")

# Botão para otimizar a rota
if st.session_state['can_optimize']:
    if st.button("🛣️ Otimizar Rota"):
        with st.spinner('Otimizando a rota, por favor aguarde...'):
            pontos = st.session_state['pontos']
            # Gerar a matriz de custos
            Mcusto = matrizDistancias(pontos)

            # Executar a otimização com Busca Tabu usando os parâmetros personalizados
            MelhorResultado, listaRotas, listaCustos, custo_inicial = buscaTabu(0.3, Mcusto, iteracoes=int(iteracoes), tabu_tenure=int(tabu_tenure))
            custo_total = MelhorResultado[0]
            ganho_otimizacao = custo_inicial - custo_total
            percentual_ganho = (ganho_otimizacao / custo_inicial) * 100

            # Salvar os resultados no session_state
            st.session_state['results'] = {
                'MelhorResultado': MelhorResultado,
                'listaRotas': listaRotas,
                'listaCustos': listaCustos,
                'custo_inicial': custo_inicial,
                'custo_total': custo_total,
                'ganho_otimizacao': ganho_otimizacao,
                'percentual_ganho': percentual_ganho,
                'iteracoes': iteracoes,
                'tabu_tenure': tabu_tenure,
                'pontos': pontos
            }
            st.session_state['optimization_done'] = True  # Indicar que a otimização foi concluída

            st.success('✅ Rota otimizada com sucesso!')

# Exibir os resultados se a otimização foi concluída
if st.session_state.get('optimization_done', False):
    resultados = st.session_state['results']
    MelhorResultado = resultados['MelhorResultado']
    listaRotas = resultados['listaRotas']
    listaCustos = resultados['listaCustos']
    custo_inicial = resultados['custo_inicial']
    custo_total = resultados['custo_total']
    ganho_otimizacao = resultados['ganho_otimizacao']
    percentual_ganho = resultados['percentual_ganho']
    pontos = resultados['pontos']

    # Dashboard - Mostrar as métricas
    st.header("📈 Dashboard de Resultados")

    # Métricas estilizadas com HTML e CSS
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric initial-cost">
            <h3>Custo Inicial</h3>
            <p>{custo_inicial:.2f}</p>
        </div>
        <div class="metric optimized-cost">
            <h3>Custo Otimizado</h3>
            <p>{custo_total:.2f}</p>
        </div>
        <div class="metric gain">
            <h3>Ganho de Otimização</h3>
            <p>{percentual_ganho:.2f}%</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Organizar as plotagens em colunas
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🛣️ Rota Otimizada")
        # Criar o mapa interativo com Folium
        m = folium.Map(location=[pontos[0][0], pontos[0][1]], zoom_start=12)
        # Adicionar marcadores para os pontos
        folium.Marker(location=[pontos[0][0], pontos[0][1]], popup='Origem', icon=folium.Icon(color='green')).add_to(m)
        for idx, ponto in enumerate(pontos[1:], start=1):
            folium.Marker(location=[ponto[0], ponto[1]], popup=f'Ponto {idx}', icon=folium.Icon(color='red')).add_to(m)
        # Adicionar a rota otimizada
        solucao_coords = [[pontos[i][0], pontos[i][1]] for i in MelhorResultado[1]]
        folium.PolyLine(solucao_coords, color='blue', weight=2.5, opacity=1).add_to(m)
        st_data = st_folium(m, width=700, height=500)

    with col2:
        st.subheader("📊 Gráfico de Convergência")
        # Filtrar apenas as iterações com melhoria
        custos_melhoria = []
        iteracoes_melhoria = []
        melhor_custo = custo_inicial
        for idx, custo in enumerate(listaCustos):
            if custo < melhor_custo:
                custos_melhoria.append(custo)
                iteracoes_melhoria.append(idx)
                melhor_custo = custo
        # Gráfico de linha mostrando o custo em cada iteração de melhoria
        fig2, ax2 = plt.subplots()
        ax2.plot(iteracoes_melhoria, custos_melhoria, marker='o', linestyle='-')
        ax2.set_xlabel('Iteração')
        ax2.set_ylabel('Custo')
        ax2.set_title('Custo por Iteração de Melhoria')
        st.pyplot(fig2)

    # Animação do processo de otimização
    st.subheader("🎥 Animação do Processo de Otimização")
    Rotas = listaRotas
    custos = listaCustos
    fig_anim, ax_anim = plt.subplots()
    data = np.array(pontos)

    # Filtrar apenas as iterações com melhoria
    Rotas_melhoria = []
    custos_melhoria_anim = []
    melhor_custo = custo_inicial
    for idx, (rota, custo) in enumerate(zip(Rotas, custos)):
        if custo <= melhor_custo:
            Rotas_melhoria.append(rota)
            custos_melhoria_anim.append(custo)
            melhor_custo = custo

    def animate(i):
        ax_anim.clear()
        rota = Rotas_melhoria[i]
        custo_iteracao = custos_melhoria_anim[i]
        sol = [pontos[j] for j in rota]
        sol_array = np.array(sol)
        ax_anim.plot(sol_array[:, 1], sol_array[:, 0], marker='o', c='b')
        ax_anim.scatter(data[1:, 1], data[1:, 0], c="red")
        ax_anim.scatter(data[0, 1], data[0, 0], c="green", marker="D", s=100)
        ax_anim.set_xlabel('Longitude')
        ax_anim.set_ylabel('Latitude')
        ax_anim.set_title(f'Iteração {i+1} - Custo: {custo_iteracao:.2f}')

    ani = animation.FuncAnimation(fig_anim, animate, frames=len(Rotas_melhoria), interval=150, repeat=False)

    # Salvar a animação como GIF
    ani.save('otimizacao.gif', writer='pillow')

    # Exibir o GIF
    gif = open('otimizacao.gif', 'rb').read()
    st.image(gif)
