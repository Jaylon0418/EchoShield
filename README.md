**EchoShield** is a floating chat assistant that enhances digital communication through **real-time AI interaction, non-violent communication guidance and more**. It helps users refine their expressions, making conversations more constructive and friendly.  

## ✨ Features  

✅ **Floating Chat Window** – Always-on-top UI for seamless interaction.  
✅ **Live Keyboard Monitoring** – Captures user input in real time.  
✅ **AI-Powered Sentiment Refinement** – Uses **non-violent communication (NVC)** to suggest improved expressions.  
✅ **Teen Mode** – Detects and covers offensive language on the entire screen.  
✅ **Instant AI Feedback** – Provides real-time, constructive communication suggestions.  

## 🛠️ Technologies Used  

- **Python** (Primary Language)  
- **PyQt5** (GUI)  
- **DBAI API** (AI-based message refinement)  
- **PyAutoGUI + OCR (Tesseract)** (Screen text detection & filtering)  

## 📦 Installation  

### 1️⃣ Clone the repository

git clone https://github.com/YOUR-GITHUB-USERNAME/SentinelUI.git
cd SentinelUI

### 2️⃣ Install dependencies

pip install -r requirements.txt

### 3️⃣ Set up DBAI API key

Create an environment variable for your DBAI API Key:

export ARK_API_KEY="your_api_key_here"  # For Mac/Linux
set ARK_API_KEY="your_api_key_here"  # For Windows

### 4️⃣ Run the application

python PyQT5.py

## 🎮 Usage
	•	Run SentinelUI, and a floating chat window will appear.
	•	Type your message, and AI will analyze and suggest improvements.
	•	Enable Teen Mode to automatically filter inappropriate language on the screen.
	•	Minimize or close the chat window when not in use.

## 📦 Packaging for Deployment

To create a standalone executable:

pyinstaller --onefile --windowed --name "EchoShield" PyQT5.py

For MacOS .app:

pyinstaller --onefile --windowed --name "Echoshield" --hidden-import PyQt5.sip PyQT5.py

## 🤝 Contributing

Contributions are welcome! Feel free to fork the project, submit pull requests, or report issues.

## 🚀 Refine. Communicate. Protect.

---

### **🛠 Key Points in this README:**
✅ **Clear Overview** – What the project does.  
✅ **Feature List** – Explains why it's useful.  
✅ **Installation Guide** – Simple, step-by-step setup.  
✅ **Usage Instructions** – How users interact with it.  
✅ **Deployment Guide** – How to create `.exe` or `.app` files.  
✅ **Contribution & License** – For future improvements.  

---

### 💡 **Need Customization?**
- If you want a **more minimal or detailed version**, let me know! 😃
