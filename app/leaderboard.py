from .config import *
from .db import *
from .models import *

import pandas as pd

# for diff
leaderboard_df = {}
def get_leaderboard(reveal_prelim = False):
    global leaderboard_df

    conn = get_db()
    cursor = conn.cursor()
    sql = 'SELECT Name, Upvote, Downvote, name AS OrigName FROM model'
    prelim_votes = 300
    if not reveal_prelim: sql += ' WHERE (Upvote + Downvote) > '+ str(prelim_votes)
    cursor.execute(sql)
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=['Name', 'Upvote', 'Downvote', 'OrigName'])
    # df['License'] = df['Name'].map(model_license)
    df['Name'] = df['Name'].replace(model_names)
    for i in range(len(df)):
        df.loc[i, "Name"] = make_link_to_space(df['Name'][i], True)

    # Calculate total votes and win rate
    df['Votes'] = df['Upvote'] + df['Downvote']
    df['Win Rate'] = (df['Upvote'] / df['Votes'] * 100).round(1)
    # convert to string
    df['Win Rate'] = df['Win Rate'].astype(str) + '%'

    # df['Score'] = round((df['Upvote'] / df['Votes']) * 100, 2) # Percentage score

    ## ELO SCORE
    df['Elo'] = 1200
    df['Elo Diff'] = ""
    for i in range(len(df)):
        for j in range(len(df)):
            if i != j:
                try:
                    expected_a = 1 / (1 + 10 ** ((df['Elo'].iloc[j] - df['Elo'].iloc[i]) / 400))
                    expected_b = 1 / (1 + 10 ** ((df['Elo'].iloc[i] - df['Elo'].iloc[j]) / 400))
                    actual_a = df['Upvote'].iloc[i] / df['Votes'].iloc[i] if df['Votes'].iloc[i] > 0 else 0.5
                    actual_b = df['Upvote'].iloc[j] / df['Votes'].iloc[j] if df['Votes'].iloc[j] > 0 else 0.5
                    df.at[i, 'Elo'] += round(32 * (actual_a - expected_a))
                    df.at[j, 'Elo'] += round(32 * (actual_b - expected_b))
                except Exception as e:
                    print(f"Error in ELO calculation for rows {i} and {j}: {str(e)}")
                    continue

        # add link to vote dataset
        orig_name = df['OrigName'].iloc[i]
        if (
            DB_DATASET_ID != ''
            and '/' in orig_name
        ):
            style = 'text-decoration: underline;text-decoration-style: dotted; color: var(--link-text-color);'
            title = 'Rejections'
            # win rate dataset
            df.at[i, 'Win Rate'] = f'<a target="_blank" style="{style}" title="{title}" href="https://huggingface.co/datasets/{DB_DATASET_ID}/viewer/summary/rejections?f[rejected][value]=%27{orig_name}%27">' + df['Win Rate'].iloc[i] + '</a>'
    df['Elo'] = round(df['Elo'])
    df['Elo Diff'] = df['Elo']

    if (
        reveal_prelim == False
        and len(leaderboard_df) == 0
    ):
        leaderboard_df = df

    # Add ELO diff from startup
    try:
        if (reveal_prelim == False):
            for i in range(len(df)):
                elo_diff = (df['Elo'].iloc[i] - leaderboard_df['Elo'].iloc[i])
                if (elo_diff == 0):
                    continue
                if (elo_diff > 0):
                    plus = '<em style="color: green; font-family: monospace">+'
                else:
                    plus = '<em style="color: red; font-family: monospace">'

                df.at[i, 'Elo Diff'] = str(df['Elo'].iloc[i]) + plus + str(elo_diff) +'</em>'
    except:
        # FIXME: crashes when a TTS from premilinary results passes the vote threshold
        pass

    # Sort by ELO score and then by Vote count
    df = df.sort_values(by=['Elo', 'Votes'], ascending=[False, False])

    # last in model series from models.py
    last_series = []
    # medals
    def assign_medal(rank, model_series, last_series, assign):
        rank = str(rank + 1)
        if (
            assign
            # and last_series != ''
            # and model_series != last_series
        ):
            if rank == '1':
                rank += '🥇'
            elif rank == '2':
                rank += '🥈'
            elif rank == '3':
                rank += '🥉'

        if (model_series != last_series):
            last_series = model_series
        return '#'+ rank

    try:
        df['Order'] = [
            assign_medal(
                i,
                HF_SPACES[df['OrigName'].iloc[i]]['series'],
                last_series,
                not reveal_prelim and len(df) > 2
            ) for i in range(len(df))
        ]
    except:
        df['Order'] = [assign_medal(
            i,
            '',
            '',
            not reveal_prelim and len(df) > 2) for i in range(len(df))
        ]
        pass

    # fetch top_five
    for orig_name in df['OrigName']:
        if (
            reveal_prelim
            and len(top_five) < 5
            and orig_name not in top_five
            and orig_name in AVAILABLE_MODELS.keys()
        ):
            top_five.append(orig_name)

    df['Elo'] = df['Elo Diff']
    df = df[['Order', 'Name', 'Win Rate', 'Elo', 'Votes']]
    return df
