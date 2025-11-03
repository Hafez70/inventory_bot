"""Main Telegram bot file - Warehouse Management Bot."""

import os
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

import database as db
import messages as msg
import handlers_category as cat_handlers
import handlers_subcategory as subcat_handlers
import handlers_brand as brand_handlers
import handlers_measure_type as mt_handlers
import handlers_item as item_handlers
import handlers_low_stock as low_stock_handlers

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token from environment
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
BOT_PASSWORD = os.getenv('BOT_PASSWORD', 'ciFarco@1213#3221')  # Default password

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command - check authentication or show main menu."""
    user_id = update.effective_user.id
    
    # Check if user is already authenticated
    if db.is_user_authenticated(user_id):
        keyboard = [
            [InlineKeyboardButton(msg.BTN_ITEMS, callback_data='item_menu')],
            [InlineKeyboardButton(msg.BTN_LOW_STOCK, callback_data='low_stock_list')],
            [InlineKeyboardButton(msg.BTN_INITIAL_SETTINGS, callback_data='initial_settings_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(msg.MAIN_MENU, reply_markup=reply_markup)
    else:
        # Ask for password
        db.set_user_state(user_id, 'AWAITING_PASSWORD')
        await update.message.reply_text(msg.AUTH_REQUEST)

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show main menu."""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton(msg.BTN_ITEMS, callback_data='item_menu')],
        [InlineKeyboardButton(msg.BTN_LOW_STOCK, callback_data='low_stock_list')],
        [InlineKeyboardButton(msg.BTN_INITIAL_SETTINGS, callback_data='initial_settings_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(msg.MAIN_MENU, reply_markup=reply_markup)

async def initial_settings_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show initial settings submenu."""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton(msg.BTN_CATEGORIES, callback_data='category_menu')],
        [InlineKeyboardButton(msg.BTN_SUBCATEGORIES, callback_data='subcategory_menu')],
        [InlineKeyboardButton(msg.BTN_BRANDS, callback_data='brand_menu')],
        [InlineKeyboardButton(msg.BTN_MEASURE_TYPES, callback_data='measure_type_menu')],
        [InlineKeyboardButton(msg.BTN_MAIN_MENU, callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(msg.INITIAL_SETTINGS_MENU, reply_markup=reply_markup)

async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages based on user state."""
    user_id = update.effective_user.id
    state, data = db.get_user_state(user_id)
    
    # Check for authentication state first
    if state == 'AWAITING_PASSWORD':
        password = update.message.text.strip()
        if password == BOT_PASSWORD:
            # Authenticate user
            user = update.effective_user
            db.authenticate_user(
                user_id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name
            )
            db.clear_user_state(user_id)
            
            # Show success message and main menu
            keyboard = [
                [InlineKeyboardButton(msg.BTN_ITEMS, callback_data='item_menu')],
                [InlineKeyboardButton(msg.BTN_LOW_STOCK, callback_data='low_stock_list')],
                [InlineKeyboardButton(msg.BTN_INITIAL_SETTINGS, callback_data='initial_settings_menu')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(msg.AUTH_SUCCESS)
            await update.message.reply_text(msg.MAIN_MENU, reply_markup=reply_markup)
        else:
            # Wrong password
            await update.message.reply_text(msg.AUTH_FAILED)
            await update.message.reply_text(msg.AUTH_REQUEST)
        return
    
    # Check if user is authenticated for all other operations
    if not db.is_user_authenticated(user_id):
        await update.message.reply_text(msg.AUTH_REQUIRED)
        return
    
    if state == 'category_create':
        await cat_handlers.category_create_handle_name(update, context)
    elif state == 'category_edit':
        await cat_handlers.category_edit_handle_name(update, context)
    elif state == 'subcategory_create':
        await subcat_handlers.subcategory_create_handle_name(update, context)
    elif state == 'subcategory_edit':
        await subcat_handlers.subcategory_edit_handle_name(update, context)
    elif state == 'brand_create':
        await brand_handlers.brand_create_handle_name(update, context)
    elif state == 'brand_edit':
        await brand_handlers.brand_edit_handle_name(update, context)
    elif state == 'measure_type_create':
        await mt_handlers.measure_type_create_handle_name(update, context)
    elif state == 'measure_type_create_threshold':
        await mt_handlers.measure_type_create_handle_threshold(update, context)
    elif state == 'measure_type_edit_name':
        await mt_handlers.measure_type_edit_handle_name(update, context)
    elif state == 'measure_type_edit_threshold':
        await mt_handlers.measure_type_edit_handle_threshold(update, context)
    elif state == 'awaiting_item_search':
        await item_handlers.item_search_handle_text(update, context)
    elif state == 'item_create_name':
        await item_handlers.item_create_handle_name(update, context)
    elif state == 'item_create_custom_code':
        await item_handlers.item_create_handle_custom_code(update, context)
    elif state == 'item_create_description':
        await item_handlers.item_create_handle_description(update, context)
    elif state == 'item_create_available_count':
        await item_handlers.item_create_handle_available_count(update, context)
    elif state == 'item_create_video_url':
        await item_handlers.item_create_handle_video_url(update, context)
    elif state == 'item_edit_name':
        await item_handlers.item_edit_handle_name(update, context)
    elif state == 'item_edit_custom_code':
        await item_handlers.item_edit_handle_custom_code(update, context)
    elif state == 'item_edit_description':
        await item_handlers.item_edit_handle_description(update, context)
    elif state == 'item_edit_available_count':
        await item_handlers.item_edit_handle_available_count(update, context)
    elif state == 'item_edit_video_url':
        await item_handlers.item_edit_handle_video_url(update, context)
    else:
        # Unknown state or no state
        keyboard = [[InlineKeyboardButton(msg.BTN_MAIN_MENU, callback_data='main_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "لطفا از منوی اصلی استفاده کنید:",
            reply_markup=reply_markup
        )

async def handle_photo_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle photo messages based on user state."""
    user_id = update.effective_user.id
    
    # Check if user is authenticated
    if not db.is_user_authenticated(user_id):
        await update.message.reply_text(msg.AUTH_REQUIRED)
        return
    
    state, data = db.get_user_state(user_id)
    
    if state == 'item_create_images':
        await item_handlers.item_create_handle_photo(update, context)
    elif state == 'item_edit_add_images':
        await item_handlers.item_edit_handle_photo(update, context)
    else:
        keyboard = [[InlineKeyboardButton(msg.BTN_MAIN_MENU, callback_data='main_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "لطفا از منوی اصلی استفاده کنید:",
            reply_markup=reply_markup
        )

async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Route callback queries to appropriate handlers."""
    query = update.callback_query
    data = query.data
    user_id = update.effective_user.id
    
    # Check if user is authenticated
    if not db.is_user_authenticated(user_id):
        await query.answer()
        await query.message.reply_text(msg.AUTH_REQUIRED)
        return
    
    # Main menu
    if data == 'main_menu':
        await main_menu(update, context)
    elif data == 'initial_settings_menu':
        await initial_settings_menu(update, context)
    
    # Category handlers
    elif data == 'category_menu':
        await cat_handlers.category_menu(update, context)
    elif data == 'category_create':
        await cat_handlers.category_create_start(update, context)
    elif data == 'category_list':
        await cat_handlers.category_list(update, context)
    elif data.startswith('category_view_'):
        await cat_handlers.category_view(update, context)
    elif data.startswith('category_edit_'):
        await cat_handlers.category_edit_start(update, context)
    elif data.startswith('category_delete_confirm_'):
        await cat_handlers.category_delete_confirm(update, context)
    elif data.startswith('category_delete_'):
        await cat_handlers.category_delete(update, context)
    
    # Subcategory handlers
    elif data == 'subcategory_menu':
        await subcat_handlers.subcategory_menu(update, context)
    elif data == 'subcategory_create':
        await subcat_handlers.subcategory_create_start(update, context)
    elif data.startswith('subcategory_create_cat_'):
        await subcat_handlers.subcategory_create_category_selected(update, context)
    elif data == 'subcategory_list':
        await subcat_handlers.subcategory_list(update, context)
    elif data.startswith('subcategory_view_'):
        await subcat_handlers.subcategory_view(update, context)
    elif data.startswith('subcategory_edit_'):
        await subcat_handlers.subcategory_edit_start(update, context)
    elif data.startswith('subcategory_delete_confirm_'):
        await subcat_handlers.subcategory_delete_confirm(update, context)
    elif data.startswith('subcategory_delete_'):
        await subcat_handlers.subcategory_delete(update, context)
    
    # Brand handlers
    elif data == 'brand_menu':
        await brand_handlers.brand_menu(update, context)
    elif data == 'brand_create':
        await brand_handlers.brand_create_start(update, context)
    elif data == 'brand_list':
        await brand_handlers.brand_list(update, context)
    elif data.startswith('brand_view_'):
        await brand_handlers.brand_view(update, context)
    elif data.startswith('brand_edit_'):
        await brand_handlers.brand_edit_start(update, context)
    elif data.startswith('brand_delete_confirm_'):
        await brand_handlers.brand_delete_confirm(update, context)
    elif data.startswith('brand_delete_'):
        await brand_handlers.brand_delete(update, context)
    
    # Measure Type handlers
    elif data == 'measure_type_menu':
        await mt_handlers.measure_type_menu(update, context)
    elif data == 'measure_type_create':
        await mt_handlers.measure_type_create_start(update, context)
    elif data == 'measure_type_list':
        await mt_handlers.measure_type_list(update, context)
    elif data.startswith('measure_type_view_'):
        await mt_handlers.measure_type_view(update, context)
    elif data.startswith('measure_type_edit_name_'):
        await mt_handlers.measure_type_edit_name_start(update, context)
    elif data.startswith('measure_type_edit_threshold_'):
        await mt_handlers.measure_type_edit_threshold_start(update, context)
    elif data.startswith('measure_type_edit_') and not data.startswith('measure_type_edit_name_') and not data.startswith('measure_type_edit_threshold_'):
        await mt_handlers.measure_type_edit_start(update, context)
    elif data.startswith('measure_type_delete_confirm_'):
        await mt_handlers.measure_type_delete_confirm(update, context)
    elif data.startswith('measure_type_delete_'):
        await mt_handlers.measure_type_delete(update, context)
    
    # Low stock handler
    elif data == 'low_stock_list':
        await low_stock_handlers.low_stock_list(update, context)
    
    # Item handlers
    elif data == 'item_menu':
        await item_handlers.item_menu(update, context)
    elif data == 'item_create':
        await item_handlers.item_create_start(update, context)
    elif data.startswith('item_create_cat_'):
        await item_handlers.item_create_category_selected(update, context)
    elif data.startswith('item_create_subcat_'):
        await item_handlers.item_create_subcategory_selected(update, context)
    elif data.startswith('item_create_brand_'):
        await item_handlers.item_create_brand_selected(update, context)
    elif data.startswith('item_create_measure_type_'):
        await item_handlers.item_create_measure_type_selected(update, context)
    elif data == 'item_create_skip_custom_code':
        await item_handlers.item_create_skip_custom_code(update, context)
    elif data == 'item_create_skip_description':
        await item_handlers.item_create_skip_description(update, context)
    elif data == 'item_create_skip_available_count':
        await item_handlers.item_create_skip_available_count(update, context)
    elif data == 'item_create_skip_video_url':
        await item_handlers.item_create_skip_video_url(update, context)
    elif data.startswith('item_create_done_'):
        await item_handlers.item_create_done(update, context)
    elif data == 'item_list':
        await item_handlers.item_list(update, context)
    elif data == 'item_list_search':
        await item_handlers.item_list_search_start(update, context)
    elif data == 'item_list_by_brand':
        await item_handlers.item_list_by_brand_start(update, context)
    elif data.startswith('item_list_brand_'):
        await item_handlers.item_list_by_brand_show(update, context)
    elif data == 'item_list_by_category':
        await item_handlers.item_list_by_category_start(update, context)
    elif data.startswith('item_list_cat_'):
        await item_handlers.item_list_by_category_show_subcategories(update, context)
    elif data.startswith('item_list_subcat_'):
        await item_handlers.item_list_by_subcategory_show(update, context)
    elif data.startswith('item_view_') and not data.startswith('item_view_images'):
        await item_handlers.item_view(update, context)
    elif data.startswith('item_images_'):
        await item_handlers.item_view_images(update, context)
    elif data.startswith('item_edit_name_'):
        await item_handlers.item_edit_name_start(update, context)
    elif data.startswith('item_edit_custom_code_'):
        await item_handlers.item_edit_custom_code_start(update, context)
    elif data.startswith('item_edit_description_'):
        await item_handlers.item_edit_description_start(update, context)
    elif data.startswith('item_edit_available_count_'):
        await item_handlers.item_edit_available_count_start(update, context)
    elif data.startswith('item_edit_video_url_'):
        await item_handlers.item_edit_video_url_start(update, context)
    elif data.startswith('item_edit_add_image_'):
        await item_handlers.item_edit_add_image_start(update, context)
    elif data.startswith('item_edit_images_done_'):
        await item_handlers.item_edit_images_done(update, context)
    elif data.startswith('item_edit_') and not data.startswith('item_edit_name_') and not data.startswith('item_edit_add_image_') and not data.startswith('item_edit_custom_code_') and not data.startswith('item_edit_description_') and not data.startswith('item_edit_available_count_') and not data.startswith('item_edit_video_url_'):
        await item_handlers.item_edit_start(update, context)
    elif data.startswith('item_delete_confirm_'):
        await item_handlers.item_delete_confirm(update, context)
    elif data.startswith('item_delete_'):
        await item_handlers.item_delete(update, context)
    
    else:
        await query.answer("گزینه نامعتبر!")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors."""
    logger.error(f"Exception while handling an update: {context.error}")
    
    try:
        if update and update.effective_message:
            keyboard = [[InlineKeyboardButton(msg.BTN_MAIN_MENU, callback_data='main_menu')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.effective_message.reply_text(
                msg.ERROR_OCCURRED,
                reply_markup=reply_markup
            )
    except Exception as e:
        logger.error(f"Error in error handler: {e}")

def main():
    """Start the bot."""
    if not BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not found in environment variables!")
        print("❌ خطا: توکن ربات یافت نشد!")
        print("لطفا فایل .env را ایجاد کرده و توکن ربات را در آن قرار دهید.")
        print("\nمثال:")
        print("TELEGRAM_BOT_TOKEN=your_bot_token_here")
        return
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_callback_query))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo_message))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    # Start the bot
    logger.info("Bot started successfully!")
    print("✅ ربات با موفقیت راه‌اندازی شد!")
    print("📱 منتظر دریافت پیام...")
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()

