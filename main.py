from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/recommendations")
def get_recommendations():
    data = {
        'Supplier': ['Supplier A', 'Supplier B', 'Supplier C', 'Supplier D', 'Supplier E'],
        'Direct Risk Score': [75, 60, 50, 90, 40],
        'Tier-N Risk Exposure': [80, 50, 45, 85, 35],
        'Self-Assessment Score': [40, 75, 80, 30, 90],
        'Geopolitical Stability': [50, 70, 85, 40, 95],
    }
    df = pd.DataFrame(data)

    scaler = MinMaxScaler()
    df[['Direct Risk Score', 'Tier-N Risk Exposure']] = scaler.fit_transform(df[['Direct Risk Score', 'Tier-N Risk Exposure']])
    df[['Self-Assessment Score', 'Geopolitical Stability']] = scaler.fit_transform(df[['Self-Assessment Score', 'Geopolitical Stability']])

    df['Recommendation Score'] = (df['Direct Risk Score'] * 0.4 +
                                  df['Tier-N Risk Exposure'] * 0.3 +
                                  (1 - df['Self-Assessment Score']) * 0.2 +
                                  (1 - df['Geopolitical Stability']) * 0.1)

    df_sorted = df.sort_values(by='Recommendation Score', ascending=True)
    return df_sorted[['Supplier', 'Recommendation Score']].to_dict(orient='records')
