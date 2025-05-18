import streamlit as st
import requests
import sqlite3
import bcrypt
import os
from dotenv import load_dotenv
from datetime import datetime
import stripe
import os

# Load environment variables
load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY")
STRIPE_PRICE_ID = os.getenv("STRIPE_PRICE_ID")
DOMAIN_URL = os.getenv("DOMAIN_URL")

# Configure Stripe
stripe.api_key = STRIPE_SECRET_KEY

# Database Manager Class
class DatabaseManager:
    def __init__(self, db_name="newshub.db"):
        self.db_name = db_name
        self.init_db()

    def init_db(self):
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            # Create users table if it doesn't exist
            c.execute('''CREATE TABLE IF NOT EXISTS users
                         (username TEXT PRIMARY KEY, 
                          password TEXT, 
                          is_premium INTEGER)''')
            # Check and add missing columns
            c.execute("PRAGMA table_info(users)")
            columns = [col[1] for col in c.fetchall()]
            if 'stripe_customer_id' not in columns:
                c.execute("ALTER TABLE users ADD COLUMN stripe_customer_id TEXT")
            if 'stripe_subscription_id' not in columns:
                c.execute("ALTER TABLE users ADD COLUMN stripe_subscription_id TEXT")
            # Create saved_articles table
            c.execute('''CREATE TABLE IF NOT EXISTS saved_articles
                         (username TEXT, article_url TEXT, title TEXT, saved_at TEXT)''')
            conn.commit()

    def add_user(self, username, password):
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            try:
                c.execute("INSERT INTO users (username, password, is_premium, stripe_customer_id, stripe_subscription_id) VALUES (?, ?, ?, ?, ?)",
                          (username, hashed, 0, None, None))
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                return False

    def verify_user(self, username, password):
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            c.execute("SELECT password FROM users WHERE username = ?", (username,))
            result = c.fetchone()
            if result and bcrypt.checkpw(password.encode('utf-8'), result[0]):
                return True
            return False

    def is_premium_user(self, username):
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            c.execute("SELECT is_premium FROM users WHERE username = ?", (username,))
            result = c.fetchone()
            return result[0] == 1 if result else False

    def save_article(self, username, article_url, title):
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO saved_articles (username, article_url, title, saved_at) VALUES (?, ?, ?, ?)",
                      (username, article_url, title, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            conn.commit()

    def get_saved_articles(self, username):
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            c.execute("SELECT title, article_url, saved_at FROM saved_articles WHERE username = ?", (username,))
            return c.fetchall()

    def update_subscription(self, username, stripe_customer_id, stripe_subscription_id, is_premium):
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            c.execute("UPDATE users SET stripe_customer_id = ?, stripe_subscription_id = ?, is_premium = ? WHERE username = ?",
                      (stripe_customer_id, stripe_subscription_id, is_premium, username))
            conn.commit()

    def get_user(self, username):
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            c.execute("SELECT stripe_customer_id, stripe_subscription_id FROM users WHERE username = ?", (username,))
            return c.fetchone()

# News Fetcher Class
class NewsFetcher:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://newsapi.org/v2/top-headlines"

    def fetch_news(self, category="general", country="us"):
        params = {
            "apiKey": self.api_key,
            "category": category,
            "country": country,
            "pageSize": 10
        }
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json().get("articles", [])
        except requests.RequestException as e:
            st.error(f"Error fetching news: {e}")
            return []

# Payment Processor Class (Stripe Integration, No Webhooks)
class PaymentProcessor:
    def __init__(self, domain_url):
        self.domain_url = domain_url

    def create_checkout_session(self, username, stripe_customer_id=None):
        try:
            # Create or use existing Stripe customer
            if not stripe_customer_id:
                customer = stripe.Customer.create(
                    email=f"{username}@newshub.example.com",
                    metadata={"username": username}
                )
                stripe_customer_id = customer.id
            else:
                customer = stripe.Customer.retrieve(stripe_customer_id)

            # Create Checkout Session
            session = stripe.checkout.Session.create(
                customer=stripe_customer_id,
                payment_method_types=["card"],
                mode="subscription",
                line_items=[{
                    "price": STRIPE_PRICE_ID,
                    "quantity": 1
                }],
                success_url=f"{self.domain_url}/success?session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=f"{self.domain_url}/cancel",
                metadata={"username": username}
            )
            return session.url, stripe_customer_id
        except stripe.error.StripeError as e:
            st.error(f"Error creating checkout session: {e}")
            return None, None

    def verify_subscription(self, session_id, username):
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            if session.payment_status == "paid" and session.subscription:
                subscription = stripe.Subscription.retrieve(session.subscription)
                if subscription.status == "active":
                    return session.customer, session.subscription
            return None, None
        except stripe.error.StripeError as e:
            st.error(f"Error verifying subscription: {e}")
            return None, None

    def check_subscription_status(self, subscription_id):
        try:
            if subscription_id:
                subscription = stripe.Subscription.retrieve(subscription_id)
                return subscription.status == "active"
            return False
        except stripe.error.StripeError as e:
            st.error(f"Error checking subscription status: {e}")
            return False

# Main Application Class
class NewsHubApp:
    def __init__(self):
        self.db = DatabaseManager()
        self.news_fetcher = NewsFetcher(NEWS_API_KEY)
        self.payment_processor = PaymentProcessor(DOMAIN_URL)
        self.session_state = st.session_state

    def run(self):
        st.set_page_config(page_title="NewsHub", page_icon="📰")
        query_params = st.query_params
        page = query_params.get("page", ["home"])[0]

        if page == "success":
            self.show_success_page()
        elif page == "cancel":
            self.show_cancel_page()
        else:
            self.show_main_app()

    def show_success_page(self):
        st.title("Subscription Successful")
        session_id = st.query_params.get("session_id", [None])[0]
        if session_id and "username" in self.session_state and self.session_state.username:
            customer_id, subscription_id = self.payment_processor.verify_subscription(session_id, self.session_state.username)
            if customer_id and subscription_id:
                self.db.update_subscription(self.session_state.username, customer_id, subscription_id, 1)
                st.success("Thank you for subscribing to NewsHub Premium! Enjoy ad-free news and exclusive features.")
            else:
                st.error("Subscription verification failed. Please contact support.")
        else:
            st.error("Invalid session. Please try subscribing again.")
        if st.button("Return to NewsHub"):
            st.query_params["page"] = "home"
            st.rerun()

    def show_cancel_page(self):
        st.title("Subscription Cancelled")
        st.warning("You cancelled the subscription process. Upgrade to Premium anytime from the sidebar.")
        if st.button("Return to NewsHub"):
            st.query_params["page"] = "home"
            st.rerun()

    def show_main_app(self):
        st.title("NewsHub: Your News, Your Way")
        if "logged_in" not in self.session_state:
            self.session_state.logged_in = False
            self.session_state.username = ""

        if not self.session_state.logged_in:
            self.show_login_signup()
        else:
            self.show_dashboard()

    def show_login_signup(self):
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        with tab1:
            st.header("Login")
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")
            if st.button("Login"):
                if self.db.verify_user(username, password):
                    self.session_state.logged_in = True
                    self.session_state.username = username
                    st.success("Logged in successfully!")
                    st.rerun()
                else:
                    st.error("Invalid credentials.")
        with tab2:
            st.header("Sign Up")
            new_username = st.text_input("New Username", key="signup_username")
            new_password = st.text_input("New Password", type="password", key="signup_password")
            if st.button("Sign Up"):
                if self.db.add_user(new_username, new_password):
                    st.success("Signed up successfully! Please log in.")
                else:
                    st.error("Username already exists.")

    def show_dashboard(self):
        st.sidebar.header(f"Welcome, {self.session_state.username}")
        if st.sidebar.button("Logout"):
            self.session_state.logged_in = False
            self.session_state.username = ""
            st.rerun()

        is_premium = self.db.is_premium_user(self.session_state.username)
        if is_premium:
            # Check subscription status for premium users
            user_data = self.db.get_user(self.session_state.username)
            if user_data and user_data[1]:  # Check if subscription_id exists
                if not self.payment_processor.check_subscription_status(user_data[1]):
                    # Subscription is no longer active
                    self.db.update_subscription(self.session_state.username, user_data[0], user_data[1], 0)
                    is_premium = False
                    st.warning("Your subscription is no longer active. Please renew to maintain premium access.")
                    st.rerun()

        if not is_premium:
            st.sidebar.subheader("Upgrade to Premium ($5/month)")
            if st.sidebar.button("Subscribe"):
                user_data = self.db.get_user(self.session_state.username)
                stripe_customer_id = user_data[0] if user_data else None
                checkout_url, customer_id = self.payment_processor.create_checkout_session(self.session_state.username, stripe_customer_id)
                if checkout_url:
                    if customer_id and not stripe_customer_id:
                        self.db.update_subscription(self.session_state.username, customer_id, None, 0)
                    st.markdown(f'<meta http-equiv="refresh" content="0;URL={checkout_url}">', unsafe_allow_html=True)
                    st.stop()

        page = st.sidebar.selectbox("Choose a page", ["News Feed", "Saved Articles"])
        if page == "News Feed":
            self.show_news_feed()
        else:
            self.show_saved_articles()

    def show_news_feed(self):
        st.header("Latest News")
        category = st.selectbox("Select Category", ["general", "business", "technology", "sports", "entertainment"])
        articles = self.news_fetcher.fetch_news(category=category)
        is_premium = self.db.is_premium_user(self.session_state.username)

        if not is_premium:
            st.warning("Free users see ads. Upgrade to premium for an ad-free experience!")
            ad_image_path = os.path.join(os.getcwd(), "assets", "my_ad.png")
            if os.path.exists(ad_image_path):
                st.image(ad_image_path, caption="Advertisement", use_column_width=True)
            else:
                st.image("https://via.placeholder.com/468x60?text=Your+Ad+Here", caption="Ad Placeholder")


        for article in articles:
            st.subheader(article["title"])
            st.write(article["description"])
            st.write(f"[Read more]({article['url']})")
            if st.button(f"Save Article: {article['title']}", key=article["url"]):
                self.db.save_article(self.session_state.username, article["url"], article["title"])
                st.success("Article saved!")

    def show_saved_articles(self):
        st.header("Saved Articles")
        articles = self.db.get_saved_articles(self.session_state.username)
        if not articles:
            st.info("No saved articles yet.")
        for title, url, saved_at in articles:
            st.subheader(title)
            st.write(f"[Read more]({url})")
            st.write(f"Saved on: {saved_at}")

if __name__ == "__main__":
    app = NewsHubApp()
    app.run()