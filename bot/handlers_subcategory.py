"""Handlers for subcategory operations."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import database as db
from bot import messages as msg
from database import utils

async def subcategory_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show subcategory management menu."""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton(msg.BTN_CREATE, callback_data='subcategory_create')],
        [InlineKeyboardButton(msg.BTN_LIST, callback_data='subcategory_list')],
        [InlineKeyboardButton(msg.BTN_BACK, callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(msg.SUBCATEGORY_MENU, reply_markup=reply_markup)

async def subcategory_create_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start subcategory creation process - first select category."""
    query = update.callback_query
    await query.answer()
    
    categories = db.get_all_categories()
    
    if not categories:
        keyboard = [[InlineKeyboardButton(msg.BTN_BACK, callback_data='subcategory_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "❌ ابتدا باید حداقل یک دسته‌بندی ثبت کنید.",
            reply_markup=reply_markup
        )
        return
    
    # Create keyboard with category buttons
    keyboard = []
    for cat in categories:
        cat_id, code, name, created_at = cat
        keyboard.append([InlineKeyboardButton(f"{name} ({code})", callback_data=f'subcategory_create_cat_{cat_id}')])
    
    keyboard.append([InlineKeyboardButton(msg.BTN_CANCEL, callback_data='subcategory_menu')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(msg.SUBCATEGORY_SELECT_CATEGORY, reply_markup=reply_markup)

async def subcategory_create_category_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle category selection for subcategory creation."""
    query = update.callback_query
    await query.answer()
    
    category_id = int(query.data.split('_')[3])
    user_id = query.from_user.id
    
    db.set_user_state(user_id, 'subcategory_create', {'category_id': category_id})
    
    keyboard = [[InlineKeyboardButton(msg.BTN_CANCEL, callback_data='subcategory_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(msg.SUBCATEGORY_NAME_REQUEST, reply_markup=reply_markup)

async def subcategory_create_handle_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle subcategory name input."""
    user_id = update.effective_user.id
    state, data = db.get_user_state(user_id)
    
    if state != 'subcategory_create':
        return
    
    name = update.message.text.strip()
    category_id = data['category_id']
    code = utils.generate_subcategory_code()
    
    subcategory_id = db.create_subcategory(name, code, category_id)
    
    if subcategory_id:
        db.clear_user_state(user_id)
        keyboard = [
            [InlineKeyboardButton(msg.BTN_MAIN_MENU, callback_data='main_menu')],
            [InlineKeyboardButton(msg.BTN_BACK, callback_data='subcategory_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            msg.SUBCATEGORY_CREATED.format(name, code),
            reply_markup=reply_markup
        )
    else:
        keyboard = [[InlineKeyboardButton(msg.BTN_CANCEL, callback_data='subcategory_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            msg.SUBCATEGORY_CREATE_ERROR,
            reply_markup=reply_markup
        )

async def subcategory_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show list of all subcategories."""
    query = update.callback_query
    await query.answer()
    
    subcategories = db.get_all_subcategories()
    
    if not subcategories:
        keyboard = [[InlineKeyboardButton(msg.BTN_BACK, callback_data='subcategory_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(msg.SUBCATEGORY_LIST_EMPTY, reply_markup=reply_markup)
        return
    
    # Create keyboard with subcategory buttons
    keyboard = []
    for subcat in subcategories:
        subcat_id, code, name, category_id, category_name, created_at = subcat
        keyboard.append([InlineKeyboardButton(
            f"{name} ({code}) - {category_name}",
            callback_data=f'subcategory_view_{subcat_id}'
        )])
    
    keyboard.append([InlineKeyboardButton(msg.BTN_BACK, callback_data='subcategory_menu')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Format subcategory list
    subcat_list = "\n".join([f"🔹 {sub[2]} ({sub[1]}) - {sub[4]}" for sub in subcategories])
    
    await query.edit_message_text(
        msg.SUBCATEGORY_LIST.format(subcat_list),
        reply_markup=reply_markup
    )

async def subcategory_view(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View subcategory details."""
    query = update.callback_query
    await query.answer()
    
    subcategory_id = int(query.data.split('_')[2])
    subcategory = db.get_subcategory_by_id(subcategory_id)
    
    if not subcategory:
        await query.edit_message_text(msg.ERROR_OCCURRED)
        return
    
    subcat_id, code, name, category_id, category_name, created_at = subcategory
    
    keyboard = [
        [InlineKeyboardButton(msg.BTN_EDIT, callback_data=f'subcategory_edit_{subcat_id}')],
        [InlineKeyboardButton(msg.BTN_DELETE, callback_data=f'subcategory_delete_confirm_{subcat_id}')],
        [InlineKeyboardButton(msg.BTN_BACK, callback_data='subcategory_list')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        msg.SUBCATEGORY_DETAILS.format(name, code, category_name, created_at),
        reply_markup=reply_markup
    )

async def subcategory_edit_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start subcategory edit process."""
    query = update.callback_query
    await query.answer()
    
    subcategory_id = int(query.data.split('_')[2])
    user_id = query.from_user.id
    
    db.set_user_state(user_id, 'subcategory_edit', {'subcategory_id': subcategory_id})
    
    keyboard = [[InlineKeyboardButton(msg.BTN_CANCEL, callback_data=f'subcategory_view_{subcategory_id}')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(msg.SUBCATEGORY_UPDATE_REQUEST, reply_markup=reply_markup)

async def subcategory_edit_handle_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle subcategory name update."""
    user_id = update.effective_user.id
    state, data = db.get_user_state(user_id)
    
    if state != 'subcategory_edit':
        return
    
    name = update.message.text.strip()
    subcategory_id = data['subcategory_id']
    
    db.update_subcategory(subcategory_id, name)
    db.clear_user_state(user_id)
    
    keyboard = [
        [InlineKeyboardButton(msg.BTN_VIEW, callback_data=f'subcategory_view_{subcategory_id}')],
        [InlineKeyboardButton(msg.BTN_BACK, callback_data='subcategory_list')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(msg.SUBCATEGORY_UPDATED, reply_markup=reply_markup)

async def subcategory_delete_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Confirm subcategory deletion."""
    query = update.callback_query
    await query.answer()
    
    subcategory_id = int(query.data.split('_')[3])
    subcategory = db.get_subcategory_by_id(subcategory_id)
    
    if not subcategory:
        await query.edit_message_text(msg.ERROR_OCCURRED)
        return
    
    keyboard = [
        [InlineKeyboardButton("✅ بله، حذف شود", callback_data=f'subcategory_delete_{subcategory_id}')],
        [InlineKeyboardButton(msg.BTN_CANCEL, callback_data=f'subcategory_view_{subcategory_id}')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"⚠️ آیا از حذف زیردسته '{subcategory[2]}' اطمینان دارید؟\n\n"
        "توجه: تمام کالاهای مرتبط نیز حذف خواهند شد.",
        reply_markup=reply_markup
    )

async def subcategory_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Delete subcategory."""
    query = update.callback_query
    await query.answer()
    
    subcategory_id = int(query.data.split('_')[2])
    db.delete_subcategory(subcategory_id)
    
    keyboard = [[InlineKeyboardButton(msg.BTN_BACK, callback_data='subcategory_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(msg.SUBCATEGORY_DELETED, reply_markup=reply_markup)

