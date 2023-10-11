INITIAL_NOTE = 'I am a treasure hunter. My goal is to collect treasures as much as I can (some treasures requiring puzzle-solving).'
INITIAL_ACT = 'wake up'
INITIAL_OBS = """West of House
You are standing in an open field west of a white house, with a boarded front door.
There is a small mailbox here."""
INITIAL_ACTIONS = ['open mailbox', 'north', 'south', 'west']

actor = {'counter': 1, 'act_res_cmds': [(INITIAL_ACT, INITIAL_OBS, INITIAL_ACTIONS)], 'notebooks': [INITIAL_NOTE], 'reward': 0}

def init_env():
    from jericho import FrotzEnv
    env = FrotzEnv("z-machine-games-master/jericho-game-suite/zork1.z5")
    initial_observation, info = env.reset()
    done = False
    return env

def back(env, actor):
    actor['counter'] -= 1
    actor['reward'] = env.last_total_reward
    actor['act_res_cmds'].pop()
    env.set_state(env.last_state)

def update_actor(env, actor, action):
    env.last_state = env.get_state
    env.last_total_reward = actor['reward']
    obs, reward, done, info = env.step(action)
    actor['counter'] += 1
    if reward > 0:
        print(f'REWARD: {reward}')
        actor['reward'] += reward
    if done:
        print('ALL DONE')
        return
    print(f'YOU: {action}')
    print(f'ENGINE: {obs}')
    engine_response = obs
    available_actions = env.get_valid_actions()
    print(f'available_actions: {available_actions}')
    actor['act_res_cmds'].append((action.strip(), engine_response.strip(), available_actions))


def update_latest_note(actor, latest_note):
    actor['counter'] += 1
    actor['notebooks'].append(latest_note)

def update_note_prompt(latest_note, recent_action_history):
    prompt = f"""TEXT ON YOUR NOTEBOOK:
{latest_note}

RECENT ACTION HISTORY
{recent_action_history}

You are very forgetful. To continue moving forward, you must summarize your action history and record it in a notebook for future reference. Now, please update notes on your notebook (keep the notes short).
NOTES ON YOUR NOTEBOOK: <fill in>
"""
    return prompt

def update_prompt(actor):
    recent_action_history = ""
    for act, res, _ in actor['act_res_cmds'][-10:]:
        act = act.strip()
        res = res.strip()
        recent_action_history += f'YOU: {act}\nENGINE:\n{res}\n'
    if len(actor['act_res_cmds']) > 10:
        recent_action_history = f'...(refering to notebook for long-term memory)\n{recent_action_history}'
    available_actions = actor['act_res_cmds'][-1][-1]
    latest_note = actor['notebooks'][-1]
    if actor['counter'] % 10 == 0:
        return update_note_prompt(latest_note, recent_action_history)
    prompt = f"""TEXT ON YOUR NOTEBOOK:
{latest_note}

RECENT ACTION HISTORY
{recent_action_history}

Now, to achieve your goal, choose your next "one" action from available command list:
{available_actions}
Your choice: <fill in>
"""
    return prompt


