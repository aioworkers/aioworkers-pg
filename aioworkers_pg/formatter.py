from aioworkers.core.formatter import AsIsFormatter, BaseFormatter, FormattedEntity, Registry


class DictFormatter(BaseFormatter):
    name = 'dict'

    @staticmethod
    def decode(row):
        return dict(row)

    @staticmethod
    def encode(data):
        return data


class RowFormatter(AsIsFormatter):
    name = 'row'


class PGFormattedEntity(FormattedEntity):
    registry = Registry()
    registry(DictFormatter)
    registry(RowFormatter)

    def set_config(self, config):
        super().set_config(config)
        self._formatter = self.registry.get(self.config.get('format'))
