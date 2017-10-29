#IMPORTS
from timer import *
Timer = Initiate()
from pyquery import PyQuery as pq
import Settings
import requests
import oanda_api

import time
def print_out(message):
  date = time.time()
  print '{}: {}'.format(date, message)

print_out('Time to go...')
api = oanda_api.API(environment=Settings.environment, access_token=Settings.access_token)
print_out('Imports... {} Milliseconds'.format(str(Timer.time())))

#GET/EDIT REPORT/SENTENCES
print_out('Getting the report...')
document = requests.get(Settings.url)
print_out('Got Report... {} Milliseconds'.format(str(Timer.time())))
report = pq(document.text)
report = report('.normalnews pre').text()
print_out('Parsing Report... {} Milliseconds'.format(str(Timer.time())))
start = report.find('THE EMPLOYMENT SITUATION')
end = start + 500
text = report[start:end]
text = text.split(Settings.year)[1]
text = text.replace('\n', ' ')
text = text.replace('   ', ' ')
text = text.replace('  ', ' ')
text = text.replace(',', '')
text = text.replace('(', '')
text = text.replace(')', '')
text = text.replace('+', '')
text = text.replace('U.S.', 'US')
sentences = text.split('. ')
print_out(sentences)
print_out('Editing Report... {} Milliseconds'.format(str(Timer.time())))

#REPORT DATA/SENTIMENT
data = {
  'nfp': 0,
  'unem': 0,
  'sentiment': 0
}
for sentence in sentences:
  last_noun = 'Blank'
  words = sentence.split(' ')
  for word in words:
    word = word.lower()
    if word in Settings.unem_rate_keywords:
      last_noun = 'unem'
    elif word in Settings.nfp_rate_keywords:
      last_noun = 'nfp'
    if last_noun == 'nfp' and word in Settings.negative_keywords:
      data['sentiment'] = 'negative'
    try:
      number = float(word)
      data[last_noun] = number
    except:
      pass
print_out(data)
print_out('Analyzing Report... {} Milliseconds'.format(str(Timer.time())))
if data['sentiment'] == 'negative':
  print_out('Negative sentiment found')
  data['nfp'] = data['nfp'] * -1
else:
  print_out('No negative sentiment found')
print_out('Analyzing Negative Sentiment... {} Milliseconds'.format(str(Timer.time())))

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
if data['nfp'] > Settings.estimate:
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
elif data['nfp'] < Settings.estimate:
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