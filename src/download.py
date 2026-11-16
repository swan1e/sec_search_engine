from sec_edgar_downloader import Downloader

dl = Downloader("Vincent", "vsuen123@gmail.com", "./data/raw")
dl.get("10-K", "AAPL", limit=10, download_details=True)