from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timedelta
import random
import string
from typing import List, Optional, Tuple
import re

class RedeemCodesDB:
    def __init__(self, database_url: str, database_name: str):
        self.client = AsyncIOMotorClient(database_url)
        self.db = self.client[database_name]
        self.redeem_codes = self.db.redeem_codes
        self.users = self.db.users
    
    async def generate_redeem_codes(self, count: int, duration_days: float) -> List[str]:
        """Generate redeem codes and store in MongoDB"""
        codes = []
        expires_at = datetime.now() + timedelta(hours=2)  # Codes expire in 2 hours
        
        for _ in range(count):
            # Generate 8-character alphanumeric code
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            
            # Insert code into database
            await self.redeem_codes.insert_one({
                "code": code,
                "premium_duration_days": duration_days,
                "created_at": datetime.now(),
                "expires_at": expires_at,
                "is_used": False,
                "used_by": None,
                "used_at": None
            })
            
            codes.append(code)
        
        return codes
    
    async def redeem_code(self, code: str, user_id: int) -> Tuple[bool, str]:
        """Redeem a code for premium access"""
        
        # Check if user already has active premium
        user = await self.users.find_one({"user_id": user_id})
        if user and user.get("is_premium") and user.get("premium_until"):
            if datetime.now() < user["premium_until"]:
                return False, "You already have premium. You can't"
        
        # Check if code exists and is valid
        code_data = await self.redeem_codes.find_one({"code": code})
        
        if not code_data:
            return False, "❌ Invalid redemption code!"
        
        if code_data["is_used"]:
            return False, "❌ This code has already been redeemed!"
        
        # Check if code has expired
        if datetime.now() > code_data["expires_at"]:
            return False, "❌ This redemption code has expired!"
        
        # Mark code as used
        await self.redeem_codes.update_one(
            {"code": code},
            {
                "$set": {
                    "is_used": True,
                    "used_by": user_id,
                    "used_at": datetime.now()
                }
            }
        )
        
        # Give new premium subscription
        premium_duration = timedelta(days=code_data["premium_duration_days"])
        new_end = datetime.now() + premium_duration
        
        # Update user's premium status
        await self.users.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "premium_until": new_end,
                    "is_premium": True
                }
            },
            upsert=True
        )
        
        duration_text = self.format_duration(code_data["premium_duration_days"])
        return True, f"🎉 **Congratulations!**\n✅ Code successfully redeemed!\n⏱️ **Premium Duration:** {duration_text}\n📅 **Expires On:** {new_end.strftime('%d-%m-%Y %I:%M:%S %p')}\n\nEnjoy your premium access! Use `/myplan` to check your subscription details."
    
    def format_duration(self, days: float) -> str:
        """Format duration in days to human readable format"""
        if days >= 365:
            years = int(days / 365)
            return f"{years} year{'s' if years > 1 else ''}"
        elif days >= 1:
            return f"{int(days)} day{'s' if int(days) > 1 else ''}"
        elif days >= 1/24:
            hours = int(days * 24)
            return f"{hours} hour{'s' if hours > 1 else ''}"
        elif days >= 1/(24*60):
            minutes = int(days * 24 * 60)
            return f"{minutes} minute{'s' if minutes > 1 else ''}"
        else:
            seconds = int(days * 24 * 60 * 60)
            return f"{seconds} second{'s' if seconds > 1 else ''}"
    
    def parse_duration_to_days(self, duration_str: str) -> Optional[float]:
        """Parse duration string to days"""
        # Remove any spaces
        duration_str = duration_str.replace(" ", "")
        
        # Match number and unit
        match = re.match(r'^(\d+)([a-zA-Z]+)$', duration_str)
        if not match:
            return None
        
        value = int(match.group(1))
        unit = match.group(2).lower()
        
        # Convert to days
        if unit in ['d', 'day', 'days']:
            return float(value)
        elif unit in ['h', 'hour', 'hours']:
            return value / 24.0
        elif unit in ['m', 'minute', 'minutes']:
            return value / (24.0 * 60.0)
        elif unit in ['s', 'second', 'seconds']:
            return value / (24.0 * 60.0 * 60.0)
        elif unit in ['y', 'year', 'years']:
            return value * 365.0
        else:
            return None
    
    async def get_codes_stats(self) -> dict:
        """Get statistics about redeem codes"""
        active_codes = await self.redeem_codes.count_documents({
            "is_used": False,
            "expires_at": {"$gt": datetime.now()}
        })
        
        used_codes = await self.redeem_codes.count_documents({"is_used": True})
        
        expired_codes = await self.redeem_codes.count_documents({
            "expires_at": {"$lte": datetime.now()}
        })
        
        return {
            'active': active_codes,
            'used': used_codes,
            'expired': expired_codes
        }
    
    async def clean_expired_codes(self) -> int:
        """Clean expired codes from database"""
        result = await self.redeem_codes.delete_many({
            "expires_at": {"$lte": datetime.now()},
            "is_used": False
        })
        return result.deleted_count
