import torch
import numpy as np
from torch.optim import Adam
from torch.distributions import MultivariateNormal
from game import Game

class PPO:
    def __init__(self, policy, game:Game, action_space_dim, obs_space_dim):
        self._init_params()
        self.act_dim = action_space_dim
        self.obs_dim = obs_space_dim
        
        self.actor = policy(self.obs_dim, self.act_dim)
        self.critic = policy(self.obs_dim, 1)
        self.game = game
        
        self.actor_o = Adam(self.actor.parameters(), lr=self.lr)
        self.critic_o = Adam(self.critic.parameters(), lr=self.lr)
        
        self.cov_var = torch.full(size=(self.act_dim,), fill_value=0.5)
        self.cov_mat = torch.diag(self.cov_var)
        
        self.logging = {
            'timesteps_done': 0,
            'iterations_done': 0,
            'batch_lengths': [],
            'batch_r': [],
            'actor_loss': []    
        }
        
    def learn(self, i):
        t_done = 0
        i_done = 0
        while i_done < i+1:
            batch_obs, batch_acts, batch_log_probs, batch_rtgs, batch_lengths = self.get_all_values()
            
            t_done += np.sum(batch_lengths)
            i_done += 1
            
            self.logging['timesteps_done'] = t_done
            self.logging['iterations_done'] = i_done
            
            V, _ = self.compare(batch_obs, batch_acts)
            A = batch_rtgs - V.detach()
            
            for _ in range(self.n_updates_per_iteration):
                V, curr_log_probs = self.compare(batch_obs, batch_acts)
                
                ratios = torch.exp(curr_log_probs - batch_log_probs)
                
                surr1 = ratios * A
                surr2 = torch.clamp(ratios, 1 - self.clip, 1 + self.clip) * A
                
                actor_loss = (-torch.min(surr1, surr2)).mean()
                critic_loss = torch.nn.MSELoss()(V, batch_rtgs)
                
                self.actor_o.zero_grad()
                actor_loss.backward(retain_graph=True)
                self.actor_o.step()
                
                self.critic_o.zero_grad()
                critic_loss.backward()
                self.critic_o.step()
                
                self.logging['actor_loss'].append(actor_loss.detach())
            
            self._log_summary()
            
            if i_done % self.save_freq == 0:
                torch.save(self.actor.state_dict(), './ppo_actor.pth')
                torch.save(self.critic.state_dict(), './ppo_critic.pth')

    def compare(self, obs, acts):
        V = self.critic(obs).squeeze()
        
        mean = self.actor(obs)
        dist = MultivariateNormal(mean, self.cov_mat)
        log_probs = dist.log_prob(acts)
        
        return V, log_probs

    def get_all_values(self):
        batch_obs = []
        batch_acts = []
        batch_log_probs = []
        batch_r = []
        batch_rtgs = []
        batch_lengths = []
        
        ep_r = []
        
        t_done = 0
        
        while t_done < self.timesteps_per_batch:
            ep_r = []
            
            obs = self.game.reset_ppo()
            obs = np.array(obs, dtype=np.float)
            obs = obs.reshape((1, 4))
            done = False
            
            for ep in range(self.max_timesteps_per_episode):
                t_done += 1
                
                batch_obs.append(obs)
                
                action, log_prob = self.get_action(obs)
                r, done, obs = self.game.play_step(np.argmax(action))
                obs = np.array(obs, dtype=np.float)
                obs = obs.reshape((1, 4))
                
                ep_r.append(r)
                batch_acts.append(action)
                batch_log_probs.append(log_prob)
                
                if done:
                    break
            
            batch_lengths.append(ep + 1)
            batch_r.append(ep_r)
                
        batch_obs = torch.tensor(batch_obs, dtype=torch.float)
        batch_acts = torch.tensor(batch_acts, dtype=torch.float)
        batch_log_probs = torch.tensor(batch_log_probs, dtype=torch.float)
        batch_rtgs = self.compute_rtgs(batch_r)
        
        return batch_obs, batch_acts, batch_log_probs, batch_rtgs, batch_lengths

    def compute_rtgs(self, r):
        batch_rtgs = []
        
        for ep in reversed(r):
            discount_r = 0
            
            for r in reversed(ep):
                discount_r = r + discount_r * self.gamma
                batch_rtgs.insert(0, discount_r)
        
        batch_rtgs = torch.tensor(batch_rtgs, dtype=torch.float)
        
        return batch_rtgs

    def get_action(self, obs):
        mean = self.actor(obs)
        dist = MultivariateNormal(mean, self.cov_mat)
        action = dist.sample()
        log_prob = dist.log_prob(action)
        
        return action.detach().numpy(), log_prob.detach()
        
    def _init_params(self):
        self.timesteps_per_batch = 4000                
        self.max_timesteps_per_episode = 2000          
        self.n_updates_per_iteration = 5               
        self.lr = 0.1                            
        self.gamma = 0.95                              
        self.clip = 0.1                               
                  
        self.save_freq = 10
    
    def _log_summary(self):
        t_done = self.logging['timesteps_done']
        i_done = self.logging['iterations_done']
        loss = np.mean([losses.float().mean() for losses in self.logging['actor_loss']])
        loss = str(round(loss, 5))

        print(flush=True)
        print(f"-------------------- Iteration #{i_done} --------------------", flush=True)
        print(f"Average Loss: {loss}", flush=True)
        print(f"Timesteps So Far: {t_done}", flush=True)
        print(f"------------------------------------------------------", flush=True)
        print(flush=True)

        self.logging['actor_loss'] = []