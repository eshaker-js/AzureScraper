# Azure Architecture Scraper

This is my submission of the Azure Cloud Architecture Scraper assignment as part of a job application.

Tech Stack was chosen according to the requirements, but here are the specifics:

- Backend - FastAPI + Python
- Frontend - React + Vite
- Database - MongoDB
- DevOps - Docker + Docker Compose



## Run Locally

1. **Clone the Repo**

   ```bash
   git clone https://github.com/eshaker-js/AzureScraper.git
   cd azure-architecture-scraper
   ```

2. **Start with Docker Compose**

   ```bash
   docker-compose up -d --build
   ```

3. **Visit in Your Browser**

   Navigate to:
   `http://localhost:80`



## How I approached this task.

### 1. Finding the API  
After a quick read of the requirements for the assignment, I visited the "Browse Azure Architectures" page on Learn Microsoft.  
After some tinkering in the DevTools I found the API request that fetches all the architectures featured.  
At first I struggled hitting the API endpoint directly so I tried using Selenium and Playwright (for session cookies and headers), but eventually figured out what I was doing wrong and managed to go straight to the source (the api endpoint).  

The payload I got back was very informative, includes:

- Title  
- Summary  
- Thumbnail  
- Categories (used by Microsoft)
- Products used  
- URL  

### 2. Scraping Detail Pages  
To enrich the architecture data, I tried visiting each url I got back in the payload with hopes of learning more about the architecture.  
This was difficult due to inconsistent HTML structure..  
The pages sometimes used paragaraphs, sometimes li (list) elements for normal sentences.
In general the flow of each architecture page was different, which made it difficult to come up with a "one size fits all" solution. 
In the end after looking at the requirements, the quote  
  
  _"Organizations spend millions on cloud infrastructure but struggle to find the best cloud
architecture solutions for their use case."_   
  
  stood out to me, so I decided to scrape the **Potential Use Cases** section that was frequently featured in those individual articles.  

  
  Somtimes that section didn't exist, which made me consider the AI hint in the assignment document, however, I didn't want to use a paid 3rd party LLM, I experimented with HuggingFace transofmers and other local LLMs, but the results were unimpressive to say the least..  

  If this was a real task, of course, we could access OpenAI's API and we would've seen very nice results!

### 3. Backend API

| Method | Endpoint         | Description                                  |
|--------|------------------|----------------------------------------------|
| POST   | `/architectures` | Triggers a new scrape and stores in MongoDB  |
| GET    | `/architectures` | Returns the stored architecture list         |

Duplicate entries are avoided by using the **architecture URL as a unique identifier**.

### 4. Frontend Dashboard  
The UI includes:
- A **home screen** with a "Get Started" button
- A **dashboard** with:
  - "Load Info" – pulls from the DB  
  - "Scrape More Architectures" – fetches fresh entries and reloads  

Architectures are displayed in styled cards showing:
- Thumbnail  
- Title + summary  
- Products used (tags)  
- Use cases (if any)  
- Fetched timestamp  

### 5. Challenges Faced

As previously discussed:

- Microsoft’s structure is **inconsistent**. 
- I thought the API endpoint was blocking me due to session cookies or headers, but I'm glad I avoided Selenium because I think waiting for a chromium boot would've worsened the performance.
- I experimented with **transformers/LLMs** to auto-generate use cases based on the text on the article page but **skipped it** due to underwhelming results.

---

### Personal Note

Thank you for the opportunity, I had to crunch a bit because I am unavailable this weekend and didn't want to miss out on my chance because of submission time.  
Definitely utilized AI tools to make this project come about so quickly, mainly for scaffolding and boilerplate code, as well as debugging.  
However I hope I managed to showcase my understanding of Backend development, networking principles, fullstack structure, DevOps, and documentation.

I would love to hear back from you!

\- Jan


Jan Salama - bojan.salama@gmail.com - 0548012822
