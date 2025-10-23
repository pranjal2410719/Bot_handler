import streamlit as st
import threading
import time
import os
import sys

# Suppress warnings
import warnings
warnings.filterwarnings("ignore")

# Import bot
from telegram_bot_controller import main as run_bot

st.set_page_config(
    page_title="Braynix Studios Bot",
    page_icon="🤖",
    layout="wide"
)

# Start bot in background
@st.cache_resource
def start_bot():
    def bot_thread():
        try:
            run_bot()
        except Exception as e:
            st.error(f"Bot error: {e}")
    
    thread = threading.Thread(target=bot_thread, daemon=True)
    thread.start()
    return "Bot Started"

# Auto-start bot
bot_status = start_bot()

# UI
st.title("🤖 Braynix Studios Telegram Bot")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Status", "🟢 Online")
with col2:
    st.metric("Services", "6")
with col3:
    st.metric("Features", "AI + Lead Gen")

st.success("✅ Bot is running and ready to handle messages!")

st.markdown("---")
st.markdown("### 🌟 Services")
st.markdown("""
- 💻 **Website Development** (₹8,000 - ₹30,000+)
- 📱 **Mobile Apps** (₹25,000+ for MVPs)
- ☁️ **SaaS Development** (₹40,000+)
- 🛒 **E-commerce** (₹15,000 - ₹50,000+)
- 🚀 **SEO & Marketing** (₹5,000/month+)
- 📊 **Data Analytics** (Custom pricing)
""")

st.markdown("---")
st.markdown("### 📋 Commands")
st.markdown("""
- `/start` - Welcome message
- `/services` - Browse services
- `/pricing` - View pricing
- `/about` - About company
- `/contact` - Contact info
- `/help` - Show help
""")

st.markdown("---")
st.markdown("### 📞 Contact")
st.markdown("""
**📱 WhatsApp:** [+91 8127314770](https://wa.me/918127314770)  
**📧 Email:** 2k24.cs1l.2410719@gmail.com  
**🏢 Company:** Braynix Studios
""")

st.info("Your Telegram bot is running 24/7 and ready to handle messages!")