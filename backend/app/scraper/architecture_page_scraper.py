import requests
from bs4 import BeautifulSoup

def parse_architecture_page(url: str):
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/134.0.0.0 Safari/537.36"
            )
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Title
        title_tag = soup.find("h1")
        title = title_tag.get_text(strip=True) if title_tag else "N/A"

        # Main content container
        content_div = soup.find("div", class_="content") or soup.find("div", class_="content-body")
        if not content_div:
            raise ValueError("Main content container not found.")

        # Capture all relevant content
        valid_tags = ["h1", "h2", "h3", "h4", "p", "li"]
        content_blocks = content_div.find_all(valid_tags)

        structured_content = []
        for tag in content_blocks:
            text = tag.get_text(strip=True)
            if text and len(text.split()) > 3:  # avoid noise
                structured_content.append(f"[{tag.name.upper()}] {text}")

        return {
            "url": url,
            "page_title": title,
            "structured_content": structured_content
        }

    except Exception as e:
        print(f"❌ Failed to parse {url}:\n   ↳ {e}")
        return {}

def main():
    test_url = "https://learn.microsoft.com/en-us/azure/architecture/ai-ml/architecture/baseline-azure-ai-foundry-chat"
    result = parse_architecture_page(test_url)

    if result:
        print(f"🔗 URL: {result['url']}")
        print(f"🧠 Page Title: {result['page_title']}\n")
        print("🧩 Structured Content Blocks:")
        for block in result['structured_content'][:20]:  # Preview first 20
            print(f"- {block}")
    else:
        print("No content extracted.")

if __name__ == "__main__":
    main()
