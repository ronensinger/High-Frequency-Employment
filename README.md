# High-Frequency-Employment
This algorithm uses a custom word recognition program and PyQuery to download the monthly unemployment report as soon as it is available, and make intelligent traders.

## The Monthly Employment Report
On the first Friday of every month at precisely 8:30 a.m., the Bureau of Labor Statistics (BLS) releases its monthly **Employment Report**. This report has a paramount impact on US and Global Markets.
If job growth exceeds estimates, the US Stock Market and US Dollar rally, and if job growth disappoints, the US Stock Market and US Dollar crash significantly.

A screenshot of what the actual report looks like is below:
![](http://ronen.io/report.PNG)


## The Algorithm
The algorithm located in the assassin.py file downloads the report as soon as it's online.

The algorithm interprets the report and searches for keywords such as "nonfarm" and "payroll" the two words that preceed the employment figure.

It then searches for trend keywords such as 'fell', 'fall', 'decrease', 'decreased', 'slumped', 'plummet', 'plummeted', 'dive', 'dived', 'retreat', 'retreated', 'decline', 'declined', and 'down' to determine whether the numerical figure represents positive or negative growth.

Once the algorithm determines the change in employment, it compares the change to analyst estimates. If the report is a clear beat, it purchases US Dollars immediately. however, if the report is a dissapointment, is shorts (sells) US Dollars.

# Files and Getting Started
The **Settings.py** file controls the execution of the algorithm. Enter the current year in the year variable, and the analyst estimates in the estimate field.
Replace units with the amount of US Dollars you want the algorithm to buy or sell, and you're ready to go. 

### Trading Strategy
Currency pairs in the **dissapoint list** in the **Settings.py** will be bought if the employment numbers are bad, and vice versa, be sold if the numbers are good.
Likewise, the pairs in the **beat list** will be bought in the event of a good report, and shorted in the event of a dissapointing report.

### Start the Bot
Enter
```
python cron.py
```
a few minutes before the report comes out, and the algorithm is ready to go!

It will  wait until 8:30, like a silent assassin, and will spring into action as soon as the report comes out, and will hopefully make you money!

If you're interested in examining the actual word recognition program, please refer to:
```
pull.py
```
If you're interested in examining the trading mechanics, please refer to:
```
assassin.py
```

### Running the Bot

To run the bot, you need a funded account at forex broker **OANDA**. Once you have your account, download the code in this repository and change:
```
access_token = 'Replace With Your Own'
account_id = 'Replace With Your Own'
```
in the **Settings.py** file to reflect your own account info. **access_token** is your **API KEY**.

### Profitability
The bot has trouble being profitable. Although it places buy and sell orders long before humans, the currency broker that executes the orders, **OANDA** can be quite slow, and thus, reduce your chances of capturing a profit.


# Conclusion
The Employment Bot itself runs lightning fast, taking on average, 250 milliseconds to initialize, import neccessary libraries, download/parse the report, and trade.
A sample file of the bots output when it ran nearly a year ago (it prints what it's thinking to help me debug) is located in the **log.txt.out** file.
All the other files are neccessary components to run the algorithm.

Credit to **PyQuery** the python program that parses PDFs into text form.

A similar trading bot has been included for the **Michigan Consumer Confidence Report** in the Michigan folder, however, it isn't profitable.

Please direct any questions to: ronensinger17@gmail.com, and have fun trading!

