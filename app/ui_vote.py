import gradio as gr
from .config import *
from .synth import *
from .vote import *
from .messages import *

blur_text_js = 'document.getElementById("arena-text-input").classList.add("blurred-text")'
unblur_text_js = 'document.getElementById("arena-text-input").classList.remove("blurred-text")'

def disable():
    return [gr.update(interactive=False), gr.update(interactive=False), gr.update(interactive=False)]
def enable():
    return [gr.update(interactive=True), gr.update(interactive=True), gr.update(interactive=True)]
def blur_text():
    return gr.update(elem_classes=['blurred-text'])
def unblur_text():
    return gr.update(elem_classes=[])

with gr.Blocks() as vote:
    # sample played
    #aplayed = gr.State(value=False)
    #bplayed = gr.State(value=False)
    # voter ID
    useridstate = gr.State()
    gr.Markdown(INSTR)
    with gr.Group():
        with gr.Row():
            text = gr.Textbox(
                container=False,
                show_label=False,
                placeholder="Enter text to synthesize",
                lines=1,
                max_lines=1,
                scale=9999999,
                min_width=0,
                elem_id="arena-text-input",
            )
            randomt = gr.Button('🎲', scale=0, min_width=0, variant='tool')
        randomt\
            .click(randomsent, outputs=[text, randomt])\
            .then(None, js="() => "+ unblur_text_js)
        btn = gr.Button("Synthesize", variant='primary')
    model1 = gr.Textbox(interactive=False, lines=1, max_lines=1, visible=False)
    #model1 = gr.Textbox(interactive=False, lines=1, max_lines=1, visible=True)
    model2 = gr.Textbox(interactive=False, lines=1, max_lines=1, visible=False)
    #model2 = gr.Textbox(interactive=False, lines=1, max_lines=1, visible=True)
    with gr.Row(visible=False) as r2:
        with gr.Column():
            with gr.Group():
                aud1 = gr.Audio(interactive=False, show_label=False, show_download_button=False, show_share_button=False)
                abetter = gr.Button(
                    "[A] is better",
                    elem_id='arena-a-better',
                    variant='primary',
                    interactive=False,
                )
                prevmodel1 = gr.Textbox(interactive=False, show_label=False, container=False, value="Vote to reveal model A", text_align="center", lines=1, max_lines=1, visible=False)
        with gr.Column():
            with gr.Group():
                aud2 = gr.Audio(interactive=False, show_label=False, show_download_button=False, show_share_button=False)
                bbetter = gr.Button(
                    "[B] is better",
                    elem_id='arena-b-better',
                    variant='primary',
                    interactive=False,
                )
                prevmodel2 = gr.Textbox(interactive=False, show_label=False, container=False, value="Vote to reveal model B", text_align="center", lines=1, max_lines=1, visible=False)
    nxtroundbtn = gr.Button(
        '⚡ [N]ext round',
        elem_id='arena-next-round',
        visible=False,
        variant='primary',
    )
    # outputs = [text, btn, r2, model1, model2, prevmodel1, aud1, prevmodel2, aud2, abetter, bbetter]
    outputs = [
        text,
        btn,
        r2,
        model1,
        model2,
        aud1,
        aud2,
        abetter,
        bbetter,
        prevmodel1,
        prevmodel2,
        nxtroundbtn
    ]
    """
    text,
        "Synthesize",
        gr.update(visible=True), # r2
        mdl1, # model1
        mdl2, # model2
        gr.update(visible=True, value=results[mdl1]), # aud1
        gr.update(visible=True, value=results[mdl2]), # aud2
        gr.update(visible=True, interactive=False), #abetter
        gr.update(visible=True, interactive=False), #bbetter
        gr.update(visible=False), #prevmodel1
        gr.update(visible=False), #prevmodel2
        gr.update(visible=False), #nxt round btn"""
    btn\
        .click(disable, outputs=[btn, abetter, bbetter])\
        .then(synthandreturn, inputs=[text], outputs=outputs)\
        .then(enable, outputs=[btn, abetter, bbetter])\
        .then(None, js="() => "+ unblur_text_js)
    # Next Round ; blur text
    nxtroundbtn\
        .click(clear_stuff, outputs=outputs)\
        .then(randomsent, outputs=[text, randomt])\
        .then(synthandreturn, inputs=[text], outputs=outputs)\
        .then(enable, outputs=[btn, abetter, bbetter])
    # blur text
    nxtroundbtn.click(None, js="() => "+ blur_text_js)

    # Allow interaction with the vote buttons only when both audio samples have finished playing
    #aud1.stop(unlock_vote, outputs=[abetter, bbetter, aplayed, bplayed], inputs=[gr.State(value=0), aplayed, bplayed])
    #aud2.stop(unlock_vote, outputs=[abetter, bbetter, aplayed, bplayed], inputs=[gr.State(value=1), aplayed, bplayed])
    # faster than sending output with elem_classes
    aud2.stop(None, js="() => "+ unblur_text_js)

    # nxt_outputs = [prevmodel1, prevmodel2, abetter, bbetter]
    nxt_outputs = [abetter, bbetter, prevmodel1, prevmodel2, nxtroundbtn]
    abetter.click(a_is_better, outputs=nxt_outputs, inputs=[model1, model2, useridstate])
    bbetter.click(b_is_better, outputs=nxt_outputs, inputs=[model1, model2, useridstate])
