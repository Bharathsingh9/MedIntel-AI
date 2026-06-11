import plotly.graph_objects as go
import os

class DashboardGenerator:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
    def generate_health_gauge(self, score, filename="health_gauge.html"):
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Overall Health Score"},
            gauge = {
                'axis': {'range': [None, 100]},
                'steps': [
                    {'range': [0, 30], 'color': "red"},
                    {'range': [30, 60], 'color': "orange"},
                    {'range': [60, 80], 'color': "yellow"},
                    {'range': [80, 100], 'color': "green"}],
                'bar': {'color': "black"}
            }))
        fig.write_html(os.path.join(self.output_dir, filename))
        
    def generate_risk_radar(self, scores_dict, filename="risk_radar.html"):
        categories = list(scores_dict.keys())
        values = list(scores_dict.values())
        
        # Close the loop for the radar chart
        categories.append(categories[0])
        values.append(values[0])
        
        fig = go.Figure(data=go.Scatterpolar(
          r=values,
          theta=categories,
          fill='toself'
        ))
        fig.update_layout(
          polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
          showlegend=False,
          title="Health Profile Radar"
        )
        fig.write_html(os.path.join(self.output_dir, filename))
