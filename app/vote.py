from .utils import *
from .config import *
from .models import *
from .db import *
from .init import *

import gradio as gr

# Logging

def log_text(text):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO spokentext (spokentext) VALUES (?)', (text,))
    if scheduler:
        with scheduler.lock:
            conn.commit()
    else:
        conn.commit()
    cursor.close()

# Vote

def upvote_model(model, uname, battle=False):
    conn = get_db()
    cursor = conn.cursor()
    if battle: uname = "unknown_battle"
    cursor.execute('UPDATE model SET upvote = upvote + 1 WHERE name = ?', (model,))
    if cursor.rowcount == 0:
        cursor.execute('INSERT OR REPLACE INTO model (name, upvote, downvote) VALUES (?, 1, 0)', (model,))
    cursor.execute('INSERT INTO vote (username, model, vote) VALUES (?, ?, ?)', (uname, model, 1,))
    if scheduler:
        with scheduler.lock:
            conn.commit()
    else:
        conn.commit()
    cursor.close()

def downvote_model(model, uname, battle=False):
    conn = get_db()
    cursor = conn.cursor()
    if battle: uname = "unknown_battle"
    cursor.execute('UPDATE model SET downvote = downvote + 1 WHERE name = ?', (model,))
    if cursor.rowcount == 0:
        cursor.execute('INSERT OR REPLACE INTO model (name, upvote, downvote) VALUES (?, 0, 1)', (model,))
    cursor.execute('INSERT INTO vote (username, model, vote) VALUES (?, ?, ?)', (uname, model, -1,))
    if scheduler:
        with scheduler.lock:
            conn.commit()
    else:
        conn.commit()
    cursor.close()

# Battle Mode

def a_is_better_battle(model1, model2, userid):
    return a_is_better(model1, model2, 'unknown_battle', True)
def b_is_better_battle(model1, model2, userid):
    return b_is_better(model1, model2, 'unknown_battle', True)

# A/B better

def a_is_better(model1, model2, userid, text):
    return is_better(model1, model2, userid, text, True)
def b_is_better(model1, model2, userid, text):
    return is_better(model1, model2, userid, text, False)

def is_better(model1, model2, userid, text, chose_a):
    if(
        (
            not model1 in AVAILABLE_MODELS.keys()
            and not model1 in AVAILABLE_MODELS.values()
        )
        or (
            not model2 in AVAILABLE_MODELS.keys()
            and not model2 in AVAILABLE_MODELS.values()
        )
    ):
        raise gr.Error('Sorry, please try voting again.')

    # userid is unique for each cast vote pair
    userid = mkuuid(userid)
    if model1 and model2:
        conn = get_db()
        cursor = conn.cursor()
        sql_query = 'INSERT INTO votelog (username, chosen, rejected) VALUES (?, ?, ?)'
        if chose_a:
            cursor.execute(sql_query, (str(userid), model1, model2))
        else:
            cursor.execute(sql_query, (str(userid), model2, model1))

        with scheduler.lock:
            conn.commit()
            # also retrieve primary key ID
            cursor.execute('SELECT last_insert_rowid()')
            votelogid = cursor.fetchone()[0]
            cursor.close()

        if chose_a:
            upvote_model(model1, str(userid))
            downvote_model(model2, str(userid))
        else:
            upvote_model(model2, str(userid))
            downvote_model(model1, str(userid))
        log_text(text)
        # log_text(text, votelogid)

    return reload(model1, model2, userid, chose_a=chose_a, chose_b=(not chose_a))

# Reload
def reload(chosenmodel1=None, chosenmodel2=None, userid=None, chose_a=False, chose_b=False):
    chosenmodel1 = make_link_to_space(chosenmodel1)
    chosenmodel2 = make_link_to_space(chosenmodel2)
    out = [
        gr.update(interactive=False, visible=False),
        gr.update(interactive=False, visible=False)
    ]
    style = 'text-align: center; font-size: 1rem; margin-bottom: 0; padding: var(--input-padding)'
    if chose_a == True:
        out.append(gr.HTML(value=f'<p style="{style}">Your vote: {chosenmodel1}</p>', visible=True))
        out.append(gr.HTML(value=f'<p style="{style}">{chosenmodel2}</p>', visible=True))
    else:
        out.append(gr.HTML(value=f'<p style="{style}">{chosenmodel1}</p>', visible=True))
        out.append(gr.HTML(value=f'<p style="{style}">Your vote: {chosenmodel2}</p>', visible=True))
    out.append(gr.update(visible=True))
    return out

def unlock_vote(autoplay, btn_index, aplayed, bplayed):
    if autoplay == False:
        return [gr.update(), gr.update(), aplayed, bplayed]

    # sample played
    if btn_index == 0:
        aplayed = True
    if btn_index == 1:
        bplayed = True

    # both audio samples played
    if bool(aplayed) and bool(bplayed):
        # print('Both audio samples played, voting unlocked')
        return [gr.update(interactive=True), gr.update(interactive=True), True, True]

    return [gr.update(), gr.update(), aplayed, bplayed]