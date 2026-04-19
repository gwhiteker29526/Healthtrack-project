from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
from sqlalchemy.orm import Session
from database import SessionLocal
import crud

app = Dash(__name__)

def get_data():
    db: Session = SessionLocal()
    patients = crud.get_all_patients(db)
    alerts = crud.get_all_alerts(db)

    data = {
        "Patients": len(patients),
        "Alerts": len(alerts)
    }

    df = pd.DataFrame(list(data.items()), columns=["Category", "Count"])
    return df

df = get_data()

fig = px.bar(df, x="Category", y="Count", title="System Overview")

app.layout = html.Div([
    html.H1("HealthTrack Dashboard"),

    dcc.Graph(figure=fig),

    html.Div([
        html.H3("Summary"),
        html.P(f"Total Patients: {df[df['Category']=='Patients']['Count'].values[0]}"),
        html.P(f"Total Alerts: {df[df['Category']=='Alerts']['Count'].values[0]}")
    ])
])

if __name__ == "__main__":
    app.run(debug=True)