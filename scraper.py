import requests
import os
from twilio.rest import Client

# Use this url for a product currently available at Target to ensure script works as intended.
available_product_url = 'https://redsky.target.com/redsky_aggregations/v1/web/pdp_fulfillment_v1?key' \
      '=ff457966e64d5e877fdbad070f276d18ecec4a01&tcin=81114477&store_id=373&store_positions_store_id=373' \
      '&has_store_positions_store_id=true&zip=55118&state=MN&latitude=44.901615142822266&longitude=-93' \
      '.09713745117188&scheduled_delivery_store_id=2046&pricing_store_id=373&fulfillment_test_mode' \
      '=grocery_opu_team_member_test&is_bot=false '

# Url for PS5 at target
ps5_url = 'https://redsky.target.com/redsky_aggregations/v1/web/pdp_fulfillment_v1?key' \
       '=ff457966e64d5e877fdbad070f276d18ecec4a01&tcin=81114595&store_id=373&store_positions_store_id=373' \
       '&has_store_positions_store_id=true&zip=55118&state=MN&latitude=44.901615142822266&longitude=-93' \
       '.09713745117188&scheduled_delivery_store_id=2046&pricing_store_id=373&fulfillment_test_mode' \
       '=grocery_opu_team_member_test&is_bot=false '

headers = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/87.0.4280.67 Safari/537.36'}


def scrape_inventory():
    # Create a free trial Twilio account to get account SID and Authentication token.
    def send_notification():
        account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
        auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
        client = Client(account_sid, auth_token)

        client.messages.create(
            body='PS5 is now in stock at Target! ' + str(quantity) + ' in stock at ' + location + ' store.',
            from_=os.environ.get("TWILIO_NUMBER"),
            to=os.environ.get("TO_PHONE_NUMBER")
        )

    try:
        response = requests.get(ps5_url, headers=headers)
        store_options = response.json()['data']['product']['fulfillment']['store_options']
        if len(store_options) == 1:
            quantity = response.json()['data']['product']['fulfillment']['store_options'][0][
                'location_available_to_promise_quantity']
            location = response.json()['data']['product']['fulfillment']['store_options'][0][
                'location_name']
        else:
            quantity = response.json()['data']['product']['fulfillment']['store_options'][1][
                'location_available_to_promise_quantity']
            location = response.json()['data']['product']['fulfillment']['store_options'][1][
                'location_name']
        if quantity < 1:
            print('Item still out of stock...')

        else:
            send_notification()
            print('SMS sent successfully')

    except Exception as e:
        print(e)


scrape_inventory()
