from langflow import CustomComponent
from typing import Dict, Any, List
from analytics import get_post_type_metrics, get_trending_hashtags
from insight_generator import generate_insights
import json

class DataFetcher(CustomComponent):
    """Component to fetch data from Astra DB"""
    
    def process(self, days: int = 30) -> Dict[str, Any]:
        metrics = get_post_type_metrics(days=days)
        hashtags = get_trending_hashtags(limit=5)
        return {
            "metrics": metrics,
            "hashtags": hashtags
        }

class MetricsAnalyzer(CustomComponent):
    """Component to analyze engagement patterns"""
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        metrics = data["metrics"]
        hashtags = data["hashtags"]
        
        # Calculate performance metrics
        best_performing = max(metrics, key=lambda x: x['avg_engagement'])
        worst_performing = min(metrics, key=lambda x: x['avg_engagement'])
        
        # Analyze trends
        analyzed_data = {
            "metrics": metrics,
            "hashtags": hashtags,
            "analysis": {
                "best_type": best_performing['post_type'],
                "best_engagement": best_performing['avg_engagement'],
                "improvement_area": worst_performing['post_type'],
                "engagement_gap": best_performing['avg_engagement'] - worst_performing['avg_engagement']
            }
        }
        return analyzed_data

class OpenAIInsightGenerator(CustomComponent):
    """Component to generate insights using OpenAI"""
    
    def process(self, analyzed_data: Dict[str, Any]) -> str:
        metrics = analyzed_data["metrics"]
        hashtags = analyzed_data["hashtags"]
        analysis = analyzed_data["analysis"]
        
        # Generate insights using OpenAI
        insights = generate_insights(metrics, hashtags)
        
        # Add summary section
        summary = f"""# 📱 Social Media Performance Analysis

> Quick Summary: {analysis['best_type'].title()} posts are performing best with {analysis['best_engagement']:.1f}% engagement rate, 
> {analysis['engagement_gap']:.1f}% higher than {analysis['improvement_area']} posts.

---

{insights}"""
        
        return summary

def build_langflow_app():
    """Build and export the Langflow application"""
    components = {
        "DataFetcher": DataFetcher,
        "MetricsAnalyzer": MetricsAnalyzer,
        "OpenAIInsightGenerator": OpenAIInsightGenerator
    }
    
    flow_config = {
        "nodes": [
            {
                "id": "fetch",
                "type": "DataFetcher",
                "position": {"x": 100, "y": 100}
            },
            {
                "id": "analyze",
                "type": "MetricsAnalyzer",
                "position": {"x": 300, "y": 100}
            },
            {
                "id": "insights",
                "type": "OpenAIInsightGenerator",
                "position": {"x": 500, "y": 100}
            }
        ],
        "edges": [
            {"source": "fetch", "target": "analyze"},
            {"source": "analyze", "target": "insights"}
        ]
    }
    
    return components, flow_config

def save_flow():
    """Save the Langflow configuration to a file"""
    components, flow_config = build_langflow_app()
    with open('langflow_config.json', 'w') as f:
        json.dump({
            "components": {name: comp.to_dict() for name, comp in components.items()},
            "flow": flow_config
        }, f, indent=2)

if __name__ == "__main__":
    save_flow() 