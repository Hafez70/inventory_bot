"""Handlers for item operations with inventory management and new fields."""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import database as db
import messages as msg
import utils
import os

async def item_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show item management menu."""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton(msg.BTN_CREATE, callback_data='item_create')],
        [InlineKeyboardButton(msg.BTN_LIST, callback_data='item_list')],
        [InlineKeyboardButton(msg.BTN_BACK, callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(msg.ITEM_MENU, reply_markup=reply_markup)

# ============================================================================
# ITEM CREATION FLOW (Required + Optional fields)
# ============================================================================

async def item_create_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start item creation - first select category (REQUIRED)."""
    query = update.callback_query
    await query.answer()
    
    categories = db.get_all_categories()
    
    if not categories:
        keyboard = [[InlineKeyboardButton(msg.BTN_BACK, callback_data='item_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "❌ ابتدا باید حداقل یک دسته‌بندی ثبت کنید.",
            reply_markup=reply_markup
        )
        return
    
    keyboard = []
    for cat in categories:
        cat_id, code, name, created_at = cat
        keyboard.append([InlineKeyboardButton(f"{name} ({code})", callback_data=f'item_create_cat_{cat_id}')])
    
    keyboard.append([InlineKeyboardButton(msg.BTN_CANCEL, callback_data='item_menu')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(msg.ITEM_SELECT_CATEGORY, reply_markup=reply_markup)

async def item_create_category_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle category selection - show subcategories (REQUIRED)."""
    query = update.callback_query
    await query.answer()
    
    category_id = int(query.data.split('_')[3])
    subcategories = db.get_subcategories_by_category(category_id)
    
    if not subcategories:
        keyboard = [[InlineKeyboardButton(msg.BTN_BACK, callback_data='item_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            f"❌ این دسته‌بندی زیردسته ندارد. لطفا ابتدا زیردسته ثبت کنید.",
            reply_markup=reply_markup
        )
        return
    
    keyboard = []
    for subcat in subcategories:
        subcat_id, code, name, created_at = subcat
        keyboard.append([InlineKeyboardButton(
            f"{name} ({code})",
            callback_data=f'item_create_subcat_{category_id}_{subcat_id}'
        )])
    
    keyboard.append([InlineKeyboardButton(msg.BTN_CANCEL, callback_data='item_menu')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(msg.ITEM_SELECT_SUBCATEGORY, reply_markup=reply_markup)

async def item_create_subcategory_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle subcategory selection - show brands (REQUIRED)."""
    query = update.callback_query
    await query.answer()
    
    parts = query.data.split('_')
    category_id = int(parts[3])
    subcategory_id = int(parts[4])
    
    brands = db.get_all_brands()
    
    if not brands:
        keyboard = [[InlineKeyboardButton(msg.BTN_BACK, callback_data='item_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "❌ ابتدا باید حداقل یک برند ثبت کنید.",
            reply_markup=reply_markup
        )
        return
    
    keyboard = []
    for brand in brands:
        brand_id, code, name, created_at = brand
        keyboard.append([InlineKeyboardButton(
            f"{name} ({code})",
            callback_data=f'item_create_brand_{category_id}_{subcategory_id}_{brand_id}'
        )])
    
    keyboard.append([InlineKeyboardButton(msg.BTN_CANCEL, callback_data='item_menu')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(msg.ITEM_SELECT_BRAND, reply_markup=reply_markup)

async def item_create_brand_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle brand selection - show measure types (REQUIRED)."""
    query = update.callback_query
    await query.answer()
    
    parts = query.data.split('_')
    category_id = int(parts[3])
    subcategory_id = int(parts[4])
    brand_id = int(parts[5])
    
    measure_types = db.get_all_measure_types()
    
    if not measure_types:
        keyboard = [[InlineKeyboardButton(msg.BTN_BACK, callback_data='item_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "❌ ابتدا باید حداقل یک واحد اندازه‌گیری ثبت کنید.",
            reply_markup=reply_markup
        )
        return
    
    keyboard = []
    for mt in measure_types:
        mt_id, code, name, threshold, created_at = mt
        keyboard.append([InlineKeyboardButton(
            f"{name} ({code})",
            callback_data=f'item_create_measure_type_{category_id}_{subcategory_id}_{brand_id}_{mt_id}'
        )])
    
    keyboard.append([InlineKeyboardButton(msg.BTN_CANCEL, callback_data='item_menu')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(msg.ITEM_SELECT_MEASURE_TYPE, reply_markup=reply_markup)

async def item_create_measure_type_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle measure type selection - ask for name (REQUIRED)."""
    query = update.callback_query
    await query.answer()
    
    parts = query.data.split('_')
    category_id = int(parts[4])
    subcategory_id = int(parts[5])
    brand_id = int(parts[6])
    measure_type_id = int(parts[7])
    
    user_id = query.from_user.id
    db.set_user_state(user_id, 'item_create_name', {
        'category_id': category_id,
        'subcategory_id': subcategory_id,
        'brand_id': brand_id,
        'measure_type_id': measure_type_id
    })
    
    keyboard = [[InlineKeyboardButton(msg.BTN_CANCEL, callback_data='item_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(msg.ITEM_NAME_REQUEST, reply_markup=reply_markup)

async def item_create_handle_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle item name input - ask for custom code (REQUIRED)."""
    user_id = update.effective_user.id
    state, data = db.get_user_state(user_id)
    
    if state != 'item_create_name':
        return
    
    name = update.message.text.strip()
    data['name'] = name
    db.set_user_state(user_id, 'item_create_custom_code', data)
    
    keyboard = [[InlineKeyboardButton(msg.BTN_CANCEL, callback_data='item_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        msg.ITEM_CUSTOM_CODE_REQUEST,
        reply_markup=reply_markup
    )

async def item_create_handle_custom_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle custom code input - ask for description (OPTIONAL)."""
    user_id = update.effective_user.id
    state, data = db.get_user_state(user_id)
    
    if state != 'item_create_custom_code':
        return
    
    custom_code = update.message.text.strip()
    data['custom_code'] = custom_code
    db.set_user_state(user_id, 'item_create_description', data)
    
    keyboard = [[InlineKeyboardButton(msg.BTN_SKIP, callback_data='item_create_skip_description')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        msg.ITEM_DESCRIPTION_REQUEST,
        reply_markup=reply_markup
    )

async def item_create_handle_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle description input - ask for available count (OPTIONAL)."""
    user_id = update.effective_user.id
    state, data = db.get_user_state(user_id)
    
    if state != 'item_create_description':
        return
    
    description = update.message.text.strip()
    data['description'] = description
    db.set_user_state(user_id, 'item_create_available_count', data)
    
    keyboard = [[InlineKeyboardButton(msg.BTN_SKIP, callback_data='item_create_skip_available_count')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        msg.ITEM_AVAILABLE_COUNT_REQUEST,
        reply_markup=reply_markup
    )

async def item_create_skip_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Skip description - ask for available count (OPTIONAL)."""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    state, data = db.get_user_state(user_id)
    
    if state == 'item_create_description':
        data['description'] = None
        db.set_user_state(user_id, 'item_create_available_count', data)
        
        keyboard = [[InlineKeyboardButton(msg.BTN_SKIP, callback_data='item_create_skip_available_count')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            msg.ITEM_AVAILABLE_COUNT_REQUEST,
            reply_markup=reply_markup
        )

async def item_create_handle_available_count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle available count input - ask for video URL (OPTIONAL)."""
    user_id = update.effective_user.id
    state, data = db.get_user_state(user_id)
    
    if state != 'item_create_available_count':
        return
    
    try:
        available_count = float(update.message.text.strip())
        if available_count < 0:
            raise ValueError()
    except ValueError:
        keyboard = [[InlineKeyboardButton(msg.BTN_SKIP, callback_data='item_create_skip_available_count')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "⚠️ لطفا یک عدد معتبر (0 یا بیشتر) وارد کنید:",
            reply_markup=reply_markup
        )
        return
    
    data['available_count'] = available_count
    db.set_user_state(user_id, 'item_create_video_url', data)
    
    keyboard = [[InlineKeyboardButton(msg.BTN_SKIP, callback_data='item_create_skip_video_url')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        msg.ITEM_VIDEO_URL_REQUEST,
        reply_markup=reply_markup
    )

async def item_create_skip_available_count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Skip available count - ask for video URL (OPTIONAL)."""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    state, data = db.get_user_state(user_id)
    
    if state == 'item_create_available_count':
        data['available_count'] = 0
        db.set_user_state(user_id, 'item_create_video_url', data)
        
        keyboard = [[InlineKeyboardButton(msg.BTN_SKIP, callback_data='item_create_skip_video_url')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            msg.ITEM_VIDEO_URL_REQUEST,
            reply_markup=reply_markup
        )

async def item_create_handle_video_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle video URL input - create item and ask for images (OPTIONAL)."""
    user_id = update.effective_user.id
    state, data = db.get_user_state(user_id)
    
    if state != 'item_create_video_url':
        return
    
    video_url = update.message.text.strip()
    data['video_url'] = video_url
    
    await _create_item_and_request_images(update, context, user_id, data)

async def item_create_skip_video_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Skip video URL - create item and ask for images (OPTIONAL)."""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    state, data = db.get_user_state(user_id)
    
    if state == 'item_create_video_url':
        data['video_url'] = None
        await _create_item_and_request_images(query, context, user_id, data)

async def _create_item_and_request_images(update_or_query, context, user_id, data):
    """Helper to create item and request images."""
    code = utils.generate_item_code()
    
    # Create item with all data
    item_id = db.create_item(
        name=data['name'],
        code=code,
        custom_code=data['custom_code'],
        category_id=data['category_id'],
        subcategory_id=data['subcategory_id'],
        brand_id=data['brand_id'],
        measure_type_id=data['measure_type_id'],
        description=data.get('description'),
        available_count=data.get('available_count', 0),
        video_url=data.get('video_url')
    )
    
    if item_id:
        db.set_user_state(user_id, 'item_create_images', {
            'item_id': item_id,
            'item_name': data['name'],
            'item_code': code,
            'custom_code': data['custom_code'],
            'image_count': 0
        })
        
        keyboard = [
            [InlineKeyboardButton(msg.BTN_DONE, callback_data=f'item_create_done_{item_id}')],
            [InlineKeyboardButton(msg.BTN_CANCEL, callback_data='item_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        message_text = msg.ITEM_IMAGE_REQUEST
        
        if hasattr(update_or_query, 'message'):
            await update_or_query.message.reply_text(message_text, reply_markup=reply_markup)
        else:
            await update_or_query.edit_message_text(message_text, reply_markup=reply_markup)
    else:
        keyboard = [[InlineKeyboardButton(msg.BTN_CANCEL, callback_data='item_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if hasattr(update_or_query, 'message'):
            await update_or_query.message.reply_text(msg.ITEM_CREATE_ERROR, reply_markup=reply_markup)
        else:
            await update_or_query.edit_message_text(msg.ITEM_CREATE_ERROR, reply_markup=reply_markup)

async def item_create_handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle photo upload during creation."""
    user_id = update.effective_user.id
    state, data = db.get_user_state(user_id)
    
    if state != 'item_create_images':
        return
    
    item_id = data['item_id']
    image_count = data['image_count']
    
    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    
    filename = f"item_{item_id}_{image_count + 1}.jpg"
    filepath = os.path.join('images', filename)
    
    await file.download_to_drive(filepath)
    db.add_item_image(item_id, filepath)
    
    data['image_count'] = image_count + 1
    db.set_user_state(user_id, 'item_create_images', data)
    
    keyboard = [
        [InlineKeyboardButton(msg.BTN_DONE, callback_data=f'item_create_done_{item_id}')],
        [InlineKeyboardButton(msg.BTN_CANCEL, callback_data='item_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        msg.ITEM_IMAGE_UPLOADED.format(data['image_count']),
        reply_markup=reply_markup
    )

async def item_create_done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Finish item creation."""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    state, data = db.get_user_state(user_id)
    
    if state == 'item_create_images':
        db.clear_user_state(user_id)
        
        keyboard = [
            [InlineKeyboardButton(msg.BTN_VIEW, callback_data=f'item_view_{data["item_id"]}')],
            [InlineKeyboardButton(msg.BTN_BACK, callback_data='item_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            msg.ITEM_CREATED.format(data['item_name'], data['item_code'], data['custom_code']),
            reply_markup=reply_markup
        )

# ============================================================================
# ITEM LIST & VIEW
# ============================================================================

async def item_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show list of all items."""
    query = update.callback_query
    await query.answer()
    
    items = db.get_all_items()
    
    if not items:
        keyboard = [[InlineKeyboardButton(msg.BTN_BACK, callback_data='item_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(msg.ITEM_LIST_EMPTY, reply_markup=reply_markup)
        return
    
    keyboard = []
    for item in items[:20]:
        item_id, code, custom_code, name, description, cat_name, subcat_name, brand_name, measure_type_name, available_count, video_url, created_at, updated_at = item
        display_text = f"{name} ({custom_code}) - {available_count} {measure_type_name}"
        keyboard.append([InlineKeyboardButton(display_text, callback_data=f'item_view_{item_id}')])
    
    keyboard.append([InlineKeyboardButton(msg.BTN_BACK, callback_data='item_menu')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    item_list_text = "\n".join([f"🔹 {item[3]} ({item[2]}) - {item[9]} {item[8]}" for item in items[:20]])
    
    await query.edit_message_text(
        msg.ITEM_LIST.format(item_list_text),
        reply_markup=reply_markup
    )

async def item_view(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View item details."""
    query = update.callback_query
    await query.answer()
    
    item_id = int(query.data.split('_')[2])
    item = db.get_item_by_id(item_id)
    
    if not item:
        await query.edit_message_text(msg.ERROR_OCCURRED)
        return
    
    (item_id, code, custom_code, name, description,
     category_id, category_name, 
     subcategory_id, subcategory_name, 
     brand_id, brand_name,
     measure_type_id, measure_type_name,
     available_count, video_url,
     created_at, updated_at) = item
    
    images = db.get_item_images(item_id)
    
    keyboard = [
        [InlineKeyboardButton(msg.BTN_EDIT, callback_data=f'item_edit_{item_id}')],
        [InlineKeyboardButton(msg.BTN_VIEW_IMAGES, callback_data=f'item_images_{item_id}')],
        [InlineKeyboardButton(msg.BTN_DELETE, callback_data=f'item_delete_confirm_{item_id}')],
        [InlineKeyboardButton(msg.BTN_BACK, callback_data='item_list')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        msg.ITEM_DETAILS.format(
            name, 
            code,
            custom_code,
            description if description else '-',
            category_name,
            subcategory_name,
            brand_name,
            measure_type_name,
            available_count,
            video_url if video_url else '-',
            created_at, 
            updated_at,
            len(images)
        ),
        reply_markup=reply_markup
    )

async def item_view_images(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show item images."""
    query = update.callback_query
    await query.answer()
    
    item_id = int(query.data.split('_')[2])
    images = db.get_item_images(item_id)
    
    if not images:
        keyboard = [[InlineKeyboardButton(msg.BTN_BACK, callback_data=f'item_view_{item_id}')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(msg.ITEM_NO_IMAGES, reply_markup=reply_markup)
        return
    
    for img_id, img_path, created_at in images:
        if os.path.exists(img_path):
            with open(img_path, 'rb') as photo:
                await context.bot.send_photo(
                    chat_id=query.message.chat_id,
                    photo=photo,
                    caption=f"تاریخ آپلود: {created_at}"
                )
    
    keyboard = [[InlineKeyboardButton(msg.BTN_BACK, callback_data=f'item_view_{item_id}')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        f"✅ تعداد {len(images)} تصویر نمایش داده شد.",
        reply_markup=reply_markup
    )

# ============================================================================
# ITEM EDIT
# ============================================================================

async def item_edit_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start item edit process - show edit menu."""
    query = update.callback_query
    await query.answer()
    
    item_id = int(query.data.split('_')[2])
    
    keyboard = [
        [InlineKeyboardButton("✏️ ویرایش نام", callback_data=f'item_edit_name_{item_id}')],
        [InlineKeyboardButton(msg.BTN_EDIT_CUSTOM_CODE, callback_data=f'item_edit_custom_code_{item_id}')],
        [InlineKeyboardButton(msg.BTN_EDIT_DESCRIPTION, callback_data=f'item_edit_description_{item_id}')],
        [InlineKeyboardButton(msg.BTN_EDIT_AVAILABLE_COUNT, callback_data=f'item_edit_available_count_{item_id}')],
        [InlineKeyboardButton(msg.BTN_EDIT_VIDEO_URL, callback_data=f'item_edit_video_url_{item_id}')],
        [InlineKeyboardButton("➕ افزودن تصویر", callback_data=f'item_edit_add_image_{item_id}')],
        [InlineKeyboardButton(msg.BTN_BACK, callback_data=f'item_view_{item_id}')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "لطفا فیلد مورد نظر برای ویرایش را انتخاب کنید:",
        reply_markup=reply_markup
    )

async def item_edit_name_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start editing item name."""
    query = update.callback_query
    await query.answer()
    
    item_id = int(query.data.split('_')[3])
    user_id = query.from_user.id
    
    db.set_user_state(user_id, 'item_edit_name', {'item_id': item_id})
    
    keyboard = [[InlineKeyboardButton(msg.BTN_CANCEL, callback_data=f'item_view_{item_id}')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(msg.ITEM_UPDATE_REQUEST, reply_markup=reply_markup)

async def item_edit_handle_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle item name update."""
    user_id = update.effective_user.id
    state, data = db.get_user_state(user_id)
    
    if state != 'item_edit_name':
        return
    
    name = update.message.text.strip()
    item_id = data['item_id']
    
    item = db.get_item_by_id(item_id)
    if item:
        db.update_item(item_id, name, item[2], item[5], item[7], item[9], item[11], item[4], item[13], item[14])
        db.clear_user_state(user_id)
        
        keyboard = [
            [InlineKeyboardButton(msg.BTN_VIEW, callback_data=f'item_view_{item_id}')],
            [InlineKeyboardButton(msg.BTN_BACK, callback_data='item_list')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(msg.ITEM_UPDATED, reply_markup=reply_markup)

async def item_edit_custom_code_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start editing item custom code."""
    query = update.callback_query
    await query.answer()
    
    item_id = int(query.data.split('_')[4])
    user_id = query.from_user.id
    
    db.set_user_state(user_id, 'item_edit_custom_code', {'item_id': item_id})
    
    keyboard = [[InlineKeyboardButton(msg.BTN_CANCEL, callback_data=f'item_view_{item_id}')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text("لطفا کد اختصاصی جدید را وارد کنید:", reply_markup=reply_markup)

async def item_edit_handle_custom_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle item custom code update."""
    user_id = update.effective_user.id
    state, data = db.get_user_state(user_id)
    
    if state != 'item_edit_custom_code':
        return
    
    custom_code = update.message.text.strip()
    item_id = data['item_id']
    
    item = db.get_item_by_id(item_id)
    if item:
        db.update_item(item_id, item[3], custom_code, item[5], item[7], item[9], item[11], item[4], item[13], item[14])
        db.clear_user_state(user_id)
        
        keyboard = [
            [InlineKeyboardButton(msg.BTN_VIEW, callback_data=f'item_view_{item_id}')],
            [InlineKeyboardButton(msg.BTN_BACK, callback_data='item_list')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(msg.ITEM_UPDATED, reply_markup=reply_markup)

async def item_edit_description_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start editing item description."""
    query = update.callback_query
    await query.answer()
    
    item_id = int(query.data.split('_')[4])
    user_id = query.from_user.id
    
    db.set_user_state(user_id, 'item_edit_description', {'item_id': item_id})
    
    keyboard = [[InlineKeyboardButton(msg.BTN_CANCEL, callback_data=f'item_view_{item_id}')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text("لطفا توضیحات جدید را وارد کنید:", reply_markup=reply_markup)

async def item_edit_handle_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle item description update."""
    user_id = update.effective_user.id
    state, data = db.get_user_state(user_id)
    
    if state != 'item_edit_description':
        return
    
    description = update.message.text.strip()
    item_id = data['item_id']
    
    item = db.get_item_by_id(item_id)
    if item:
        db.update_item(item_id, item[3], item[2], item[5], item[7], item[9], item[11], description, item[13], item[14])
        db.clear_user_state(user_id)
        
        keyboard = [
            [InlineKeyboardButton(msg.BTN_VIEW, callback_data=f'item_view_{item_id}')],
            [InlineKeyboardButton(msg.BTN_BACK, callback_data='item_list')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(msg.ITEM_UPDATED, reply_markup=reply_markup)

async def item_edit_available_count_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start editing item available count."""
    query = update.callback_query
    await query.answer()
    
    item_id = int(query.data.split('_')[4])
    user_id = query.from_user.id
    
    db.set_user_state(user_id, 'item_edit_available_count', {'item_id': item_id})
    
    keyboard = [[InlineKeyboardButton(msg.BTN_CANCEL, callback_data=f'item_view_{item_id}')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text("لطفا موجودی جدید را وارد کنید:", reply_markup=reply_markup)

async def item_edit_handle_available_count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle item available count update."""
    user_id = update.effective_user.id
    state, data = db.get_user_state(user_id)
    
    if state != 'item_edit_available_count':
        return
    
    try:
        available_count = float(update.message.text.strip())
        if available_count < 0:
            raise ValueError()
    except ValueError:
        keyboard = [[InlineKeyboardButton(msg.BTN_CANCEL, callback_data='item_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "⚠️ لطفا یک عدد معتبر (0 یا بیشتر) وارد کنید:",
            reply_markup=reply_markup
        )
        return
    
    item_id = data['item_id']
    
    item = db.get_item_by_id(item_id)
    if item:
        db.update_item(item_id, item[3], item[2], item[5], item[7], item[9], item[11], item[4], available_count, item[14])
        db.clear_user_state(user_id)
        
        keyboard = [
            [InlineKeyboardButton(msg.BTN_VIEW, callback_data=f'item_view_{item_id}')],
            [InlineKeyboardButton(msg.BTN_BACK, callback_data='item_list')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(msg.ITEM_UPDATED, reply_markup=reply_markup)

async def item_edit_video_url_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start editing item video URL."""
    query = update.callback_query
    await query.answer()
    
    item_id = int(query.data.split('_')[4])
    user_id = query.from_user.id
    
    db.set_user_state(user_id, 'item_edit_video_url', {'item_id': item_id})
    
    keyboard = [[InlineKeyboardButton(msg.BTN_CANCEL, callback_data=f'item_view_{item_id}')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text("لطفا لینک ویدئوی جدید را وارد کنید:", reply_markup=reply_markup)

async def item_edit_handle_video_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle item video URL update."""
    user_id = update.effective_user.id
    state, data = db.get_user_state(user_id)
    
    if state != 'item_edit_video_url':
        return
    
    video_url = update.message.text.strip()
    item_id = data['item_id']
    
    item = db.get_item_by_id(item_id)
    if item:
        db.update_item(item_id, item[3], item[2], item[5], item[7], item[9], item[11], item[4], item[13], video_url)
        db.clear_user_state(user_id)
        
        keyboard = [
            [InlineKeyboardButton(msg.BTN_VIEW, callback_data=f'item_view_{item_id}')],
            [InlineKeyboardButton(msg.BTN_BACK, callback_data='item_list')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(msg.ITEM_UPDATED, reply_markup=reply_markup)

async def item_edit_add_image_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start adding images to existing item."""
    query = update.callback_query
    await query.answer()
    
    item_id = int(query.data.split('_')[4])
    user_id = query.from_user.id
    
    images = db.get_item_images(item_id)
    
    db.set_user_state(user_id, 'item_edit_add_images', {
        'item_id': item_id,
        'image_count': len(images)
    })
    
    keyboard = [
        [InlineKeyboardButton(msg.BTN_DONE, callback_data=f'item_edit_images_done_{item_id}')],
        [InlineKeyboardButton(msg.BTN_CANCEL, callback_data=f'item_view_{item_id}')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "📷 لطفا تصاویر جدید را ارسال کنید.\n\nبرای اتمام، روی دکمه 'اتمام' کلیک کنید.",
        reply_markup=reply_markup
    )

async def item_edit_handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle photo upload during edit."""
    user_id = update.effective_user.id
    state, data = db.get_user_state(user_id)
    
    if state != 'item_edit_add_images':
        return
    
    item_id = data['item_id']
    image_count = data['image_count']
    
    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    
    filename = f"item_{item_id}_{image_count + 1}.jpg"
    filepath = os.path.join('images', filename)
    
    await file.download_to_drive(filepath)
    db.add_item_image(item_id, filepath)
    
    data['image_count'] = image_count + 1
    db.set_user_state(user_id, 'item_edit_add_images', data)
    
    keyboard = [
        [InlineKeyboardButton(msg.BTN_DONE, callback_data=f'item_edit_images_done_{item_id}')],
        [InlineKeyboardButton(msg.BTN_CANCEL, callback_data=f'item_view_{item_id}')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        msg.ITEM_IMAGE_UPLOADED.format(data['image_count']),
        reply_markup=reply_markup
    )

async def item_edit_images_done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Finish adding images."""
    query = update.callback_query
    await query.answer()
    
    item_id = int(query.data.split('_')[3])
    user_id = query.from_user.id
    
    db.clear_user_state(user_id)
    
    keyboard = [[InlineKeyboardButton(msg.BTN_VIEW, callback_data=f'item_view_{item_id}')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "✅ تصاویر با موفقیت اضافه شدند!",
        reply_markup=reply_markup
    )

# ============================================================================
# ITEM DELETE
# ============================================================================

async def item_delete_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Confirm item deletion."""
    query = update.callback_query
    await query.answer()
    
    item_id = int(query.data.split('_')[3])
    item = db.get_item_by_id(item_id)
    
    if not item:
        await query.edit_message_text(msg.ERROR_OCCURRED)
        return
    
    keyboard = [
        [InlineKeyboardButton("✅ بله، حذف شود", callback_data=f'item_delete_{item_id}')],
        [InlineKeyboardButton(msg.BTN_CANCEL, callback_data=f'item_view_{item_id}')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"⚠️ آیا از حذف کالا '{item[3]}' اطمینان دارید؟\n\n"
        "توجه: تمام تصاویر مرتبط نیز حذف خواهند شد.",
        reply_markup=reply_markup
    )

async def item_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Delete item."""
    query = update.callback_query
    await query.answer()
    
    item_id = int(query.data.split('_')[2])
    db.delete_item(item_id)
    
    keyboard = [[InlineKeyboardButton(msg.BTN_BACK, callback_data='item_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(msg.ITEM_DELETED, reply_markup=reply_markup)
