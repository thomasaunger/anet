from anet.tasks.mnist.envs.mnist_env import MNISTEnv

class MNISTEnvSenary(MNISTEnv):
    def __init__(self, procs=0, proc_id=-1, train=True):
        MNISTEnv.__init__(self, 6, procs=procs, proc_id=proc_id, train=train)
