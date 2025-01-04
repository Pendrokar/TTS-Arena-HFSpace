import gradio as gr
from .config import *
from .messages import *
from .ui_vote import *
from .ui_leaderboard import *
from .ui_contenders import *

# JavaScript within HTML head
head_js = ""
shortcut_js = """
<script>
function shortcuts(e) {
    var event = document.all ? window.event : e;
    switch (e.target.tagName.toLowerCase()) {
        case "input":
        case "textarea":
            break;
        default:
            switch (e.key.toLowerCase()) {
                case "a":
                    document.getElementById("arena-a-better").click();
                    break;
                case "b":
                    document.getElementById("arena-b-better").click();
                    break;
                case "n":
                    document.getElementById("arena-next-round").click();
                    break;
            }
    }
}
document.addEventListener('keypress', shortcuts, false);

"""
head_js += shortcut_js
head_js += open("app/cookie.js").read()
head_js += '</script>'

with gr.Blocks() as about:
    gr.Markdown(ABOUT)

with gr.Blocks(
    css="footer {visibility: hidden}textbox{resize:none} .blurred-text {filter: blur(0.15em);}",
    head=head_js,
    title="TTS Arena"
) as app:
    gr.Markdown(DESCR)
    gr.TabbedInterface([vote, leaderboard, about, tts_info], ['🗳️ Vote', '🏆 Leaderboard', '📄 About', '🗣 Contenders'])
    if CITATION_TEXT:
        with gr.Row():
            with gr.Accordion("Citation", open=False):
                gr.Markdown(f"If you use this data in your publication, please cite us!\n\nCopy the BibTeX citation to cite this source:\n\n```bibtext\n{CITATION_TEXT}\n```\n\nPlease note that all generated audio clips should be assumed unsuitable for redistribution or commercial use.")
