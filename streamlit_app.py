import streamlit as st
import subprocess
import sys
import threading
import time
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

if 'bot_running' not in st.session_state:
    st.session_state.bot_running = False

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🟢 Start Bot", disabled=st.session_state.bot_running):
        if not st.session_state.bot_running:
            st.session_state.bot_running = True
            
            def run_bot_thread():
                try:
                    run_bot()
                except Exception as e:
                    st.error(f"Bot error: {e}")
                    st.session_state.bot_running = False
            
            thread = threading.Thread(target=run_bot_thread, daemon=True)
            thread.start()
            st.success("Bot started successfully!")
            st.rerun()

with col2:
    if st.button("🔄 Restart Bot"):
        st.session_state.bot_running = False
        time.sleep(1)
        st.session_state.bot_running = True
        st.info("Bot restarted!")
        st.rerun()

with col3:
    if st.button("📊 View Logs"):
        st.info("Check the terminal/console for detailed logs")

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

**Bot Username:** `@your_bot_username` (configure in BotFather)
""")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; margin-top: 2rem;">
    <p>🏢 <strong>Braynix Studios</strong> - "Build digital experiences that think, feel, and sell."</p>
    <p>📱 WhatsApp: +91 8127314770 | 📧 Email: 2k24.cs1l.2410719@gmail.com</p>
</div>
""", unsafe_allow_html=True)

# Auto-start bot when app loads
if not st.session_state.bot_running:
    st.session_state.bot_running = True
    def auto_start_bot():
        try:
            run_bot()
        except Exception as e:
            st.error(f"Auto-start failed: {e}")
            st.session_state.bot_running = False
    
    thread = threading.Thread(target=auto_start_bot, daemon=True)
    thread.start()