# Jobotron 🚀

Jobotron, a playful nod to Megatron from Transformers, is an intelligent job-posting bot that automates finding, summarizing, and sharing job opportunities on Twitter. Powered by Gemini AI, it creates concise tweets with job descriptions and links, keeping job seekers informed and motivated.

---

## Features ✨

- **Job Scraping**: Automatically scrapes job postings from Jobwebghana and Jobberman.
- **AI Summarization**: Uses Gemini AI to summarize job descriptions to fit within a single tweet, complete with a link to apply.
- **Deadline Validation**: Ensures that job deadlines have not passed before posting.
- **Job Reposting**: Saves jobs in a MongoDB database to repost periodically, as long as the deadlines are still valid.
- **Admin Portal**: A password-protected web dashboard to monitor the bot, browse the job queue, read logs, trigger runs manually, and change settings live (schedule, search keywords, sources, posting behavior).
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
   - Copy `example.env` to `.env` and fill in your **X (Twitter) API keys**, **MongoDB connection string**, **Gemini AI API key**, and an **admin portal password** (`ADMIN_PASSWORD`).

---

## Usage 📖

1. Start the bot (FastAPI server + scheduler):
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

2. The bot will:
   - Run a post cycle at the scheduled hours (default 9:00, 12:00, 15:00, 18:00 Africa/Accra).
   - Scrape job listings when the queue runs low, filtered by your configured keywords.
   - Use Gemini AI to summarize job descriptions and post tweets with job details and links.
   - Repost queued jobs (if deadlines are still valid) up to the configured limit.

---

## Admin Portal 🖥️

The server also hosts a web dashboard at `http://<host>:8000/`, protected by `ADMIN_PASSWORD`. From there you can:

- **Dashboard**: DB/scheduler health, queue size, and next scheduled post.
- **Jobs Queue**: browse, open, or delete queued jobs.
- **Controls**: trigger a scrape or a post cycle manually.
- **Logs**: read and download the bot's log file.
- **Settings**: change the posting schedule, job search keywords, enabled sources, and posting behavior. Settings are stored in MongoDB and applied immediately — no restart or redeploy needed.

All API endpoints except `/health` require the `X-Admin-Key` header (the portal handles this after sign-in).

### Portal development

The frontend lives in `admin/` (React + Vite + Tailwind). For local development run `npm run dev` there alongside the API server (requests are proxied to `localhost:8000`). The production build is committed in `admin/dist` and served by FastAPI directly — after changing the frontend, run:

```bash
cd admin && npm run build
```

---

## Technologies Used 🛠️

- **Languages**: Python, JavaScript
- **Backend**: FastAPI + Uvicorn
- **Web Scraping**: BeautifulSoup, Requests
- **AI Summarization**: Gemini AI
- **Database**: MongoDB (via PyMongo)
- **Social Media Integration**: Tweepy (for Twitter API)
- **Environment Management**: Python dotenv
- **Scheduling**: APScheduler
- **Admin Portal**: React, Vite, Tailwind CSS

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

Run the integration check script (needs live credentials in `.env`):
```bash
python test_refactor.py
```

---

## Contact 📬

Created by [Blaise S. Mennia](https://www.linkedin.com/in/blaise-mennia-50b25369/) - feel free to reach out for collaboration or questions!

---

With **Jobotron**, job searching just got smarter. Let the bot work while you focus on landing your dream job! 🚀
