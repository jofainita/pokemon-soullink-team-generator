# Enlace a google sheets = https://docs.google.com/spreadsheets/d/1to92JrHeyPc5GlwUN0SYykqV50tvg8P4UsorwD5rlmY/edit?usp=share_link

import pandas as pd
sheet_id = '1to92JrHeyPc5GlwUN0SYykqV50tvg8P4UsorwD5rlmY'
sheet_name = 'Bocatacas'
url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'

df = pd.read_csv(url)

df['Disponible'] = True

for a in range(len(df['Tipo_'])):
    for b in range(len(df['Tipo'])):
        if df['Tipo_'][a] == df['Tipo'][b] and df['Estado'][b] == 'Equipo':
            df['Disponible'][a] = False

for a in range(len(df['Tipo'])):
    for b in range(len(df['Tipo_'])):
        if df['Tipo'][a] == df['Tipo_'][b] and df['Estado'][b] == 'Equipo':
            df['Disponible'][a] = False

for a in range(len(df['Tipo_'])):
    if df['Estado'][a] == 'Con Arceus' or df['Estado'][a] == 'Huido':
        df['Disponible'][a] = False

for a in range(len(df['Disponible'])):
    print(df['Disponible'][a])

