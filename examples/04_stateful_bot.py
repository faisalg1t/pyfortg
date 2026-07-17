"""
Example: Stateful Bot with Redis Session Management

This bot demonstrates user state management using Redis storage.
Users can create a profile with their name, age, and favorite color.
"""

import asyncio
from pyfortg import TelegramBot, Filters
from pyfortg.keyboards import InlineKeyboardMarkup, ReplyKeyboardMarkup
from pyfortg.storage import RedisStorage


async def main():
    # Initialize bot and storage
    bot = TelegramBot(token="YOUR_BOT_TOKEN")
    storage = RedisStorage(url="redis://localhost")

    # Define conversation states
    STATES = {
        "IDLE": 0,
        "ASKING_NAME": 1,
        "ASKING_AGE": 2,
        "ASKING_COLOR": 3,
        "COMPLETE": 4
    }

    # Helper functions
    async def get_user_state(user_id: int) -> dict:
        """Get user state from Redis"""
        state_key = f"user:state:{user_id}"
        state = await storage.get(state_key)
        return state or {"status": STATES["IDLE"], "profile": {}}

    async def set_user_state(user_id: int, state: dict):
        """Save user state to Redis"""
        state_key = f"user:state:{user_id}"
        await storage.set(state_key, state)

    # Handler: /start command
    @bot.on_command("start")
    async def handle_start(bot, update, context):
        user_id = update.message.from_user.id
        
        keyboard = InlineKeyboardMarkup()
        keyboard.add_button("Create Profile", callback_data="create_profile")
        keyboard.add_button("View Profile", callback_data="view_profile")
        
        await bot.send_message(
            chat_id=update.message.chat.id,
            text="Welcome! What would you like to do?",
            reply_markup=keyboard
        )

    # Handler: Callback queries
    @bot.on_callback_query()
    async def handle_callback(bot, update, context):
        user_id = update.callback_query.from_user.id
        callback_data = update.callback_query.data

        if callback_data == "create_profile":
            state = await get_user_state(user_id)
            state["status"] = STATES["ASKING_NAME"]
            await set_user_state(user_id, state)
            
            await bot.send_message(
                chat_id=update.callback_query.message.chat.id,
                text="What's your name?"
            )
            await bot.answer_callback_query(
                callback_query_id=update.callback_query.id,
                text="Let's create your profile!"
            )

        elif callback_data == "view_profile":
            state = await get_user_state(user_id)
            profile = state.get("profile", {})
            
            if profile:
                profile_text = f"""
Your Profile:
Name: {profile.get('name', 'N/A')}
Age: {profile.get('age', 'N/A')}
Favorite Color: {profile.get('color', 'N/A')}
                """
            else:
                profile_text = "No profile created yet. Create one to get started!"
            
            await bot.send_message(
                chat_id=update.callback_query.message.chat.id,
                text=profile_text
            )

    # Handler: Text messages (profile creation flow)
    @bot.on_message(Filters.text)
    async def handle_text(bot, update, context):
        user_id = update.message.from_user.id
        state = await get_user_state(user_id)
        current_status = state["status"]

        if current_status == STATES["ASKING_NAME"]:
            state["profile"]["name"] = update.message.text
            state["status"] = STATES["ASKING_AGE"]
            await set_user_state(user_id, state)
            
            await bot.send_message(
                chat_id=update.message.chat.id,
                text=f"Nice to meet you, {update.message.text}! How old are you?"
            )

        elif current_status == STATES["ASKING_AGE"]:
            try:
                age = int(update.message.text)
                state["profile"]["age"] = age
                state["status"] = STATES["ASKING_COLOR"]
                await set_user_state(user_id, state)
                
                await bot.send_message(
                    chat_id=update.message.chat.id,
                    text="What's your favorite color?"
                )
            except ValueError:
                await bot.send_message(
                    chat_id=update.message.chat.id,
                    text="Please enter a valid number."
                )

        elif current_status == STATES["ASKING_COLOR"]:
            state["profile"]["color"] = update.message.text
            state["status"] = STATES["COMPLETE"]
            await set_user_state(user_id, state)
            
            profile = state["profile"]
            await bot.send_message(
                chat_id=update.message.chat.id,
                text=f"""
Profile completed!
Name: {profile['name']}
Age: {profile['age']}
Color: {profile['color']}

Use /start to see more options.
                """
            )

    # Run bot
    await bot.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
