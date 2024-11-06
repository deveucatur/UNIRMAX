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

# Funções auxiliares e de otimização

def euclideanDistances(x1, y1, x2, y2):
    # Distância euclidiana multiplicada por 120 (ajuste de escala)
    return (((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5) * 120

def matrizDistancias(coord):
    X = []
    Y = []
    for i in coord:
        X.append(i[1])  # Longitude
        Y.append(i[0])  # Latitude
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

def dois_opt(rota, Mcusto):
    melhorou = True
    melhor_rota = rota[:]
    melhor_custo = calCusto(melhor_rota, Mcusto)
    while melhorou:
        melhorou = False
        for i in range(1, len(rota) - 2):
            for j in range(i + 1, len(rota) - 1):
                if j - i == 1: continue  # Não faz sentido trocar segmentos adjacentes
                nova_rota = melhor_rota[:]
                # Inverter o segmento entre i e j
                nova_rota[i:j] = melhor_rota[j - 1:i - 1:-1]
                novo_custo = calCusto(nova_rota, Mcusto)
                if novo_custo < melhor_custo:
                    melhor_rota = nova_rota
                    melhor_custo = novo_custo
                    melhorou = True
        rota = melhor_rota
    return melhor_rota

def buscaTabu(alpha, Mcusto, iteracoes=50, tabu_tenure=5, num_vizinhos=100):
    MelhorResultado = (float('inf'), [])
    listaCustos = []
    listaRotas = []
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
        movimentos_possiveis = []
        for i in range(1, n - 1):
            for j in range(i + 1, n):
                movimentos_possiveis.append((i, j))
        # Amostrar movimentos aleatórios
        movimentos_selecionados = random.sample(movimentos_possiveis, min(num_vizinhos, len(movimentos_possiveis)))
        for i, j in movimentos_selecionados:
            vizinho = s[:]
            vizinho[i], vizinho[j] = vizinho[j], vizinho[i]
            movimento = (s[i], s[j])
            if movimento not in listaTabu:
                custo_vizinho = calCusto(vizinho, Mcusto)
                if custo_vizinho < melhor_custo:
                    # Aplicar 2-opt somente se o custo for menor
                    vizinho_otimizado = dois_opt(vizinho, Mcusto)
                    custo_vizinho = calCusto(vizinho_otimizado, Mcusto)
                    vizinhos.append((custo_vizinho, vizinho_otimizado, movimento))
                else:
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
col_param1, col_param2, col_param3 = st.columns(3)
with col_param1:
    iteracoes = st.number_input("Número de Iterações", min_value=10, max_value=1000, value=100, step=10)
with col_param2:
    tabu_tenure = st.number_input("Tamanho da Lista Tabu", min_value=1, max_value=100, value=5, step=1)
with col_param3:
    num_vizinhos = st.number_input("Número de Vizinhos", min_value=10, max_value=1000, value=100, step=10)

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
            MelhorResultado, listaRotas, listaCustos, custo_inicial = buscaTabu(
                0.3, Mcusto, iteracoes=int(iteracoes), tabu_tenure=int(tabu_tenure), num_vizinhos=int(num_vizinhos)
            )
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
                'num_vizinhos': num_vizinhos,
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

    # Criar a animação apenas se houver melhorias
    if Rotas_melhoria:
        fig_anim, ax_anim = plt.subplots()

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

        ani = animation.FuncAnimation(fig_anim, animate, frames=len(Rotas_melhoria), interval=1000, repeat=False)

        # Salvar a animação como GIF
        ani.save('otimizacao.gif', writer='pillow')

        # Exibir o GIF
        gif = open('otimizacao.gif', 'rb').read()
        st.image(gif)
    else:
        st.write("Nenhuma melhoria encontrada para criar a animação.")

