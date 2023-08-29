from typing import Dict, Any

from src.common.middlewares.i18n import gettext as _


def get_test_button() -> Dict[str, Any]:
    '''
    We can transalate our inline button as well, it'll we traslated right it is called
    '''
    return {'text': _('test'), 'callback_data': 'test'} 