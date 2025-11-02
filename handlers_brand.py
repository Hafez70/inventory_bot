"""Handlers for brand operations."""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import database as db
import messages as msg
import utils

async def brand_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show brand management menu."""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton(msg.BTN_CREATE, callback_data='brand_create')],
        [InlineKeyboardButton(msg.BTN_LIST, callback_data='brand_list')],
        [InlineKeyboardButton(msg.BTN_BACK, callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(msg.BRAND_MENU, reply_markup=reply_markup)

async def brand_create_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start brand creation process."""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    db.set_user_state(user_id, 'brand_create', {})
    
    keyboard = [[InlineKeyboardButton(msg.BTN_CANCEL, callback_data='brand_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(msg.BRAND_NAME_REQUEST, reply_markup=reply_markup)

async def brand_create_handle_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle brand name input."""
    user_id = update.effective_user.id
    state, data = db.get_user_state(user_id)
    
    if state != 'brand_create':
        return
    
    name = update.message.text.strip()
    code = utils.generate_brand_code()
    
    brand_id = db.create_brand(name, code)
    
    if brand_id:
        db.clear_user_state(user_id)
        keyboard = [
            [InlineKeyboardButton(msg.BTN_MAIN_MENU, callback_data='main_menu')],
            [InlineKeyboardButton(msg.BTN_BACK, callback_data='brand_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            msg.BRAND_CREATED.format(name, code),
            reply_markup=reply_markup
        )
    else:
        keyboard = [[InlineKeyboardButton(msg.BTN_CANCEL, callback_data='brand_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            msg.BRAND_CREATE_ERROR,
            reply_markup=reply_markup
        )

async def brand_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show list of all brands."""
    query = update.callback_query
    await query.answer()
    
    brands = db.get_all_brands()
    
    if not brands:
        keyboard = [[InlineKeyboardButton(msg.BTN_BACK, callback_data='brand_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(msg.BRAND_LIST_EMPTY, reply_markup=reply_markup)
        return
    
    # Create keyboard with brand buttons
    keyboard = []
    for brand in brands:
        brand_id, code, name, created_at = brand
        keyboard.append([InlineKeyboardButton(f"{name} ({code})", callback_data=f'brand_view_{brand_id}')])
    
    keyboard.append([InlineKeyboardButton(msg.BTN_BACK, callback_data='brand_menu')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Format brand list
    brand_list_text = "\n".join([f"🔹 {b[2]} ({b[1]})" for b in brands])
    
    await query.edit_message_text(
        msg.BRAND_LIST.format(brand_list_text),
        reply_markup=reply_markup
    )

async def brand_view(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View brand details."""
    query = update.callback_query
    await query.answer()
    
    brand_id = int(query.data.split('_')[2])
    brand = db.get_brand_by_id(brand_id)
    
    if not brand:
        await query.edit_message_text(msg.ERROR_OCCURRED)
        return
    
    b_id, code, name, created_at = brand
    
    keyboard = [
        [InlineKeyboardButton(msg.BTN_EDIT, callback_data=f'brand_edit_{b_id}')],
        [InlineKeyboardButton(msg.BTN_DELETE, callback_data=f'brand_delete_confirm_{b_id}')],
        [InlineKeyboardButton(msg.BTN_BACK, callback_data='brand_list')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        msg.BRAND_DETAILS.format(name, code, created_at),
        reply_markup=reply_markup
    )

async def brand_edit_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start brand edit process."""
    query = update.callback_query
    await query.answer()
    
    brand_id = int(query.data.split('_')[2])
    user_id = query.from_user.id
    
    db.set_user_state(user_id, 'brand_edit', {'brand_id': brand_id})
    
    keyboard = [[InlineKeyboardButton(msg.BTN_CANCEL, callback_data=f'brand_view_{brand_id}')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(msg.BRAND_UPDATE_REQUEST, reply_markup=reply_markup)

async def brand_edit_handle_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle brand name update."""
    user_id = update.effective_user.id
    state, data = db.get_user_state(user_id)
    
    if state != 'brand_edit':
        return
    
    name = update.message.text.strip()
    brand_id = data['brand_id']
    
    db.update_brand(brand_id, name)
    db.clear_user_state(user_id)
    
    keyboard = [
        [InlineKeyboardButton(msg.BTN_VIEW, callback_data=f'brand_view_{brand_id}')],
        [InlineKeyboardButton(msg.BTN_BACK, callback_data='brand_list')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(msg.BRAND_UPDATED, reply_markup=reply_markup)

async def brand_delete_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Confirm brand deletion."""
    query = update.callback_query
    await query.answer()
    
    brand_id = int(query.data.split('_')[3])
    brand = db.get_brand_by_id(brand_id)
    
    if not brand:
        await query.edit_message_text(msg.ERROR_OCCURRED)
        return
    
    keyboard = [
        [InlineKeyboardButton("✅ بله، حذف شود", callback_data=f'brand_delete_{brand_id}')],
        [InlineKeyboardButton(msg.BTN_CANCEL, callback_data=f'brand_view_{brand_id}')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"⚠️ آیا از حذف برند '{brand[2]}' اطمینان دارید؟\n\n"
        "توجه: تمام کالاهای مرتبط نیز حذف خواهند شد.",
        reply_markup=reply_markup
    )

async def brand_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Delete brand."""
    query = update.callback_query
    await query.answer()
    
    brand_id = int(query.data.split('_')[2])
    db.delete_brand(brand_id)
    
    keyboard = [[InlineKeyboardButton(msg.BTN_BACK, callback_data='brand_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(msg.BRAND_DELETED, reply_markup=reply_markup)

