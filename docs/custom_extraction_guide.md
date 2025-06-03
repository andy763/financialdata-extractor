You will recieve the following input: 
1. Share price or Outstanding shares custom function (meaning update excel_stock_updater.py or outstanding_shares_updater.py respectively)
2. The general, root URL which off you must create a custom function for. F.ex https://aminagroup.com/
3. One or multiple example URL within the root URL. F.ex https://aminagroup.com/individuals/investments/btc-usd-tracker-certificate/
4. The share price or number of oustanding shares for said example URLs inlcuding the words before the number to make it easier for you to locate and implement in the code what to look for. The order of the numbers will be the same order as the URLs in 3. we listed, think of it as respectively. 
5. Custom requests, warnings, etc.

Before we start, note: if we are trying to create a custom function for root/general URL, for example: google.com and say we are doing it for share price (excel_stock_updater.py) then go into the outstanding custom function area inside outstanding_shares_updater.py and see if we already created a google.com general URL function and learn how the outstanding shares were extracted, through what methods/ tools. Ofc it will not be identical but f.ex how to handle the website and cookies, permissions, etc. may remain the same. And vice versa as well. 

Also note: If I say Share price or Outstanding shares in the 1. input, never edit the code of the other say I say share price do not edit outstanding_shares_updater.py and if I say Outstanding shares in 1. do not edit excel_stock_updater.py.

Also note: when dealing with share price functions never pick up NAV or AUM.

Most importantly: Never ever radically change the main files, that is excel_stock_updater.py and outstanding_shares_updater.py. For share price edit and create  `get_..._price()` functions in `excel_stock_updater.py` same for outstanding shares just inside outstanding_shares_updater.py and using the equivalent of `get_..._price()` functions.

You are then to do the following: 

create a custom function to find the 1. share price/outstanding shares for the 2. general/ root URL (example: @https://aminagroup.com/) or fix the existing one if there is one. Take 3. the example URL (@https://aminagroup.com/individuals/investments/btc-usd-tracker-certificate/) where the share price / number of oustanding shares is 4. (f.ex Current price 8.0734 USD*). Take a look at this example URL using the web and analyze how to best extract it. Then create a test case with this URL on your proposed code, if it works add it to excel_stock_updater.py / outstanding_shares_updater.py if not try another fix and keep analyzing the webpage. 5. if anything