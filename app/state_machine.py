# app/state_machine.py
class BaseState:
    def __init__(self, ctx: "AppContext"):
        self.ctx = ctx

    def handle_events(self, events):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def render(self):
        raise NotImplementedError

class StateMachine:
    """Keeps the current state and delegates."""
    def __init__(self, initial: BaseState):
        self.current = initial

    def switch(self, new_state: BaseState):
        self.current = new_state

    def handle_events(self, events):
        self.current.handle_events(events)

    def update(self):
        self.current.update()

    def render(self):
        self.current.render()