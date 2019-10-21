import requests
import time
from datetime import datetime

BITCOIN_PRICE_THRESHOLD = 9000
BITCOIN_API_URL = 'https://api.coinmarketcap.com/v1/ticker/bitcoin/'
IFTTT_WEBHOOKS_URL = 'https://maker.ifttt.com/trigger/{}/with/key/dNt2Bw0hTV-MDOb-oot0lp'

def get_latest_bitcoin_price():
    response = requests.get(BITCOIN_API_URL)
    response_json = response.json()
    return float(response_json[0]['price_usd'])  # Konvertuj cenu u decimalni broj

def post_ifttt_webhook(event, value):
    data = {'value1': value}  # Vrednost koja ce biti poslata na IFTTT servis
    ifttt_event_url = IFTTT_WEBHOOKS_URL.format(event)  # Ubacuje nas zeljeni dogadjaj
    requests.post(ifttt_event_url, json=data)  # Salje HTTP POST zahtev na webhook URL

def format_bitcoin_history(bitcoin_history):
    rows = []
    for bitcoin_price in bitcoin_history:
        date = bitcoin_price['date'].strftime('%d.%m.%Y %H:%M')  # Formatira datum u string: '24.02.2018 15:09'
        price = bitcoin_price['price']
        # <b> (bold) tag stvara boldovan tekst
        row = '{} : $<b>{}</b>'.format(date, price)  # 24.02.2018 15:09 : $<b>10123.4</b>
        rows.append(row)

    # <br> (break) tag stvara novi red
    return '<br>'.join(rows)  # Spaja redove koji su razdvojeni sa <br> tag: red1<br>red2<br>red3

def main():
    bitcoin_history = []
    while True:
        price = get_latest_bitcoin_price()
        date = datetime.now()
        bitcoin_history.append({'date': date, 'price': price})

        # Salje upozoravajucu notifikaciju
        if price < BITCOIN_PRICE_THRESHOLD:
            post_ifttt_webhook('bitcoin_price_emergency', price)

        # Salje Telegram notifikaciju
        if len(bitcoin_history) == 5:  # Kada imamo 5 stvari u bitcoin_history, saljemo update
            post_ifttt_webhook('bitcoin_price_update', format_bitcoin_history(bitcoin_history))
            # Resetujemo history
            bitcoin_history = []

        time.sleep(5 * 60)  # Pauza 5 minuta

if __name__ == '__main__':
    main()
