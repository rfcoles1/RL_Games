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
#Variable MC
register(
    id='VMC-v0',
    entry_point='Games.VariableMountainCar.VarMC_BothSides:VMC_Env',
    max_episode_steps = 200,
)

register(
    id='VMC-v1',
    entry_point='Games.VariableMountainCar.VarMC_RightSide:VMC_Env',
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

#---------------------------------------------#
#Function Learning

register(
    id = 'SinGame-v11',
    entry_point = 'Games.FunctionLearning.SinGame_Old:SinEnv',
    max_episode_steps = 100,
)

register(
    id = 'SinGame-v1',
    entry_point = 'Games.FunctionLearning.SinGame_v1:SinEnv2',
    max_episode_steps = 100,
)

register(
    id = 'SinGame-v2',
    entry_point = 'Games.FunctionLearning.SinGame_v2:SinEnv2',
    max_episode_steps = 100,
)

register(
    id = 'SinGame-v3',
    entry_point = 'Games.FunctionLearning.SinGame_v3:SinEnv2',
    max_episode_steps = 100,
)

#---------------------------------------------#
#Gaussian Processes

register(
    id = 'GP_Water-v0',
    entry_point = 'Games.Boiling.boiling_env:HeatEnv',
    max_episode_steps = 100,
)



