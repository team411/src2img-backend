import os
import codecs
from ConfigParser import ConfigParser


class ConfigLoader(object):

    def __init__(self, paths, filename):
        self.filename = filename
        self._config = self._merge(self._load_configs(paths))

    def _check_config(self, path):
        # Implement ME
        return True, None

    def _load_configs(self, paths):
        res = []
        for path in paths:
            config = self._load_config(path)
            if config is None:
                continue
            sections = config.sections()
            config_dict = {}
            for section in sections:
                items = config.items(section)
                items_dict = {}
                for key, value in items:
                    items_dict[key] = value

                config_dict[section] = items_dict
            res.append(config_dict)

        if len(res) == 0:
            raise RuntimeError(
                'No config files found. Check your paths `{0}`'.format(paths))

        return res

    def _merge(self, configs):
        res = {}
        for config in configs:
            for section, content in config.iteritems():
                if section not in res:
                    res[section] = {}
                res[section].update(content)

        return res

    def _load_config(self, path):
        full_path = os.path.join(path, self.filename)
        if not os.path.exists(full_path):
            return None
        is_valid, err = self._check_config(full_path)
        if not is_valid:
            raise TypeError('Invalid config data: {0}'.format(err))

        config = ConfigParser()
        config.readfp(codecs.open(full_path, 'r', 'utf-8'))

        return config

    def has_section(self, section):
        return section in self._config

    def dict(self):
        return self._config

    def get(self, section, key, default=None):
        return self._config.get(section, {}).get(key, default)
