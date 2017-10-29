#IMPORTS
from timer import *
from pyquery import PyQuery as pq
import Settings
import requests
import traceback
import oanda_api

import time
def print_out(message):
  date = time.time()
  print '{}: {}'.format(date, message)

api = oanda_api.API(environment=Settings.environment, access_token=Settings.access_token)

while True:
  try:
    Timer = Initiate()
    print_out('Time to go...')
    trade = api.create_order(
      account_id=Settings.account_id,
      instrument='AUD_JPY',
      units=1,
      side='sell',
      type='market'
    )
    print_out('Test Trade... {} Milliseconds'.format(str(Timer.time())))
    
    #GET/EDIT REPORT/SENTENCES
    print_out('Getting the report...')
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36'}
    document = requests.get(Settings.url)
    print_out('Got Report... {} Milliseconds'.format(str(Timer.time())))
    print(document.text)
    print_out('Printed Document... {} Milliseconds'.format(str(Timer.time())))
    print_out('Document Request Data:')
    print('Url: {}'.format(document.url))
    print('STATUS CODE: {}'.format(document.status_code))
    print('Request History {}'.format(document.history))
    print('Headers: {}'.format(document.headers))
    print('Encoding: {}'.format(document.encoding))
    print('Response Length: {}'.format(len(document.text)))
    print_out('Got Report... {} Milliseconds'.format(str(Timer.time())))
    report = pq(document.text)
    report = report('.em').text()
    print_out('Parsing Report... {} Milliseconds'.format(str(Timer.time())))
    print_out(report)
    fragment = report.split(Settings.year)[1]
    print_out(fragment)
    if fragment[0] == ' ':
      fragment = fragment[1:len(fragment)]
    actual = float(fragment.split(' ')[0])
    print_out(actual)
    print_out('Got Actual... {} Milliseconds'.format(str(Timer.time())))

    #GET POSITIONS
    positions = {}
    api_positions = api.get_positions(
      account_id=Settings.account_id
    )['positions']
    for position in api_positions:
      if position['side'] == 'sell':
        positions[position['instrument']] = -position['units']
      else:
        positions[position['instrument']] = position['units']
    for instrument in Settings.beat:
      if instrument not in positions:
        positions[instrument] = 0
    for instrument in Settings.disappoint:
      if instrument not in positions:
        positions[instrument] = 0
    print_out(positions)
    print_out('Got Positions... {} Milliseconds'.format(str(Timer.time())))

    #PLACE TRADES
    print_out('Trading...')
    if actual > Settings.estimate:
      #BUYING USD
      print_out('Decision: BUY the US Dollar')
      #USD PAIRS - LONG
      for instrument in Settings.beat:
        imbalance = int(-positions[instrument] + Settings.units)
        print_out('Imbalance of {} for {}'.format(imbalance,instrument))
        if imbalance > 0:
          print_out('Buying {} {}'.format(imbalance, instrument))
          trade = api.create_order(
            account_id=Settings.account_id,
            instrument=instrument,
            units=imbalance,
            side='buy',
            type='market'
          )
          print_out(trade)
          print_out('Bought {}... {} Milliseconds'.format(instrument, str(Timer.time())))
        elif imbalance < 0:
          print_out('Selling {} {}'.format(imbalance, instrument))
          trade = api.create_order(
            account_id=Settings.account_id,
            instrument=instrument,
            units=abs(imbalance),
            side='sell',
            type='market'
          )
          print_out(trade)
          print_out('Sold {}... {} Milliseconds'.format(instrument, str(Timer.time())))
        else:
          print_out('{} is balanced'.format(instrument))
      #NON USD PAIRS - SHORT
      for instrument in Settings.disappoint:
        imbalance = int(-positions[instrument] - Settings.units)
        print_out('Imbalance of {} for {}'.format(imbalance,instrument))
        if imbalance > 0:
          print_out('Buying {} {}'.format(imbalance, instrument))
          trade = api.create_order(
            account_id=Settings.account_id,
            instrument=instrument,
            units=imbalance,
            side='buy',
            type='market'
          )
          print_out(trade)
          print_out('Bought {}... {} Milliseconds'.format(instrument, str(Timer.time())))
        elif imbalance < 0:
          print_out('Selling {} {}'.format(imbalance, instrument))
          trade = api.create_order(
            account_id=Settings.account_id,
            instrument=instrument,
            units=abs(imbalance),
            side='sell',
            type='market'
          )
          print_out(trade)
          print_out('Sold {}... {} Milliseconds'.format(instrument, str(Timer.time())))
        else:
          print_out('{} is balanced'.format(instrument))
    elif actual < Settings.estimate:
      #SELLING USD
      print_out('Decision: SELL the US Dollar')
      #USD PAIRS - SHORT
      for instrument in Settings.beat:
        imbalance = int(-positions[instrument] - Settings.units)
        print_out('Imbalance of {} for {}'.format(imbalance,instrument))
        if imbalance > 0:
          print_out('Buying {} {}'.format(imbalance, instrument))
          trade = api.create_order(
            account_id=Settings.account_id,
            instrument=instrument,
            units=imbalance,
            side='buy',
            type='market'
          )
          print_out(trade)
          print_out('Bought {}... {} Milliseconds'.format(instrument, str(Timer.time())))
        elif imbalance < 0:
          print_out('Selling {} {}'.format(imbalance, instrument))
          trade = api.create_order(
            account_id=Settings.account_id,
            instrument=instrument,
            units=abs(imbalance),
            side='sell',
            type='market'
          )
          print_out(trade)
          print_out('Sold {}... {} Milliseconds'.format(instrument, str(Timer.time())))
        else:
          print_out('{} is balanced'.format(instrument))
      #NON USD PAIRS - LONG
      for instrument in Settings.disappoint:
        imbalance = int(-positions[instrument] + Settings.units)
        print_out('Imbalance of {} for {}'.format(imbalance,instrument))
        if imbalance > 0:
          print_out('Buying {} {}'.format(imbalance, instrument))
          trade = api.create_order(
            account_id=Settings.account_id,
            instrument=instrument,
            units=imbalance,
            side='buy',
            type='market'
          )
          print_out(trade)
          print_out('Bought {}... {} Milliseconds'.format(instrument, str(Timer.time())))
        elif imbalance < 0:
          print_out('Selling {} {}'.format(imbalance, instrument))
          trade = api.create_order(
            account_id=Settings.account_id,
            instrument=instrument,
            units=abs(imbalance),
            side='sell',
            type='market'
          )
          print_out(trade)
          print_out('Sold {}... {} Milliseconds'.format(instrument, str(Timer.time())))
        else:
          print_out('{} is balanced'.format(instrument))

    #FINISHED GOOD LUCK :---->- >>> Always out, Always fast, HARAMBE 2016
    print_out('Done... {} Milliseconds'.format(str(Timer.finished())))
    raise SystemExit
  except Exception as e:
    print_out('A massive clusterfuck occured @ {}'.format(traceback.format_exc()))
    time.sleep(0.5)