import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from google import genai

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# API Keys
TELEGRAM_BOT_TOKEN = "8454185284:AAEOVgJQas-LVC8IwW_YvsLz1SaCXaxKgvA"
GEMINI_API_KEY = "AIzaSyDoy0XRc85_oI44KPmZdLxwo0B3k3K7PIM"

# Initialize Gemini client
os.environ['GEMINI_API_KEY'] = GEMINI_API_KEY
client = genai.Client()

# User data storage
user_data = {}

# Service pricing
SERVICE_PRICING = {
    'website': '₹8,000 - ₹30,000+',
    'mobile': '₹25,000+ for MVPs',
    'saas': '₹40,000+',
    'ecommerce': '₹15,000 - ₹50,000+',
    'seo': '₹5,000/month+',
    'analytics': 'Custom pricing'
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send welcome message with service buttons."""
    keyboard = [
        [InlineKeyboardButton("💻 Website Development", callback_data='service_website')],
        [InlineKeyboardButton("📱 Mobile App", callback_data='service_mobile')],
        [InlineKeyboardButton("☁️ SaaS Product", callback_data='service_saas')],
        [InlineKeyboardButton("🛒 E-commerce", callback_data='service_ecommerce')],
        [InlineKeyboardButton("🚀 SEO & Marketing", callback_data='service_seo')],
        [InlineKeyboardButton("📊 Data Analytics", callback_data='service_analytics')],
        [InlineKeyboardButton("💬 Get Quote", callback_data='capture_lead')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_msg = """🌟 Welcome to Braynix Studios!

Your digital growth partner — we build websites, apps, and SaaS platforms that help your business grow.

**Our Philosophy:** "Build digital experiences that think, feel, and sell."

What service interests you today?"""
    
    await update.message.reply_text(welcome_msg, reply_markup=reply_markup, parse_mode='Markdown')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button callbacks."""
    query = update.callback_query
    await query.answer()
    
    if query.data.startswith('service_'):
        service = query.data.replace('service_', '')
        await show_service_details(query, service)
    elif query.data == 'capture_lead':
        await start_lead_capture(query)
    elif query.data == 'back_to_services':
        await show_services_menu(query)

async def show_service_details(query, service: str) -> None:
    """Show service details with pricing."""
    service_info = {
        'website': {
            'title': '💻 Website Development',
            'description': 'Custom, responsive, SEO-optimized websites that convert visitors into customers.',
            'features': '• Modern UI/UX design\n• Mobile-responsive\n• SEO optimization\n• Fast loading speeds',
            'pricing': SERVICE_PRICING['website']
        },
        'mobile': {
            'title': '📱 Mobile App Development',
            'description': 'High-performance Android & iOS apps with stunning design.',
            'features': '• Native & Cross-platform\n• Modern UI/UX\n• API integrations\n• App Store deployment',
            'pricing': SERVICE_PRICING['mobile']
        },
        'saas': {
            'title': '☁️ SaaS Development',
            'description': 'Scalable software platforms with multi-tenant architecture.',
            'features': '• Cloud-based solutions\n• Multi-tenant systems\n• Subscription billing\n• Admin dashboards',
            'pricing': SERVICE_PRICING['saas']
        },
        'ecommerce': {
            'title': '🛒 E-commerce Solutions',
            'description': 'Smart online stores with conversion-optimized design.',
            'features': '• Product catalogs\n• Payment gateways\n• Inventory management\n• Order tracking',
            'pricing': SERVICE_PRICING['ecommerce']
        },
        'seo': {
            'title': '🚀 SEO & Digital Marketing',
            'description': 'Data-driven strategies to boost your online visibility.',
            'features': '• SEO optimization\n• Content marketing\n• Social media marketing\n• PPC campaigns',
            'pricing': SERVICE_PRICING['seo']
        },
        'analytics': {
            'title': '📊 Data Analytics',
            'description': 'Transform your data into actionable insights.',
            'features': '• Business intelligence\n• Custom dashboards\n• Predictive analytics\n• Data visualization',
            'pricing': SERVICE_PRICING['analytics']
        }
    }
    
    info = service_info[service]
    keyboard = [
        [InlineKeyboardButton("📞 Get Quote", callback_data='capture_lead')],
        [InlineKeyboardButton("🔙 Back to Services", callback_data='back_to_services')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = f"""**{info['title']}**

{info['description']}

**Key Features:**
{info['features']}

**Pricing:** {info['pricing']}

Ready to get started?"""
    
    await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='Markdown')

async def start_lead_capture(query) -> None:
    """Start the lead capture process."""
    user_id = query.from_user.id
    user_data[user_id] = {'step': 'name'}
    
    await query.edit_message_text(
        "Great! Let's get you connected with our team.\n\n**Please share your name:**",
        parse_mode='Markdown'
    )

async def show_services_menu(query) -> None:
    """Show the main services menu."""
    keyboard = [
        [InlineKeyboardButton("💻 Website Development", callback_data='service_website')],
        [InlineKeyboardButton("📱 Mobile App", callback_data='service_mobile')],
        [InlineKeyboardButton("☁️ SaaS Product", callback_data='service_saas')],
        [InlineKeyboardButton("🛒 E-commerce", callback_data='service_ecommerce')],
        [InlineKeyboardButton("🚀 SEO & Marketing", callback_data='service_seo')],
        [InlineKeyboardButton("📊 Data Analytics", callback_data='service_analytics')],
        [InlineKeyboardButton("💬 Get Quote", callback_data='capture_lead')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = """🌟 **Braynix Studios Services**

Choose a service to learn more:"""
    
    await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle text messages and lead capture."""
    user_id = update.message.from_user.id
    message_text = update.message.text
    
    # Check if user is in lead capture flow
    if user_id in user_data:
        await handle_lead_capture_step(update, context)
        return
    
    # Regular AI response for general queries
    try:
        system_prompt = """You are Braynix Studios' AI assistant. Focus on our digital services: websites, mobile apps, SaaS, e-commerce, SEO, and analytics. Be professional and encourage users to discuss their project needs."""
        
        full_prompt = f"{system_prompt}\n\nUser: {message_text}"
        chat = client.chats.create(model="gemini-2.5-flash")
        response = chat.send_message(full_prompt)
        
        # Add service buttons after AI response
        keyboard = [
            [InlineKeyboardButton("🚀 View Our Services", callback_data='back_to_services')],
            [InlineKeyboardButton("💬 Get Quote", callback_data='capture_lead')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(response.text, reply_markup=reply_markup)
        
    except Exception as e:
        logger.error(f"Error with Gemini API: {e}")
        await update.message.reply_text("I'm experiencing technical difficulties. Please try again or use /start to see our services.")

async def handle_lead_capture_step(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle lead capture conversation flow."""
    user_id = update.message.from_user.id
    message_text = update.message.text
    
    if user_data[user_id]['step'] == 'name':
        user_data[user_id]['name'] = message_text
        user_data[user_id]['step'] = 'contact'
        await update.message.reply_text("**Thanks! Now please share your contact number or email:**", parse_mode='Markdown')
    
    elif user_data[user_id]['step'] == 'contact':
        user_data[user_id]['contact'] = message_text
        user_data[user_id]['step'] = 'service'
        await update.message.reply_text("**What service are you interested in?**\n(e.g., Website, Mobile App, SaaS, etc.)", parse_mode='Markdown')
    
    elif user_data[user_id]['step'] == 'service':
        user_data[user_id]['service'] = message_text
        user_data[user_id]['step'] = 'budget'
        await update.message.reply_text("**What's your approximate budget range?**\n(This helps us provide better recommendations)", parse_mode='Markdown')
    
    elif user_data[user_id]['step'] == 'budget':
        user_data[user_id]['budget'] = message_text
        
        # Show lead summary
        lead_data = user_data[user_id]
        summary = f"""**Perfect! 🎉**

**Your Details:**
• **Name:** {lead_data['name']}
• **Contact:** {lead_data['contact']}
• **Service:** {lead_data['service']}
• **Budget:** {message_text}

Your details have been shared with our team. We'll contact you within 24 hours to discuss your project.

Thank you for choosing Braynix Studios!"""
        
        await update.message.reply_text(summary, parse_mode='Markdown')
        
        # Log the lead
        logger.info(f"New lead: {lead_data}")
        
        # Clear user data
        del user_data[user_id]

def main() -> None:
    """Start the Braynix Studios bot."""
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run the bot
    print("🚀 Braynix Studios Telegram Bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()