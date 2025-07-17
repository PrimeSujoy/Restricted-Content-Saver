# Add these imports to your main bot file
from telegram import Update
from telegram.ext import ContextTypes
from config import OWNER_ID, MONGO_DB
from redeem_codes_db import RedeemCodesDB

# Initialize database
redeem_db = RedeemCodesDB(MONGO_DB, "your_database_name")  # Replace with your database name

async def gen_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /gen command for bot admin and owner"""
    user_id = update.effective_user.id
    
    # Check if user is admin/owner
    if user_id not in OWNER_ID:
        await update.message.reply_text("❌ You don't have permission to use this command!")
        return
    
    if len(context.args) != 2:
        error_msg = "❌ **Invalid format!**\n\n"
        error_msg += "**Usage:** `/gen <count> <duration>`\n\n"
        error_msg += "**Examples:**\n"
        error_msg += "• `/gen 10 7d` - 10 codes for 7 days\n"
        error_msg += "• `/gen 5 2h` - 5 codes for 2 hours\n"
        error_msg += "• `/gen 3 30m` - 3 codes for 30 minutes\n"
        error_msg += "• `/gen 1 1y` - 1 code for 1 year\n"
        error_msg += "• `/gen 15 45s` - 15 codes for 45 seconds\n\n"
        error_msg += "**Supported formats:** `d` (days), `h` (hours), `m` (minutes), `s` (seconds), `y` (years)"
        await update.message.reply_text(error_msg, parse_mode='Markdown')
        return
    
    try:
        count = int(context.args[0])
        duration_str = context.args[1].lower()
        
        if count > 40:
            await update.message.reply_text("❌ Maximum 40 codes can be generated at once!")
            return
        
        if count < 1:
            await update.message.reply_text("❌ Count must be at least 1!")
            return
        
        # Parse duration with flexible format
        duration_days = redeem_db.parse_duration_to_days(duration_str)
        
        if duration_days is None:
            error_msg = "❌ **Invalid duration format!**\n\n"
            error_msg += "**Supported formats:**\n"
            error_msg += "• `7d` or `7days` - 7 days\n"
            error_msg += "• `2h` or `2hours` - 2 hours\n"
            error_msg += "• `30m` or `30minutes` - 30 minutes\n"
            error_msg += "• `45s` or `45seconds` - 45 seconds\n"
            error_msg += "• `1y` or `1year` - 1 year"
            await update.message.reply_text(error_msg, parse_mode='Markdown')
            return
        
        # Generate codes
        codes = await redeem_db.generate_redeem_codes(count, duration_days)
        expires_at = datetime.now() + timedelta(hours=2)
        
        # Format response
        response = f"🎟️ **{count} Premium Code(s) Generated**\n"
        response += f"⏱️ **Duration:** {duration_str}\n"
        response += f"📅 **Valid Until:** {expires_at.strftime('%d-%m-%Y %I:%M:%S %p')}\n\n"
        response += "**Redemption Codes:**\n\n"
        
        for code in codes:
            response += f"```\n/redeem {code}\n```\n\n"
        
        response += "**Note:** Users can redeem these codes using the `/redeem` command."
        
        await update.message.reply_text(response, parse_mode='Markdown')
        
    except ValueError:
        await update.message.reply_text("❌ Invalid input! Please use correct format.")

async def redeem_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /redeem command for bot users"""
    user = update.effective_user
    
    if len(context.args) != 1:
        await update.message.reply_text("❌ **Usage:** `/redeem <code>`\n**Example:** `/redeem JS19MNUX`", parse_mode='Markdown')
        return
    
    code = context.args[0].upper()
    success, message = await redeem_db.redeem_code(code, user.id)
    
    if success:
        await update.message.reply_text(f"🎉 **Congratulations, {user.mention_html()}!**\n{message}", parse_mode='HTML')
    else:
        await update.message.reply_text(message)

# Add these handlers to your main bot application
# application.add_handler(CommandHandler("gen", gen_command))
# application.add_handler(CommandHandler("redeem", redeem_command))