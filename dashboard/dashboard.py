import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils.performance import PerformanceMonitor
from zpt_analysis import analyze, meme_shitcoin_analysis, multi_timeframe_confluence
from zpt_pricefeed import get_price
import time

# Page config
st.set_page_config(
    page_title="ChatZiPT v4 - AI Trading Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header { 
        font-size: 3rem; 
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4, #45B7D1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
    }
    .signal-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    .confidence-high { background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%); }
    .confidence-medium { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
    .confidence-low { background: linear-gradient(135deg, #4b6cb7 0%, #182848 100%); }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<h1 class="main-header">🚀 ChatZiPT v4 - AI Trading Dashboard</h1>', unsafe_allow_html=True)

# Performance monitoring
monitor = PerformanceMonitor()
monitor.start()

# Sidebar
st.sidebar.title("🎯 Trading Controls")

# Symbol selection
symbol = st.sidebar.selectbox(
    "Select Trading Pair:",
    ["BTCUSDT", "ETHUSDT", "XAUUSD", "DOGEUSDT", "SHIBUSDT", "PEPEUSDT"],
    index=0
)

# AI Features toggle
ai_features = st.sidebar.multiselect(
    "🧠 AI Features:",
    ["Multi-Timeframe Analysis", "SMC Analysis", "Wyckoff Signals", "AI Explanations", "Meme Coin Scanner"],
    default=["Multi-Timeframe Analysis", "AI Explanations"]
)

# Trading psychology
user_vibe = st.sidebar.selectbox(
    "🧘 Current Trading Mindset:",
    ["confident", "anxious", "revenge", "neutral"],
    index=3
)

# Auto-refresh
auto_refresh = st.sidebar.checkbox("🔄 Auto-refresh (30s)", value=False)

if auto_refresh:
    time.sleep(1)
    st.rerun()

# Main content
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.subheader(f"📊 {symbol} Analysis")
    
    # Get analysis
    if st.button("🔍 Analyze Signal", type="primary"):
        with st.spinner("🤖 AI is analyzing market data..."):
            analysis = analyze(symbol)
            
            # Signal display
            confidence_class = "confidence-high" if analysis["confidence"] > 0.9 else "confidence-medium" if analysis["confidence"] > 0.8 else "confidence-low"
            
            st.markdown(f"""
            <div class="signal-card {confidence_class}">
                <h3>🎯 Signal: {analysis["action"]}</h3>
                <h4>📊 Confidence: {analysis["confidence"]:.1%}</h4>
                <h4>💰 Current Price: ${analysis["price"]:.4f}</h4>
            </div>
            """, unsafe_allow_html=True)
            
            # AI Explanation
            if "AI Explanations" in ai_features:
                st.subheader("🧠 AI Analysis")
                st.info(analysis["explanation"])
            
            # Multi-timeframe
            if "Multi-Timeframe Analysis" in ai_features:
                st.subheader("⏰ Multi-Timeframe Confluence")
                mtf_data = analysis["details"]
                mtf_df = pd.DataFrame.from_dict(mtf_data, orient='index')
                st.dataframe(mtf_df, use_container_width=True)
            
            # SL/TP Levels
            st.subheader("🎯 Risk Management")
            sl_tp = analysis["SLTP"]
            col_sl, col_tp = st.columns(2)
            
            with col_sl:
                st.metric("🛡️ Stop Loss", f"${sl_tp['SL']:.4f}" if sl_tp['SL'] else "N/A")
            
            with col_tp:
                tp_levels = sl_tp['TP'][:3] if sl_tp['TP'] else []
                for i, tp in enumerate(tp_levels):
                    st.metric(f"🎯 TP{i+1}", f"${tp:.4f}")

with col2:
    st.subheader("📈 Live Price")
    price = get_price(symbol)
    st.metric(
        label="Current Price",
        value=f"${price:.4f}" if price else "N/A",
        delta="Live"
    )
    
    # Performance stats
    st.subheader("⚡ Performance")
    st.metric("Response Time", f"{monitor.elapsed():.3f}s")
    
with col3:
    st.subheader("🎮 Quick Actions")
    
    if st.button("🔥 Meme Coin Scan", type="secondary"):
        if "Meme Coin Scanner" in ai_features:
            with st.spinner("Scanning meme coins..."):
                meme_results = meme_shitcoin_analysis()
                if meme_results:
                    st.success(f"Found {len(meme_results)} high-confidence signals!")
                    for result in meme_results[:3]:  # Show top 3
                        st.write(f"🚀 {result['symbol']}: {result['action']} ({result['confidence']:.1%})")
                else:
                    st.warning("No high-confidence meme signals found.")
        else:
            st.info("Enable 'Meme Coin Scanner' in AI Features")
    
    if st.button("🧘 Trading Psychology"):
        from zpt_analysis import vibe_response
        advice = vibe_response(user_vibe, "LONG")  # Example signal
        st.info(advice)

# Footer
st.markdown("---")
st.markdown("© ChatZiPT v4 by Tiffany | Powered by AI & Technical Analysis")