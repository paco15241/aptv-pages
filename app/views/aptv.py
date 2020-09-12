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

        shelves = get_landing_data(url, params)
        return render_template('aptv/landing.html', shelves=shelves, country=country, lang=lang)

    def collection(country, lang, collection_id):
        url = f'https://uts-api.itunes.apple.com/uts/v2/browse/collection/{collection_id}'

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

        collection = get_collection_data(url, params)
        return render_template('aptv/collection.html', collection=collection, country=country, lang=lang)

    def bundle(country, lang, bundle_id):
        url = f'https://uts-api.itunes.apple.com/uts/v2/view/product/{bundle_id}'

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

        bundle = get_bundle_data(url, params)
        return render_template('aptv/bundle.html', bundle=bundle, country=country, lang=lang)


def get_landing_data(url, params):
    shelves = []
    nextToken = 0
    while True:
        params['nextToken'] = nextToken
        res = requests.get(url, params=params)
        data = json.loads(res.text)

        for shelf in data.get('data', {}).get('canvas', {}).get('shelves', []):
            shelf_id = shelf.get('id')
            shelf_title = 'Channels on Apple TV' if shelf_id == 'edt.col.5d6da1c0-92df-4ee0-a215-c939ad7dfc02'\
                            else shelf.get('title')
            more = True if shelf.get('nextToken') else False

            shelf_items = []

            items = shelf.get('items')
            for item in items:
                item_title = item.get('title', '')
                item_title = item_title if item_title else item.get('name', '')

                item_id = item.get('id')
                item_type = item.get('type')
                item_url = item.get('url')

                image = item.get('images', {}).get('shelfImage', {})
                image = image if image else item.get('images', {}).get('coverArt16X9', {})
                image = image if image else item.get('images', {}).get('coverArt', {})
                w = int(image['width'] * 225 / image['height'])  if 'width' in image else 0
                h = 225 if 'width' in image else 0
                item_image_url = image.get('url', '').replace('{w}', str(w)).replace('{h}', str(h)).replace('{f}', 'png')

                item_badgeText = item.get('badge', {}).get('text', '')
                item_badgeText = item_badgeText if item_badgeText else item.get('showTitle', '')

                if '{c}' not in item_image_url:
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


def get_collection_data(url, params):
    collection = {
        'collection_title': '',
        'collection_id': '',
        'collection_items': []
    }
    nextToken = 0
    while True:
        params['nextToken'] = nextToken
        res = requests.get(url, params=params)
        data = json.loads(res.text)

        collection_title = data.get('data', {}).get('title', '')
        collection_id = data.get('data', {}).get('id', '')

        collection['collection_title'] = collection['collection_title'] if collection[
            'collection_title'] else collection_title
        collection['collection_id'] = collection['collection_id'] if collection['collection_id'] else collection_id

        for item in data.get('data', {}).get('items', []):
            item_id = item.get('id', '')
            item_type = item.get('type', '')
            item_title = item.get('title', '')
            item_url = item.get('url', '')

            image = item.get('images', {}).get('shelfImage', {})
            image = image if image else item.get('images', {}).get('coverArt16X9', {})
            image = image if image else item.get('images', {}).get('coverArt', {})
            w = int(image['width'] * 225 / image['height']) if 'width' in image else 0
            h = 225 if 'width' in image else 0
            item_image_url = image.get('url', '').replace('{w}', str(w)).replace('{h}', str(h)).replace('{f}', 'png')

            collection['collection_items'].append({
                'item_id': item_id,
                'item_type': item_type,
                'item_title': item_title,
                'item_url': item_url,
                'item_image_url': item_image_url
            })

        nextToken = data.get('data', {}).get('nextToken')
        if not nextToken:
            break

    return collection


def get_bundle_data(url, params):
    bundle = {
        'bundle_title': '',
        'bundle_id': '',
        'bundle_items': []
    }
    nextToken = 0
    index = 0
    while True:
        params['nextToken'] = nextToken
        res = requests.get(url, params=params)
        data = json.loads(res.text)

        bundle_title = data.get('data', {}).get('content', {}).get('title', '')
        bundle_id = data.get('data', {}).get('content', {}).get('id', '')

        bundle['bundle_title'] = bundle['bundle_title'] if bundle['bundle_title'] else bundle_title
        bundle['bundle_id'] = bundle['bundle_id'] if bundle['bundle_id'] else bundle_id

        for item in data.get('data', {}).get('movies', []):
            item_id = item.get('canonicalId', '')
            item_type = item.get('type', '')
            item_title = item.get('title', '')
            item_url = item.get('url', '')

            image = item.get('images', {}).get('shelfImage', {})
            image = image if image else item.get('images', {}).get('coverArt16X9', {})
            image = image if image else item.get('images', {}).get('coverArt', {})
            w = int(image['width'] * 225 / image['height']) if 'width' in image else 0
            h = 255 if 'width' in image else 0
            item_image_url = image.get('url', '').replace('{w}', str(w)).replace('{h}', str(h)).replace('{f}', 'png')

            bundle['bundle_items'].append({
                'item_id': item_id,
                'item_type': item_type,
                'item_title': item_title,
                'item_url': item_url,
                'item_image_url': item_image_url
            })

        nextToken = data.get('data', {}).get('nextToken')
        if not nextToken:
            break

    return bundle
