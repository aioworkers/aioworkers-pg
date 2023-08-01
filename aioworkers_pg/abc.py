from typing import Optional

from aioworkers.core.base import AbstractConnector
from aioworkers.core.config import ValueExtractor
from aioworkers.net.uri import URI


class AbstractPGConnector(AbstractConnector):
    _dsn: Optional[URI] = None
    _default_dsn: URI = URI("postgresql:///")
    _default_port: int = 5432

    def set_config(self, config: ValueExtractor) -> None:
        cfg: ValueExtractor = config.new_parent(logger=__package__)
        super().set_config(cfg)

        dsn = self.config.get_uri("dsn", null=True)

        host = self.config.get("host")
        if host:
            dsn = (dsn or self._default_dsn).with_host(host)

        port = self.config.get_int("port", null=True)
        if port in {self._default_port}:
            port = 0
        if port is not None:
            dsn = (dsn or self._default_dsn).with_port(port)

        username = self.config.get("username")
        if username:
            dsn = (dsn or self._default_dsn).with_username(username)

        password = self.config.get("password")
        if password:
            dsn = (dsn or self._default_dsn).with_password(password)

        database = self.config.get("database")
        if database:
            dsn = (dsn or self._default_dsn).with_path(database)

        self._dsn = dsn
