from fastapi import FastAPI
import random

app = FastAPI()

side_hustles =[
    "freelancing - Start offering your skills online!",
    "online surveys - Get paid for your opinions!",
    "online tutoring - Share your knowledge with others!",
    "social media management - Manage social media accounts for businesses!",
    "virtual assistant - Help businesses with administrative tasks!",
    "e-commerce - Start your own online store!",
    "blogging - Share your thoughts and ideas online!",
    "podcasting - Start your own podcast!",
    "dropshipping - Sell products without holding inventory!",
    "affiliate marketing - Earn commissions by promoting products!",
    "web design - Create websites for clients!",
    "graphic design - Design logos, graphics, and more!",
    "content writing - Write articles, blog posts, and more!",
    "SEO services - Help businesses improve their online visibility!",
]

money_quotes = [
    "The best way to predict the future is to create it. - Peter Drucker",
    "Money is a terrible master but an excellent servant. - P.T. Barnum",
    "The more you learn, the more you earn. - Warren Buffett",
    "Don't tell me where your priorities are. Show me where you spend your money and I'll tell you what they are. - James W. Frick",
    "Money is only a tool. It will take you wherever you wish, but it will not replace you as the driver. - Ayn Rand",
    "The art is not in making money, but in keeping it. - Proverb",
    "A wise person should have money in their head, but not in their heart. - Jonathan Swift",
    "Money is a guarantee that we may have what we want in the future. Though we need nothing at the moment it insures the possibility of satisfying a new desire when it arises. - Aristotle",
    "Money is usually attracted, not pursued. - Jim Rohn",
    "Empty pockets never held anyone back. Only empty heads and empty hearts can do that. - Norman Vincent Peale",
    "Money is a terrible master but an excellent servant. - P.T. Barnum",
    "The more you learn, the more you earn. - Warren Buffett",
    "Don't tell me where your priorities are. Show me where you spend your money and I'll tell you what they are. - James W. Frick",
    "Money is only a tool. It will take you wherever you wish, but it will not replace you as the driver. - Ayn Rand",
    "The art is not in making money, but in keeping it. - Proverb",
    "A wise person should have money in their head, but not in their heart. - Jonathan Swift",
    "Money is a guarantee that we may have what we want in the future. Though we need nothing at the moment it insures the possibility of satisfying a new desire when it arises. - Aristotle",
]

@app.get("/side_business")
def get_side_hustle(apikey : str):
    """Returms a random side hustle"""
    if apikey != "12345":
        return{"error": "Unauthorized"}
    return{"side_hustle": random.choice(side_hustles)}

@app.get("/money_quote")
def get_money_quotes(apikey: str):
    """Return a random money quotes"""
    if apikey != "12345":
        return{"error": "Unauthorized"}
    return{"money_quote": random.choice(money_quotes)}