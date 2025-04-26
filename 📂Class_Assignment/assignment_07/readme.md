# MediScan AI Pro

**MediScan AI Pro** is a cutting-edge, AI-powered medical image diagnostic tool built with Streamlit and powered by Google's Gemini AI. It enables users to upload images of visible body parts (e.g., eye, skin) for automated diagnosis, delivering disease identification, treatment recommendations, and medication suggestions. The application also includes robust features like user authentication, diagnosis history tracking, reminder management, and multilingual support (English and Urdu). Designed for both healthcare accessibility and developer extensibility, MediScan AI Pro is a versatile tool for medical diagnostics and AI-driven applications.

**Built with ❤️ by Areeba Irfan | Powered by Gemini AI | © 2025**

---

## Table of Contents

- [Features](#features)
- [Why MediScan AI Pro?](#why-mediscan-ai-pro)
  - [Unique and Reusable Aspects](#unique-and-reusable-aspects)
  - [Best Part](#best-part)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [For End Users](#for-end-users)
  - [For Developers](#for-developers)
- [Project Structure](#project-structure)
- [Dependencies](#dependencies)
- [Limitations](#limitations)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Features

- **AI-Powered Diagnosis**: Upload images of body parts (eye, skin, etc.) for accurate diagnosis using Google's Gemini AI.
- **Multilingual Support**: User interface available in English and Urdu, with a flexible translation system for adding more languages.
- **Secure User Authentication**: Login and registration with SHA-256 password hashing for data security.
- **Diagnosis History**: Store, view, and export past diagnoses in CSV, JSON, or TXT formats.
- **Reminder Tracker**: Automated reminders for doctor visits, medication schedules, and rest periods.
- **Customizable Settings**: Switch between light/dark themes and select preferred language.
- **Comprehensive Logging**: Tracks user actions, system metrics, and recommendations for debugging and analytics.
- **Responsive UI**: Built with Streamlit for a clean, intuitive, and responsive interface.
- **Modular Architecture**: Organized codebase with reusable classes for easy integration into other projects.
- **Error Handling**: Robust handling of API failures, invalid inputs, and file operations.

---

## Why MediScan AI Pro?

### Unique and Reusable Aspects
MediScan AI Pro stands out due to its thoughtful design and developer-friendly architecture:
- **Modular Class Structure**: The codebase is divided into independent classes (`MediScanConfig`, `DiagnosisEngine`, `ImageProcessor`, `UserManager`, etc.), allowing developers to reuse specific components without adopting the entire application.
- **Extensible Translation System**: The `MediScanConfig` class uses a dictionary-based translation system, making it simple to add new languages by updating the `translations` dictionary.
- **Secure Authentication**: Implements SHA-256 hashing for password storage, ensuring user data privacy and security.
- **Flexible Data Export**: Supports multiple formats (CSV, JSON, TXT) for diagnosis history, enabling integration with other tools or workflows.
- **AI Integration**: Seamlessly connects with Gemini AI for image-based diagnostics, with fallback mechanisms for API errors.
- **Customizable UI**: Theme (light/dark) and language settings enhance accessibility and user experience, with easy hooks for further customization.
- **Comprehensive Logging**: The `MediScanLogger` class provides detailed logs for user actions, system metrics, and AI recommendations, useful for debugging and analytics.

These features make MediScan AI Pro reusable in various contexts, such as healthcare apps, AI diagnostic tools, or educational projects.

### Best Part
The **best part** of MediScan AI Pro is its **end-to-end diagnostic pipeline**, which integrates AI-driven analysis, a user-friendly interface, and actionable healthcare features. The combination of Gemini AI's accurate diagnosis with automated reminders for doctor visits, medication, and rest creates a holistic tool that empowers users to take charge of their health. For developers, the modular codebase and clear documentation make it an ideal foundation for building or extending AI-powered medical applications. The reminder system, in particular, stands out for its proactive approach to healthcare, ensuring users follow through on critical actions.

---

## Prerequisites

To run or integrate MediScan AI Pro, you need:
- **Python 3.8+**
- **Google Gemini API Key** (obtain from Google and configure in a `.env` file)
- **Internet Connection** (for Gemini AI API calls)
- **Dependencies** (listed in `requirements.txt`)

---

## Installation

Follow these steps to set up MediScan AI Pro locally:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/mediscan-ai-pro.git
   cd mediscan-ai-pro
   ```
2. **Create a Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
5. **Set Up Environment Variables:**
   ```bash
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
6. **Run the Application:**
   ```bash
   streamlit run app.py
   ```


# Usage

## For End Users
MediScan AI Pro is designed to be intuitive for non-technical users. Here's how to use it:

### Login or Register
- Create an account or log in to access full functionality.
- Registration requires a username (>3 characters) and password (>5 characters).

### Diagnose
- Upload an image (PNG, JPG, or JPEG) of a body part (e.g., eye, skin).
- Select the body part from the dropdown menu.
- Click "Diagnose" to receive AI-generated results, including diagnosis, description, treatment, and medication suggestions.

### View History
- Access past diagnoses with details and uploaded images under the "History" tab.

### Track Reminders
- View and manage reminders for doctor visits, medications, or rest in the "Reminder Tracker" tab.
- Mark reminders as complete or dismiss them as needed.

### Export Data
- Download diagnosis history in CSV, JSON, or TXT formats from the "Download All Data" tab.

### Customize
- Adjust language (English/Urdu) and theme (Light/Dark) in the "Settings" tab.

### Provide Feedback
- Share feedback and rate the app (1-5) in the "Feedback" tab.

**Note**: AI diagnoses are not a substitute for professional medical advice. Always consult a certified doctor for confirmation.



## Project Structure

mediscan-ai-pro/
├── Uploads/                  # Directory for uploaded images
├── logs/                     # Directory for log files
├── .env                      # Environment variables (e.g., GEMINI_API_KEY)
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── user_data.json            # User credentials (auto-generated)
├── history.json              # Diagnosis history (auto-generated)
├── reminders.json            # Reminders data (auto-generated)
└── README.md                 # This documentation

