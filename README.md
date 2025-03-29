# Climate Risk & Insurance News Analyzer

A real-time dashboard that analyzes news and research related to climate risk and insurance using AI. The application fetches content from various news sources, analyzes it using AI, and presents insights about risks and opportunities in the industry.

## Features

- Real-time news analysis from multiple sources
- AI-powered insights and risk assessment
- Research paper recommendations
- Category-based filtering
- Interactive dashboard interface
- Source selection and filtering capabilities

## Prerequisites

- Python 3.12
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/VatchalaBakthavatchalu/Climate-risk-insurance-agent.git
cd Climate-risk-insurance-agent
```

2. Create and activate a virtual environment:
```bash
python3.12 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## API Keys Required


### Gemini API Key
- Model used: `gemini-2.0-flash`
- Get your API key from: [Google AI Studio](https://makersuite.google.com/app/apikey)

### Tavily API Key
- Get your API key from: [Tavily API](https://tavily.com/)


The application requires two API keys:
- **Gemini API Key**: For AI-powered analysis
- **Tavily API Key**: For research paper fetching

You'll need to enter these keys in the application's sidebar settings.

## Running the Application

1. Start the Streamlit server:
```bash
streamlit run main.py
```

2. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

3. Enter your API keys in the sidebar settings

## Usage

1. **Configure API Keys**:
   - Enter your API keys in the sidebar under "API Configuration"
   - Keys are required before fetching data

2. **Select News Sources**:
   - Choose from available news sources in the sidebar
   - Multiple sources can be selected

3. **Filter Categories**:
   - Filter news by categories like Climate Risk, InsureTech, Policies, etc.
   - Multiple categories can be selected

4. **Fetch Data**:
   - Click "Fetch Latest News & Research" to update the dashboard
   - Analysis results will be displayed with key insights, risks, and opportunities

## Project Structure

- `app.py`: Main application file with Streamlit interface
- `utils.py`: Utility functions for fetching and analyzing content
- `config.py`: Configuration settings and API endpoints

## News Sources

The application fetches news from various sources including:
- The Guardian Environment
- Risk Management Monitor
- Climate Home News
- Yale Climate Connections
- Nature Climate Change

## Categories

News is categorized into:
- Climate Risk
- InsureTech
- Policies
- Natural Disasters
- Market Trends
- Regulatory Changes

## Error Handling

- API key validation before fetching data
- Error logging in sidebar
- Graceful handling of failed requests


## Configuration

The application can be configured by modifying `config.py`:
- News sources and RSS feeds
- Research paper domains
- Categories for news classification
- Update intervals
- Maximum number of articles/papers to process



