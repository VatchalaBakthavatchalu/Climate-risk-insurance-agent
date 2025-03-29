# InsureTech-Climate-Risk-Agent
An AI-powered agent platform that analyzes real-time news and climate risk data to provide actionable insights for insurance underwriting decisions.

## Prerequisites

### System Dependencies
Before installing Python packages, ensure you have the following system dependencies:

For macOS:
```bash
brew install libxml2 libxslt
```

For Ubuntu/Debian:
```bash
sudo apt-get install python3-dev libxml2-dev libxslt1-dev
sudo apt-get install libjpeg-dev zlib1g-dev libpng-dev
```

For Windows:
- Install Visual C++ Build Tools
- Install wget
- The required dependencies should be automatically handled by pip

## Quick Start

1. Clone and setup:
```bash
git clone https://github.com/VatchalaBakthavatchalu/Climate-risk-insurance-agent.git
cd InsureTech-Climate-Risk-Agent
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
python -m pip install --upgrade pip  # Upgrade pip first



pip install -r requirements.txt
```


2. Create `.env` file with your API keys:
```
GEMINI_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
```

3. Run the app:
```bash
streamlit run main.py
```

The app will open in your browser with an interactive dashboard for climate risk analysis and insurance insights.

## Configuration

The application can be configured by modifying `config.py`:
- News sources and RSS feeds
- Research paper domains
- Categories for news classification
- Update intervals
- Maximum number of articles/papers to process

## API Requirements

The application requires the following API keys:
- Google Gemini API key for AI-powered analysis
- Tavily API key for web search capabilities

Make sure to keep your API keys secure and never commit them to version control.

## Streamlit Features

The application provides an interactive web interface with:
- Real-time data visualization
- Interactive filters and controls
- Responsive dashboard layout
- Automatic data updates
- Export capabilities for reports and insights


