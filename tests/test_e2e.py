import asyncio
from playwright.async_api import async_playwright
import sys
import os

async def test_app():
    port = 8512
    # Mock Ollama
    with open("ollama.py", "w") as f:
        f.write('class MockOllama:\n    def list(self): return {"models": [{"name": "llama3.2"}]}\n    def generate(self, model, prompt, format=None, options=None): return {"response": \'{"tool": "query", "parameters": {"metrics": ["revenue_by_state"], "group_by": ["geo_key__state"]}}\'}\n_instance = MockOllama()\nlist = _instance.list\ngenerate = _instance.generate')

    os.system(f"streamlit run streamlit_app.py --server.port {port} --server.headless true > streamlit.log 2>&1 &")
    await asyncio.sleep(20)

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(f"http://localhost:{port}")
            await asyncio.sleep(15)

            # Type query
            await page.get_by_label("Ask a question about your data or project:").fill("revenue")
            await page.keyboard.press("Enter")

            # Click the Run button by its data-testid or just being the first primary button
            await page.get_by_role("button", name="Run", exact=True).click()

            print("Waiting for results...")
            await asyncio.sleep(20)

            content = await page.content()
            if "Execution complete" in content or "geo_key__state" in content:
                print("SUCCESS")
            else:
                print("FAILURE")

            await browser.close()
    finally:
        os.system(f"kill $(lsof -t -i :{port})")
        if os.path.exists("ollama.py"): os.remove("ollama.py")

if __name__ == "__main__":
    asyncio.run(test_app())
