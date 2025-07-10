import asyncio
from scraper.link_finder import fetch_architecture_objects
from scraper.architecture_page_scraper import parse_architecture_page

async def main():
    page_num = 0  # You can loop over skip counts if needed
    print(f"🔍 Fetching architecture metadata from API response...")
    architectures = await fetch_architecture_objects(page_num)

    print(f"\n🚀 Parsing {len(architectures)} architecture pages...\n")
    for arch in architectures:
        url = "https://learn.microsoft.com" + arch.get("url", "")
        print(f"📄 Parsing: {url}")
        detailed_data = parse_architecture_page(url)
        # Here you could merge API data + Soup data, or store them both.
        print(f"✅ Done parsing: {url}\n")

if __name__ == "__main__":
    asyncio.run(main())
