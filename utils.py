import requests
from bs4 import BeautifulSoup
from newspaper import Article
from datetime import datetime
import google.generativeai as genai
import json
import nltk
import feedparser
import time
from config import (
    GEMINI_API_KEY, TAVILY_API_KEY, CATEGORIES, RESEARCH_DOMAINS,
    MAX_RESEARCH_PAPERS, MAX_RSS_ITEMS, RSS_CACHE_TIMEOUT
)
from openai import OpenAI

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# RSS feed cache
rss_cache = {}

# Add OpenAI client initialization after the RSS cache initialization
client = OpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

def fetch_rss_feed(source):
    """
    Fetch and parse RSS feed with caching
    """
    cache_key = source['rss_url']
    current_time = time.time()
    
    # Check cache
    if cache_key in rss_cache:
        cached_data = rss_cache[cache_key]
        if current_time - cached_data['timestamp'] < RSS_CACHE_TIMEOUT:
            return cached_data['entries']
    
    try:
        feed = feedparser.parse(source['rss_url'])
        entries = feed.entries[:MAX_RSS_ITEMS]
        
        # Filter entries if keywords are specified
        if source['keywords']:
            filtered_entries = []
            for entry in entries:
                text = (entry.title + ' ' + entry.get('description', '')).lower()
                if any(keyword.lower() in text for keyword in source['keywords']):
                    filtered_entries.append(entry)
            entries = filtered_entries
        
        # Cache the results
        rss_cache[cache_key] = {
            'timestamp': current_time,
            'entries': entries
        }
        
        return entries
    except Exception as e:
        print(f"Error fetching RSS feed from {source['name']}: {str(e)}")
        return []

def fetch_article_content(source):
    """
    Fetch articles from RSS feed and parse content
    """
    articles = []
    entries = fetch_rss_feed(source)
    
    for entry in entries[:MAX_RSS_ITEMS]:
        try:
            # Get the full article URL
            article_url = entry.link
            
            # Try to get content using newspaper3k
            article = Article(article_url)
            article.download()
            article.parse()
            article.nlp()
            
            articles.append({
                'title': article.title or entry.title,
                'text': article.text,
                'summary': article.summary or entry.get('description', ''),
                'keywords': article.keywords,
                'publish_date': article.publish_date or entry.get('published_parsed'),
                'url': article_url,
                'source_name': source['name']
            })
        except Exception as e:
            print(f"Error processing article from {source['name']}: {str(e)}")
            # Fallback to RSS entry content
            articles.append({
                'title': entry.title,
                'text': entry.get('description', ''),
                'summary': entry.get('description', ''),
                'keywords': source['keywords'],
                'publish_date': entry.get('published_parsed'),
                'url': article_url,
                'source_name': source['name']
            })
    
    return articles

def fetch_research_papers(topic):
    """
    Fetch relevant research papers using Tavily API directly
    """
    try:
        headers = {
            'Content-Type': 'application/json',
            'api-key': TAVILY_API_KEY
        }
        
        data = {
            'query': f"latest research papers on {topic} in insurance and climate risk",
            'search_depth': 'advanced',
            'max_results': MAX_RESEARCH_PAPERS,
            'include_domains': RESEARCH_DOMAINS
        }
        
        response = requests.post(
            'https://api.tavily.com/search',
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            results = response.json().get('results', [])
            papers = []
            for result in results:
                papers.append({
                    'title': result.get('title'),
                    'url': result.get('url'),
                    'snippet': result.get('content'),
                    'score': result.get('score', 0)
                })
            return papers
        else:
            print(f"Error from Tavily API: {response.text}")
            return []
            
    except Exception as e:
        print(f"Error fetching research papers: {str(e)}")
        return []

def fetch_news(source):
    """
    Fetch news from RSS feed
    """
    try:
        feed = feedparser.parse(source['rss_url'])
        articles = []
        
        for entry in feed.entries[:5]:
            text = (entry.title + ' ' + entry.get('description', '')).lower()
            if not source['keywords'] or any(keyword.lower() in text for keyword in source['keywords']):
                articles.append({
                    'title': entry.title,
                    'summary': entry.get('description', ''),
                    'url': entry.link,
                    'source_name': source['name'],
                    'publish_date': entry.get('published', '')
                })
        
        return articles
    except Exception as e:
        print(f"Error fetching from {source['name']}: {str(e)}")
        return []

def analyze_article(article):
    """
    Analyze article using Gemini Flash API through OpenAI client
    """
    try:
        response = client.chat.completions.create(
            model="gemini-2.0-flash",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert insurance and climate risk analyst. Analyze the article and provide structured insights."
                },
                {
                    "role": "user",
                    "content": f"""
                    Analyze this article and provide insights relevant to insurance and climate risk:
                    Title: {article['title']}
                    Content: {article['summary']}
                    Source: {article['source_name']}
                    
                    Provide a JSON response with the following structure:
                    {{
                        "category": "one of: {', '.join(CATEGORIES)}",
                        "key_insights": ["2-3 key insights for insurance industry"],
                        "risks_opportunities": {{
                            "risks": ["1-2 potential risks"],
                            "opportunities": ["1-2 potential opportunities"]
                        }},
                        "relevance_score": number between 1-10
                    }}
                    """
                }
            ]
        )
        
        if response.choices[0].message.content:
            try:
                # Clean the response text
                content = response.choices[0].message.content.strip()
                if content.startswith('```json'):
                    content = content[7:-3]
                elif content.startswith('```'):
                    content = content[3:-3]
                
                analysis = json.loads(content)
                return {
                    'title': article['title'],
                    'url': article['url'],
                    'source': article['source_name'],
                    'analysis': analysis,
                    'category': analysis.get('category', 'Uncategorized')
                }
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON for {article['title']}: {str(e)}")
                return None
        else:
            print("No content in response")
            return None
                
    except Exception as e:
        print(f"Error analyzing {article['title']}: {str(e)}")
        return None

def format_report(articles):
    """
    Format analyzed articles into a report
    """
    return {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'articles': [a for a in articles if a is not None],
        'summary': {
            'total_articles': len([a for a in articles if a is not None]),
            'categories': {}
        }
    }

def extract_category(text):
    """
    Extract category from text if JSON parsing fails
    """
    for category in CATEGORIES:
        if category.lower() in text.lower():
            return category
    return "Uncategorized" 