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
        'name': 'Reuters Sustainability',
        'rss_url': 'https://www.reutersagency.com/feed/?taxonomy=best-topics&post_type=best',
        'keywords': ['climate', 'sustainability', 'insurance', 'risk']
    },
    {
        'name': 'Insurance Journal',
        'rss_url': 'https://www.insurancejournal.com/feed/',
        'keywords': ['climate', 'risk', 'natural disaster', 'sustainability']
    },
    {
        'name': 'The Guardian Environment',
        'rss_url': 'https://www.theguardian.com/environment/climate-crisis/rss',
        'keywords': []  # No filtering needed as feed is already focused
    },
    {
        'name': 'Science Daily Environment',
        'rss_url': 'https://www.sciencedaily.com/rss/earth_climate/climate.xml',
        'keywords': ['insurance', 'risk', 'economic']
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