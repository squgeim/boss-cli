''' Initialization module. '''

import sys
from fabric.api import env, task
from .config import load as load_config, get as get_config, get_stage_config
from .api.shell import get_stage


def init(module_name):
    ''' Initialize the boss configuration. '''
    config = load_config()
    stage = get_stage()
    module = sys.modules[module_name]
    define_stage_tasks(module, config)

    return (config, stage)


def define_stage_tasks(module, config):
    ''' Define tasks for the stages dynamically. '''
    for (stage_name, value) in config['stages'].iteritems():
        task_func = task(name=stage_name)(configure_env)
        setattr(module, stage_name, task_func)


def configure_env():
    ''' Configures the fabric env. '''
    config = get_config()
    stage = get_stage()
    stage_config = get_stage_config(stage)
    env.user = config['user']
    env.cwd = stage_config.get('app_dir') or config['app_dir']
    env.hosts = [stage_config['host']]
