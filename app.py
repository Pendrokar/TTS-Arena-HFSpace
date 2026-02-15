from app.ui import app, head_js

if __name__ == "__main__":
    app\
        .queue(default_concurrency_limit=4, api_open=False)\
        .launch(
            footer_links=["gradio", "settings"],
            css="footer {visibility: hidden}textbox{resize:none} .blurred-text {filter: blur(0.15em);}",
            head=head_js
        )
