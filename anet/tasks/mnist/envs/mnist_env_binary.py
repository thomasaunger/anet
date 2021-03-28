import gym
import numpy as np
import torch
import torchvision

from gym import error, spaces, utils
from gym.utils import seeding
from torchvision import transforms

transform = transforms.Compose([
    # you can add other transformations in this list
    transforms.ToTensor()
])

def newLoader():
    mnist_data = torchvision.datasets.MNIST("", train=True, download=True, transform=transform)
    
    idx = ~(~(mnist_data.targets == 0) * ~(mnist_data.targets == 1))
    mnist_data.data    = mnist_data.data[   idx]
    mnist_data.targets = mnist_data.targets[idx]
    
    data_loader = torch.utils.data.DataLoader(mnist_data,
                                              batch_size = 1,
                                              shuffle    = True)
    
    return data_loader

class MNISTEnvBinary(gym.Env):
    
    def __init__(self):
        self.action_space = spaces.Discrete(10)
        
        self.observation_space = spaces.Box(
            low   = 0.0,
            high  = 1.0,
            shape = (28, 28, 1),
            dtype = "float32"
        )
        self.observation_space = spaces.Dict({
            "image": self.observation_space
        })
        
        data_loader = newLoader()
        self.data = enumerate(data_loader)
    
    def step(self, action):
        # Examples
        #reward    = 0
        #done      = False
        #image     = np.zeros((self.width, self.height, 3), dtype='uint8')
        #agent_dir = 0
        #mission   = ""
        
        if action == self.target:
            reward = 1.0
        else:
            reward = 0.0
        
        done = True
        
        return self.obs, reward, done, {}
    
    def reset(self):
        try:
            batch_idx, (data, target) = next(self.data)
        except StopIteration:
            data_loader = newLoader()
            self.data = enumerate(data_loader)
            batch_idx, (data, target) = next(self.data)
        
        image = np.zeros((28, 28, 1))
        image[:, :, 0] = data.squeeze().numpy()
        self.target = target
        
        agent_dir = 0
        
        mission   = "unknown"
        
        # Observations are dictionaries containing:
        # - an image (partially observable view of the environment)
        # - the agent's direction/orientation (acting as a compass)
        # - a textual mission string (instructions for the agent)
        self.obs = {
            "image":     image,
            "direction": agent_dir,
            "mission":   mission
        }
        
        return self.obs