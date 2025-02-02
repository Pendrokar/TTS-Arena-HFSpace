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
    prelim_votes = 300
    if not reveal_prelim: sql += ' WHERE (upvote + downvote) > '+ str(prelim_votes)
    cursor.execute(sql)
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=['name', 'upvote', 'downvote', 'orig_name'])
    # df['license'] = df['name'].map(model_license)
    df['name'] = df['name'].replace(model_names)
    for i in range(len(df)):
        df.loc[i, "name"] = make_link_to_space(df['name'][i], True)

    # Calculate total votes and win rate
    df['votes'] = df['upvote'] + df['downvote']
    df['win_rate'] = (df['upvote'] / df['votes'] * 100).round(1)
    # df['score'] = round((df['upvote'] / df['votes']) * 100, 2) # Percentage score

    ## ELO SCORE
    df['elo'] = 1200
    df['elo_diff'] = ""
    for i in range(len(df)):
        for j in range(len(df)):
            if i != j:
                try:
                    expected_a = 1 / (1 + 10 ** ((df['elo'].iloc[j] - df['elo'].iloc[i]) / 400))
                    expected_b = 1 / (1 + 10 ** ((df['elo'].iloc[i] - df['elo'].iloc[j]) / 400))
                    actual_a = df['upvote'].iloc[i] / df['votes'].iloc[i] if df['votes'].iloc[i] > 0 else 0.5
                    actual_b = df['upvote'].iloc[j] / df['votes'].iloc[j] if df['votes'].iloc[j] > 0 else 0.5
                    df.at[i, 'elo'] += round(32 * (actual_a - expected_a))
                    df.at[j, 'elo'] += round(32 * (actual_b - expected_b))
                except Exception as e:
                    print(f"Error in ELO calculation for rows {i} and {j}: {str(e)}")
                    continue
    df['elo'] = round(df['elo'])
    df['elo_diff'] = df['elo']

    if (
        reveal_prelim == False
        and len(leaderboard_df) == 0
    ):
        leaderboard_df = df

    # Add ELO diff from startup
    try:
        if (reveal_prelim == False):
            for i in range(len(df)):
                elo_diff = (df['elo'].iloc[i] - leaderboard_df['elo'].iloc[i])
                if (elo_diff == 0):
                    continue
                if (elo_diff > 0):
                    plus = '<em style="color: green; font-family: monospace">+'
                else:
                    plus = '<em style="color: red; font-family: monospace">'

                df.at[i, 'elo_diff'] = str(df['elo'].iloc[i]) + plus + str(elo_diff) +'</em>'
    except:
        # FIXME: crashes when a TTS from premilinary results passes the vote threshold
        pass

    ## ELO score
    df = df.sort_values(by='elo', ascending=False)
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

    df['elo'] = df['elo_diff']
    df = df[['order', 'name', 'win_rate', 'elo', 'votes']]
    return df
