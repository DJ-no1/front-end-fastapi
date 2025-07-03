import streamlit as st
import requests
import json
import time
import os
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://3.110.40.177:8000")

# Page configuration
st.set_page_config(
    page_title="URL Intelligence Dashboard",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .security-good {
        color: #28a745;
        font-weight: bold;
    }
    .security-warning {
        color: #ffc107;
        font-weight: bold;
    }
    .security-danger {
        color: #dc3545;
        font-weight: bold;
    }
    .stButton > button {
        background-color: #1f77b4;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 0.5rem 1rem;
        font-size: 1rem;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #0d5aa7;
    }
</style>
""", unsafe_allow_html=True)

def get_security_color(score):
    """Return color class based on security score"""
    if score >= 80:
        return "security-good"
    elif score >= 60:
        return "security-warning"
    else:
        return "security-danger"

def test_api_connectivity():
    """Test if API is reachable"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def analyze_url(url):
    """Send URL to API for analysis"""
    try:
        payload = {"url": url}
        response = requests.post(
            f"{API_BASE_URL}/analyze",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json(), None
        else:
            return None, f"API Error: {response.status_code} - {response.text}"
    
    except requests.exceptions.Timeout:
        return None, "Request timed out. The analysis is taking longer than expected."
    except requests.exceptions.ConnectionError:
        return None, "Failed to connect to the API. Please check if the service is running."
    except Exception as e:
        return None, f"An error occurred: {str(e)}"

def test_connectivity(url):
    """Test URL connectivity without full analysis"""
    try:
        payload = {"url": url}
        response = requests.post(
            f"{API_BASE_URL}/test-connectivity",
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json(), None
        else:
            return None, f"API Error: {response.status_code} - {response.text}"
    
    except Exception as e:
        return None, f"Connectivity test failed: {str(e)}"

def display_analysis_results(data):
    """Display the analysis results in a formatted way"""
    
    # Header with URL and analysis time
    st.markdown(f"### 🎯 Analysis Results for: `{data['url']}`")
    st.markdown(f"**Analysis completed in:** `{data['analysis_time']}`")
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🔒 Security", "⚡ Performance", "📄 Content", "🛠️ Technology", "🌐 Domain"])
    
    with tab1:
        st.markdown("### Security Analysis")
        security = data['security']
        
        # Security score with color coding
        score_color = get_security_color(security['safety_score'])
        st.markdown(f"<div class='{score_color}'>Security Score: {security['safety_score']}/100</div>", 
                   unsafe_allow_html=True)
        
        # Security metrics in columns
        col1, col2, col3 = st.columns(3)
        
        with col1:
            ssl_status = "✅ Enabled" if security['ssl_enabled'] else "❌ Disabled"
            st.metric("SSL/HTTPS", ssl_status)
        
        with col2:
            ssl_valid = "✅ Valid" if security['ssl_valid'] else "❌ Invalid"
            st.metric("SSL Certificate", ssl_valid)
        
        with col3:
            https_redirect = "✅ Available" if security['https_redirect'] else "❌ Not Available"
            st.metric("HTTPS Redirect", https_redirect)
        
        # Suspicious patterns
        if security['suspicious_patterns']:
            st.markdown("**⚠️ Suspicious Patterns Detected:**")
            for pattern in security['suspicious_patterns']:
                st.markdown(f"- {pattern}")
        else:
            st.markdown("**✅ No suspicious patterns detected**")
    
    with tab2:
        st.markdown("### Performance Analysis")
        performance = data['performance']
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Response Time", f"{performance['response_time']}s")
        
        with col2:
            st.metric("Status Code", performance['status_code'])
        
        with col3:
            page_size_kb = round(performance['page_size'] / 1024, 2)
            st.metric("Page Size", f"{page_size_kb} KB")
        
        with col4:
            st.metric("Load Speed", performance['load_speed'])
    
    with tab3:
        st.markdown("### Content Analysis")
        content = data['content']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Page Title:**")
            st.write(content['title'] or "Not available")
            
            st.markdown("**Meta Description:**")
            st.write(content['description'] or "Not available")
        
        with col2:
            st.metric("Word Count", content['word_count'])
            st.metric("External Links", content['external_links'])
            
            forms_status = "✅ Yes" if content['has_forms'] else "❌ No"
            st.metric("Has Forms", forms_status)
        
        if content['meta_keywords']:
            st.markdown("**Meta Keywords:**")
            st.write(content['meta_keywords'])
    
    with tab4:
        st.markdown("### Technology Stack")
        tech = data['technology']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Server:**")
            st.write(tech['server'] or "Unknown")
            
            st.markdown("**CMS Detected:**")
            st.write(tech['cms_detected'] or "None detected")
        
        with col2:
            if tech['technologies']:
                st.markdown("**Technologies:**")
                for tech_item in tech['technologies']:
                    st.markdown(f"- {tech_item}")
            
            if tech['frameworks']:
                st.markdown("**Frameworks:**")
                for framework in tech['frameworks']:
                    st.markdown(f"- {framework}")
    
    with tab5:
        st.markdown("### Domain Information")
        domain = data['domain']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Domain:**")
            st.write(domain['domain'])
            
            st.markdown("**Registrar:**")
            st.write(domain['registrar'] or "Not available")
        
        with col2:
            st.markdown("**Creation Date:**")
            st.write(domain['creation_date'] or "Not available")
            
            st.markdown("**Expiration Date:**")
            st.write(domain['expiration_date'] or "Not available")
        
        if domain['country'] and domain['country'] != "Unable to fetch":
            st.markdown("**Country:**")
            st.write(domain['country'])

def main():
    # Header
    st.markdown('<h1 class="main-header">🔍 URL Intelligence Dashboard</h1>', unsafe_allow_html=True)
    
    # Sidebar with API status
    with st.sidebar:
        st.markdown("### 📊 Dashboard Info")
        
        # Check API connectivity
        api_status = test_api_connectivity()
        if api_status:
            st.success("✅ API Connected")
        else:
            st.error("❌ API Disconnected")
        
        st.markdown(f"**API Endpoint:** `{API_BASE_URL}`")
        st.markdown("**Status:** Real-time URL analysis")
        
        st.markdown("---")
        st.markdown("### 📝 How to Use")
        st.markdown("""
        1. Enter a URL to analyze
        2. Choose analysis type
        3. Click 'Analyze' button
        4. Review detailed results
        """)
        
        st.markdown("---")
        st.markdown("### 🛡️ Security Scoring")
        st.markdown("""
        - **80-100**: Excellent Security
        - **60-79**: Good Security  
        - **Below 60**: Needs Attention
        """)
    
    # Main content area
    st.markdown("### 🌐 Enter URL for Analysis")
    
    # URL input
    url_input = st.text_input(
        "URL to analyze:",
        placeholder="https://example.com",
        help="Enter a complete URL starting with http:// or https://"
    )
    
    # Analysis type selection
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        analysis_type = st.selectbox(
            "Analysis Type:",
            ["Full Analysis", "Quick Connectivity Test"],
            help="Choose between comprehensive analysis or quick connectivity check"
        )
    
    with col2:
        analyze_button = st.button("🔍 Analyze", use_container_width=True)
    
    with col3:
        clear_button = st.button("🗑️ Clear", use_container_width=True)
    
    # Handle clear button
    if clear_button:
        st.rerun()
    
    # Handle analysis
    if analyze_button and url_input:
        if not url_input.startswith(('http://', 'https://')):
            st.error("❌ Please enter a valid URL starting with http:// or https://")
            return
        
        # Show progress
        with st.spinner(f"Analyzing {url_input}..."):
            if analysis_type == "Full Analysis":
                result, error = analyze_url(url_input)
                
                if result:
                    display_analysis_results(result)
                else:
                    st.error(f"❌ Analysis failed: {error}")
            
            else:  # Quick connectivity test
                result, error = test_connectivity(url_input)
                
                if result:
                    st.markdown("### 🚀 Connectivity Test Results")
                    
                    if result.get('reachable', False):
                        st.success(f"✅ {result['message']}")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Status Code", result.get('status_code', 'N/A'))
                        with col2:
                            st.metric("Reachable", "Yes")
                        
                        # Show headers if available
                        if result.get('headers'):
                            with st.expander("🔍 Response Headers"):
                                headers_df = pd.DataFrame(
                                    list(result['headers'].items()),
                                    columns=['Header', 'Value']
                                )
                                st.dataframe(headers_df, use_container_width=True)
                    else:
                        st.error(f"❌ {result['message']}")
                        st.info(f"Error Type: {result.get('error', 'Unknown')}")
                else:
                    st.error(f"❌ Connectivity test failed: {error}")
    
    elif analyze_button and not url_input:
        st.warning("⚠️ Please enter a URL to analyze")
    
    # Example URLs section
    st.markdown("---")
    st.markdown("### 💡 Try These Example URLs")
    
    example_cols = st.columns(3)
    examples = [
        ("GitHub", "https://github.com"),
        ("Google", "https://google.com"),
        ("HTTP Site", "http://neverssl.com")
    ]
    
    for i, (name, url) in enumerate(examples):
        with example_cols[i]:
            if st.button(f"📝 {name}", key=f"example_{i}", use_container_width=True):
                st.text_input("URL to analyze:", value=url, key=f"example_input_{i}")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666; padding: 1rem;'>"
        "🔍 URL Intelligence Dashboard | Powered by FastAPI & Streamlit"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
