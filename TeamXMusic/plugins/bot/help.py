import random
import aiohttp
from typing import Union, List

from pyrogram import filters, types
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Message,
    CallbackQuery,
)
from pyrogram.errors import MessageNotModified
from pyrogram.enums import ParseMode

from TeamXMusic import app
from TeamXMusic.misc import SUDOERS
from TeamXMusic.utils import help_pannel
from TeamXMusic.utils.database import get_lang, get_model_settings, update_model_settings
from TeamXMusic.utils.decorators.language import LanguageStart, languageCB
from TeamXMusic.utils.inline.help import help_back_markup, private_help_panel
from config import BANNED_USERS, SUPPORT_CHAT, YTPROXY_URL
import config
from strings import get_string, helpers


# ---------------------------
# Fetch model lists from API
# ---------------------------

async def fetch_tts_models() -> List[dict]:
    """Fetch TTS models from the API."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{YTPROXY_URL}/tts/models", timeout=15) as r:
                if r.status == 200:
                    data = await r.json()
                    return data.get("speakers", []) or []
    except Exception as e:
        print(f"Error fetching TTS models: {e}")
    return []


async def fetch_image_models() -> List[str]:
    """Fetch image models from the API."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{YTPROXY_URL}/image/models", timeout=15) as r:
                if r.status == 200:
                    data = await r.json()
                    return data.get("models", []) or []
    except Exception as e:
        print(f"Error fetching image models: {e}")
    return []


async def fetch_ai_models() -> List[str]:
    """Fetch AI models from the API."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{YTPROXY_URL}/ai/models", timeout=15) as r:
                if r.status == 200:
                    data = await r.json()
                    return data.get("models", []) or []
    except Exception as e:
        print(f"Error fetching AI models: {e}")
    return []


# --------------------------------
# /help in PM and groups
# --------------------------------

@app.on_message(filters.command(["help"]) & filters.private & ~BANNED_USERS)
# Support both variants from your inline buttons file:
@app.on_callback_query(filters.regex(r"^(settings_back_helper|settingsback_helper)$") & ~BANNED_USERS)
async def helper_private(client, update: Union[types.Message, types.CallbackQuery]):
    """Main /help entry (PM) + back-from-settings callback."""
    is_callback = isinstance(update, types.CallbackQuery)
    is_sudo = update.from_user.id in SUDOERS

    if is_callback:
        try:
            await update.answer()
        except Exception:
            pass
        chat_id = update.message.chat.id
        language = await get_lang(chat_id)
        _ = get_string(language)
        keyboard = help_pannel(_, is_sudo, True)
        await update.edit_message_text(
            _["help_1"].format(SUPPORT_CHAT),
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )
        return

    # Message path
    try:
        await update.delete()
    except Exception:
        pass
    language = await get_lang(update.chat.id)
    _ = get_string(language)
    keyboard = help_pannel(_, is_sudo)
    await update.reply_photo(
        photo=random.choice(config.START_IMG_URL),
        caption=_["help_1"].format(SUPPORT_CHAT),
        reply_markup=keyboard,
    )


@app.on_message(filters.command(["help"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def help_com_group(client, message: Message, _):
    keyboard = private_help_panel(_)
    await message.reply_text(
        _["help_2"],
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# --------------------------------
# Help pages + Settings fanout
# --------------------------------

@app.on_callback_query(filters.regex(r"^help_callback") & ~BANNED_USERS)
@languageCB
async def helper_cb(client, cq: CallbackQuery, _):
    """
    Handles:
      - Static help pages hb1..hb15
      - hb16: menu for AI/TTS/IMAGE settings
      - hb17/hb18/hb19: dynamic model lists
    """
    try:
        await cq.answer()
    except Exception:
        pass

    # Expected format: "help_callback hbXX"
    parts = cq.data.split(maxsplit=1)
    cb = parts[1].strip() if len(parts) == 2 else ""

    # Back keyboard for static pages
    back_keyboard = help_back_markup(_)

    # Static pages map
    static_map = {
        "hb1": helpers.HELP_1, "hb2": helpers.HELP_2, "hb3": helpers.HELP_3,
        "hb4": helpers.HELP_4, "hb5": helpers.HELP_5, "hb6": helpers.HELP_6,
        "hb7": helpers.HELP_7, "hb8": helpers.HELP_8, "hb9": helpers.HELP_9,
        "hb10": helpers.HELP_10, "hb11": helpers.HELP_11, "hb12": helpers.HELP_12,
        "hb13": helpers.HELP_13, "hb14": helpers.HELP_14, "hb15": helpers.HELP_15,
    }

    if cb in static_map:
        try:
            await cq.edit_message_text(
                static_map[cb],
                reply_markup=back_keyboard,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
            )
        except MessageNotModified:
            pass
        return

    if cb == "hb16":
        # Landing menu for model settings (dynamic here is fine)
        btn = [
            [InlineKeyboardButton("Ai Model Setting", callback_data="help_callback hb19")],
            [InlineKeyboardButton("TTS Model Setting", callback_data="help_callback hb17")],
            [InlineKeyboardButton("IMAGE Model Setting", callback_data="help_callback hb18")],
            # Respect both back variants from your inline file:
            [InlineKeyboardButton(_["BACK_BUTTON"], callback_data="settings_back_helper")],
        ]
        try:
            await cq.edit_message_text(
                "AI, TTS and Image Model Settings\n\n[Check Docs here](https://teamx-docs.netlify.app/)",
                reply_markup=InlineKeyboardMarkup(btn),
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
            )
        except MessageNotModified:
            pass
        return

    if cb == "hb17":
        # TTS models
        model_settings = await get_model_settings()
        current_tts = model_settings.get("tts", "athena")
        speakers = await fetch_tts_models()

        if not speakers:
            btn = [[InlineKeyboardButton(_["BACK_BUTTON"], callback_data="help_callback hb16")]]
            try:
                await cq.edit_message_text(
                    "❌ Unable to fetch TTS models. Please try again later.",
                    reply_markup=InlineKeyboardMarkup(btn),
                    parse_mode=ParseMode.MARKDOWN,
                )
            except MessageNotModified:
                pass
            return

        # Build grid (2 columns)
        rows, row = [], []
        for sp in speakers:
            sp_id = sp.get("speaker")
            name = sp.get("name", sp_id)
            text = f"✅ {name}" if sp_id == current_tts else name
            row.append(InlineKeyboardButton(text=text, callback_data=f"tts_model_{sp_id}"))
            if len(row) == 2:
                rows.append(row)
                row = []
        if row:
            rows.append(row)
        rows.append([InlineKeyboardButton(_["BACK_BUTTON"], callback_data="help_callback hb16")])

        try:
            await cq.edit_message_text(
                "🎤 **TTS Model Settings**\n\nSelect a voice model.\n\n[Check out the samples here](https://t.me/TeamXUpdate/41)",
                reply_markup=InlineKeyboardMarkup(rows),
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
            )
        except MessageNotModified:
            pass
        return

    if cb == "hb18":
        # Image models
        model_settings = await get_model_settings()
        current_image = model_settings.get("image", "stable-diffusion")
        models = await fetch_image_models()

        if not models:
            btn = [[InlineKeyboardButton(_["BACK_BUTTON"], callback_data="help_callback hb16")]]
            try:
                await cq.edit_message_text(
                    "❌ Unable to fetch image models. Please try again later.",
                    reply_markup=InlineKeyboardMarkup(btn),
                    parse_mode=ParseMode.MARKDOWN,
                )
            except MessageNotModified:
                pass
            return

        buttons = []
        for m in models:
            text = f"✅ {m}" if m == current_image else m
            buttons.append([InlineKeyboardButton(text=text, callback_data=f"image_model_{m}")])
        buttons.append([InlineKeyboardButton(_["BACK_BUTTON"], callback_data="help_callback hb16")])

        try:
            await cq.edit_message_text(
                "🎨 **Image Model Settings**\n\nSelect an image generation model:",
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=ParseMode.MARKDOWN,
            )
        except MessageNotModified:
            pass
        return

    if cb == "hb19":
        # AI models
        model_settings = await get_model_settings()
        current_ai = model_settings.get("ai", "GPT4")
        models = await fetch_ai_models()

        if not models:
            btn = [[InlineKeyboardButton(_["BACK_BUTTON"], callback_data="help_callback hb16")]]
            try:
                await cq.edit_message_text(
                    "❌ Unable to fetch AI models. Please try again later.",
                    reply_markup=InlineKeyboardMarkup(btn),
                    parse_mode=ParseMode.MARKDOWN,
                )
            except MessageNotModified:
                pass
            return

        buttons = []
        for m in models:
            text = f"✅ {m}" if m == current_ai else m
            buttons.append([InlineKeyboardButton(text=text, callback_data=f"ai_model_{m}")])
        buttons.append([InlineKeyboardButton(_["BACK_BUTTON"], callback_data="help_callback hb16")])

        try:
            await cq.edit_message_text(
                "🤖 **AI Model Settings**\n\nSelect an AI model:",
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=ParseMode.MARKDOWN,
            )
        except MessageNotModified:
            pass
        return


# --------------------------------
# Model selection handlers
# --------------------------------

@app.on_callback_query(filters.regex(r"^tts_model_") & ~BANNED_USERS)
@languageCB
async def tts_model_callback(client, cq: CallbackQuery, _):
    try:
        await cq.answer()
    except Exception:
        pass

    model_name = cq.data.replace("tts_model_", "", 1)
    success = await update_model_settings({"tts": model_name})
    if not success:
        btn = [[InlineKeyboardButton(_["BACK_BUTTON"], callback_data="help_callback hb16")]]
        try:
            await cq.edit_message_text(
                "❌ Failed to update TTS model. Please try again.",
                reply_markup=InlineKeyboardMarkup(btn),
                parse_mode=ParseMode.MARKDOWN,
            )
        except MessageNotModified:
            pass
        return

    # Re-render the list with selection highlighted
    model_settings = await get_model_settings()
    current_tts = model_settings.get("tts", model_name)
    speakers = await fetch_tts_models()

    rows, row = [], []
    if speakers:
        for sp in speakers:
            sp_id = sp.get("speaker")
            name = sp.get("name", sp_id)
            text = f"✅ {name}" if sp_id == current_tts else name
            row.append(InlineKeyboardButton(text=text, callback_data=f"tts_model_{sp_id}"))
            if len(row) == 2:
                rows.append(row)
                row = []
        if row:
            rows.append(row)
    rows.append([InlineKeyboardButton(_["BACK_BUTTON"], callback_data="help_callback hb16")])

    try:
        await cq.edit_message_text(
            f"✅ **TTS Model Updated!**\n\nCurrent model: **{model_name}**",
            reply_markup=InlineKeyboardMarkup(rows),
            parse_mode=ParseMode.MARKDOWN,
        )
    except MessageNotModified:
        pass


@app.on_callback_query(filters.regex(r"^image_model_") & ~BANNED_USERS)
@languageCB
async def image_model_callback(client, cq: CallbackQuery, _):
    try:
        await cq.answer()
    except Exception:
        pass

    model_name = cq.data.replace("image_model_", "", 1)
    success = await update_model_settings({"image": model_name})
    if not success:
        btn = [[InlineKeyboardButton(_["BACK_BUTTON"], callback_data="help_callback hb16")]]
        try:
            await cq.edit_message_text(
                "❌ Failed to update image model. Please try again.",
                reply_markup=InlineKeyboardMarkup(btn),
                parse_mode=ParseMode.MARKDOWN,
            )
        except MessageNotModified:
            pass
        return

    model_settings = await get_model_settings()
    current_image = model_settings.get("image", model_name)
    models = await fetch_image_models()

    buttons = []
    if models:
        for m in models:
            text = f"✅ {m}" if m == current_image else m
            buttons.append([InlineKeyboardButton(text=text, callback_data=f"image_model_{m}")])
    buttons.append([InlineKeyboardButton(_["BACK_BUTTON"], callback_data="help_callback hb16")])

    try:
        await cq.edit_message_text(
            f"✅ **Image Model Updated!**\n\nCurrent model: **{model_name}**",
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=ParseMode.MARKDOWN,
        )
    except MessageNotModified:
        pass


@app.on_callback_query(filters.regex(r"^ai_model_") & ~BANNED_USERS)
@languageCB
async def ai_model_callback(client, cq: CallbackQuery, _):
    try:
        await cq.answer()
    except Exception:
        pass

    model_name = cq.data.replace("ai_model_", "", 1)
    success = await update_model_settings({"ai": model_name})
    if not success:
        btn = [[InlineKeyboardButton(_["BACK_BUTTON"], callback_data="help_callback hb16")]]
        try:
            await cq.edit_message_text(
                "❌ Failed to update AI model. Please try again.",
                reply_markup=InlineKeyboardMarkup(btn),
                parse_mode=ParseMode.MARKDOWN,
            )
        except MessageNotModified:
            pass
        return

    model_settings = await get_model_settings()
    current_ai = model_settings.get("ai", model_name)
    models = await fetch_ai_models()

    buttons = []
    if models:
        for m in models:
            text = f"✅ {m}" if m == current_ai else m
            buttons.append([InlineKeyboardButton(text=text, callback_data=f"ai_model_{m}")])
    buttons.append([InlineKeyboardButton(_["BACK_BUTTON"], callback_data="help_callback hb16")])

    try:
        await cq.edit_message_text(
            f"✅ **AI Model Updated!**\n\nCurrent model: **{model_name}**",
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=ParseMode.MARKDOWN,
        )
    except MessageNotModified:
        pass
