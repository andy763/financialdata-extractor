You will recieve the following input: 
1. Share price or Outstanding shares custom function (meaning update excel_stock_updater.py or outstanding_shares_updater.py respectively)
2. The general, root URL which off you must create a custom function for. F.ex https://aminagroup.com/
3. One or multiple example URL within the root URL. F.ex https://aminagroup.com/individuals/investments/btc-usd-tracker-certificate/
4. The share price or number of oustanding shares for said example URLs inlcuding the words before the number to make it easier for you to locate and implement in the code what to look for. The order of the numbers will be the same order as the URLs in 3. we listed, think of it as respectively. 
5. Custom requests, warnings, etc.

Before we start, note: if we are trying to create a custom function for root/general URL, for example: google.com and say we are doing it for share price (excel_stock_updater.py) then go into the outstanding custom function area inside outstanding_shares_updater.py and see if we already created a google.com general URL function and learn how the outstanding shares were extracted, through what methods/ tools. Ofc it will not be identical but f.ex how to handle the website and cookies, permissions, etc. may remain the same. And vice versa as well. 

Also note: of course the custom function shouldn't only work for the example URLs but for all URLs that start with the root URL. F.ex all URLs starting with https://aminagroup.com/ should work for the https://aminagroup.com/ custom function.

## ⚠️ CRITICAL: CUSTOM FUNCTIONS MUST WORK FOR ALL URLs ⚠️
Custom functions are created for an ENTIRE DOMAIN (root URL), NOT just specific example URLs. Your custom function MUST work for ALL URLs from that domain following the same pattern, not just the specific examples provided. The examples are ONLY for testing and reference - your implementation must be general enough to handle any URL from that domain.

Example: If asked to create a custom function for valour.com, it must work for ALL these URLs:
- https://valour.com/en/products/physical-bitcoin-carbon-neutral-usd
- https://valour.com/en/products/valour-bitcoin-physical-staking
- https://valour.com/en/products/valour-ethereum-physical-staking
- And ANY other page on valour.com following the same pattern

Do not create narrow functions that only handle specific example URLs. Consider the variety of page layouts and content structures across the entire domain.

Also note: If I say Share price or Outstanding shares in the 1. input, never edit the code of the other say I say share price do not edit outstanding_shares_updater.py and if I say Outstanding shares in 1. do not edit excel_stock_updater.py.

Also note: when dealing with share price functions never pick up NAV or AUM.

Most importantly: Never ever radically change the main files, that is excel_stock_updater.py and outstanding_shares_updater.py. For share price edit and create  `get_..._price()` functions in `excel_stock_updater.py` same for outstanding shares just inside outstanding_shares_updater.py and using the equivalent of `get_..._price()` functions.

You are then to do the following: 

create a custom function to find the 1. share price/outstanding shares for the 2. general/ root URL (example: @https://aminagroup.com/) or fix the existing one if there is one. Take 3. the example URL (@https://aminagroup.com/individuals/investments/btc-usd-tracker-certificate/) where the share price / number of oustanding shares is 4. (f.ex Current price 8.0734 USD*). Take a look at this example URL using the web and analyze how to best extract it. Then create a test case with this URL on your proposed code, if it works add it to excel_stock_updater.py / outstanding_shares_updater.py if not try another fix and keep analyzing the webpage. 5. if anything