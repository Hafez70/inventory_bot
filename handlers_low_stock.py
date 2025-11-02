"""Handler for low stock/lack of inventory operations."""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import database as db
import messages as msg

async def low_stock_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show list of low stock items."""
    query = update.callback_query
    await query.answer()
    
    low_stock_items = db.get_low_stock_items()
    
    if not low_stock_items:
        keyboard = [[InlineKeyboardButton(msg.BTN_MAIN_MENU, callback_data='main_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(msg.LOW_STOCK_LIST_EMPTY, reply_markup=reply_markup)
        return
    
    # Create keyboard with item buttons
    keyboard = []
    message_text = msg.LOW_STOCK_MENU + "\n\n"
    
    for item in low_stock_items:
        item_id, code, custom_code, name, available_count, cat_name, subcat_name, brand_name, measure_type_name, threshold = item
        
        item_text = msg.LOW_STOCK_ITEM.format(
            name,
            code,
            custom_code,
            available_count,
            measure_type_name,
            threshold,
            cat_name,
            subcat_name,
            brand_name
        )
        message_text += item_text + "\n\n"
        
        keyboard.append([InlineKeyboardButton(
            f"{name} ({custom_code}) - {available_count} {measure_type_name}",
            callback_data=f'item_view_{item_id}'
        )])
    
    keyboard.append([InlineKeyboardButton(msg.BTN_MAIN_MENU, callback_data='main_menu')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Split message if too long (Telegram limit is 4096 characters)
    if len(message_text) > 4000:
        message_text = message_text[:4000] + "\n\n... (لیست طولانی است)"
    
    await query.edit_message_text(message_text, reply_markup=reply_markup)

