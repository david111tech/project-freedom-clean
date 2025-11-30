from .xxl_controller import XXLController
from .xxl_logic import XXLLogic
from .xxl_signals import XXLSignals
from .xxl_state import XXLState

def init_xxl():
    return XXLController(
        logic=XXLLogic(),
        signals=XXLSignals(),
        state=XXLState()
    )
