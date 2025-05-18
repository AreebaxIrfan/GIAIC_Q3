# 📰 NewsHub

**NewsHub** is a Streamlit-based news aggregation app that allows users to browse top headlines, save articles, and upgrade to a premium plan for an ad-free experience.

## 🚀 Features

- 🔐 User Authentication (Sign up & Log in)
- 🗞️ Browse News by Category (general, business, tech, sports, entertainment)
- 💾 Save Articles for Later
- 💳 Premium Subscription via Stripe ($5/month)
- 🚫 Ad-Free Experience for Premium Users
- 🌐 NewsAPI Integration for real-time headlines

## 🛠️ Tech Stack

- **Frontend/Backend**: Streamlit
- **Database**: SQLite
- **APIs**: NewsAPI, Stripe
- **Auth**: bcrypt
- **Env Config**: python-dotenv

## 📦 Installation

```bash
git clone <repo-url>
cd newshub  # or D:\class_09
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
🔑 Configuration
Create a .env file:
NEWS_API_KEY=your_news_api_key
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_PRICE_ID=price_...
DOMAIN_URL=http://localhost:8501
🖼️ Add Advertisement Image
Place a small banner in:
assets/my_ad.png  # (Recommended: 468x60px, <2MB)
▶️ Run the App
bash
Copy code
streamlit run app.py
Open in browser: http://localhost:8501

🧪 Test Stripe (Optional)
Use test card 4242 4242 4242 4242 with any expiry & CVC.

❗ Troubleshooting
🔑 NewsAPI 401: Check NEWS_API_KEY

💵 Stripe Price Error: Verify STRIPE_PRICE_ID

🖼️ Image Not Found: Ensure assets/my_ad.png exists

🗃️ DB Issues: Delete newshub.db and restart the app

📤 Deployment Tips
Use HTTPS in DOMAIN_URL

Add Stripe webhooks for live updates

Secure .env and newshub.db

🤝 Contributing
Fork the repo

Create a branch: git checkout -b feature/xyz

Commit: git commit -m "Add xyz"

Push: git push origin feature/xyz

Open a Pull Request

© 2025 NewsHub — Built with ❤️ using Streamlit