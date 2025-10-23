import streamlit as st
import os
from google import genai
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Initialize Telegram bot
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Welcome to Braynix Studios Bot! How can I help you today?')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
    Available commands:
    /start - Start the bot
    /help - Show this help message
    /services - List our services
    /quote - Request a quote
    
    You can also chat with our AI assistant by simply sending a message!
    """
    await update.message.reply_text(help_text)

async def services_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    services = "\n".join([f"- {service}" for service in SERVICE_PRICING.keys()])
    await update.message.reply_text(f"Our Services:\n{services}")

async def quote_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quote_text = "Please provide the following information:\n1. Your Name\n2. Contact Details\n3. Service Required\n4. Budget Range"
    await update.message.reply_text(quote_text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        client = init_gemini()
        system_prompt = """You are Braynix Studios' AI assistant. Focus on our digital services: websites, mobile apps, SaaS, e-commerce, SEO, and analytics. Be professional and encourage users to discuss their project needs."""
        
        full_prompt = f"{system_prompt}\n\nUser: {update.message.text}"
        chat = client.chats.create(model="gemini-2.5-flash")
        response = chat.send_message(full_prompt)
        
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text("I'm experiencing technical difficulties. Please try again later.")

@st.cache_resource
def init_telegram_bot():
    if "TELEGRAM_BOT_TOKEN" not in st.secrets:
        st.error("Please set your Telegram bot token in .streamlit/secrets.toml")
        return None
    
    app = Application.builder().token(st.secrets["TELEGRAM_BOT_TOKEN"]).build()
    
    # Add handlers
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('services', services_command))
    app.add_handler(CommandHandler('quote', quote_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    return app

# Page config
st.set_page_config(
    page_title="Braynix Studios - Digital Growth Partner",
    page_icon="🚀",
    layout="wide"
)

# Initialize Gemini client
@st.cache_resource
def init_gemini():
    os.environ['GEMINI_API_KEY'] = st.secrets.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")
    return genai.Client()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "lead_data" not in st.session_state:
    st.session_state.lead_data = {}
if "lead_step" not in st.session_state:
    st.session_state.lead_step = None
if "bot_running" not in st.session_state:
    st.session_state.bot_running = False

# Service pricing
SERVICE_PRICING = {
    'Website Development': '₹8,000 - ₹30,000+',
    'Mobile App Development': '₹25,000+ for MVPs',
    'SaaS Development': '₹40,000+',
    'E-commerce Solutions': '₹15,000 - ₹50,000+',
    'SEO & Digital Marketing': '₹5,000/month+',
    'Data Analytics': 'Custom pricing'
}

# Header
st.markdown("""
<div style='text-align: center; padding: 2rem 0;'>
    <h1>🌟 Braynix Studios</h1>
    <h3>Your Digital Growth Partner</h3>
    <p><em>"Build digital experiences that think, feel, and sell."</em></p>
</div>
""", unsafe_allow_html=True)

# Sidebar - Services
with st.sidebar:
    st.header("🚀 Our Services")
    
    service_buttons = [
        "💻 Website Development",
        "📱 Mobile App Development", 
        "☁️ SaaS Development",
        "🛒 E-commerce Solutions",
        "🚀 SEO & Digital Marketing",
        "📊 Data Analytics"
    ]
    
    selected_service = st.selectbox("Choose a service:", ["Select a service..."] + service_buttons)
    
    if selected_service != "Select a service...":
        service_name = selected_service.split(" ", 1)[1]
        st.write(f"**Pricing:** {SERVICE_PRICING.get(service_name, 'Contact for pricing')}")
        
        if st.button("Get Quote for " + service_name):
            st.session_state.lead_step = "name"
            st.session_state.lead_data = {"service": service_name}
            st.rerun()
    
    st.markdown("---")
    st.markdown("### 📂 Portfolio Highlights")
    st.markdown("""
    - 🏪 **ShopEase** - E-commerce platform
    - 📚 **StudyXpress** - Learning platform
    - 📱 **PadhaiXpress** - Student app
    - 🎓 **CupConnect** - Social media app
    """)

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    # Lead capture form
    if st.session_state.lead_step:
        st.header("📞 Get Your Quote")
        
        with st.form("lead_form"):
            if st.session_state.lead_step == "name":
                name = st.text_input("Your Name *")
                if st.form_submit_button("Next"):
                    if name:
                        st.session_state.lead_data["name"] = name
                        st.session_state.lead_step = "contact"
                        st.rerun()
            
            elif st.session_state.lead_step == "contact":
                contact = st.text_input("Contact Number or Email *")
                if st.form_submit_button("Next"):
                    if contact:
                        st.session_state.lead_data["contact"] = contact
                        st.session_state.lead_step = "budget"
                        st.rerun()
            
            elif st.session_state.lead_step == "budget":
                budget = st.text_input("Approximate Budget Range")
                if st.form_submit_button("Submit Quote Request"):
                    st.session_state.lead_data["budget"] = budget
                    
                    # Display success message
                    st.success("🎉 Thank you! Your quote request has been submitted.")
                    st.balloons()
                    
                    # Show lead summary
                    st.write("**Your Details:**")
                    st.write(f"- **Name:** {st.session_state.lead_data['name']}")
                    st.write(f"- **Contact:** {st.session_state.lead_data['contact']}")
                    st.write(f"- **Service:** {st.session_state.lead_data['service']}")
                    st.write(f"- **Budget:** {budget or 'Not specified'}")
                    
                    # Reset form
                    st.session_state.lead_step = None
                    st.session_state.lead_data = {}
    
    else:
        # Chat interface
        st.header("💬 Chat with Our AI Assistant")
        
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask about our services..."):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate AI response
            try:
                client = init_gemini()
                system_prompt = """You are Braynix Studios' AI assistant. Focus on our digital services: websites, mobile apps, SaaS, e-commerce, SEO, and analytics. Be professional and encourage users to discuss their project needs."""
                
                full_prompt = f"{system_prompt}\n\nUser: {prompt}"
                chat = client.chats.create(model="gemini-2.5-flash")
                response = chat.send_message(full_prompt)
                
                # Add assistant response
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                with st.chat_message("assistant"):
                    st.markdown(response.text)
                    
            except Exception as e:
                error_msg = "I'm experiencing technical difficulties. Please try again or contact us directly."
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
                with st.chat_message("assistant"):
                    st.markdown(error_msg)

with col2:
    st.header("🏢 About Braynix Studios")
    st.markdown("""
    **Next-gen digital agency** driven by creativity, logic, and design thinking.
    
    **Our Mission:** To empower businesses with intelligent, aesthetic, and scalable digital products.
    
    **Services:**
    - 💻 Custom Websites
    - 📱 Mobile Apps  
    - ☁️ SaaS Platforms
    - 🛒 E-commerce Stores
    - 🚀 Digital Marketing
    - 📊 Data Analytics
    
    **Why Choose Us:**
    - ✅ 50+ successful projects
    - ✅ 95% client satisfaction
    - ✅ Modern, scalable solutions
    - ✅ On-time delivery guarantee
    """)
    
    if st.button("🚀 Start Your Project", type="primary"):
        st.session_state.lead_step = "name"
        st.session_state.lead_data = {"service": "General Inquiry"}
        st.rerun()

# Telegram Bot Management Section
st.markdown("---")
st.header("🤖 Telegram Bot Management")

bot_app = init_telegram_bot()

if bot_app:
    col1, col2 = st.columns(2)
    
    with col1:
        if not st.session_state.bot_running:
            if st.button("🟢 Start Telegram Bot"):
                st.session_state.bot_running = True
                asyncio.run(bot_app.run_polling())
                st.success("Bot is running!")
        else:
            if st.button("🔴 Stop Telegram Bot"):
                st.session_state.bot_running = False
                asyncio.run(bot_app.stop())
                st.info("Bot has been stopped.")
    
    with col2:
        st.markdown("""
        **Bot Commands:**
        - `/start` - Welcome message
        - `/help` - Show available commands
        - `/services` - List our services
        - `/quote` - Request a quote
        """)

else:
    st.error("Please configure your Telegram bot token in .streamlit/secrets.toml")
    st.code("""
# Add this to your .streamlit/secrets.toml file:
TELEGRAM_BOT_TOKEN = "your-bot-token-here"
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 1rem 0;'>
    <p>Built with ❤️ by <strong>Braynix Studios</strong></p>
    <p>🌐 Turning complexity into elegance through design, data, and code</p>
</div>
""", unsafe_allow_html=True)