from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CustomPasswordValidator:
    def validate(self, password, user=None):
        # Check minimum length
        if len(password) < 5:
            raise ValidationError(_('Password must be at least 5 characters long'), code='assword_too_short')
        # Check for special character
        if not any(char in password for char in '!@#$%^&*().+-/:;<=>?'):
            raise ValidationError(_('Password must contain at least one special character'), code='password_no_special_char')

        # Check for capital letter
        if not any(char.isupper() for char in password):
            raise ValidationError(_('Password must contain at least one capital letter'), code='password_no_capital_letter')

        # Check for alphanumeric
        # if not any(char.isdigit() for char in password) or not any(char.isalpha() for char in password):
        #     raise ValidationError(_('Password must be alphanumeric'), code='password_not_alphanumeric')

    def get_help_text(self):
        return _('Your password must contain at least one special character, one capital letter, and be at least 5 characters long.')
