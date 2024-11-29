from .config import *
from .db import *
from .models import *
from .synth import top_five

import pandas as pd

# for diff
leaderboard_df = {}
def get_leaderboard(reveal_prelim = False):
    global leaderboard_df

    conn = get_db()
    cursor = conn.cursor()
    sql = 'SELECT name, upvote, downvote, name AS orig_name FROM model'
    if not reveal_prelim: sql += ' WHERE (upvote + downvote) > 300'
    cursor.execute(sql)
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=['name', 'upvote', 'downvote', 'orig_name'])
    # df['license'] = df['name'].map(model_license)
    df['name'] = df['name'].replace(model_names)
    for i in range(len(df)):
        df.loc[i, "name"] = make_link_to_space(df['name'][i], True)
    df['votes'] = df['upvote'] + df['downvote']
    # df['score'] = round((df['upvote'] / df['votes']) * 100, 2) # Percentage score

    ## ELO SCORE
    df['score'] = 1200
    df['score_diff'] = ""
    for i in range(len(df)):
        for j in range(len(df)):
            if i != j:
                try:
                    expected_a = 1 / (1 + 10 ** ((df['score'].iloc[j] - df['score'].iloc[i]) / 400))
                    expected_b = 1 / (1 + 10 ** ((df['score'].iloc[i] - df['score'].iloc[j]) / 400))
                    actual_a = df['upvote'].iloc[i] / df['votes'].iloc[i] if df['votes'].iloc[i] > 0 else 0.5
                    actual_b = df['upvote'].iloc[j] / df['votes'].iloc[j] if df['votes'].iloc[j] > 0 else 0.5
                    df.at[i, 'score'] += round(32 * (actual_a - expected_a))
                    df.at[j, 'score'] += round(32 * (actual_b - expected_b))
                except Exception as e:
                    print(f"Error in ELO calculation for rows {i} and {j}: {str(e)}")
                    continue
    df['score'] = round(df['score'])
    df['score_diff'] = df['score']

    if (
        reveal_prelim == False
        and len(leaderboard_df) == 0
    ):
        leaderboard_df = df

    if (reveal_prelim == False):
        for i in range(len(df)):
            score_diff = (df['score'].iloc[i] - leaderboard_df['score'].iloc[i])
            if (score_diff == 0):
                continue
            if (score_diff > 0):
                plus = '<em style="color: green; font-family: monospace">+'
            else:
                plus = '<em style="color: red; font-family: monospace">'

            df.at[i, 'score_diff'] = str(df['score'].iloc[i]) + plus + str(score_diff) +'</em>'

    ## ELO SCORE
    df = df.sort_values(by='score', ascending=False)
    # medals
    def assign_medal(rank, assign):
        rank = str(rank + 1)
        if assign:
            if rank == '1':
                rank += '🥇'
            elif rank == '2':
                rank += '🥈'
            elif rank == '3':
                rank += '🥉'

        return '#'+ rank

    df['order'] = [assign_medal(i, not reveal_prelim and len(df) > 2) for i in range(len(df))]
    # fetch top_five
    for orig_name in df['orig_name']:
        if (
            reveal_prelim
            and len(top_five) < 5
            and orig_name in AVAILABLE_MODELS.keys()
        ):
            top_five.append(orig_name)

    df['score'] = df['score_diff']
    df = df[['order', 'name', 'score', 'votes']]
    return df

def make_link_to_space(model_name, for_leaderboard=False):
    # create a anchor link if a HF space
    style = 'text-decoration: underline;text-decoration-style: dotted;'
    title = ''

    if model_name in AVAILABLE_MODELS:
        style += 'color: var(--link-text-color);'
        title = model_name
    else:
        style += 'font-style: italic;'
        title = 'Disabled for Arena (See AVAILABLE_MODELS within code for why)'

    model_basename = model_name
    if model_name in HF_SPACES:
        model_basename = HF_SPACES[model_name]['name']

    try:
        if(
            for_leaderboard
            and HF_SPACES[model_name]['is_proprietary']
        ):
            model_basename += ' 🔐'
            title += '; 🔐 = online only or proprietary'
    except:
        pass

    if '/' in model_name:
        return '🤗 <a target="_blank" style="'+ style +'" title="'+ title +'" href="'+ 'https://huggingface.co/spaces/'+ model_name +'">'+ model_basename +'</a>'

    # otherwise just return the model name
    return '<span style="'+ style +'" title="'+ title +'" href="'+ 'https://huggingface.co/spaces/'+ model_name +'">'+ model_name +'</span>'

def markdown_link_to_space(model_name):
    # create a anchor link if a HF space using markdown syntax
    if '/' in model_name:
        return '🤗 [' + model_name + '](https://huggingface.co/spaces/' + model_name + ')'
    # otherwise just return the model name
    return model_name
