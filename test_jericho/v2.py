from game import init_env, update_actor, back

INITIAL_ACT = 'wake up'
INITIAL_OBS = """West of House
You are standing in an open field west of a white house, with a boarded front door.
There is a small mailbox here."""
INITIAL_ACTIONS = ['open mailbox', 'north', 'south', 'west']
INITIAL_NOTE = 'I am a treasure hunter. My goal is to collect treasures as much as I can.'
INITIAL_REWARD = 0

actor = {'counter': 1, 'history': [(INITIAL_ACT, INITIAL_OBS, INITIAL_ACTIONS, INITIAL_REWARD)], 'notebooks': [''], 'reward': 0, 'old_history': []}

def print_summarization_prompt(actor):
    prompt = 'Summarize your action history.\n\n'
    history = actor['history']
    for item in history:
        act, obs, available_actions, reward = item
        prompt += f'YOU: {act}\n'
        prompt += f'OBSERVATION: {obs}\n'
    prompt += f'\nSummarization: <fill in>\n'
    print(prompt)
    # update notebook
    actor['old_history'] += history
    actor['history'].clear()

def update_notebook(actor, note):
    actor['notebooks'].append(note)

def update_actor(env, actor, action, things_so_far = None, now_have_to_do = None, comment = None):
    env.last_state = env.get_state()
    env.last_total_reward = actor['reward']
    obs, reward, done, info = env.step(action)
    obs = obs.strip()
    actor['counter'] += 1
    if reward > 0:
        actor['reward'] += reward
        # 增加分数说明到obs里面
        obs += f"\nTreasure Reward: {reward}, Total Reward: {actor['reward']}"
    if done:
        print('ALL DONE')
        return
    engine_response = obs
    available_actions = env.get_valid_actions()
    print(f'{obs}\n')
    if (actor['counter'] - 1) % 10 == 0:
        print('Before moving on, summarize your action history: <fill in>')
    print(f'Now, think step by step and take your next "one" action (some suggestions: {available_actions}).')
    actor['history'].append((action.strip(), engine_response.strip(), available_actions, reward))
    if things_so_far is not None:
        actor['notebooks'].append((things_so_far, now_have_to_do, comment))
    location = env.get_player_location()
    print(f'{location.name}\n{location.num}\n')

def print_prompt(actor):
    act, obs, available_actions, reward = actor['history'][-1]
    total_reward = actor['reward']
    latest_note = actor['notebooks'][-1]
    if len(latest_note) < 1:
        latest_note = '(empty)'
    notebook_prompt = "TEXT ON YOUR NOTEBOOK\n"
    notebook_prompt += f"{INITIAL_NOTE}\n"
    notebook_prompt += f"Summarization of what I have done: {latest_note}"
    ###
    prompt = f"""{notebook_prompt}

YOUR LAST ACTION
{act}

NEW OBSERVATION
{obs}

---

Now, to achieve your goal, let's think about the situation step by step then choose your next "one" action (some suggetions: {available_actions}).
"""
    print(prompt)
    if actor['counter'] % 10 == 0:
        print(print_summarization_prompt(actor))
