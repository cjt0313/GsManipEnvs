from dataclasses import dataclass, field
from typing import Optional, Any
import genesis as gs
import hydra
from hydra.core.config_store import ConfigStore
from omegaconf import ListConfig, OmegaConf

@dataclass
class InitConfig:
    seed: int = 42
    precision: str = "32"
    debug: bool = False
    logging_level: Any = None
    backend: Any = gs.constants.backend.gpu
    theme: str = "light"
    logger_verbose_time: bool = False

@dataclass
class SimConfig:
    dt: float =0.02
    substeps: int =1
    substeps_local: Any =None
    gravity: tuple = (0.0, 0.0, -9.81)
    floor_height :float=0.0
    requires_grad : bool=False

@dataclass
class SceneConfig:
    show_FPS: bool = True
    show_viewer: bool = True

@dataclass
class VisConfig:
    show_world_frame: bool = True
    world_frame_size: float = 1.0
    show_link_frame: bool = True
    link_frame_size: float = 0.2
    show_cameras: bool = False
    shadow: bool = True
    plane_reflection: bool = False
    background_color: tuple = (0.04, 0.08, 0.12)
    ambient_light: tuple = (0.1, 0.1, 0.1)
    visualize_mpm_boundary: bool = False
    visualize_sph_boundary: bool = False
    visualize_pbd_boundary: bool = False
    # ['entity', 'link', 'geom']
    segmentation_level: str = "link"
    # ['sphere', 'tet']
    render_particle_as: str = "sphere"
    # scale applied to actual particle size for rendering
    particle_size_scale: float = 1.0
    # scale of force visualization, m/N. E.g. the force arrow representing 10N wille be 0.1m long if scale is 0.01.
    contact_force_scale: float = 0.01
    # number of neighbor particles used to compute vertex position of the visual mesh. Used for rendering deformable bodies.
    n_support_neighbors: int = 12
    n_rendered_envs: Optional[int] = None  # number of environments being rendered
    lights: ListConfig = OmegaConf.create([
        {"type": "directional", "dir": (-1, -1, -1), "color": (1.0, 1.0, 1.0), "intensity": 5.0}
    ])

@dataclass
class ViewerConfig:
    res: Optional[tuple] = None
    refresh_rate: int = 60
    max_FPS: Optional[int] = 60
    camera_pos: tuple = (4, 4, 4)
    camera_lookat: tuple = (0.0, 0.0, 0)
    camera_up: tuple = (0.0, 0.0, 1.0)
    camera_fov: float = 40


@dataclass
class RigidConfig:
    enable_collision: bool = True
    enable_joint_limit: bool = True
    enable_self_collision: bool = True
    max_collision_pairs: int = 100
    integrator: Any = gs.integrator.approximate_implicitfast
    IK_max_targets: int = 6

    # constraint solver
    constraint_solver: Any = gs.constraint_solver.CG
    iterations: int = 100
    tolerance: float = 1e-5
    ls_iterations: int = 50
    ls_tolerance: float = 1e-2
    sparse_solve: bool = False
    contact_resolve_time: Optional[float] = None
    use_contact_island: bool = False
    # collision detection branch for box-box pair, slower but more stable.
    box_box_detection: bool = True

@dataclass
class RobotConfig:
    path: str ='xml/franka_emika_panda/panda.xml'
    # gs.materials.Rigid()
    material=None
    # gs.surfaces.Default()
    surface=None
    #
    visualize_contact=True
    # rigid: ["visual", "collision", "sdf"]
    # deformable: ["particle", "recon"]
    vis_mode=None

@dataclass
class BaseConfig:
    ## basic config of simulator
    init: InitConfig = field(default_factory=InitConfig)
    scene: SceneConfig = field(default_factory=SceneConfig)
    sim: SimConfig = field(default_factory=SimConfig)
    vis: VisConfig = field(default_factory=VisConfig)
    viewer: ViewerConfig = field(default_factory=ViewerConfig)
    ## config of rigid object model
    rigid: RigidConfig = field(default_factory=RigidConfig)
    ## config of scene entities
    robot: RobotConfig = field(default_factory=RobotConfig)
    
# # Hydra configuration setup
from hydra.core.config_store import ConfigStore
cs = ConfigStore.instance()
cs.store(name="base_config", node=BaseConfig)
