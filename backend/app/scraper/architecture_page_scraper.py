import re
import requests
import json
from bs4 import BeautifulSoup

# Optional: uncomment if you want the LLM fallback
# from openai import OpenAI
# llm = OpenAI()


def extract_use_cases(soup: BeautifulSoup):
    # 1) Try to find explicit “Use cases”–style headings
    sections = {}
    for h in soup.find_all(["h1", "h2", "h3", "h4"]):
        key = h.get_text(strip=True).lower()
        # grab the next <ul> or <ol> or <p>
        nxt = h.find_next_sibling(lambda t: t.name in ("ul", "ol", "p"))
        if nxt:
            sections[key] = nxt

    for label in ("use cases", "potential use cases", "scenarios", "when to use this"):
        if label in sections:
            # return list items if it’s a list, or split a paragraph
            node = sections[label]
            if node.name in ("ul", "ol"):
                return [li.get_text(strip=True) for li in node.find_all("li")]
            else:
                return [s.strip() for s in node.get_text().split(".") if s.strip()]

    # 2) Heuristic: pick sentences with “for” in the first paragraph
    first_p = soup.find("div", class_="content").find("p")
    if first_p:
        sentences = re.split(r"\.\s+", first_p.get_text())
        heuristics = [s for s in sentences if " for " in s.lower()]
        if heuristics:
            return heuristics[:5]

    # 3) (Optional) LLM fallback to infer use cases
    # desc = first_p.get_text(strip=True)
    # prompt = f"""
    # Extract 3–5 potential real-world use cases from this Azure architecture description:
    # \"\"\"{desc}\"\"\"
    # Return them as a JSON array of short sentences.
    # """
    # resp = llm.chat.create(model="gpt-4o", messages=[{"role":"user","content":prompt}])
    # return resp.choices[0].message.content  # parse JSON as needed

    return []


def parse_architecture_page(url: str):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/134.0.0.0 Safari/537.36"
        )
    }
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "lxml")

    # Page title
    title = soup.find("h1").get_text(strip=True) if soup.find("h1") else "N/A"

    # 🔍 Pick the <div class="content"> with the most text inside
    content_divs = soup.find_all("div", class_="content")
    if not content_divs:
        raise RuntimeError("No <div class='content'> blocks found")

    content_div = max(content_divs, key=lambda d: len(d.get_text(strip=True)))

    # Structured content extraction
    blocks = []
    for tag in content_div.find_all(["h1", "h2", "h3", "h4", "p", "li"]):
        text = tag.get_text(strip=True)
        if text and len(text.split()) > 3:
            blocks.append({"tag": tag.name, "text": text})

    # Extract use cases
    use_cases = extract_use_cases(soup)

    return {
        "url": url,
        "page_title": title,
        "structured_content": blocks,
        "use_cases": use_cases,
    }


def main():
    test_url = "https://learn.microsoft.com/en-us/azure/architecture/ai-ml/architecture/baseline-azure-ai-foundry-chat"
    result = parse_architecture_page(test_url)

    if result:
        print(f"🔗 URL: {result['url']}")
        print(f"🧠 Page Title: {result['page_title']}\n")
        print("🧩 Structured Content Blocks (first 20):")
        for block in result["structured_content"][:20]:
            print(f"- [{block['tag'].upper()}] {block['text']}")
        print("\n🎯 Use Cases:")
        for uc in result["use_cases"]:
            print(f"- {uc}")
    else:
        print("No content extracted.")


def main():
    test_url = "https://learn.microsoft.com/en-us/azure/architecture/ai-ml/architecture/baseline-azure-ai-foundry-chat"
    result = parse_architecture_page(test_url)

    # Pretty-print as JSON
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
