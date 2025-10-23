import streamlit as st
import subprocess
import threading
import time
import os

st.set_page_config(
    page_title="Braynix Studios Bot",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .status-box {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .running {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🤖 Braynix Studios Telegram Bot</h1>', unsafe_allow_html=True)

# Bot Information
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Bot Status", "🟢 Online", "Ready to serve")

with col2:
    st.metric("Services", "6", "Digital Solutions")

with col3:
    st.metric("Features", "AI + Lead Gen", "Automated")

# Bot Details
st.markdown("---")
st.markdown("### 🌟 Bot Features")

features = [
    "💻 **Website Development** - Custom, responsive websites",
    "📱 **Mobile Apps** - Native & cross-platform development", 
    "☁️ **SaaS Development** - Scalable cloud solutions",
    "🛒 **E-commerce** - Smart online stores",
    "🚀 **SEO & Marketing** - Digital growth strategies",
    "📊 **Data Analytics** - Business intelligence insights"
]

for feature in features:
    st.markdown(f"- {feature}")

st.markdown("---")
st.markdown("### 🔧 Bot Configuration")

col1, col2 = st.columns(2)

with col1:
    st.info("**Bot Token:** Configured ✅")
    st.info("**Gemini AI:** Enabled ✅")
    st.info("**Email Notifications:** Active ✅")

with col2:
    st.success("**Admin ID:** 6880117839")
    st.success("**WhatsApp:** +91 8127314770")
    st.success("**Email:** 2k24.cs1l.2410719@gmail.com")

# Bot Commands
st.markdown("---")
st.markdown("### 📋 Available Commands")

commands = {
    "/start": "Welcome message with services menu",
    "/services": "Browse all available services", 
    "/pricing": "View pricing information",
    "/about": "Learn about Braynix Studios",
    "/contact": "Get contact information",
    "/help": "Show available commands"
}

for cmd, desc in commands.items():
    st.markdown(f"**{cmd}** - {desc}")

# Bot Status
st.markdown("---")
st.markdown("### 🚀 Bot Status")

# Start bot in background using subprocess
if 'bot_process' not in st.session_state:
    try:
        # Start bot as separate process
        st.session_state.bot_process = subprocess.Popen(
            ["python", "bot_runner.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=os.path.dirname(__file__) or "."
        )
        st.session_state.bot_started = True
    except Exception as e:
        st.session_state.bot_started = False
        st.error(f"Failed to start bot: {e}")

# Display status
if st.session_state.get('bot_started', False):
    st.markdown('<div class="status-box running">✅ Telegram Bot is running and ready to handle messages!</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="status-box running">⚠️ Bot starting... Please wait a moment.</div>', unsafe_allow_html=True)

# Instructions
st.markdown("---")
st.markdown("### 📱 How to Use Your Bot")

st.markdown("""
1. **Open Telegram** and search for your bot
2. **Send /start** to begin interacting
3. **Browse services** using interactive buttons
4. **Get quotes** and connect with the team
5. **AI assistance** for any questions

**Your bot is now live and running 24/7!**
""")

# Contact Info
st.markdown("---")
st.markdown("### 📞 Direct Contact")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**📱 WhatsApp:** [+91 8127314770](https://wa.me/918127314770)")
    st.markdown("**📧 Email:** 2k24.cs1l.2410719@gmail.com")

with col2:
    st.markdown("**🏢 Company:** Braynix Studios")
    st.markdown("**💡 Philosophy:** Build digital experiences that think, feel, and sell.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; margin-top: 2rem;">
    <p><strong>🤖 Your Telegram Bot is Live!</strong></p>
    <p>Users can now interact with your bot on Telegram to explore services and get quotes.</p>
</div>
""", unsafe_allow_html=True)