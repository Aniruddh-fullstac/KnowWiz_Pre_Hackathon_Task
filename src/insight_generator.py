import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def generate_insights(metrics, hashtags):
    """Generate insights using OpenAI API"""
    try:
        prompt = construct_prompt(metrics, hashtags)
        response = client.chat.completions.create(
            model=os.getenv('OPENAI_MODEL', 'gpt-4'),
            messages=[
                {"role": "system", "content": "You are a social media analytics expert who provides detailed, data-driven insights and recommendations."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating insights: {str(e)}"

def construct_prompt(metrics, hashtags):
    """Construct a detailed prompt for analysis"""
    prompt = "Analyze these social media metrics and provide detailed insights. Format your response in markdown with clear sections:\n\n"
    prompt += "Performance Metrics by Post Type:\n"
    
    for metric in metrics:
        prompt += f"""
{metric['post_type'].title()} Posts:
- Total Posts: {metric['total_posts']}
- Engagement Metrics:
  * Average Likes: {metric['avg_likes']}
  * Average Comments: {metric['avg_comments']}
  * Average Shares: {metric['avg_shares']}
  * Overall Engagement Rate: {metric['avg_engagement']}%
- Reach and Visibility:
  * Average Reach: {metric['avg_reach']}
  * Average Impressions: {metric['avg_impressions']}
  * Click-Through Rate: {metric['avg_ctr']}%"""

        if metric.get('avg_watch_time', 0) > 0:
            prompt += f"\n  * Average Watch Time: {metric['avg_watch_time']} seconds"

    if hashtags:
        prompt += "\n\nTrending Hashtags:"
        for tag in hashtags:
            prompt += f"\n- #{tag['hashtag']}: Used {tag['usage_count']} times, {tag['avg_engagement']}% engagement"

    prompt += """

Please provide a comprehensive analysis in the following format:

## 📊 Overall Performance Summary
[Provide a concise summary of overall social media performance across all post types]

## 📈 Content Performance Analysis
[Analyze the effectiveness of different content types, including which types perform best and why]

## 👥 Engagement Patterns
[Detail user behavior insights and engagement patterns across different post types]

## 🎯 Strategic Recommendations
1. Content Strategy:
   [Specific recommendations for content improvement]
2. Posting Schedule:
   [Best times to post based on engagement patterns]
3. Hashtag Strategy:
   [Recommendations for hashtag usage]
4. Engagement Optimization:
   [Tips for improving engagement across different metrics]

## 🔍 Areas for Improvement
[Identify specific areas that need attention and optimization]

Format your analysis with proper markdown headings, bullet points, and emphasis where appropriate. Focus on actionable insights and data-driven recommendations."""

    return prompt

def test_insights():
    print("\nGenerating insights from metrics...")
    insights = generate_insights()
    print("\nINSIGHTS:")
    print(insights)

if __name__ == "__main__":
    test_insights()