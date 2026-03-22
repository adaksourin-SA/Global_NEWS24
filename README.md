🚀 Overview

Global News 24 is a desktop news aggregation application built using
Python and Tkinter. It fetches real-time headlines using NewsAPI and
presents them in a clean, scrollable interface with support for
bookmarking and persistent user state.

This project focuses on combining API integration, GUI design,
asynchronous operations, and state management into a cohesive desktop
application.

✨ Features 
🗞️ News Browsing Fetch real-time headlines using NewsAPI
Browse categorized news: General, Business, Health, Sports, Science, Technology
Smooth scrolling interface for multiple articles 
🔍 Search Functionality 
Search news by keywords 
Dynamically updates results 
⚡ Performance Optimizations
Multi-threaded API calls (non-blocking UI)
Local image caching for faster rendering
⭐ Bookmark System
Save/Removebookmarks (toggle functionality)
Persistent storage using JSON 
Visual feedback (button color changes) 
Bookmark state retained across sessions
📂 Bookmark Manager
Dedicated bookmarks window
Scrollable list of saved articles
Open or remove bookmarks directly
🌐 Article Access 
Open full articles in browser with one click 
📊 UI/UX Enhancements
  Dynamic content rendering (no hardcoded layouts)
  Loading indicator (progress bar)
  Structured layout with responsive components 
🧠 Technical Highlights
  Modular Architecture
    main.py → entry point
    ui.py → GUI logic
    api.py → API handling
    utils.py → caching & bookmarks
  Concurrency
    Threading used for API calls to prevent UI freezing
  State Management
    Bookmark persistence using JSON 
    UI synchronized with stored state
  Custom Scroll System
    Canvas + Frame + Scrollbar pattern for dynamic content 
    
⚙️ Installation 
1️⃣ Clone the repository 
  git clone https://github.com/adaksourin-SA/Global_NEWS24 cd news-app 
2️⃣ Install dependencies 
  pip install -r requirements.txt 
3️⃣ Add your News API key
  In main.py:
  API_KEY = \"YOUR_API_KEY\"
  #Get your API key from: https://newsapi.org/
▶️ Run the App
python main.py

🔮 Future Improvements
📊 News analytics (most frequent topics) 
🧠 Sentiment analysis of articles
🗂️ Filter bookmarks by category/source
🌍 Country-based news filtering
💾 SQLite integration instead of JSON


🤝 Contributing
Feel free to fork this repo and submit pull requests. Suggestions and
improvements are welcome!

📜 License
This project is open-source and available under the MIT License.
