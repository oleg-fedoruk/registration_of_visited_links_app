import time
import json
from flask import Flask, request
import redis

app = Flask(__name__)
server = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
try:
    server.ping()
except redis.exceptions.ConnectionError:
    print("Doesn't work")


@app.route('/visited_links', methods=['POST'])
def visited_links():
    """Первый ресурс служит для передачи в сервис массива ссылок в POST-запросе.
    Временем их посещения считается время получения запроса сервисом."""
    links_json = request.get_data(as_text=True)

    try:
        data_object = json.loads(links_json)
    except json.JSONDecodeError:
        status_code = 400
        return "Invalid data. Can not parse data to JSON", status_code

    try:
        links = data_object.get('links')
    except AttributeError:
        status_code = 400
        return "Invalid data", status_code

    if links is None:
        status_code = 400
        return "Invalid data. Your JSON don't have key 'links'", status_code

    now = int(time.time())
    print(now)
    links = json.dumps(links)
    try:
        server.zadd('bd', {links: now})
    except:
        pass
    response = '{"status": "ok"}'
    return response


@app.route('/visited_domains', methods=['GET'])
def visited_domains():
    """Второй ресурс служит для получения GET-запросом списка уникальных доменов,
    посещенных за переданный интервал времени."""

    time_from = request.args.get("from", type=int)
    time_to = request.args.get("to", type=int)

    try:
        req_result = server.zrangebyscore('bd', time_from, time_to)
    except:
        return 'DB Error', 400
    final_values = list()
    for x in req_result:
        final_values.extend(json.loads(x))
    data = {'domains': list(set(final_values)), 'status': 'ok'}
    data = json.dumps(data)
    return data


if __name__ == "__main__":
    app.run(debug=True)
