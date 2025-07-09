import asyncio
from playwright.async_api import async_playwright

async def fetch_architecture_objects(page_num: int):
    base_url = "https://learn.microsoft.com"
    target_url = f"{base_url}/en-us/azure/architecture/browse/?expanded=azure&skip={page_num}"
    api_prefix = "/api/contentbrowser/search/architectures"
    collected_objects = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        async def capture_response(response):
            if api_prefix in response.url and response.status == 200:
                data = await response.json()
                results = data.get("results", [])
                collected_objects.extend(results)
                print(f"✅ Captured {len(results)} architecture objects from: {response.url}")

        page.on("response", capture_response)
        await page.goto(target_url)
        await page.wait_for_timeout(5000)

        await browser.close()
        return collected_objects


async def main():
    page_num = 0  # you can loop later, start with 0
    architectures = await fetch_architecture_objects(page_num)

    print(f"\n🎯 Total architecture objects found: {len(architectures)}\n")
    for arch in architectures:
        print(f"🔹 {arch.get('title')}")
        print(f"   ➤ URL: https://learn.microsoft.com{arch.get('url')}")
        print(f"   ➤ Summary: {arch.get('summary')}")
        print(f"   ➤ Products: {arch.get('display_products')}")
        print(f"   ➤ Categories: {arch.get('display_azure_categories')}")
        print()

if __name__ == "__main__":
    asyncio.run(main())
