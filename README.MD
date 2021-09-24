# Registration of visited links app

## Dependencies & packages

- `sudo apt-get install python3.x`

- `sudo apt install python3.x-venv`

- `sudo apt install redis-server`

## Local installation

1. `git clone https://github.com/oleg-fedoruk/registration_of_visited_links_app.git`

2. setup venv

    ```sh
    python3 -m venv env

    source env/bin/activate

    pip install --upgrade pip && pip install -r req.txt
    ```
3. run app
   ```sh
    python3 main.py
    ```
