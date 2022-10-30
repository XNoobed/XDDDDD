from zippyshare_downloader import extract_info_coro

async def zdl(url: str):
    file = await extract_info_coro(url, download=True)

    return file