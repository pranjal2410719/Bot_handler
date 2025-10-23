import logging
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from telegram.error import TimedOut, NetworkError
from google import genai

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# API Keys
TELEGRAM_BOT_TOKEN = "8454185284:AAEOVgJQas-LVC8IwW_YvsLz1SaCXaxKgvA"
GEMINI_API_KEY = "AIzaSyDoy0XRc85_oI44KPmZdLxwo0B3k3K7PIM"

# Your personal Telegram user ID
ADMIN_CHAT_ID = 6880117839  # @mrdev_Forever001

# Email configuration
EMAIL_ADDRESS = "pistudios.netlify.app@gmail.com"
EMAIL_PASSWORD = "vdgs rzsy nssw sejb"
RECEIVER_EMAIL = "jalka22jan@gmail.com"

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

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors."""
    logger.error(f"Exception while handling an update: {context.error}")
    
    if isinstance(context.error, (TimedOut, NetworkError)):
        logger.warning("Network timeout occurred, continuing...")
        return
    
    if update and hasattr(update, 'effective_message') and update.effective_message:
        try:
            await update.effective_message.reply_text(
                "⚠️ Sorry, I'm experiencing technical difficulties. Please try again in a moment."
            )
        except Exception:
            pass

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

async def services(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show services menu."""
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
    
    await update.message.reply_text(
        "🌟 **Braynix Studios Services**\n\nChoose a service to learn more:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def pricing(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show pricing information."""
    pricing_msg = """💰 **Braynix Studios Pricing**

💻 **Website Development:** ₹8,000 - ₹30,000+
📱 **Mobile Apps:** ₹25,000+ for MVPs
☁️ **SaaS Development:** ₹40,000+
🛒 **E-commerce:** ₹15,000 - ₹50,000+
🚀 **SEO & Marketing:** ₹5,000/month+
📊 **Data Analytics:** Custom pricing

*Prices vary based on complexity and requirements*"""
    
    keyboard = [
        [InlineKeyboardButton("💬 Get Custom Quote", callback_data='capture_lead')],
        [InlineKeyboardButton("🚀 View Services", callback_data='back_to_services')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(pricing_msg, reply_markup=reply_markup, parse_mode='Markdown')

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show about information."""
    about_msg = """🏢 **About Braynix Studios**

We are a next-gen digital agency specializing in creating intelligent, aesthetic, and scalable digital products.

**Our Philosophy:** "Build digital experiences that think, feel, and sell."

**What We Do:**
• Custom website development
• Mobile app creation
• SaaS platform development
• E-commerce solutions
• SEO & digital marketing
• Data analytics & insights

**Why Choose Us:**
✅ Professional team
✅ Modern technologies
✅ Competitive pricing
✅ 24/7 support
✅ On-time delivery"""
    
    keyboard = [
        [InlineKeyboardButton("💬 Get Quote", callback_data='capture_lead')],
        [InlineKeyboardButton("🚀 View Services", callback_data='back_to_services')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(about_msg, reply_markup=reply_markup, parse_mode='Markdown')

async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show contact information."""
    contact_msg = """📞 **Contact Braynix Studios**

**Get in Touch:**
• Use /start to explore services
• Click "Get Quote" for instant consultation
• Chat with our AI assistant anytime

**Direct Contact:**
📱 WhatsApp: +91 8127314770
📧 Email: 2k24.cs1l.2410719@gmail.com

**Response Time:** Within 24 hours
**Support:** 24/7 available

**Ready to start your project?**"""
    
    keyboard = [
        [InlineKeyboardButton("📱 WhatsApp", url='https://wa.me/918127314770')],
        [InlineKeyboardButton("💬 Start Consultation", callback_data='capture_lead')],
        [InlineKeyboardButton("🚀 View Services", callback_data='back_to_services')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(contact_msg, reply_markup=reply_markup, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show help information."""
    help_msg = """🤖 **Braynix Studios Bot Help**

**Available Commands:**
/start - Welcome & services menu
/services - Browse all services
/pricing - View pricing information
/about - Learn about Braynix Studios
/contact - Get contact information
/help - Show this help message

**How to Use:**
1. Browse services with interactive buttons
2. Get instant quotes and consultations
3. Chat with AI for any questions
4. Connect directly with our team

**Need assistance? Just type your question!**"""
    
    keyboard = [
        [InlineKeyboardButton("🚀 View Services", callback_data='back_to_services')],
        [InlineKeyboardButton("💬 Get Quote", callback_data='capture_lead')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(help_msg, reply_markup=reply_markup, parse_mode='Markdown')

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
    elif query.data.startswith('lead_'):
        await handle_service_selection(query)

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
    
    if user_id in user_data:
        await handle_lead_capture_step(update, context)
        return
    
    try:
        system_prompt = """You are Braynix Studios' AI assistant. Focus on our digital services: websites, mobile apps, SaaS, e-commerce, SEO, and analytics. Be professional and encourage users to discuss their project needs."""
        
        full_prompt = f"{system_prompt}\n\nUser: {message_text}"
        chat = client.chats.create(model="gemini-2.5-flash")
        response = chat.send_message(full_prompt)
        
        keyboard = [
            [InlineKeyboardButton("🚀 View Our Services", callback_data='back_to_services')],
            [InlineKeyboardButton("💬 Get Quote", callback_data='capture_lead')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(response.text, reply_markup=reply_markup)
        
    except (TimedOut, NetworkError):
        await update.message.reply_text("⚠️ Connection timeout. Please try again.")
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
        
        keyboard = [
            [InlineKeyboardButton("💻 Website", callback_data='lead_website')],
            [InlineKeyboardButton("📱 Mobile App", callback_data='lead_mobile')],
            [InlineKeyboardButton("☁️ SaaS", callback_data='lead_saas')],
            [InlineKeyboardButton("🛒 E-commerce", callback_data='lead_ecommerce')],
            [InlineKeyboardButton("🚀 SEO/Marketing", callback_data='lead_seo')],
            [InlineKeyboardButton("📊 Analytics", callback_data='lead_analytics')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "**Which service are you interested in?**",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    elif user_data[user_id]['step'] == 'budget':
        user_data[user_id]['budget'] = message_text
        
        await send_lead_notification(user_data[user_id], update.message.from_user)
        
        del user_data[user_id]
        
        keyboard = [
            [InlineKeyboardButton("🚀 View Services", callback_data='back_to_services')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "✅ **Thank you!** Your inquiry has been submitted.\n\nOur team will contact you within 24 hours to discuss your project.",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

async def handle_service_selection(query) -> None:
    """Handle service selection during lead capture."""
    user_id = query.from_user.id
    service = query.data.replace('lead_', '')
    
    service_names = {
        'website': 'Website Development',
        'mobile': 'Mobile App Development', 
        'saas': 'SaaS Development',
        'ecommerce': 'E-commerce Solutions',
        'seo': 'SEO & Digital Marketing',
        'analytics': 'Data Analytics'
    }
    
    user_data[user_id]['service'] = service_names[service]
    user_data[user_id]['step'] = 'budget'
    
    await query.edit_message_text(
        f"**Great choice! {service_names[service]}**\n\nWhat's your approximate budget for this project?",
        parse_mode='Markdown'
    )

async def send_lead_notification(lead_data: dict, user_info) -> None:
    """Send lead notification via Telegram and Email."""
    lead_message = f"""🎯 **NEW LEAD CAPTURED**

👤 **Name:** {lead_data['name']}
📞 **Contact:** {lead_data['contact']}
🎯 **Service:** {lead_data['service']}
💰 **Budget:** {lead_data['budget']}

**User Info:**
• Username: @{user_info.username or 'N/A'}
• User ID: {user_info.id}
• First Name: {user_info.first_name or 'N/A'}"""
    
    try:
        from telegram import Bot
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        await bot.send_message(chat_id=ADMIN_CHAT_ID, text=lead_message, parse_mode='Markdown')
    except Exception as e:
        logger.error(f"Failed to send Telegram notification: {e}")
    
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = f"New Lead: {lead_data['service']} - {lead_data['name']}"
        
        email_body = f"""New lead captured from Braynix Studios Bot:

Name: {lead_data['name']}
Contact: {lead_data['contact']}
Service: {lead_data['service']}
Budget: {lead_data['budget']}

User Details:
Username: @{user_info.username or 'N/A'}
User ID: {user_info.id}
First Name: {user_info.first_name or 'N/A'}

Please follow up within 24 hours."""
        
        msg.attach(MIMEText(email_body, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        
    except Exception as e:
        logger.error(f"Failed to send email notification: {e}")

def main() -> None:
    """Start the bot."""
    application = (
        Application.builder()
        .token(TELEGRAM_BOT_TOKEN)
        .connect_timeout(30)
        .read_timeout(30)
        .write_timeout(30)
        .pool_timeout(30)
        .build()
    )
    
    application.add_error_handler(error_handler)
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("services", services))
    application.add_handler(CommandHandler("pricing", pricing))
    application.add_handler(CommandHandler("about", about))
    application.add_handler(CommandHandler("contact", contact))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Braynix Studios Bot is starting...")
    application.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True,
        timeout=30
    )

if __name__ == '__main__':
    main()