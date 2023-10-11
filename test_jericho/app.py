from jericho import *
env = FrotzEnv("z-machine-games-master/jericho-game-suite/zork1.z5")
initial_observation, info = env.reset()
done = False
valid_actions = env.get_valid_actions()
obs, reward, done, info = env.step('break egg')
