from bs4 import BeautifulSoup
import httpx
import asyncio

BASE_URL = "https://learn.microsoft.com"
TARGET_URL = f"{BASE_URL}/en-us/azure/architecture/browse/"


async def scrape_index_page():
    async with httpx.AsyncClient() as client:  # Start httpx client

        # response check
        response = await client.get(TARGET_URL)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch page: {response.status_code}")

        soup = BeautifulSoup(response.text, "lxml")
        print(soup)
        # cards = soup.select("div.card")

        # results = []
        # for card in cards:
        #     link_tag = card.select_one("a")
        #     title_tag = card.select_one("h3")
        #     desc_tag = card.select_one("p")

        #     if not link_tag or not title_tag:
        #         continue

        #     results.append(
        #         {
        #             "title": title_tag.text.strip(),
        #             "url": BASE_URL + link_tag["href"],
        #             "description": desc_tag.text.strip() if desc_tag else "",
        #         }
        #     )

        # return results


if __name__ == "__main__":
    asyncio.run(scrape_index_page())
