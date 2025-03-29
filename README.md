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

- Python 3.x
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Climate-risk-insurance-agent
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## API Keys Required

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

- `main.py`: Main application file with Streamlit interface
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

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Add your license information here]

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


