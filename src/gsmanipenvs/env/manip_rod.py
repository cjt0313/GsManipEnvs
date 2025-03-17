from omegaconf import DictConfig
import numpy as np
import genesis as gs
import sys
import torch
from gsmanipenvs.env.util import euler_to_quaternion
import hydra
from hydra.core.config_store import ConfigStore
from gsmanipenvs.config.base_config import BaseConfig 
from omegaconf import OmegaConf

class ExploreRod:
    def __init__(self, cfg: DictConfig):
        self.cfg = OmegaConf.to_container(cfg, resolve=True)
        ## genesis init
        print(self.cfg["init"])
        gs.init(**self.cfg["init"])
        self.scene = gs.Scene(
            sim_options=gs.options.SimOptions(**self.cfg["sim"]),
            vis_options=gs.options.VisOptions(**self.cfg["vis"]),
            viewer_options=gs.options.ViewerOptions(
                **self.cfg["viewer"]
                ),
            rigid_options=gs.options.RigidOptions(
                **self.cfg["rigid"]
                ),
            **self.cfg["scene"]
                )
        plane = self.scene.add_entity(gs.morphs.Plane())

        path = self.cfg["robot"]["path"]
        print(self.cfg["robot"], path)
        franka = self.scene.add_entity(
            gs.morphs.MJCF(file = path)
            # **self.cfg["robot"]
        )

        B = 20
        cam_0 = self.scene.add_camera()
        self.scene.build(n_envs=B, env_spacing=(2.0, 2.0))

    def step(self):
        self.scene.step()

@hydra.main(version_base=None, config_name="base_config")
def main(cfg: DictConfig):
    # 将配置传递给类
    env = ExploreRod(cfg)
    for i in range(1000):
        env.step()

if __name__ == "__main__":
    main()