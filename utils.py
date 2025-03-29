import requests
from bs4 import BeautifulSoup
from newspaper import Article
from datetime import datetime
import google.generativeai as genai
import json
import nltk
import feedparser
import time
from typing import List, Dict, Any, Optional
from config import (
    GEMINI_API_KEY, TAVILY_API_KEY, CATEGORIES, RESEARCH_DOMAINS,
    MAX_RESEARCH_PAPERS, MAX_RSS_ITEMS, RSS_CACHE_TIMEOUT
)
from openai import OpenAI

# Initialize NLTK
def initialize_nltk():
    """Initialize NLTK dependencies"""
    required_packages = ['punkt', 'averaged_perceptron_tagger', 'wordnet']
    for package in required_packages:
        try:
            nltk.data.find(f'tokenizers/{package}')
        except LookupError:
            nltk.download(package)

initialize_nltk()

# RSS feed cache
rss_cache: Dict[str, Dict[str, Any]] = {}

# Initialize OpenAI client
client = OpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

def clean_html(html_text: str) -> str:
    """Clean HTML content from text"""
    soup = BeautifulSoup(html_text, 'html.parser')
    return soup.get_text(separator=' ', strip=True)

def fetch_rss_feed(source: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Fetch and parse RSS feed with caching"""
    cache_key = source['rss_url']
    current_time = time.time()
    
    # Check cache
    if cache_key in rss_cache:
        cached_data = rss_cache[cache_key]
        if current_time - cached_data['timestamp'] < RSS_CACHE_TIMEOUT:
            return cached_data['entries']
    
    try:
        # Add allow_redirects=True to handle 301/303 redirects
        feed = feedparser.parse(
            source['rss_url'],
            agent='Mozilla/5.0 (compatible; ClimateRiskBot/1.0)'
        )
        
        # Check for successful response or redirect
        if hasattr(feed, 'status'):
            if feed.status not in [200, 301, 302, 303]:
                raise Exception(f"Feed returned status code: {feed.status}")
        
        if not feed.entries:
            raise Exception("No entries found in feed")
            
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

def fetch_article_content(url: str) -> Optional[Dict[str, Any]]:
    """Fetch and parse article content"""
    try:
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()
        
        return {
            'title': article.title,
            'text': article.text,
            'summary': article.summary,
            'keywords': article.keywords,
            'publish_date': article.publish_date,
            'url': url
        }
    except Exception as e:
        print(f"Error fetching article content from {url}: {str(e)}")
        return None

def fetch_news(source: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Fetch news from RSS feed"""
    articles = []
    entries = fetch_rss_feed(source)
    
    for entry in entries[:MAX_RSS_ITEMS]:
        try:
            # Clean description of HTML tags
            description = BeautifulSoup(entry.get('description', ''), 'html.parser').get_text()
            
            # Handle missing publish date gracefully
            publish_date = entry.get('published', entry.get('pubDate', entry.get('date', '')))
            
            articles.append({
                'title': entry.get('title', 'Untitled'),
                'summary': description,
                'url': entry.get('link', ''),
                'source_name': entry.get('source_name', source['name']),
                'publish_date': publish_date,
                'categories': entry.get('categories', [])
            })
        except Exception as e:
            print(f"Error processing article from {source['name']}: {str(e)}")
            continue
            
    return articles

def analyze_article(article: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Analyze article using AI"""
    try:
        # Simplified prompt to reduce JSON parsing errors
        response = client.chat.completions.create(
            model="gemini-2.0-flash",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert insurance and climate risk analyst. Provide analysis in valid JSON format only."
                },
                {
                    "role": "user",
                    "content": f"""
                    Analyze this article and return a JSON object with exactly this structure:
                    {{
                        "category": "Climate Risk",
                        "key_insights": ["insight1", "insight2"],
                        "risks_opportunities": {{
                            "risks": ["risk1", "risk2"],
                            "opportunities": ["opportunity1", "opportunity2"]
                        }},
                        "relevance_score": 5
                    }}

                    Title: {article['title']}
                    Content: {article['summary']}
                    Source: {article['source_name']}

                    Only use these categories: {', '.join(CATEGORIES)}
                    Ensure relevance_score is between 1 and 10.
                    """
                }
            ]
        )
        
        if response.choices[0].message.content:
            content = response.choices[0].message.content.strip()
            
            # Clean up the JSON string
            if '```json' in content:
                content = content.split('```json')[1].split('```')[0]
            elif '```' in content:
                content = content.split('```')[1].split('```')[0]
            
            # Remove any leading/trailing whitespace or special characters
            content = content.strip('` \n\r\t')
            
            # Parse the JSON
            try:
                analysis = json.loads(content)
                
                # Validate the analysis structure
                required_keys = ['category', 'key_insights', 'risks_opportunities', 'relevance_score']
                if not all(key in analysis for key in required_keys):
                    raise ValueError("Missing required keys in analysis")
                
                if analysis['category'] not in CATEGORIES:
                    analysis['category'] = 'Climate Risk'  # Default category
                
                # Ensure relevance_score is within bounds
                analysis['relevance_score'] = max(1, min(10, int(analysis['relevance_score'])))
                
                return {
                    'title': article['title'],
                    'url': article['url'],
                    'source': article['source_name'],
                    'analysis': analysis,
                    'category': analysis['category']
                }
            except json.JSONDecodeError as je:
                print(f"JSON parsing error for article '{article['title']}': {str(je)}")
                print(f"Problematic content: {content}")
                return None
                
    except Exception as e:
        print(f"Error analyzing article '{article['title']}': {str(e)}")
        return None

def fetch_research_papers(topic: str) -> List[Dict[str, Any]]:
    """Fetch relevant research papers"""
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
            json=data,
            timeout=10
        )
        
        if response.status_code == 200:
            results = response.json().get('results', [])
            return [
                {
                    'title': result.get('title'),
                    'url': result.get('url'),
                    'snippet': result.get('content'),
                    'score': result.get('score', 0)
                }
                for result in results
            ]
    except Exception as e:
        print(f"Error fetching research papers: {str(e)}")
    return []

def format_report(articles: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Format analyzed articles into a report"""
    category_counts = {}
    for article in articles:
        category = article.get('category', 'Uncategorized')
        category_counts[category] = category_counts.get(category, 0) + 1
    
    return {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'articles': articles,
        'summary': {
            'total_articles': len(articles),
            'categories': category_counts
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