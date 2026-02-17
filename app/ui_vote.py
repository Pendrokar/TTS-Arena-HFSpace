import gradio as gr
from .config import *
from .synth import *
from .vote import *
from .messages import *
from .sample_caching import *

blur_text_js = 'document.getElementById("arena-text-input").classList.add("blurred-text")'
unblur_text_js = 'document.getElementById("arena-text-input").classList.remove("blurred-text")'

def disable():
    return [gr.update(interactive=False), gr.update(interactive=False), gr.update(interactive=False), gr.update(interactive=False)]
def enable():
    return [gr.update(interactive=True), gr.update(interactive=True), gr.update(interactive=True), gr.update(interactive=True)]
def failed():
    return [gr.update(interactive=True), gr.update(interactive=False), gr.update(interactive=False), gr.update(interactive=True)]
def blur_text():
    return gr.update(elem_classes=['blurred-text'])
def unblur_text():
    return gr.update(elem_classes=[])
def hidetips():
    return gr.update(open=False)

with gr.Blocks() as vote:
    session_hash = gr.Textbox(visible=False, value='')

    # sample played, using Checkbox so that JS can fetch the value
    aplayed = gr.Checkbox(visible=False, value=False)
    bplayed = gr.Checkbox(visible=False, value=False)
    # voter ID
    useridstate = gr.State()
    with gr.Accordion("Tips", open=True) as tips:
        gr.Markdown(INSTR)
    with gr.Group():
        with gr.Row():
            cachedt = gr.Button('⚡', scale=0, min_width=0, variant='tool', interactive=True)
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
            .click(randomsent, outputs=[cachedt, text, randomt])\
            .then(None, js="() => "+ unblur_text_js)
        btn = gr.Button("Synthesize", variant='primary')
    model1 = gr.Textbox(interactive=False, lines=1, max_lines=1, visible=False)
    model2 = gr.Textbox(interactive=False, lines=1, max_lines=1, visible=False)
    with gr.Row(visible=False) as r2:
        with gr.Column():
            with gr.Group():
                aud1 = gr.Audio(
                    interactive=False,
                    show_label=False,
                    buttons=[],
                    elem_id="vote-a-audio",
                    # waveform_options={'waveform_progress_color': '#EF4444'},
                    # var(--color-red-500)'}); gradio only accepts HEX and CSS color
                )
                abetter = gr.Button(
                    "[A] is better",
                    elem_id='arena-a-better',
                    variant='primary',
                    interactive=False,
                )
                prevmodel1 = gr.HTML(
                    show_label=False,
                    value="Vote to reveal model A",
                    visible=False,
                )
        with gr.Column():
            with gr.Group():
                aud2 = gr.Audio(
                    interactive=False,
                    show_label=False,
                    buttons=[],
                    waveform_options={'waveform_progress_color': '#3C82F6'},
                    elem_id="vote-b-audio",
                    # var(--secondary-500)'}); gradio only accepts HEX and CSS color
                )
                bbetter = gr.Button(
                    "[B] is better",
                    elem_id='arena-b-better',
                    variant='primary',
                    interactive=False,
                )
                prevmodel2 = gr.HTML(
                    show_label=False,
                    value="Vote to reveal model B",
                    visible=False,
                )
    nxtroundbtn = gr.Button(
        '⚡ [N]ext round',
        elem_id='arena-next-round',
        visible=False,
        variant='primary',
    )

    with gr.Row():
        with gr.Column():
            autoplay = gr.Checkbox(
                label="Autoplay audio",
                value=True
            )

        with gr.Column():
            autonext = gr.Checkbox(
                label="Auto continue",
                value=True
            )

    # hardcoded voice instruct prompt (ParlerTTS, CosyVoice)
    gr.Textbox(
        interactive=False,
        lines=1,
        max_lines=1,
        visible=True,
        show_label=False,
        placeholder="Hardcoded voice instruction prompt (ParlerTTS): "+ DEFAULT_VOICE_PROMPT,
    )

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
        nxtroundbtn,
        aplayed,
        bplayed,
    ]
    """
    text,
        "Synthesize 🐢",
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
    # , concurrency_count=1, concurrency_id="sync_queue"
    btn\
        .click(disable, outputs=[btn, abetter, bbetter, cachedt])\
        .then(synthandreturn, inputs=[text, autoplay], outputs=outputs)\
        .failure(failed, outputs=[btn, abetter, bbetter, cachedt])\
        .then(enable, outputs=[btn, gr.State(), gr.State(), gr.State()])\
        .then(None, js="() => "+ unblur_text_js)
    # Next Round ; blur text
    nxtroundbtn\
        .click(clear_stuff, outputs=outputs)\
        .then(disable, outputs=[btn, abetter, bbetter, cachedt])\
        .then(give_cached_sample, inputs=[session_hash, autoplay], outputs=[*outputs, cachedt])\
        .failure(failed, outputs=[btn, abetter, bbetter, cachedt])\
        .success(enable, outputs=[btn, gr.State(), gr.State(), gr.State()])
    # blur text
    nxtroundbtn.click(None, js="() => "+ blur_text_js)

    # fetch a comparison pair from cache
    cachedt\
        .click(disable, outputs=[btn, abetter, bbetter, cachedt])\
        .then(give_cached_sample, inputs=[session_hash, autoplay], outputs=[*outputs, cachedt])\
        .failure(failed, outputs=[btn, abetter, bbetter, cachedt])\
        .success(enable, outputs=[btn, gr.State(), gr.State(), gr.State()])
    # TODO: await download of sample before allowing playback

    # Allow interaction with the vote buttons only when both audio samples have finished playing
    aud1\
        .stop(
            unlock_vote,
            inputs=[autoplay, gr.State(value=0), aplayed, bplayed],
            outputs=[abetter, bbetter, aplayed, bplayed],
        )\
        .then(
            None,
            inputs=[bplayed if autoplay else True],
            js="(b) => b ? 0 : document.getElementById('vote-b-audio')?.querySelector('button.play-pause-button')?.click()",
        )
    # autoplay if unplayed
    aud2\
        .stop(
            unlock_vote,
            inputs=[autoplay, gr.State(value=1), aplayed, bplayed],
            outputs=[abetter, bbetter, aplayed, bplayed],
        )
    # unblur text with JS; faster than sending output with elem_classes
    aud2.stop(None, inputs=[aplayed], js="(a) => a ? "+ unblur_text_js +" : 0")
    
    # Vote Section
    trigger_next_js = """
    (a) => {
        setTimeout(
            function(){
                elem = document.getElementById('arena-next-round');
                if (a && elem.classList.contains('next-round'))
                {
                    document.getElementById('arena-next-round').click();
                }
            },3000);
    }
    """

    nxt_outputs = [abetter, bbetter, prevmodel1, prevmodel2, nxtroundbtn]
    abetter\
        .click(a_is_better, outputs=nxt_outputs, inputs=[model1, model2, useridstate, text])\
        .failure(failed, outputs=[btn, abetter, bbetter, cachedt])\
        .then(voted_on_cached, inputs=[model1, model2, text, session_hash], outputs=[])
    abetter.click(hidetips, outputs=[tips])
    abetter.click(None, inputs=[autonext], js=trigger_next_js)
    
    bbetter\
        .click(b_is_better, outputs=nxt_outputs, inputs=[model1, model2, useridstate, text])\
        .failure(failed, outputs=[btn, abetter, bbetter, cachedt])\
        .then(voted_on_cached, inputs=[model1, model2, text, session_hash], outputs=[])
    bbetter.click(hidetips, outputs=[tips])
    bbetter.click(None, inputs=[autonext], js=trigger_next_js)

    # get session cookie
    vote\
        .load(
            None,
            None,
            session_hash,
            js="() => { return getArenaCookie('session') }",
        )
    # give a cached sample pair to voter; .then() did not work here
    vote\
        .load(give_cached_sample, inputs=[session_hash, autoplay], outputs=[*outputs, cachedt])
