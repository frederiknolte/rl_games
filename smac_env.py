import gym
import numpy as np
from smac.env import StarCraft2Env

class SMACEnv(gym.Env):
    def __init__(self, name="3m", replay_save_freq=5000, **kwargs):
        gym.Env.__init__(self)
        self.env = StarCraft2Env(map_name=name)
        self.env_info = self.env.get_env_info()
        self.replay_save_freq = replay_save_freq
        self._game_num = 0
        self.n_actions = self.env_info["n_actions"]
        self.n_agents = self.env_info["n_agents"]

        self.action_space = gym.spaces.Discrete(self.n_actions)

        self.observation_space = gym.spaces.Box(low=0, high=1, shape=(self.env_info['obs_shape'], ), dtype=np.float32)

    def _preproc_state_obs(self, state, obs):
        return obs

    def get_number_of_agents(self):
        return self.n_agents

    def reset(self):
        if self._game_num % self.replay_save_freq == 1:
            print('saving replay')
            self.env.save_replay()
        self._game_num += 1
        obs, state = self.env.reset()
        obses = self._preproc_state_obs(state, obs)

        return obses

    def step(self, actions):
        rewards, dones, info = self.env.step(actions)
        obs = self.env.get_obs()
        state = self.env.get_state()
        obses = self._preproc_state_obs(state, obs)
        return obses, rewards, dones, info

    def get_action_mask(self):
        avail_actions = []
        for agent_id in range(self.n_agents):
            avail_actions.append(self.env.get_avail_agent_actions(agent_id))

        return np.array(avail_actions, dtype=np.bool)

