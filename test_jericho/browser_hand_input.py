from game import init_env, update_actor

# INITIAL_NOTE = 'I am a treasure hunter. My goal is to collect treasures as much as I can (some treasures requiring puzzle-solving).'
INITIAL_ACT = 'wake up'
INITIAL_OBS = """West of House
You are standing in an open field west of a white house, with a boarded front door.
There is a small mailbox here."""
INITIAL_ACTIONS = ['open mailbox', 'north', 'south', 'west']
INITIAL_REWARD = 0

actor = {'counter': 1, 'history': [(INITIAL_ACT, INITIAL_OBS, INITIAL_ACTIONS, INITIAL_REWARD)], 'notebooks': [('','','')], 'reward': 0}
# things_so_far, now_have_to_do, comment = latest_note

def update_latest_note(actor, things_so_far, now_have_to_do, comment):
    actor['notebooks'].append((things_so_far, now_have_to_do, comment))

def print_prompt_v1(actor):
    act, obs, available_actions, reward = actor['history'][-1]
    if reward > 0: 
        obs += f'\nReward got: {reward}\n'
    latest_note = actor['notebooks'][-1]
    things_so_far, now_have_to_do, comment = latest_note
    prompt = f"""TEXT ON YOUR NOTEBOOK
Who am I? I am a treasure hunter. My goal is to collect treasures as much as I can.
I need updating my notebook to keep a dense long-term memory.
Things I have done so far: {things_so_far}
To achieve my goal, now I have to do: {now_have_to_do}
Any comment: {comment}

MY LAST ACTION
{act}

NEW OBSERVATION
{obs}

---

Now, to achieve your goal, think carefully and update your notebook (keep important infomation), then take your next "one" action.

### note start
Who am I? I am a treasure hunter. My goal is to collect treasures as much as I can.
I need updating my notebook to keep a dense long-term memory.
Things I have done so far: <fill in>
To achieve my goal, now I have to do: <fill in> 
Any comment: <fill in>
### note end

My next "one" action is (some suggetions: {available_actions}): <fill in>
"""
    return prompt


