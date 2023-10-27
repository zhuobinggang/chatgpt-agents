from game import init_env
DOTFILE = 'dd.dot'
PNGFILE = 'dd.png'
NAME_OF_NODE_EXIST = []

# 遍历地图

def back(env):
    env.set_state(env.last_state)

def add_node_avoid_name_repeat(G, key, name):
    global NAME_OF_NODE_EXIST
    if name in NAME_OF_NODE_EXIST:
        name = f'{name}({key})'
    else:
        NAME_OF_NODE_EXIST.append(name)
    G.add_node(key, label = name, updated = 0)


def explore_all_directions(env, G):
    global NAME_OF_NODE_EXIST
    directions_to_explore = []
    states_to_explore = []
    location = env.get_player_location()
    print(f'START EXPLORE: {location.name}({location.num})')
    if location.num not in G.nodes:
        add_node_avoid_name_repeat(G, location.num, location.name)
    if G.nodes[location.num]['updated'] == 1:
        print(f'{location.name}({location.num}) already updated!')
        return [], []
    else:
        print(f'Trying to update {location.name}({location.num}).')
        G.nodes[location.num]['updated'] = 1
        env.last_state = env.get_state()
        available_actions = env.get_valid_actions()
        for direction in ['east', 'south', 'west', 'north', 'up', 'down', 'southwest', 'northwest', 'southeast', 'northeast']:
            if direction not in available_actions:
                print(f'{direction} not in available_actions')
            else: # 只要存在可以探索的方向即增加边, 然后判断是否需要探索这个新的地点
                # obs, reward, done, info = env.step(action)
                _ = env.step(direction) # NOTE: location updated, record as edge
                new_location = env.get_player_location()
                # 如果这个地点已经存在地图里边(不一定探索过)
                if new_location.num in G:
                    print(f'From {location.name} go {direction} is {new_location.name}')
                    if G.nodes[new_location.num]['updated'] == 1: # 如果已经探索过，增加边就结束了
                        print(f'But already explore.')
                    else: # 否则标明需要探索这个方向
                        directions_to_explore.append(direction)
                        states_to_explore.append(env.get_state())
                else: # 如果不存在需要增加节点
                    print(f'Adding new position: {new_location.name}({new_location.num})')
                    add_node_avoid_name_repeat(G, new_location.num, new_location.name)
                    directions_to_explore.append(direction) # 标明需要探索这个方向
                    states_to_explore.append(env.get_state())
                # 增加边
                G.add_edge(location.num, new_location.num, label=direction)
                back(env) # 回退
    return directions_to_explore, states_to_explore

def draw(G):
    import networkx as nx
    import pydot
    nx.drawing.nx_pydot.write_dot(G, DOTFILE)
    (graph,) = pydot.graph_from_dot_file(DOTFILE)
    graph.write_png(PNGFILE)

def bfs(G, env, prev_level_states, level = 0):
    if len(prev_level_states) < 1:
        print('ALL DONE')
    else:
        print(f'LEVEL {level} BFS START')
        print('')
        new_level_states = []
        for state in prev_level_states:
            env.set_state(state)
            directions, new_states = explore_all_directions(env, G)
            new_level_states += new_states
        bfs(G, env, new_level_states, level + 1)


def start():
    import networkx as nx
    G = nx.MultiDiGraph()
    env = init_env()
    bfs(G, env, [env.get_state()])
    return G

