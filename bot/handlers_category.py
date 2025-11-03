"""Handlers for category operations."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from database import database as db
from bot import messages as msg
from database import utils

# Conversation states
CATEGORY_NAME = 1

async def category_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show category management menu."""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton(msg.BTN_CREATE, callback_data='category_create')],
        [InlineKeyboardButton(msg.BTN_LIST, callback_data='category_list')],
        [InlineKeyboardButton(msg.BTN_BACK, callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(msg.CATEGORY_MENU, reply_markup=reply_markup)

async def category_create_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start category creation process."""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    db.set_user_state(user_id, 'category_create', {})
    
    keyboard = [[InlineKeyboardButton(msg.BTN_CANCEL, callback_data='category_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(msg.CATEGORY_NAME_REQUEST, reply_markup=reply_markup)

async def category_create_handle_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle category name input."""
    user_id = update.effective_user.id
    state, data = db.get_user_state(user_id)
    
    if state != 'category_create':
        return
    
    name = update.message.text.strip()
    code = utils.generate_category_code()
    
    category_id = db.create_category(name, code)
    
    if category_id:
        db.clear_user_state(user_id)
        keyboard = [
            [InlineKeyboardButton(msg.BTN_MAIN_MENU, callback_data='main_menu')],
            [InlineKeyboardButton(msg.BTN_BACK, callback_data='category_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            msg.CATEGORY_CREATED.format(name, code),
            reply_markup=reply_markup
        )
    else:
        keyboard = [[InlineKeyboardButton(msg.BTN_CANCEL, callback_data='category_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            msg.CATEGORY_CREATE_ERROR,
            reply_markup=reply_markup
        )

async def category_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show list of all categories."""
    query = update.callback_query
    await query.answer()
    
    categories = db.get_all_categories()
    
    if not categories:
        keyboard = [[InlineKeyboardButton(msg.BTN_BACK, callback_data='category_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(msg.CATEGORY_LIST_EMPTY, reply_markup=reply_markup)
        return
    
    # Create keyboard with category buttons
    keyboard = []
    for cat in categories:
        cat_id, code, name, created_at = cat
        keyboard.append([InlineKeyboardButton(f"{name} ({code})", callback_data=f'category_view_{cat_id}')])
    
    keyboard.append([InlineKeyboardButton(msg.BTN_BACK, callback_data='category_menu')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Format category list
    cat_list = "\n".join([f"🔹 {cat[2]} ({cat[1]})" for cat in categories])
    
    await query.edit_message_text(
        msg.CATEGORY_LIST.format(cat_list),
        reply_markup=reply_markup
    )

async def category_view(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View category details."""
    query = update.callback_query
    await query.answer()
    
    category_id = int(query.data.split('_')[2])
    category = db.get_category_by_id(category_id)
    
    if not category:
        await query.edit_message_text(msg.ERROR_OCCURRED)
        return
    
    cat_id, code, name, created_at = category
    
    keyboard = [
        [InlineKeyboardButton(msg.BTN_EDIT, callback_data=f'category_edit_{cat_id}')],
        [InlineKeyboardButton(msg.BTN_DELETE, callback_data=f'category_delete_confirm_{cat_id}')],
        [InlineKeyboardButton(msg.BTN_BACK, callback_data='category_list')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        msg.CATEGORY_DETAILS.format(name, code, created_at),
        reply_markup=reply_markup
    )

async def category_edit_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start category edit process."""
    query = update.callback_query
    await query.answer()
    
    category_id = int(query.data.split('_')[2])
    user_id = query.from_user.id
    
    db.set_user_state(user_id, 'category_edit', {'category_id': category_id})
    
    keyboard = [[InlineKeyboardButton(msg.BTN_CANCEL, callback_data=f'category_view_{category_id}')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(msg.CATEGORY_UPDATE_REQUEST, reply_markup=reply_markup)

async def category_edit_handle_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle category name update."""
    user_id = update.effective_user.id
    state, data = db.get_user_state(user_id)
    
    if state != 'category_edit':
        return
    
    name = update.message.text.strip()
    category_id = data['category_id']
    
    db.update_category(category_id, name)
    db.clear_user_state(user_id)
    
    keyboard = [
        [InlineKeyboardButton(msg.BTN_VIEW, callback_data=f'category_view_{category_id}')],
        [InlineKeyboardButton(msg.BTN_BACK, callback_data='category_list')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(msg.CATEGORY_UPDATED, reply_markup=reply_markup)

async def category_delete_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Confirm category deletion."""
    query = update.callback_query
    await query.answer()
    
    category_id = int(query.data.split('_')[3])
    category = db.get_category_by_id(category_id)
    
    if not category:
        await query.edit_message_text(msg.ERROR_OCCURRED)
        return
    
    keyboard = [
        [InlineKeyboardButton("✅ بله، حذف شود", callback_data=f'category_delete_{category_id}')],
        [InlineKeyboardButton(msg.BTN_CANCEL, callback_data=f'category_view_{category_id}')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"⚠️ آیا از حذف دسته‌بندی '{category[2]}' اطمینان دارید؟\n\n"
        "توجه: تمام زیردسته‌ها و کالاهای مرتبط نیز حذف خواهند شد.",
        reply_markup=reply_markup
    )

async def category_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Delete category."""
    query = update.callback_query
    await query.answer()
    
    category_id = int(query.data.split('_')[2])
    db.delete_category(category_id)
    
    keyboard = [[InlineKeyboardButton(msg.BTN_BACK, callback_data='category_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(msg.CATEGORY_DELETED, reply_markup=reply_markup)

