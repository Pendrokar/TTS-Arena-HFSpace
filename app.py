from app.ui import app

if __name__ == "__main__":
    app.queue(default_concurrency_limit=4, api_open=False).launch(show_api=False)
