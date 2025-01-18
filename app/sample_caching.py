import gradio as gr
import itertools
import random
from typing import List, Tuple, Set, Dict
from hashlib import md5, sha1
# from .synth import clear_stuff

class User:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.voted_pairs: Set[Tuple[str, str]] = set()

class Sample:
    def __init__(self, filename: str, transcript: str, modelName: str):
        self.filename = filename
        self.transcript = transcript
        self.modelName = modelName

# cache audio samples for quick voting
cached_samples: List[Sample] = []

@spaces.GPU(duration=10)
def asr_cached_for_dataset():

    for caudio in cached_samples:
        pass
    return True

voting_users = {
    # userid as the key and USER() as the value
}
# List[Tuple[Sample, Sample]]
all_pairs = []


def get_userid(session_hash: str, request):
    # JS cookie
    if (session_hash != ''):
        # print('auth by session cookie')
        return sha1(bytes(session_hash.encode('ascii')), usedforsecurity=False).hexdigest()

    if request.username:
        # print('auth by username')
        # by HuggingFace username - requires `auth` to be enabled therefore denying access to anonymous users
        return sha1(bytes(request.username.encode('ascii')), usedforsecurity=False).hexdigest()
    else:
        # print('auth by ip')
        # by IP address - unreliable when gradio within HTML iframe
        # return sha1(bytes(request.client.host.encode('ascii')), usedforsecurity=False).hexdigest()
        # by browser session cookie - Gradio on HF is run in an HTML iframe, access to parent session required to reach session token
        # return sha1(bytes(request.headers.encode('ascii'))).hexdigest()
        # by browser session hash - Not a cookie, session hash changes on page reload
        return sha1(bytes(request.session_hash.encode('ascii')), usedforsecurity=False).hexdigest()

# Give user a cached audio sample pair they have yet to vote on
def give_cached_sample(session_hash: str, autoplay: bool, request: gr.Request):
    # add new userid to voting_users from Browser session hash
    # stored only in RAM
    userid = get_userid(session_hash, request)

    if userid not in voting_users:
        voting_users[userid] = User(userid)

    def get_next_pair(user: User):
        # FIXME: all_pairs var out of scope
        # all_pairs = generate_matching_pairs(cached_samples)

        # for pair in all_pairs:
        for pair in generate_matching_pairs(cached_samples):
            hash1 = md5(bytes((pair[0].modelName + pair[0].transcript).encode('ascii'))).hexdigest()
            hash2 = md5(bytes((pair[1].modelName + pair[1].transcript).encode('ascii'))).hexdigest()
            pair_key = (hash1, hash2)
            if (
                pair_key not in user.voted_pairs
                # or in reversed order
                and (pair_key[1], pair_key[0]) not in user.voted_pairs
            ):
                return pair
        return None

    pair = get_next_pair(voting_users[userid])
    if pair is None:
        comp_defaults = []
        for i in range(0, 14):
            comp_defaults.append(gr.update())
        return [
            *comp_defaults,
            # *clear_stuff(),
            # disable get cached sample button
            gr.update(interactive=False)
        ]

    return (
        gr.update(visible=True, value=pair[0].transcript, elem_classes=['blurred-text']),
        "Synthesize",
        gr.update(visible=True), # r2
        pair[0].modelName, # model1
        pair[1].modelName, # model2
        gr.update(visible=True, value=pair[0].filename, interactive=False, autoplay=autoplay), # aud1
        gr.update(visible=True, value=pair[1].filename, interactive=False, autoplay=False), # aud2
        gr.update(visible=True, interactive=False), #abetter
        gr.update(visible=True, interactive=False), #bbetter
        gr.update(visible=False), #prevmodel1
        gr.update(visible=False), #prevmodel2
        gr.update(visible=False), #nxt round btn
        # reset aplayed, bplayed audio playback events
        False, #aplayed
        False, #bplayed
        # fetch cached btn
        gr.update(interactive=True)
    )

def generate_matching_pairs(samples: List[Sample]) -> List[Tuple[Sample, Sample]]:
    transcript_groups: Dict[str, List[Sample]] = {}
    samples = random.sample(samples, k=len(samples))
    for sample in samples:
        if sample.transcript not in transcript_groups:
            transcript_groups[sample.transcript] = []
        transcript_groups[sample.transcript].append(sample)

    matching_pairs: List[Tuple[Sample, Sample]] = []
    for group in transcript_groups.values():
        matching_pairs.extend(list(itertools.combinations(group, 2)))

    return matching_pairs



# note the vote on cached sample pair
def voted_on_cached(modelName1: str, modelName2: str, transcript: str, session_hash: str, request: gr.Request):
    userid = get_userid(session_hash, request)
    # print(f'userid voted on cached: {userid}')

    if userid not in voting_users:
        voting_users[userid] = User(userid)

    hash1 = md5(bytes((modelName1 + transcript).encode('ascii'))).hexdigest()
    hash2 = md5(bytes((modelName2 + transcript).encode('ascii'))).hexdigest()

    voting_users[userid].voted_pairs.add((hash1, hash2))
    return []