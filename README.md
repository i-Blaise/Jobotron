# Jobotron 🚀

Jobotron, a playful nod to Megatron from Transformers, is an intelligent job-posting bot that automates finding, summarizing, and sharing job opportunities on Twitter. Powered by Gemini AI, it creates concise tweets with job descriptions and links, keeping job seekers informed and motivated.

---

## Features ✨

- **Job Scraping**: Automatically scrapes job postings from multiple websites.
- **AI Summarization**: Uses Gemini AI to summarize job descriptions to fit within a single tweet, complete with a link to apply.
- **Deadline Validation**: Ensures that job deadlines have not passed before posting.
- **Motivational Posts**: Periodically posts motivational messages and job-search tips using Gemini AI.
- **Job Reposting**: Saves jobs in a MongoDB database to repost periodically, as long as the deadlines are still valid.
- **Easy Setup**: Includes a `requirements.txt` file for effortless installation of dependencies.

---

## Installation 💻

Follow these steps to set up Jobotron on your local machine:

1. Clone the repository:
   ```bash
   git clone https://github.com/i-Blaise/Jobobot.git
   cd jobotron
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate     # For Windows
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your environment variables:
   - Add your **Twitter API keys**, **MongoDB connection string**, and **Gemini AI API key** to a `.env` file.
   - Example `.env` file content:
     ```env
     TWITTER_API_KEY=your_api_key
     TWITTER_API_SECRET=your_api_secret
     MONGO_URI=your_mongodb_connection_string
     GEMINI_AI_KEY=your_gemini_api_key
     ```

---

## Usage 📖

1. Run the main script to start the bot:
   ```bash
   python index.py
   ```

2. The bot will:
   - Scrape job listings from predefined websites.
   - Use Gemini AI to summarize job descriptions and generate motivational tweets.
   - Post tweets with job details and links.
   - Post up to 10 time per day (5 job post and 5 motivtional and job search tip tweets
   - Periodically repost jobs stored in MongoDB (if deadlines are still valid).

---

## Technologies Used 🛠️

- **Languages**: Python
- **Web Scraping**: BeautifulSoup, Requests
- **AI Summarization**: Gemini AI
- **Database**: MongoDB (via PyMongo)
- **Social Media Integration**: Tweepy (for Twitter API)
- **Environment Management**: Python dotenv
- **Scheduling**: Python `schedule` module

---

## Motivation 🌟

Jobotron was created to assist job seekers by automating the discovery and sharing of job opportunities. It also aims to provide encouragement and guidance for individuals navigating the job market.

---

## Future Improvements 🔮

- Add support for more job scraping sources.
- Enhance AI summarization for even more concise and engaging tweets.
- Integrate analytics to measure tweet engagement and improve content strategy.
- Include support for multiple social media platforms (e.g., LinkedIn).
- Add Images to tweets to diversify types of content (AI generated images and images scraped from job listings)

---

## Testing 🧪

Run unit tests to ensure everything works as expected:
```bash
pytest tests/
```

---

## Contact 📬

Created by [Blaise S. Mennia](https://www.linkedin.com/in/blaise-mennia-50b25369/) - feel free to reach out for collaboration or questions!

---

With **Jobotron**, job searching just got smarter. Let the bot work while you focus on landing your dream job! 🚀
```
