from os import environ
from types import NoneType

from flask.ext.cache import Cache


def init_cacheify(app, config=None):
    """Auto-configure an appropriate cache for your Flask application.

    :param app app: Your Flask application.
    :param dict config: Your Flask configuration dictionary.
    """
    if not isinstance(config, (NoneType, dict)):
        raise ValueError('ERROR: config must be an instance of dict or '
                'NoneType.')

    config = config if config else app.config
    config.setdefault('CACHE_TYPE', 'simple')

    # Look for MemCachier.
    if any([k.startswith('MEMCACHIER_') for k in environ]):
        config.setdefault('CACHE_TYPE', 'saslmemcached')
        config.setdefault('CACHE_MEMCACHED_SERVERS',
                [environ.get('MEMCACHIER_SERVERS')])
        config.setdefault('CACHE_MEMCACHED_USERNAME',
                environ.get('MEMCACHIER_USERNAME'))
        config.setdefault('CACHE_MEMCACHED_PASSWORD',
                environ.get('MEMCACHIER_PASSWORD'))

    # Look for RedisGreen.
    if any([k.startswith('REDISGREEN_') for k in environ]):
        config['CACHE_TYPE'] = 'redis'
        config.setdefault('CACHE_REDIS_URL', environ.get('REDISGREEN_URL'))

    return Cache(app, config)
