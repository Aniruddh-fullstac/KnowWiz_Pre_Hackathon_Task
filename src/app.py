import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from analytics import get_post_type_metrics, get_trending_hashtags
from insight_generator import generate_insights
import pandas as pd
import time
import json
from datetime import datetime
import base64

def create_download_link(df, filename):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download CSV</a>'
    return href

def main():
    st.set_page_config(page_title="Social Media Analytics Dashboard", layout="wide")
    
    # Header with refresh button
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("📊 Social Media Analytics Dashboard")
    with col2:
        if st.button("🔄 Refresh Data"):
            st.experimental_rerun()
    
    st.markdown("---")

    # Sidebar filters and controls
    st.sidebar.header("Filters & Controls")
    update_frequency = st.sidebar.selectbox(
        "Auto-refresh Interval",
        ["Off", "30 seconds", "1 minute", "5 minutes"],
        index=0
    )
    
    view_mode = st.sidebar.radio(
        "View Mode",
        ["Overview", "Detailed Analysis", "Export"]
    )

    # Initialize session state for real-time updates
    if 'last_update' not in st.session_state:
        st.session_state.last_update = datetime.now()
        st.session_state.metrics_history = []

    # Load data
    with st.spinner("Fetching metrics..."):
        metrics = get_post_type_metrics(30)
        hashtags = get_trending_hashtags(5)
        
        if not metrics:
            st.error("Unable to fetch metrics from the database. Please check your database connection.")
            st.stop()
            
        df_metrics = pd.DataFrame(metrics)
        df_hashtags = pd.DataFrame(hashtags) if hashtags else pd.DataFrame()
        
        # Store metrics history for trend analysis
        st.session_state.metrics_history.append({
            'timestamp': datetime.now(),
            'metrics': metrics
        })
        if len(st.session_state.metrics_history) > 100:
            st.session_state.metrics_history.pop(0)

    if view_mode == "Overview":
        # Main metrics cards
        metric_cols = st.columns(4)
        with metric_cols[0]:
            st.metric("Total Posts", df_metrics['total_posts'].sum())
        with metric_cols[1]:
            st.metric("Avg Engagement Rate", f"{df_metrics['avg_engagement'].mean():.2f}%")
        with metric_cols[2]:
            st.metric("Total Reach", df_metrics['avg_reach'].sum())
        with metric_cols[3]:
            st.metric("Best Performing Type", 
                     df_metrics.loc[df_metrics['avg_engagement'].idxmax(), 'post_type'])

        # Interactive charts
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Post Performance by Type")
            metrics_to_show = st.multiselect(
                "Select Metrics",
                ['avg_likes', 'avg_comments', 'avg_shares'],
                default=['avg_likes', 'avg_comments', 'avg_shares']
            )
            fig1 = px.bar(df_metrics, 
                         x='post_type', 
                         y=metrics_to_show,
                         title="Average Engagement Metrics by Post Type",
                         barmode='group')
            st.plotly_chart(fig1, use_container_width=True)

            st.subheader("Engagement Funnel")
            # Calculate funnel metrics
            funnel_metrics = pd.DataFrame([{
                'stage': 'Impressions',
                'count': df_metrics['avg_impressions'].mean(),
            }, {
                'stage': 'Reach',
                'count': df_metrics['avg_reach'].mean(),
            }, {
                'stage': 'Engagement',
                'count': df_metrics['avg_likes'].mean() + df_metrics['avg_comments'].mean() + df_metrics['avg_shares'].mean(),
            }, {
                'stage': 'Likes',
                'count': df_metrics['avg_likes'].mean(),
            }, {
                'stage': 'Comments',
                'count': df_metrics['avg_comments'].mean(),
            }, {
                'stage': 'Shares',
                'count': df_metrics['avg_shares'].mean(),
            }])

            fig2 = go.Figure(go.Funnel(
                y=funnel_metrics['stage'],
                x=funnel_metrics['count'],
                textinfo="value+percent initial",
                textposition="inside",
                textfont=dict(size=14),
                marker=dict(
                    color=["#1f77b4", "#2ca02c", "#ff7f0e", "#d62728", "#9467bd", "#8c564b"]
                ),
                connector={"line": {"color": "royalblue", "width": 3}}
            ))
            
            fig2.update_layout(
                title="Engagement Funnel Analysis",
                showlegend=False,
                height=400
            )
            st.plotly_chart(fig2, use_container_width=True)

        with col2:
            st.subheader("Trending Hashtags")
            fig3 = px.bar(df_hashtags,
                         x='hashtag',
                         y='usage_count',
                         title="Top Hashtags by Usage",
                         color='avg_engagement',
                         hover_data=['avg_engagement'])
            st.plotly_chart(fig3, use_container_width=True)

            st.subheader("Reach vs Impressions")
            fig4 = px.scatter(df_metrics,
                            x='avg_reach',
                            y='avg_impressions',
                            size='avg_engagement',
                            color='post_type',
                            title="Reach vs Impressions",
                            hover_data=['total_posts'])
            st.plotly_chart(fig4, use_container_width=True)

    elif view_mode == "Detailed Analysis":
        st.subheader("🤖 AI-Generated Insights")
        
        # Add a container for the insights with custom styling
        insights_container = st.container()
        with insights_container:
            with st.spinner("Generating detailed analysis..."):
                insights = generate_insights()
                if insights:
                    st.markdown("""
                    <style>
                        .detailed-insights h2 {
                            color: #1f77b4;
                            margin-top: 1.5em;
                        }
                        .detailed-insights ul {
                            margin-bottom: 1em;
                        }
                    </style>
                    """, unsafe_allow_html=True)
                    st.markdown(f'<div class="detailed-insights">{insights}</div>', unsafe_allow_html=True)
                else:
                    st.error("Failed to generate insights. Please try again.")

        st.markdown("---")
        st.subheader("Advanced Metrics")
        
        # Replace bar chart with radar/spider chart
        st.subheader("Engagement Metrics Comparison")
        # Prepare data for radar chart
        metrics_to_compare = ['avg_likes', 'avg_comments', 'avg_shares', 'avg_engagement', 'avg_reach', 'avg_impressions']
        
        # Normalize the data for better visualization
        df_normalized = pd.DataFrame()
        for metric in metrics_to_compare:
            max_val = df_metrics[metric].max()
            if max_val != 0:  # Avoid division by zero
                df_normalized[metric] = df_metrics[metric] / max_val * 100
            else:
                df_normalized[metric] = df_metrics[metric]
        
        fig5 = go.Figure()
        
        for idx, post_type in enumerate(df_metrics['post_type']):
            fig5.add_trace(go.Scatterpolar(
                r=df_normalized.iloc[idx],
                theta=[m.replace('avg_', '').title() for m in metrics_to_compare],
                name=post_type.title(),
                fill='toself',
                line=dict(width=2)
            ))
        
        fig5.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    ticksuffix="%"
                )
            ),
            showlegend=True,
            title="Engagement Metrics Radar Chart (Normalized %)",
            height=600,
            legend=dict(
                yanchor="top",
                y=1.2,
                xanchor="left",
                x=1.1
            )
        )
        st.plotly_chart(fig5, use_container_width=True)

        # Correlation Matrix
        numeric_cols = df_metrics.select_dtypes(include=['float64', 'int64']).columns
        correlation = df_metrics[numeric_cols].corr()
        fig6 = px.imshow(correlation,
                        title="Metrics Correlation Matrix",
                        color_continuous_scale='RdBu')
        st.plotly_chart(fig6, use_container_width=True)

    else:  # Export view
        st.subheader("Export Data")
        
        export_options = st.multiselect(
            "Select data to export",
            ["Metrics", "Hashtags", "Insights"],
            default=["Metrics", "Hashtags"]
        )
        
        if "Metrics" in export_options:
            st.markdown("### Metrics Data")
            st.dataframe(df_metrics.style.highlight_max(axis=0))
            st.markdown(create_download_link(df_metrics, "social_media_metrics.csv"), unsafe_allow_html=True)
            
        if "Hashtags" in export_options:
            st.markdown("### Hashtags Data")
            st.dataframe(df_hashtags)
            st.markdown(create_download_link(df_hashtags, "hashtag_metrics.csv"), unsafe_allow_html=True)
            
        if "Insights" in export_options:
            insights = generate_insights()
            st.markdown("### AI Insights")
            st.markdown(insights)
            
            # Export insights as JSON
            insights_dict = {"timestamp": datetime.now().isoformat(), "insights": insights}
            insights_json = json.dumps(insights_dict, indent=2)
            b64 = base64.b64encode(insights_json.encode()).decode()
            st.markdown(
                f'<a href="data:file/json;base64,{b64}" download="social_media_insights.json">Download Insights JSON</a>',
                unsafe_allow_html=True
            )

    # Auto-refresh logic
    if update_frequency != "Off":
        seconds = {"30 seconds": 30, "1 minute": 60, "5 minutes": 300}[update_frequency]
        time_since_update = (datetime.now() - st.session_state.last_update).total_seconds()
        
        if time_since_update >= seconds:
            st.session_state.last_update = datetime.now()
            time.sleep(1)  # Small delay to prevent too frequent updates
            st.experimental_rerun()
        
        st.sidebar.markdown(f"Next update in: {max(0, int(seconds - time_since_update))} seconds")

if __name__ == "__main__":
    main() 