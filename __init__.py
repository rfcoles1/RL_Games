from gym.envs.registration import register

#Dumb Loop
register(
    id='DumbLoop-v0',
    entry_point='Games.Dumb_Loop.loop_perimeter:LoopEnv',
    max_episode_steps = 200,
)

register(
    id='DumbLoop-v1',
    entry_point='Games.Dumb_Loop.loop_off_perimeter:LoopEnv',
    max_episode_steps = 200,
)

register(
    id='DumbLoop-v2',
    entry_point='Games.Dumb_Loop.loop_area:LoopEnv',
    max_episode_steps = 200,
)

#---------------------------------------------#
#ODE Reactions 
register(
    id='Reaction-v0',
    entry_point='Games.ODE_Reactions.Reaction_1:Reaction_Env',
    max_episode_steps=100,
)

register(
    id='Reaction-v1',
    entry_point='Games.ODE_Reactions.Reaction_2:Reaction_Env',
    max_episode_steps=100,
)

register(
    id='Reaction-v2',
    entry_point='Games.ODE_Reactions.Reaction_3:Reaction_Env',
    max_episode_steps=100,
)

register(
    id='Reaction-v3',
    entry_point='Games.ODE_Reactions.Reaction_4:Reaction_Env',
    max_episode_steps=100,
)

#---------------------------------------------#
#Water Heating 

#up or down increase
register(
    id='WaterHeater-v0',
    entry_point='Games.WaterHeater.heat_game_v0:HeatEnv',
    max_episode_steps = 100,
)

#discrete 'clicks' on a dial
register(
    id='WaterHeater-v1',
    entry_point='Games.WaterHeater.heat_game_v1:HeatEnv',
    max_episode_steps = 100,
)

#continuous dial 
register(
    id='WaterHeater-v2',
    entry_point='Games.WaterHeater.heat_game_v2:HeatEnv',
    max_episode_steps = 100,
)

#---------------------------------------------#
#Function Learning

register(
    id = 'SinGame-v0',
    entry_point = 'Games.FunctionLearning.SinGame:SinEnv',
    max_episode_steps = 100,
)

register(
    id = 'SinGame-v1',
    entry_point = 'Games.FunctionLearning.SinGame_v2:SinEnv2',
    max_episode_steps = 100,
)

register(
    id = 'FuncGame-v1',
    entry_point = 'Games.FunctionLearning.FuncGame2d:FuncEnv',
    max_episode_steps = 100,
)

#---------------------------------------------#

