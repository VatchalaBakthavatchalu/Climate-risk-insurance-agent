import streamlit as st
from datetime import datetime
import time
from utils import fetch_news, analyze_article, format_report, fetch_research_papers
from config import NEWS_SOURCES, UPDATE_INTERVAL, CATEGORIES

def filter_by_tag(data, selected_tag):
    """Filter items by tag"""
    if not data or selected_tag == "All":
        return data
    return [item for item in data if selected_tag.lower() in 
            [tag.lower() for tag in item.get('analysis', {}).get('key_insights', [])]]

def get_all_tags(articles):
    """Get unique tags from articles"""
    tags = set()
    for article in articles:
        insights = article.get('analysis', {}).get('key_insights', [])
        for insight in insights:
            tags.add(insight.lower())
    return sorted(list(tags))

def main():
    st.set_page_config(
        page_title="Climate Risk & Insurance Analyzer",
        page_icon="🌍",
        layout="wide"
    )
    
    st.title("🌍 Climate Risk & Insurance News Analyzer")
    st.write("Real-time analysis of climate risk and insurance news")
    
    # Initialize session state
    if 'last_update' not in st.session_state:
        st.session_state.last_update = None
    if 'reports' not in st.session_state:
        st.session_state.reports = []
    if 'all_articles' not in st.session_state:
        st.session_state.all_articles = []
    if 'error_log' not in st.session_state:
        st.session_state.error_log = []

    # Sidebar configuration
    with st.sidebar:
        st.title("Settings")
        selected_sources = st.multiselect(
            "Select News Sources",
            options=[s['name'] for s in NEWS_SOURCES],
            default=[NEWS_SOURCES[0]['name']],
            help="Choose the news sources you want to analyze"
        )
        
        category_filter = st.multiselect(
            "Filter by Categories",
            options=CATEGORIES,
            default=[],
            help="Select categories to filter news articles"
        )

    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fetch_button = st.button("🔄 Fetch Latest News & Research", use_container_width=True)
        if fetch_button:
            with st.spinner("Fetching and analyzing content..."):
                all_articles = []
                errors = []
                
                # Progress tracking
                progress_text = st.empty()
                progress_bar = st.progress(0)
                total_sources = len(selected_sources)
                
                for idx, source in enumerate(NEWS_SOURCES):
                    if source['name'] in selected_sources:
                        try:
                            progress_text.text(f"Processing: {source['name']}")
                            articles = fetch_news(source)
                            
                            for article in articles:
                                analysis = analyze_article(article)
                                if analysis:
                                    if not category_filter or analysis['category'] in category_filter:
                                        all_articles.append(analysis)
                            
                            progress = min(1.0, (idx + 1) / total_sources)
                            progress_bar.progress(progress)
                            
                        except Exception as e:
                            errors.append(f"Error processing {source['name']}: {str(e)}")
                
                # Clear progress indicators
                progress_text.empty()
                progress_bar.empty()
                
                # Update session state
                st.session_state.all_articles = all_articles
                st.session_state.error_log = errors
                st.session_state.last_update = datetime.now()
                
                # Show success/error messages
                if all_articles:
                    st.success(f"Successfully analyzed {len(all_articles)} articles")
                if errors:
                    st.error("Some errors occurred during processing. Check the error log in settings.")

    # Display content
    if st.session_state.all_articles:
        display_articles = st.session_state.all_articles
        
        # News Section
        st.header("📰 News Analysis")
        for article in display_articles:
            with st.expander(f"📄 {article['title']} ({article['source']})"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Category:** `{article['category']}`")
                    
                    st.markdown("**🔍 Key Insights:**")
                    for insight in article['analysis']['key_insights']:
                        st.markdown(f"- {insight}")
                    
                    col_risks, col_opps = st.columns(2)
                    with col_risks:
                        st.markdown("**⚠️ Risks:**")
                        for risk in article['analysis']['risks_opportunities']['risks']:
                            st.markdown(f"- {risk}")
                    
                    with col_opps:
                        st.markdown("**💡 Opportunities:**")
                        for opp in article['analysis']['risks_opportunities']['opportunities']:
                            st.markdown(f"- {opp}")
                
                with col2:
                    st.metric("Relevance Score", f"{article['analysis']['relevance_score']}/10")
                    st.markdown(f"**Source:** [{article['source']}]({article['url']})")
                    st.markdown("---")
                    st.markdown("**📚 Related Research:**")
                    papers = fetch_research_papers(article['category'])
                    for paper in papers[:2]:
                        st.markdown(f"- [{paper['title']}]({paper['url']})")

    # Sidebar stats and info
    with st.sidebar:
        if st.session_state.last_update:
            st.markdown("---")
            st.markdown("### 📊 Stats")
            st.write(f"Last updated: {st.session_state.last_update.strftime('%Y-%m-%d %H:%M:%S')}")
            st.metric("Articles Analyzed", len(st.session_state.all_articles))
            
            if st.session_state.error_log:
                st.markdown("### ⚠️ Error Log")
                with st.expander("View Errors"):
                    for error in st.session_state.error_log:
                        st.error(error)
        
        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.info(
            "This dashboard provides real-time analysis of climate risk and insurance news. "
            "Select news sources and categories to focus on specific areas of interest."
        )

if __name__ == "__main__":
    main() 