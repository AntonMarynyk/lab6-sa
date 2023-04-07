import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
from addEdge import addEdge, get_color

class MapBuild:
    def __init__(self):
        self.nodeColor = 'white'
        self.nodeSize = 50
        self.lineWidth = 3
        self.lineColor = 'white'


    def make_graph_fig(self, adj_matrix, feature_names):
        N = adj_matrix.shape[0]
        R = 1
        X = R * np.cos(2 * np.pi * np.arange(N) / N)
        Y = R * np.sin(2 * np.pi * np.arange(N) / N)
        
        # параметри побудови - для plottly
        edge_x = []
        edge_y = []
        weight_x = []
        weight_y  = []
        weight_values = []
        weight_text = []
        dash_styles = []
        seen_pairs = []
        
        # положення ребер 
        for edge in np.argwhere(adj_matrix != 0):
            start_node = X[edge[0]], Y[edge[0]]
            end_node = X[edge[1]], Y[edge[1]]
            if start_node != end_node:
                sorted_pair = tuple(np.sort([edge[0], edge[1]])) 
                if sorted_pair in seen_pairs:
                    dash_styles.append('dash')
                else:
                    dash_styles.append('solid')

                edge_x, edge_y = addEdge(
                    start_node, end_node, 
                    edge_x, edge_y, 
                    lengthFrac=1, arrowPos=0.8, 
                    arrowLength=0.04, arrowAngle=30, dotSize=self.nodeSize,
                )

                weight_x.append(0.8*start_node[0] + 0.2*end_node[0])
                weight_y.append(0.8*start_node[1] + 0.2*end_node[1])
                weight_values.append(adj_matrix[edge[0], edge[1]])
                weight_text.append(
                    f'Connection weight: {weight_values[-1]}'
                )
                seen_pairs.append(sorted_pair)
       

        edge_trace = [] 

        # грані (ребра фігури) - інформація при наведеннні
        for i in range(len(weight_values)):
            edge_trace.append(
                go.Scatter(
                    x=edge_x[9*i:9*(i+1)], y=edge_y[9*i:9*(i+1)],
                    line=dict(
                        width=self.lineWidth, 
                        color=get_color('tempo', 0.5*weight_values[i]+0.5),
                        dash=dash_styles[i]
                    ),
                    hoverinfo='none', mode='lines'
                )
            )

            node_trace = go.Scatter(
                x=X, y=Y,
                mode='markers+text',
                text=list(range(1, N+1)),
                textposition='middle center',
                hoverinfo='text', 
                hovertext=feature_names,
                textfont=dict(
                    size=30,
                    color="black"
                ),
                marker=dict(
                    showscale=False, 
                    color=self.nodeColor, 
                    size=self.nodeSize,
                    line_width=3
                )
            )

            weight_trace = go.Scatter(
                x=weight_x, y=weight_y,
                hoverinfo='text',
                hovertext=weight_text,
                mode='markers',
                marker=dict(
                    showscale=False, 
                    size=0.0001,
                    color=[get_color('RdYlGn', 0.5*w+0.5) for w in weight_values]
                )
            )
        #Як кінець - фігура графу
        fig = go.Figure(
            data=edge_trace + [node_trace, weight_trace],
            layout=go.Layout(
                showlegend=False,
                hovermode='closest',
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                width=550, height=500,
                margin=dict(b=0,l=50,r=0,t=0),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
        )

        return fig

    def make_impulse_fig(self, values, names):
        res_df = pd.DataFrame(values, columns=names)
        print(res_df.columns)
        res_df = res_df.rename(columns={
            "X1": "Добувна промисловість", 
            "X2": "Постачання електроенергії",
            "X3": "Постачання газу", 
            "X4": "Виробництво коксу",
            "X5": "Вироблення виробів з деревини", 
            "X6": "Виробництво гумових виробів",
            "X7": "Металургійне виробництво", 
            "X8": "Виробництво хім речовин",
            "X9": "Машинобудування", 
            "X10": "Виробництво вугілля"
            })
        print(res_df)
        impulse_plot_fig = px.line(
            res_df, markers=True
        )

        impulse_plot_fig.update_layout(
            xaxis=dict(
                showgrid=True, 
                zeroline=False, 
                gridcolor='black', 
                showline=True, 
                showticklabels=True
            ),
            yaxis=dict(
                showgrid=True, 
                zeroline=False, 
                gridcolor='blue', 
                showline=True, 
                showticklabels=True
            ),
            xaxis_title='Step',
            yaxis_title='Value',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            width=1000, height=600,
            hovermode="x unified"
        )

        return impulse_plot_fig
