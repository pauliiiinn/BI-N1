import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 Indicadores do Ensino Médio (2013 - 2022)")
st.write("Dados de Aparecida de Goiânia, Goiânia e Senador Canedo")

anos = list(range(2013, 2023))
dados = {
    "Aparecida de Goiânia": {
        "Reprovação (%)": [8.5, 10.8, 9.5, 9.4, 7.9, 7.8, 7.7, 1, 1.2, 4.2],
        "Abandono (%)": [10, 8.3, 9.2, 8.4, 5.9, 5, 6.1, 5.1, 4.2, 4.6],
        "Matrículas": [20768, 20715, 21207, 20511, 18259, 18904, 19564, 21788, 21185, 20757]
    },
    "Goiânia": {
        "Reprovação (%)": [8.6, 9.7, 7.1, 7.5, 3.7, 5.3, 4.7, 2.5, 2.4, 2.2],
        "Abandono (%)": [5.3, 4.2, 4.3, 4.3, 0.9, 1.3, 0.9, 0.9, 0.5, 0.8],
        "Matrículas": [61390, 59779, 58708, 55401, 50038, 49807, 49696, 49630, 50373, 48796]
    },
    "Senador Canedo": {
        "Reprovação (%)": [14.5, 14.8, 11.4, 14.6, 7.0, 8, 2.6, 1.2, 4.6, 4.2],
        "Abandono (%)": [11.8, 11.5, 14.6, 8.2, 4.7, 5.4, 3.9, 5.9, 2.1, 4.9],
        "Matrículas": [3579, 3927, 4143, 4019, 3654, 3957, 4110, 4506, 4586, 4593]
    }
}

cores_cidades = {
    "Goiânia": "green",
    "Aparecida de Goiânia": "gold",
    "Senador Canedo": "red"
}

st.sidebar.header("🔍 Filtros")
cidades = st.sidebar.multiselect("Selecione as cidades:", list(dados.keys()), default=list(dados.keys()))
anos_selecionados = st.sidebar.multiselect("Selecione os anos:", anos, default=anos)

linhas = []
for cidade in cidades:
    for i, ano in enumerate(anos):
        if ano in anos_selecionados:
            matriculas = dados[cidade]["Matrículas"][i]
            taxa_rep = dados[cidade]["Reprovação (%)"][i]
            taxa_aban = dados[cidade]["Abandono (%)"][i]
            reprovados = round(matriculas * taxa_rep / 100)
            abandonos = round(matriculas * taxa_aban / 100)

            linhas.append({
                "Cidade": cidade,
                "Ano": ano,
                "Matrículas": matriculas,
                "Reprovação (%)": taxa_rep,
                "Abandono (%)": taxa_aban,
                "Reprovados (alunos)": reprovados,
                "Abandonos (alunos)": abandonos
            })

df = pd.DataFrame(linhas)

st.subheader("📋 Dados Selecionados")
st.dataframe(df, use_container_width=True)

st.subheader("📈 Matrículas por Cidade")
fig1 = px.line(df, x="Ano", y="Matrículas", color="Cidade", markers=True,
               color_discrete_map=cores_cidades)
st.plotly_chart(fig1, use_container_width=True)

st.subheader("📉 Reprovados e Abandonos (alunos)")
df_meltado = df.melt(id_vars=["Cidade", "Ano"], value_vars=["Reprovados (alunos)", "Abandonos (alunos)"],
                     var_name="Indicador", value_name="Quantidade")
fig2 = px.line(df_meltado, x="Ano", y="Quantidade", color="Cidade", line_dash="Indicador", markers=True,
               color_discrete_map=cores_cidades,
               labels={"Quantidade": "Número de Alunos"})
st.plotly_chart(fig2, use_container_width=True)
