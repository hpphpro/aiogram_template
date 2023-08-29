from src.common.middlewares.i18n import gettext as _

"""
Prefers to wrap our text in gettext() function
We need to say Babel what text we need and want to translate.
But in only need for .pot file. If we need to transale it, we should wrap in our routers again

Translates are optional.
"""

ERROR_RESPONSE = _('What da heck is going on')
START_COMMAND_MESSAGE = _('It works!')
USER_STOP_SPAM_MESSAGE = _('Are you kidding me?')
USER_STOP_SPAM_CALLBACK_MESSAGE = _('Ah shit here we go again')