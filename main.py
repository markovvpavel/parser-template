from selenium import webdriver
import asyncio
import time


async def main():

    while True:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Remote(
            options=options,
            command_executor="http://host.docker.internal:4448/wd/hub",
        )

        print('New cycle...')
        time.sleep(0.5)


asyncio.run(main())
