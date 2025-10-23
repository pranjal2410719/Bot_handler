import streamlit as st
import asyncio
import threading
import time
import os
from telegram_bot_controller import main as run_bot

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
    .stopped {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
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

# Bot Status and Control
st.markdown("---")
st.markdown("### 🚀 Bot Control Panel")

# Initialize session state
if 'bot_running' not in st.session_state:
    st.session_state.bot_running = False
if 'bot_thread' not in st.session_state:
    st.session_state.bot_thread = None

def start_bot_in_thread():
    """Start bot in a separate thread with proper async handling."""
    def run_async_bot():
        try:
            # Create new event loop for this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Run the bot
            run_bot()
        except Exception as e:
            print(f"Bot error: {e}")
            st.session_state.bot_running = False
        finally:
            loop.close()
    
    if not st.session_state.bot_running:
        st.session_state.bot_running = True
        st.session_state.bot_thread = threading.Thread(target=run_async_bot, daemon=True)
        st.session_state.bot_thread.start()
        return True
    return False

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🟢 Start Bot", disabled=st.session_state.bot_running):
        if start_bot_in_thread():
            st.success("Bot started successfully!")
            st.rerun()

with col2:
    if st.button("🔄 Restart Bot"):
        st.session_state.bot_running = False
        time.sleep(1)
        if start_bot_in_thread():
            st.info("Bot restarted!")
            st.rerun()

with col3:
    if st.button("📊 View Logs"):
        st.info("Bot logs are displayed in the Streamlit Cloud console")

# Status Display
if st.session_state.bot_running:
    st.markdown('<div class="status-box running">✅ Bot is running and ready to handle messages!</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="status-box stopped">⚠️ Bot is stopped. Click "Start Bot" to begin.</div>', unsafe_allow_html=True)

# Instructions
st.markdown("---")
st.markdown("### 📱 How to Use")

st.markdown("""
1. **Start the bot** using the button above
2. **Open Telegram** and search for your bot
3. **Send /start** to begin interacting
4. **Browse services** using interactive buttons
5. **Get quotes** and connect with the team
6. **AI assistance** for any questions

**Bot Username:** Configure in @BotFather on Telegram
""")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; margin-top: 2rem;">
    <p>🏢 <strong>Braynix Studios</strong> - "Build digital experiences that think, feel, and sell."</p>
    <p>📱 WhatsApp: +91 8127314770 | 📧 Email: 2k24.cs1l.2410719@gmail.com</p>
</div>
""", unsafe_allow_html=True)

# Auto-start bot when app loads (only once)
if 'auto_started' not in st.session_state:
    st.session_state.auto_started = True
    if start_bot_in_thread():
        st.success("🤖 Bot auto-started successfully!")
        time.sleep(1)
        st.rerun()