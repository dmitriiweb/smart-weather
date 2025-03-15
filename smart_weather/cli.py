import asyncio

from .app import App


def main():
    asyncio.run(run())


async def run():
    app = App()
    await app.run()


if __name__ == "__main__":
    asyncio.run(run())
