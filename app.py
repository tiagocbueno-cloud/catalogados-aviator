import streamlit as st
import random
import pandas as pd

st.set_page_config(page_title="Simulador Estatístico Aviator", page_icon="✈️", layout="centered")

st.title("✈️ Simulador Estatístico & Gestão Aviator")
st.write("Testador matemático de estratégias baseado no algoritmo real de Crash.")

# Inicializar estados de sessão para manter o histórico e o saldo da banca
if 'historico' not in st.session_state:
    st.session_state.historico = []
if 'banca' not in st.session_state:
    st.session_state.banca = 100.00

# Barra lateral de configurações
st.sidebar.header("⚙️ Configurações da Banca")
banca_inicial = st.sidebar.number_input("Banca Inicial (R$)", min_value=1.0, value=100.0, step=10.0)
if st.sidebar.button("Resetar Banca"):
    st.session_state.banca = banca_inicial
    st.session_state.historico = []

st.sidebar.markdown("---")
st.sidebar.header("🎰 Configurações de Aposta")
valor_aposta = st.sidebar.number_input("Valor da Aposta (R$)", min_value=1.0, value=2.0, step=1.0)
meta_cashout = st.sidebar.number_input("Meta de Auto-Cashout (x)", min_value=1.01, value=1.50, step=0.1)

# Função geradora baseada em regras matemáticas reais (Provably Fair)
def rodar_algoritmo():
    if random.random() < 0.10: # Taxa de perda instantânea (1.00x)
        return 1.00
    semente = random.random()
    multiplicador = 0.99 / (1.0 - semente)
    return max(1.00, round(multiplicador, 2))

# Botão principal de ação
if st.button("🚀 Simular Próxima Rodada", use_container_width=True):
    if st.session_state.banca < valor_aposta:
        st.error("❌ Banca insuficiente para realizar esta aposta!")
    else:
        resultado = rodar_algoritmo()
        st.session_state.historico.append(resultado)
        st.session_state.banca -= valor_aposta
        
        if resultado >= meta_cashout:
            lucro = valor_aposta * meta_cashout
            st.session_state.banca += lucro
            st.success(f"✅ VITÓRIA! O avião voou até {resultado:.2f}x. Você retirou em {meta_cashout:.2f}x e ganhou R${lucro:.2f}!")
        else:
            st.error(f"❌ DERROTA! O avião deu crash em {resultado:.2f}x antes da sua meta de {meta_cashout:.2f}x. Você perdeu R${valor_aposta:.2f}!")

# Mostrar Painel de Resultados
st.markdown("### 📊 Status da sua Banca")
st.metric(label="Saldo Atual", value=f"R$ {st.session_state.banca:.2f}")

if st.session_state.historico:
    # Exibir últimas rodadas com as cores padrões do jogo
    st.markdown("### 🕒 Histórico Recente de Velas")
    
    html_historico = ""
    for v in reversed(st.session_state.historico[-10:]):
        if v < 2.0:
            cor, txt_cor = "#2b6cb0", "white" # Azul
        elif v < 10.0:
            cor, txt_cor = "#6b46c1", "white" # Roxo
        else:
            cor, txt_cor = "#b83280", "white" # Rosa
        html_historico += f'<span style="background-color:{cor}; color:{txt_cor}; padding:5px 10px; margin:2px; border-radius:5px; font-weight:bold; display:inline-block;">{v:.2f}x</span>'
    
    st.markdown(html_historico, unsafe_allow_html=True)

    # Análise Estatística Percentual
    total = len(st.session_state.historico)
    azuis = sum(1 for x in st.session_state.historico if x < 2.0)
    roxas = sum(1 for x in st.session_state.historico if 2.0 <= x < 10.0)
    rosas = sum(1 for x in st.session_state.historico if x >= 10.0)

    st.markdown("### 📉 Distribuição de Tendências")
    col1, col2, col3 = st.columns(3)
    col1.metric("Velas Azuis (<2x)", f"{(azuis/total)*100:.1f}%")
    col2.metric("Velas Roxas (2x-10x)", f"{(roxas/total)*100:.1f}%")
    col3.metric("Velas Rosas (>=10x)", f"{(rosas/total)*100:.1f}%")