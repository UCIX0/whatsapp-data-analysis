
# 🧭 App Directory – WhatsApp Chat Analyzer

This folder contains the **core logic and components** of the WhatsApp Chat Analyzer application, organized into modular packages.

Use this as a guide to navigate to the appropriate part of the codebase depending on what you need to modify or understand.

---

## 📁 Submodules Overview

| Module                     | Description                                                                                                                      |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| [`pipeline/`](./pipeline/) | 📥 Responsible for parsing, cleaning, and transforming raw WhatsApp `.txt` chat exports into structured and filtered DataFrames. |
| [`analysis/`](./analysis/) | 📊 Performs statistical computations and generates visualizations based on the cleaned data.                                     |
| [`services/`](./services/) | 🧩 Orchestrates the full analysis workflow, including caching logic and integration of the pipeline and analysis components.     |
| [`ui/`](./ui/)             | 🖼 Renders the interactive Streamlit user interface, including navigation, tables, charts, and summary info cards.               |

---

## 📌 Entry Points by Purpose

| Goal                           | Start Here                                                                                                              |
| ------------------------------ | ----------------------------------------------------------------------------------------------------------------------- |
| Parse and clean WhatsApp chats | [`pipeline/chat_to_df.py`](./pipeline/chat_to_df.py) and [`pipeline/clean_dataframe.py`](./pipeline/clean_dataframe.py) |
| Analyze message patterns       | [`analysis/stats.py`](./analysis/stats.py)                                                                              |
| Detect conversation starters   | [`analysis/analizar_inicios.py`](./analysis/analizar_inicios.py)                                                        |
| Build charts and word clouds   | [`analysis/visualization.py`](./analysis/visualization.py)                                                              |
| Coordinate app logic & caching | [`services/data_manager.py`](./services/data_manager.py)                                                                |
| Modify the user interface      | [`ui/render_pages.py`](./ui/render_pages.py) and [`ui/optionbar.py`](./ui/optionbar.py)                                 |

---

📎 All folders include their own `README.md` with more detailed documentation.