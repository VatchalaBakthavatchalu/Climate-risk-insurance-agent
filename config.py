from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()



# API Configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY') # Make sure this is set in your .env file
TAVILY_API_KEY = os.getenv('TAVILY_API_KEY')

# News sources for climate risk and insurance
NEWS_SOURCES = [
    {
        'name': 'The Guardian Environment',
        'rss_url': 'https://www.theguardian.com/environment/climate-crisis/rss',
        'keywords': []  # No filtering needed as feed is already focused
    },
    
    
    {
        'name': 'Risk Management Monitor',
        'rss_url': 'http://www.riskmanagementmonitor.com/feed/',
        'keywords': ['climate', 'insurance', 'environmental', 'disaster']
    },
    {
        'name': 'Climate Home News',
        'rss_url': 'https://www.climatechangenews.com/feed/',
        'keywords': ['insurance', 'risk', 'finance', 'policy']
    },
    
    {
        'name': 'Yale Climate Connections',
        'rss_url': 'https://yaleclimateconnections.org/feed/',
        'keywords': ['insurance', 'risk', 'business', 'economic']
    },
   
    {
        'name': 'Nature Climate Change',
        'rss_url': 'https://www.nature.com/nclimate.rss',
        'keywords': ['insurance', 'risk', 'economic', 'policy']
    }
]

# Research paper sources
RESEARCH_DOMAINS = [
    'arxiv.org',
    'scholar.google.com',
    'researchgate.net',
    'sciencedirect.com'
]

# Categories for news classification
CATEGORIES = [
    'Climate Risk',
    'InsureTech',
    'Policies',
    'Natural Disasters',
    'Market Trends',
    'Regulatory Changes'
]

# RSS Feed Configuration
RSS_CACHE_TIMEOUT = 3600  # Cache RSS feeds for 1 hour
MAX_RSS_ITEMS = 10  # Maximum number of items to fetch per feed

# Time intervals for news fetching (in minutes)
UPDATE_INTERVAL = 60

# Maximum number of articles to process per source
MAX_ARTICLES_PER_SOURCE = 5

# Maximum number of research papers to fetch
MAX_RESEARCH_PAPERS = 3 