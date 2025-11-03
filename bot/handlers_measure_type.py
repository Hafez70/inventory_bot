"""Handlers for measure type operations."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import database as db
from bot import messages as msg
from database import utils

async def measure_type_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show measure type management menu."""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton(msg.BTN_CREATE, callback_data='measure_type_create')],
        [InlineKeyboardButton(msg.BTN_LIST, callback_data='measure_type_list')],
        [InlineKeyboardButton(msg.BTN_BACK, callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(msg.MEASURE_TYPE_MENU, reply_markup=reply_markup)

async def measure_type_create_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start measure type creation process."""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    db.set_user_state(user_id, 'measure_type_create', {})
    
    keyboard = [[InlineKeyboardButton(msg.BTN_CANCEL, callback_data='measure_type_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(msg.MEASURE_TYPE_NAME_REQUEST, reply_markup=reply_markup)

async def measure_type_create_handle_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle measure type name input."""
    user_id = update.effective_user.id
    state, data = db.get_user_state(user_id)
    
    if state != 'measure_type_create':
        return
    
    name = update.message.text.strip()
    
    # Save name and ask for threshold
    data['name'] = name
    db.set_user_state(user_id, 'measure_type_create_threshold', data)
    
    keyboard = [[InlineKeyboardButton(msg.BTN_CANCEL, callback_data='measure_type_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        msg.MEASURE_TYPE_THRESHOLD_REQUEST,
        reply_markup=reply_markup
    )

async def measure_type_create_handle_threshold(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle measure type threshold input."""
    user_id = update.effective_user.id
    state, data = db.get_user_state(user_id)
    
    if state != 'measure_type_create_threshold':
        return
    
    try:
        threshold = float(update.message.text.strip())
        if threshold < 0:
            raise ValueError()
    except ValueError:
        keyboard = [[InlineKeyboardButton(msg.BTN_CANCEL, callback_data='measure_type_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "⚠️ لطفا یک عدد معتبر (0 یا بیشتر) وارد کنید:",
            reply_markup=reply_markup
        )
        return
    
    name = data['name']
    code = utils.generate_measure_type_code()
    
    measure_type_id = db.create_measure_type(name, code, threshold)
    
    if measure_type_id:
        db.clear_user_state(user_id)
        keyboard = [
            [InlineKeyboardButton(msg.BTN_MAIN_MENU, callback_data='main_menu')],
            [InlineKeyboardButton(msg.BTN_BACK, callback_data='measure_type_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            msg.MEASURE_TYPE_CREATED.format(name, code, threshold),
            reply_markup=reply_markup
        )
    else:
        keyboard = [[InlineKeyboardButton(msg.BTN_CANCEL, callback_data='measure_type_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            msg.MEASURE_TYPE_CREATE_ERROR,
            reply_markup=reply_markup
        )

async def measure_type_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show list of all measure types."""
    query = update.callback_query
    await query.answer()
    
    measure_types = db.get_all_measure_types()
    
    if not measure_types:
        keyboard = [[InlineKeyboardButton(msg.BTN_BACK, callback_data='measure_type_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(msg.MEASURE_TYPE_LIST_EMPTY, reply_markup=reply_markup)
        return
    
    # Create keyboard with measure type buttons
    keyboard = []
    for mt in measure_types:
        mt_id, code, name, threshold, created_at = mt
        keyboard.append([InlineKeyboardButton(
            f"{name} ({code}) - آستانه: {threshold}",
            callback_data=f'measure_type_view_{mt_id}'
        )])
    
    keyboard.append([InlineKeyboardButton(msg.BTN_BACK, callback_data='measure_type_menu')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Format measure type list
    mt_list = "\n".join([f"🔹 {mt[2]} ({mt[1]}) - آستانه کمبود: {mt[3]}" for mt in measure_types])
    
    await query.edit_message_text(
        msg.MEASURE_TYPE_LIST.format(mt_list),
        reply_markup=reply_markup
    )

async def measure_type_view(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View measure type details."""
    query = update.callback_query
    await query.answer()
    
    mt_id = int(query.data.split('_')[3])
    mt = db.get_measure_type_by_id(mt_id)
    
    if not mt:
        await query.edit_message_text(msg.ERROR_OCCURRED)
        return
    
    mt_id, code, name, threshold, created_at = mt
    
    keyboard = [
        [InlineKeyboardButton(msg.BTN_EDIT, callback_data=f'measure_type_edit_{mt_id}')],
        [InlineKeyboardButton(msg.BTN_DELETE, callback_data=f'measure_type_delete_confirm_{mt_id}')],
        [InlineKeyboardButton(msg.BTN_BACK, callback_data='measure_type_list')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        msg.MEASURE_TYPE_DETAILS.format(name, code, threshold, created_at),
        reply_markup=reply_markup
    )

async def measure_type_edit_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start measure type edit process."""
    query = update.callback_query
    await query.answer()
    
    mt_id = int(query.data.split('_')[3])
    
    keyboard = [
        [InlineKeyboardButton("✏️ ویرایش نام", callback_data=f'measure_type_edit_name_{mt_id}')],
        [InlineKeyboardButton("🔢 ویرایش آستانه", callback_data=f'measure_type_edit_threshold_{mt_id}')],
        [InlineKeyboardButton(msg.BTN_BACK, callback_data=f'measure_type_view_{mt_id}')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "لطفا فیلد مورد نظر برای ویرایش را انتخاب کنید:",
        reply_markup=reply_markup
    )

async def measure_type_edit_name_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start editing measure type name."""
    query = update.callback_query
    await query.answer()
    
    mt_id = int(query.data.split('_')[4])
    user_id = query.from_user.id
    
    db.set_user_state(user_id, 'measure_type_edit_name', {'mt_id': mt_id})
    
    keyboard = [[InlineKeyboardButton(msg.BTN_CANCEL, callback_data=f'measure_type_view_{mt_id}')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text("لطفا نام جدید واحد اندازه‌گیری را وارد کنید:", reply_markup=reply_markup)

async def measure_type_edit_handle_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle measure type name update."""
    user_id = update.effective_user.id
    state, data = db.get_user_state(user_id)
    
    if state != 'measure_type_edit_name':
        return
    
    name = update.message.text.strip()
    mt_id = data['mt_id']
    
    # Get current data
    mt = db.get_measure_type_by_id(mt_id)
    if mt:
        db.update_measure_type(mt_id, name, mt[3])
        db.clear_user_state(user_id)
        
        keyboard = [
            [InlineKeyboardButton(msg.BTN_VIEW, callback_data=f'measure_type_view_{mt_id}')],
            [InlineKeyboardButton(msg.BTN_BACK, callback_data='measure_type_list')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(msg.MEASURE_TYPE_UPDATED, reply_markup=reply_markup)

async def measure_type_edit_threshold_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start editing measure type threshold."""
    query = update.callback_query
    await query.answer()
    
    mt_id = int(query.data.split('_')[4])
    user_id = query.from_user.id
    
    db.set_user_state(user_id, 'measure_type_edit_threshold', {'mt_id': mt_id})
    
    keyboard = [[InlineKeyboardButton(msg.BTN_CANCEL, callback_data=f'measure_type_view_{mt_id}')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "لطفا آستانه کمبود موجودی جدید را وارد کنید:",
        reply_markup=reply_markup
    )

async def measure_type_edit_handle_threshold(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle measure type threshold update."""
    user_id = update.effective_user.id
    state, data = db.get_user_state(user_id)
    
    if state != 'measure_type_edit_threshold':
        return
    
    try:
        threshold = float(update.message.text.strip())
        if threshold < 0:
            raise ValueError()
    except ValueError:
        keyboard = [[InlineKeyboardButton(msg.BTN_CANCEL, callback_data='measure_type_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "⚠️ لطفا یک عدد معتبر (0 یا بیشتر) وارد کنید:",
            reply_markup=reply_markup
        )
        return
    
    mt_id = data['mt_id']
    
    # Get current data
    mt = db.get_measure_type_by_id(mt_id)
    if mt:
        db.update_measure_type(mt_id, mt[2], threshold)
        db.clear_user_state(user_id)
        
        keyboard = [
            [InlineKeyboardButton(msg.BTN_VIEW, callback_data=f'measure_type_view_{mt_id}')],
            [InlineKeyboardButton(msg.BTN_BACK, callback_data='measure_type_list')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(msg.MEASURE_TYPE_UPDATED, reply_markup=reply_markup)

async def measure_type_delete_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Confirm measure type deletion."""
    query = update.callback_query
    await query.answer()
    
    mt_id = int(query.data.split('_')[4])
    mt = db.get_measure_type_by_id(mt_id)
    
    if not mt:
        await query.edit_message_text(msg.ERROR_OCCURRED)
        return
    
    keyboard = [
        [InlineKeyboardButton("✅ بله، حذف شود", callback_data=f'measure_type_delete_{mt_id}')],
        [InlineKeyboardButton(msg.BTN_CANCEL, callback_data=f'measure_type_view_{mt_id}')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"⚠️ آیا از حذف واحد اندازه‌گیری '{mt[2]}' اطمینان دارید؟\n\n"
        "توجه: تمام کالاهای مرتبط نیز حذف خواهند شد.",
        reply_markup=reply_markup
    )

async def measure_type_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Delete measure type."""
    query = update.callback_query
    await query.answer()
    
    mt_id = int(query.data.split('_')[3])
    db.delete_measure_type(mt_id)
    
    keyboard = [[InlineKeyboardButton(msg.BTN_BACK, callback_data='measure_type_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(msg.MEASURE_TYPE_DELETED, reply_markup=reply_markup)

