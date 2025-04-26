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


# MediScan AI Pro

## How OOP’s 4 Fundamentals Work in MediScan AI Pro

A concise overview of how **Encapsulation**, **Abstraction**, **Inheritance**, and **Polymorphism** drive MediScan AI Pro’s modular, secure, and scalable design.

- **Encapsulation**: Bundles data/methods in classes. `UserManager` secures user data (hashed passwords), exposing only `authenticate_user`. `DiagnosisEngine` hides Gemini API logic, offering `analyze_image_with_gemini`. Protects data and simplifies use.
- **Abstraction**: Hides complexity via high-level interfaces. `MediScanApp` simplifies diagnosis/UI flow, while `ImageProcessor` abstracts image tasks (`save_image`). Enhances user-friendliness for developers/users.
- **Inheritance**: Implicit in Streamlit’s framework, where `MediScanApp` leverages base classes for UI. Future subclasses (e.g., `BaseProcessor`) could extend `ImageProcessor`. Promotes code reuse, though less prominent.
- **Polymorphism**: Enables flexible method implementations. `ReportGenerator`’s `export_to_csv`/`export_to_json` vary outputs. `HistoryManager`’s `render_history` customizes UI. Boosts extensibility.

**Impact**: Encapsulation and Abstraction ensure secure, simple interactions with AI diagnosis and authentication. Inheritance and Polymorphism support extensibility. Together, they make the code modular, readable, and scalable, powering features like multilingual UI, reminders, and history tracking.

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

---

For Developers
MediScan AI Pro’s modular design makes it easy to extend or integrate into other projects. Key components include:
MediScanConfig: Manages app settings, themes, and translations. Add new languages by updating the translations dictionary.

DiagnosisEngine: Handles Gemini AI integration. Modify analyze_image_with_gemini to integrate other AI models.

ImageProcessor: Processes uploaded images. Extend save_image or validate_image for custom workflows.

UserManager: Manages authentication. Customize authenticate_user for alternative auth systems (e.g., OAuth).

HistoryManager: Stores diagnosis history. Extend export_history for additional formats.

ReminderManager: Manages reminders. Add new reminder types or scheduling logic in add_reminder.

MediScanLogger: Logs actions and metrics. Customize logging formats or destinations in log_action.

To extend the app:
Explore the codebase in app.py and related classes.

Use the modular classes to integrate specific features into your project.

Refer to the logging system (logs/) for debugging.

Test changes in a virtual environment to avoid conflicts.

---

## Project Structure
```
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
```
---

## Dependencies
MediScan AI Pro relies on the following Python libraries (listed in requirements.txt):
streamlit>=1.20.0 - For the web-based UI.

python-dotenv>=0.19.0 - For loading environment variables.

google-generativeai>=0.3.0 - For Gemini AI integration.

pillow>=9.0.0 - For image processing.

pandas>=1.5.0 - For data handling and CSV export.

hashlib - For SHA-256 password hashing (built-in).

json - For JSON data handling (built-in).

logging - For logging system (built-in).

Install all dependencies using:
```
bash

pip install -r requirements.txt

```
## Limitations
While MediScan AI Pro is a powerful tool, it has some limitations:
Diagnostic Accuracy: Relies on Gemini AI, which may not always provide accurate diagnoses, especially for complex or rare conditions. Always consult a medical professional.

Image Requirements: Only supports PNG, JPG, and JPEG formats. Images must be clear and well-lit for accurate analysis.

Body Part Limitation: Currently supports visible body parts (e.g., eye, skin). Internal organs or X-ray/MRI images are not supported.

API Dependency: Requires an active internet connection and valid Gemini API key. API downtime or rate limits may disrupt functionality.

Language Support: Limited to English and Urdu. Additional languages require manual translation updates.

Data Storage: Stores user data locally (user_data.json, history.json). Not designed for large-scale or cloud-based deployments without modification.

Scalability: Built for individual or small-scale use. High user volumes may require database integration (e.g., SQLite, MongoDB).

Future updates may address these limitations by expanding AI capabilities, adding cloud storage, and supporting more image types.

## Contributing
Contributions are welcome to enhance MediScan AI Pro! 

Make Changes:
Follow the coding style in app.py (PEP 8).

Update documentation for new features.

Add tests if possible.

Commit and Push:
```
bash

git commit -m "Add your feature description"
git push origin feature/your-feature-name

```
Submit a Pull Request:
Open a PR on GitHub with a clear description of changes.

Reference any related issues.

Contribution Ideas:
Add support for new languages in MediScanConfig.

Integrate additional AI models for diagnostics.

Enhance reminder scheduling with calendar integration.

Add cloud storage for user data.

Improve UI with custom Streamlit components.

Please adhere to the Code of Conduct (CODE_OF_CONDUCT.md) when contributing.
## License
MediScan AI Pro is licensed under the MIT License. You are free to use, modify, and distribute the code, provided you include the original copyright notice and license. See the LICENSE file for details.
## Contact
For questions, feedback, or collaboration, reach out to the developer:
Areeba Irfan

Email: the.areebairfan@gmail.com

GitHub:[ areeba irfan](https://github.com/AreebaxIrfan/)

Project Repository: [MediScan AI Pro](https://github.com/AreebaxIrfan/GIAIC_Q3/tree/main/%F0%9F%93%82Class_Assignment/assignment_07)

For issues or bugs, please open a ticket on the GitHub repository.
Built with  by Areeba Irfan | Powered by Gemini AI | © 2025


---
