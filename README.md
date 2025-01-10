# Social Media Analytics Dashboard

A real-time analytics dashboard for social media performance metrics using Streamlit, Astra DB, and AI-powered insights.

## Features

- 📊 Real-time metrics visualization
- 🤖 AI-powered performance insights
- 📈 Engagement funnel analysis
- 🏷️ Hashtag trend tracking
- 📱 Post type performance comparison
- 💾 Data export capabilities

## Tech Stack

- **Frontend**: Streamlit
- **Database**: DataStax Astra DB (Cassandra)
- **AI**: OpenAI (GPT-4)
- **Data Processing**: Pandas, Plotly

## Demo

[Watch the demo on YouTube](https://youtu.be/TQcCdB3WXAw)

## Screenshots

![Dashboard Overview](https://i.imghippo.com/files/ITm2690po.jpg)

![Metrics Visualization](https://i.imghippo.com/files/wYl7213NuY.jpg)

![Engagement Analysis](https://i.imghippo.com/files/kN5789bmc.jpg)

![Hashtag Trends](https://i.imghippo.com/files/rJoV6421Tw.jpg)

![Detailed Insights](https://i.imghippo.com/files/JKj4655QqI.jpg)


## Project Structure

```
social-media-analytics/
├── src/
│   ├── app.py              # Main Streamlit dashboard
│   ├── analytics.py        # Data analysis functions
│   ├── insight_generator.py # AI insights generation
│   ├── init_db.py         # Database initialization
│   └── db_connection.py   # Database connectivity
├── .env                   # Environment variables
├── .env.example          # Environment variables template
└── requirements.txt      # Python dependencies
```

## Quick Start

### Setup and Installation

1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd social-media-analytics
    ```

2. Set up environment variables:
    ```bash
    cp .env.example .env
    ```

3. Update `.env` with your credentials:
    ```
    ASTRA_DB_TOKEN=your_token_here
    ASTRA_DB_KEYSPACE=social_media_analytics
    ASTRA_SECURE_CONNECT_BUNDLE=./secure-connect-bundle.zip
    OPENAI_API_KEY=your_openai_api_key_here
    OPENAI_MODEL=gpt-4
    ```

4. Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

5. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

6. Initialize the database:
    ```bash
    python src/init_db.py
    ```

7. Run the application:
    ```bash
    streamlit run src/app.py
    ```

8. Access the dashboard at `http://localhost:8501`

## Database Setup

1. Create an Astra DB Account:
   - Visit [Astra DB](https://astra.datastax.com)
   - Sign up for a free account
   - Create a new database

2. Get Your Credentials:
   - Download the secure connect bundle
   - Generate an application token
   - Note your keyspace name

3. Configure Database:
   - Place the secure connect bundle in project root
   - Update `.env` with your credentials
   - Run database initialization script

## Dashboard Features

### Overview Mode

- Total post metrics
- Engagement rates by post type
- Trending hashtags analysis
- Engagement funnel visualization
- Reach vs Impressions comparison

### Detailed Analysis

- AI-generated insights
- Advanced metric correlations
- Engagement distribution analysis
- Performance trends

### Export Capabilities

- CSV export for metrics data
- JSON export for insights
- Hashtag performance reports

## Troubleshooting

### Common Issues

1. **Database Connection:**
    ```
    Error: Missing required environment variables
    Solution: Verify all credentials in .env file
    ```

2. **API Rate Limits:**
    ```
    Error: API rate limit exceeded
    Solution: Adjust refresh interval in dashboard settings
    ```

3. **Data Loading:**
    ```
    Error: No metrics available
    Solution: Run init_db.py to populate sample data
    ```

### Environment Variables

Make sure all required environment variables are set in your `.env` file:

- `ASTRA_DB_TOKEN`
- `ASTRA_DB_KEYSPACE`
- `ASTRA_SECURE_CONNECT_BUNDLE`
- `OPENAI_API_KEY`
- `OPENAI_MODEL`

## Development

### Local Development

1. Fork the repository
2. Create a feature branch
3. Install development dependencies
4. Make your changes
5. Run tests
6. Submit a pull request

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Add docstrings for functions
- Comment complex logic

## License

MIT License - See LICENSE file for details

## Contributors

- Your Name - Initial work

## Acknowledgments

- DataStax Astra DB for database
- OpenAI for AI capabilities
- Streamlit for dashboard framework

