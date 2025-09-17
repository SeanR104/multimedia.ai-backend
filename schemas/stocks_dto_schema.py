from typing import List
from pydantic import BaseModel, field_validator

from utilities.utils import utils
from utilities.constants import OutputLogType


class StockDto(BaseModel):
    stocks: List[str]
    errors: List[str] = []
    format_warnings: List[str] = []

    @staticmethod
    def _is_valid_ticker(t: str) -> bool:
        if not t:
            return False
        if len(t) > 10:
            return False
        first = t[0]
        if not ('A' <= first <= 'Z'):
            return False
        for ch in t:
            if ('A' <= ch <= 'Z') or ('0' <= ch <= '9') or ch == '-' or ch == '.':
                continue
            return False
        return True

    @field_validator('stocks', mode='before')
    @classmethod
    def collect_errors_and_filter(cls, v):
        # Accept only list; otherwise raise to signal bad body
        if not isinstance(v, list):
            raise TypeError('stocks must be a list')

        valid: List[str] = []
        errors: List[str] = []
        warnings: List[str] = []

        for i, item in enumerate(v):
            if not isinstance(item, str):
                errors.append(f'stocks[{i}] must be a string')
                continue
            s = item.strip()
            if s == '':
                errors.append(f'stocks[{i}] cannot be empty')
                continue
            # Normalize ticker similar to utils.read_ticker_symbol behavior
            try:
                s_norm = s.upper().replace('.', '-').replace('/', '-')
            except Exception:
                errors.append(f'stocks[{i}] normalization failed')
                continue

            # Validate format (allow letters, digits, dashes, dots; start with letter; max 10)
            # Note: We check the original prior to normalization as a warning if changed
            if s != s_norm:
                warnings.append(f'stocks[{i}] normalized from "{s}" to "{s_norm}"')

            # Non-regex validation: start with A-Z, length 1-10, allowed chars A-Z, 0-9, '-', '.'
            if not cls._is_valid_ticker(s_norm):
                warnings.append(f'stocks[{i}] "{s_norm}" is not a valid ticker format')
                # Do not include invalid-format ticker in valid list
                continue

            valid.append(s_norm)

        # Log any errors (as errors) and format warnings (as warnings/info) but still return valid strings
        if errors:
            utils.output_to_logfile(
                log_type=OutputLogType.apilog,
                title='stocks_update_schema validation errors',
                log_message='; '.join(errors)
            )

        if warnings:
            utils.output_to_logfile(
                log_type=OutputLogType.infolog,
                title='stocks_update_schema ticker format warnings',
                log_message='; '.join(warnings)
            )

        # Enforce max of 200 tickers; if more, log warning and truncate
        if len(valid) > 200:
            utils.output_to_logfile(
                log_type=OutputLogType.infolog,
                title='update_from_list cap exceeded',
                log_message=f'sent={len(v)} valid_before_cap={len(valid)} using=200 truncated={len(valid) - 200}'
            )
            valid = valid[:200]

        # Attach lists to the instance post-init via model fields defaulting here is not straightforward in validator.
        # We only return the valid list; the model fields errors/format_warnings will remain defaults.
        return valid

    class Config:
        from_attribute = True
