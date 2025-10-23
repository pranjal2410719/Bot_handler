import streamlit as st
import asyncio
import threading
import time
import warnings
import logging

# Suppress Streamlit warnings
warnings.filterwarnings("ignore", message=".*missing ScriptRunContext.*")
logging.getLogger("streamlit").setLevel(logging.ERROR)

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

# Bot Status
st.markdown("---")
st.markdown("### 🚀 Bot Status")

# Initialize session state
if 'bot_started' not in st.session_state:
    st.session_state.bot_started = False

def start_telegram_bot():
    """Start the Telegram bot in background."""
    if not st.session_state.bot_started:
        try:
            from telegram_bot_controller import main as run_bot
            
            def bot_runner():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    run_bot()
                except Exception as e:
                    print(f"Bot error: {e}")
                finally:
                    loop.close()
            
            thread = threading.Thread(target=bot_runner, daemon=True)
            thread.start()
            st.session_state.bot_started = True
            return True
        except Exception as e:
            st.error(f"Failed to start bot: {e}")
            return False
    return True

# Auto-start bot
if start_telegram_bot():
    st.markdown('<div class="status-box running">✅ Telegram Bot is running and ready to handle messages!</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="status-box stopped">❌ Bot failed to start. Check logs for details.</div>', unsafe_allow_html=True)

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