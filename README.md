# 📊 WhatsApp Data Analysis Project

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Analyze and visualize WhatsApp chat exports with a powerful, intuitive, and customizable Python tool!  
Get insights into messaging patterns, conversation starters, most active users, and much more.

![Demo Screenshot](https://via.placeholder.com/900x400?text=WhatsApp+Data+Analysis+Demo)

---

## ✨ Features

- 📜 Parse WhatsApp chats (Android and iOS formats)
- 🧹 Clean messy, multi-line messages automatically
- 📈 Visualize activity over time
- 🗣️ Identify who initiates conversations most often
- ☁️ Generate word clouds from chat content
- 🔧 Customize filtering and analysis via `config.yaml`
- 🌐 Multilingual (supports English & Spanish chats)
- 🖥️ Beautiful web app interface using Streamlit

---

## 👢 Project Structure

```bash
whatsapp-data-analysis/
├── app/
│   ├── analysis/
│   │   ├── __init__.py
│   │   ├── analizar_inicios.py    # Conversation starter analysis
│   │   ├── stats.py               # Statistical calculations
│   │   └── visualization.py       # Visualization functions
│   ├── pipeline/
│   │   ├── __init__.py
│   │   ├── chat_parser.py         # Raw chat parsing
│   │   ├── chat_to_df.py          # DataFrame conversion
│   │   └── clean_dataframe.py     # Data cleaning
│   ├── __init__.py
│   ├── config.yaml                # Configuration settings
│   ├── environment.yml            # Conda environment specification
│   ├── main.py                    # Streamlit application
│   └── README.md
├── .gitignore
└── README.md (this file)
```

---

## ⚙️ Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone https://github.com/bielng/whatsapp-data-analysis.git
   cd whatsapp-data-analysis
   ```

2. **Create and activate the environment:**

   ```bash
   conda env create -f app/environment.yml
   conda activate whatsapp-proyect
   ```

3. **Run the Streamlit app:**
   ```bash
   streamlit run app/main.py
   ```

---

## 📋 How to Use

1. **Export your WhatsApp chat** (without media) from WhatsApp:

   - Chat → More Options → Export Chat → Without Media.

2. **Upload the exported `.txt` file** into the app.

3. **Explore results:**
   - Conversation starter statistics 📈
   - Message frequency over time 🗕️
   - Word clouds ☁️
   - User activity patterns 🔥

---

## 📚 Key Components

| Component             | Purpose                                                    |
| :-------------------- | :--------------------------------------------------------- |
| `chat_parser.py`      | Parse raw WhatsApp chat text                               |
| `chat_to_df.py`       | Convert parsed chat to Pandas DataFrame                    |
| `stats.py`            | Generate statistics (messages per user, activity patterns) |
| `analizar_inicios.py` | Detect who starts conversations                            |
| `visualization.py`    | Create beautiful plots and word clouds                     |
| `main.py`             | Main Streamlit web app                                     |

---

## 💅 Example Outputs

### Conversation Starters Table

| User  | Conversations Started | %   |
| ----- | --------------------- | --- |
| Alice | 42                    | 58% |
| Bob   | 30                    | 42% |

### Message Frequency Over Time

_(Streamlit line graph based on daily or monthly message counts)_

### Word Cloud Example

_(Automatically generated from the most frequent words)_

---

## 🔗 Dependencies

- [Python 3.11](https://www.python.org/)
- [Pandas](https://pandas.pydata.org/)
- [Matplotlib](https://matplotlib.org/)
- [Seaborn](https://seaborn.pydata.org/)
- [Streamlit](https://streamlit.io/)
- [Wordcloud](https://amueller.github.io/word_cloud/)
- [PyYAML](https://pyyaml.org/)
- [emoji](https://pypi.org/project/emoji/)

> Full dependency list in `app/environment.yml`

---

## 📢 Configuration

Customize analysis settings in `app/config.yaml`:

- Filter system messages
- Ignore deleted messages
- Skip multimedia notifications
- Adjust user name matching

---

# 👍🏼 How to Contribute

We welcome contributions to **WhatsApp Data Analysis**! 🚀  
Follow these simple steps to make your contribution count:

## 🛠️ Contribution Workflow

1. **Fork the repository**  
   ➔ Click the `Fork` button at the top right of this page to create your own copy.

2. **Clone your fork locally**

   ```bash
   git clone https://github.com/your-username/whatsapp-data-analysis.git
   cd whatsapp-data-analysis
   ```

3. **Create a new branch for your changes**

   ```bash
   git checkout -b your-branch-name
   ```

   _Branch names should be descriptive like `improve-readme`, `fix-chat-parser`, or `add-visualization`._

4. **Make your changes**

   - Edit the files with your improvements.
   - Save and test your changes locally.

5. **Stage and commit your changes**

   ```bash
   git add .
   git commit -m "Clear description of what you changed"
   ```

6. **Push your branch to GitHub**

   ```bash
   git push origin your-branch-name
   ```

7. **Open a Pull Request (PR)**
   - Go to your repository on GitHub.
   - Click "**Compare & Pull Request**."
   - Write a clear title and description of what you changed.
   - Submit your PR for review.

---

## 📜 Good Practices

- Always make your changes in a **new branch**, not directly on `main`.
- Keep your **commits small and focused**.
- Write **clear commit messages**.
- If fixing a bug, **reference the issue number** in your PR.
- Be **respectful and clear** in communication.

---

## 📢 Need Help?

If you're stuck or have questions, feel free to open an [Issue](https://github.com/bielng/whatsapp-data-analysis/issues) or ask in the Pull Request comments.

---

# 🚀 Happy Analyzing and Contributing! 📊💬

- Participants
  - Javier Uc Ix
  - Taban Ngunar
