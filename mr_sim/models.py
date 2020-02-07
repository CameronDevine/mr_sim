from .base import Base

__all__ = ["Preston"]


class Preston(Base):
    def __init__(self, *args, kp=1, **kwargs):
        super().__init__(*args, **kwargs)
        self.kp = kp

    def mrr(self):
        return (
            self.kp
            * self.pressure(*self.local_grid())
            * self.velocity(*self.local_grid())
        )
