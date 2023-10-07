"""sample jupyterhub config file for testing

configures jupyterhub with dummyauthenticator and simplespawner
to enable testing without administrative privileges.
"""

c = get_config()  # noqa

from jupyterhub.auth import DummyAuthenticator

c.JupyterHub.authenticator_class = DummyAuthenticator

# Optionally set a global password that all users must use
# c.DummyAuthenticator.password = "your_password"

from jupyterhub.spawner import SimpleLocalProcessSpawner

c.JupyterHub.spawner_class = SimpleLocalProcessSpawner

# only listen on localhost for testing
# c.JupyterHub.bind_url = 'http://127.0.0.1:8001'

# ------------------------------------------------------------------------------

# configurable_http_proxy 代理设置
# 允许hub启动代理 可以不写，默认为False   启动configurable-http-proxy
c.ConfigurableHTTPProxy.should_start = True
# proxy与hub与代理通讯
c.ConfigurableHTTPProxy.api_url = 'http://127.0.0.1:8088'

# 对外登录设置的ip
c.JupyterHub.ip = '192.168.0.21'
c.JupyterHub.port = 8088
c.PAMAuthenticator.encoding = 'utf8'
c.JupyterHub.db_url = "mysql+pymysql://jupyter:jpy123@192.168.0.21:3972/jupyter?charset=utf8mb4"
# 用户名单设置，默认身份验证方式PAM与NUIX系统用户管理层一致，root用户可以添加用户等，

# c.Authenticator.allowed_users = {'test1', 'test2'}
c.Authenticator.admin_users = {'root'}  # 管理员用户
c.DummyAuthenticator.password = "123123"  # 初始密码设置
# 管理员有权在各自计算机上以其他用户身份登录，以进行调试
c.JupyterHub.admin_access = True
# 此选项通常用于 JupyterHub 的托管部署，以避免在启动服务之前手动创建所有用户
c.LocalAuthenticator.create_system_users = True

# 设置每个用户的 book类型和工作目录（创建.ipynb文件自动保存的地方）
c.Spawner.notebook_dir = '~'
c.Spawner.default_url = '/lab'
c.Spawner.args = ['--allow-root']

# 为jupyterhub 添加额外服务，用于处理闲置用户进程。
# 使用时不好使安装一下：pip install jupyterhub-ilde-culler
c.JupyterHub.services = [
    {
        'name': 'idle-culler',
        'command': ['python3', '-m', 'jupyterhub_idle_culler', '--timeout=3600'],
        'admin': True
        # 1.5.0 需要服务管理员权限，去kill 部分闲置的进程notebook, 2.0版本已经改了，
        # 可以只赋给 idel-culler 部分特定权限，roles
    }
]
