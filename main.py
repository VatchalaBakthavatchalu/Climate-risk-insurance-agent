import streamlit as st
from datetime import datetime
from utils import fetch_news, analyze_article, format_report, fetch_research_papers
from config import NEWS_SOURCES, UPDATE_INTERVAL

def filter_by_tag(data, selected_tag):
    """Filter items by tag"""
    return [item for item in data if selected_tag.lower() in 
            [tag.lower() for tag in item.get('analysis', {}).get('key_insights', [])]]

def get_all_tags(articles):
    """Get unique tags from articles"""
    tags = set()
    for article in articles:
        insights = article.get('analysis', {}).get('key_insights', [])
        for insight in insights:
            tags.add(insight.lower())
    return sorted(tags)

def main():
    st.title("Climate Risk & Insurance News Analyzer")
    st.write("Real-time analysis of climate risk and insurance news")
    
    # Initialize session state
    if 'last_update' not in st.session_state:
        st.session_state.last_update = None
    if 'reports' not in st.session_state:
        st.session_state.reports = []
    if 'all_articles' not in st.session_state:
        st.session_state.all_articles = []

    # Sidebar configuration
    st.sidebar.title("Settings")
    selected_sources = st.sidebar.multiselect(
        "Select News Sources",
        options=[s['name'] for s in NEWS_SOURCES],
        default=[NEWS_SOURCES[0]['name']]
    )
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.button("Fetch Latest News & Research"):
            with st.spinner("Analyzing content..."):
                all_articles = []
                
                # Fetch and analyze articles from selected sources
                for source in NEWS_SOURCES:
                    if source['name'] in selected_sources:
                        articles = fetch_news(source)
                        for article in articles:
                            analysis = analyze_article(article)
                            if analysis:
                                all_articles.append(analysis)
                
                # Store articles in session state
                st.session_state.all_articles = all_articles
                
                # Generate report
                report = format_report(all_articles)
                st.session_state.reports.append(report)
                st.session_state.last_update = datetime.now()

    # Tag filtering in sidebar
    if st.session_state.all_articles:
        st.sidebar.header("Filter by Topic")
        all_tags = get_all_tags(st.session_state.all_articles)
        selected_tag = st.sidebar.selectbox("Select a topic", ["All"] + all_tags)

    # Display content
    if st.session_state.all_articles:
        # Filter articles if tag selected
        display_articles = (st.session_state.all_articles if selected_tag == "All" 
                          else filter_by_tag(st.session_state.all_articles, selected_tag))
        
        # News Section
        st.header("News Analysis")
        for article in display_articles:
            with st.expander(f"{article['title']} ({article['source']})"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**Category:** {article['category']}")
                    
                    st.write("**Key Insights:**")
                    for insight in article['analysis']['key_insights']:
                        st.write(f"- {insight}")
                    
                    st.write("**Risks:**")
                    for risk in article['analysis']['risks_opportunities']['risks']:
                        st.write(f"- {risk}")
                    
                    st.write("**Opportunities:**")
                    for opp in article['analysis']['risks_opportunities']['opportunities']:
                        st.write(f"- {opp}")
                
                with col2:
                    st.metric("Relevance Score", article['analysis']['relevance_score'])
                    st.write(f"**Source:** [{article['source']}]({article['url']})")
                    
                    # Fetch related research papers
                    if selected_tag != "All":
                        st.write("**Related Research:**")
                        papers = fetch_research_papers(selected_tag)
                        for paper in papers[:2]:  # Show top 2 related papers
                            st.write(f"- [{paper['title']}]({paper['url']})")

    # Stats and info in sidebar
    if st.session_state.last_update:
        st.sidebar.markdown("---")
        st.sidebar.write(f"Last updated: {st.session_state.last_update.strftime('%Y-%m-%d %H:%M:%S')}")
        if st.session_state.reports:
            st.sidebar.metric("Articles Analyzed", len(st.session_state.all_articles))
            
    # About section in sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("### About")
    st.sidebar.info(
        "This dashboard analyzes news and research related to climate risk and insurance. "
        "Select topics to filter content and discover related research papers."
    )

if __name__ == "__main__":
    main() 