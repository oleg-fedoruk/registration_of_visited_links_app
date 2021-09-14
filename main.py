import time
import json
from flask import Flask, request
import redis

app = Flask(__name__)
server = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
try:
    server.ping()
except redis.exceptions.ConnectionError:
    print("Connection to DB doesn't work")


@app.route('/visited_links', methods=['POST'])
def visited_links():
    """Первый ресурс служит для передачи в сервис массива ссылок в POST-запросе.
    Временем их посещения считается время получения запроса сервисом."""
    links_json = request.get_data(as_text=True)
    status_code = 'ok'
    try:
        data_object = json.loads(links_json)
        links = data_object.get('links')
        if not links:
            status_code = 400
        now = int(time.time())
        links = json.dumps(links)
        server.zadd('bd', {links: now})
    except:
        status_code = 400
    response = json.dumps({"status": status_code})
    return response


@app.route('/visited_domains', methods=['GET'])
def visited_domains():
    """Второй ресурс служит для получения GET-запросом списка уникальных доменов,
    посещенных за переданный интервал времени."""

    time_from = request.args.get("from", type=int)
    time_to = request.args.get("to", type=int)
    data = {'status': 'ok'}
    try:
        req_result = server.zrangebyscore('bd', time_from, time_to)
        final_values = list()
        for x in req_result:
            final_values.extend(json.loads(x))
        sorted_list = sorted(list(set(final_values)))
        data['domains'] = sorted_list
    except:
        data['status'] = 400
    data = json.dumps(data)
    return data


if __name__ == "__main__":
    app.run(debug=True)
