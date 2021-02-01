Make a Web Scraper that will traverse the RPTech website. Scraper will look at RTX 3060TI, RTX 3070, RTX 3080 and RTX 3090 pages. 
If any of the GPUs is not out of stock, and the price is below an arbitrary threshold (no scalping) then script will activate.
Upon activation, it should send its user aka me a Whatsapp Message. 
Finally script should only be called from within the script itself. 
Add logic that script will run itself every hour. 
Add support to allow Telegram and Gmail messages as well.
Move all API keys and authentications to a Secrets.txt file and fetch details from there.
Eventually, create a UI for this.