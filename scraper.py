import asyncio
import os
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

async def scrape_uoft():
    # 1. Setup the browser (Headless means no window pops up)
    browser_config = BrowserConfig(headless=True, verbose=True)
    
    # 2. Setup the crawler config to extract clean Markdown
    run_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,  # Ensure we get fresh data, not old cache
        markdown_generator=DefaultMarkdownGenerator(
            options={"ignore_links": False, "body_width": 120}
        )
    )

    # 3. List of "High Value" targets we found for you
    urls = [
        "https://www.registrar.utoronto.ca/financial-aid-awards/awards-scholarships/",
        "https://engineering.calendar.utoronto.ca/scholarships-and-financial-aid",
        "https://www.artsci.utoronto.ca/future/ready-apply/awards-scholarships"
    ]

    # Create a directory to store our "Knowledge Base"
    os.makedirs("knowledge_base", exist_ok=True)

    async with AsyncWebCrawler(config=browser_config) as crawler:
        for url in urls:
            print(f"--- Crawling: {url} ---")
            result = await crawler.arun(url=url, config=run_config)

            if result.success:
                # Create a filename based on the URL
                filename = url.split("/")[-2] if url.endswith("/") else url.split("/")[-1]
                filepath = f"knowledge_base/{filename}.md"
                
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(result.markdown)
                
                print(f"✅ Saved to {filepath}")
            else:
                print(f"❌ Failed to crawl {url}: {result.error_message}")

if __name__ == "__main__":
    asyncio.run(scrape_uoft())