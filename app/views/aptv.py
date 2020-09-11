from flask import render_template
import json, requests

class views:
    def index():
        return render_template('aptv/index.html')
    
    def landing(country, lang):
        url = f'https://uts-api.itunes.apple.com/uts/v2/browse/watchNow'
        params = {
            "caller": "js",
            "gac": "true",
            "locale": f"{lang}",
            "nextToken": "0",
            "pfm": "iphone",
            "sf": "143470",
            "utsk": "e2648c8552395150::::::ac0e30f9a5790f93",
            "v": "36"
        }
        
        # data = get_landing_data(url, params)

        shelves = get_landing_data(url, params)
        return render_template('aptv/landing.html', shelves=shelves, country=country, lang=lang)

    def collection(country, lang, shelf_id):

        return 'Hello'


# def get_landing_data(url, params):
#     shelves = []
#     nextToken = 0
#     while True:
#         params['nextToken'] = nextToken
#         res = requests.get(url, params=params)
#         data = json.loads(res.text)
#
#         shelves.extend(data.get('data', {}).get('canvas', {}).get('shelves', []))
#
#         nextToken = data.get('data', {}).get('canvas', {}).get('nextToken')
#         if not nextToken:
#             break
#     return shelves


def get_landing_data(url, params):
    shelves = []
    nextToken = 0
    while True:
        params['nextToken'] = nextToken
        res = requests.get(url, params=params)
        data = json.loads(res.text)

        for shelf in data.get('data', {}).get('canvas', {}).get('shelves', []):
            shelf_id = shelf.get('id')
            shelf_title = shelf.get('title')
            more = True if shelf.get('nextToken') else False

            shelf_items = []
            items = shelf.get('items')
            for item in items:
                item_title = item.get('title')

                if not item_title:
                    continue

                item_id = item.get('id')
                item_type = item.get('type')
                item_url = item.get('url')

                image = item.get('images', {}).get('coverArt16X9', {})
                image = image if image else item.get('images', {}).get('shelfImage', {})
                w = int(image['width'] * 225 / image['height'])
                h = 225
                item_image_url = image.get('url', '').replace('{w}', str(w)).replace('{h}', str(h)).replace('{f}', 'png')

                item_badgeText = item.get('badge', {}).get('text')

                shelf_items.append({
                    'item_id': item_id,
                    'item_type': item_type,
                    'item_title': item_title,
                    'item_url': item_url,
                    'item_image_url': item_image_url,
                    'item_badgeText': item_badgeText
                })

            if shelf_items:
                shelves.append({
                    'shelf_id': shelf_id,
                    'shelf_title': shelf_title,
                    'shelf_items': shelf_items,
                    'more': more
                })

        nextToken = data.get('data', {}).get('canvas', {}).get('nextToken')
        if not nextToken:
            break

    return shelves