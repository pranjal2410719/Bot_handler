#!/usr/bin/env python3
"""
Standalone bot runner for deployment
"""
import os
import sys
import asyncio
from telegram_bot_controller import main

if __name__ == "__main__":
    print("🤖 Starting Braynix Studios Bot...")
    try:
        main()
    except KeyboardInterrupt:
        print("Bot stopped by user")
    except Exception as e:
        print(f"Bot error: {e}")
        sys.exit(1)