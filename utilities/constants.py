class OptionType:
    call = 'Call'
    put = 'Put'


class TransactionCategories:
    equity = 'Equity'
    cash = 'Cash'


class TransactionEvents:
    open = 'Open'
    close = 'Close'


class CashType:
    cash_usd = 'Cash USD'
    debt_usd = 'USD Debt'

    @staticmethod
    def exists(value) -> bool:
        cash_types = (
            CashType.cash_usd,
            CashType.debt_usd
        )

        if value in cash_types:
            return True
        else:
            return False


class StockType:
    equity = 'Equity'
    index = 'Index'
    exchange_fund = 'ETF'
    mutual_fund = 'Mutual Fund'

    @staticmethod
    def exists(value) -> bool:
        stock_types = (
            StockType.equity,
            StockType.index,
            StockType.exchange_fund,
            StockType.mutual_fund
        )

        if value in stock_types:
            return True
        else:
            return False


class CountryCodes:
    united_states = 'USA'
    united_kingdom = 'GBR'
    australia = 'AUS'
    canada = 'CAN'
    china = 'CHN'
    france = 'FRA'
    germany = 'DEU'
    hong_kong = 'HKG'
    japan = 'JPN'
    south_korea = 'KOR'

    @staticmethod
    def exists(value) -> bool:
        country_codes = (
            CountryCodes.united_states,
            CountryCodes.united_kingdom,
            CountryCodes.australia,
            CountryCodes.canada,
            CountryCodes.china,
            CountryCodes.france,
            CountryCodes.germany,
            CountryCodes.hong_kong,
            CountryCodes.japan,
            CountryCodes.south_korea
        )

        if value in country_codes:
            return True
        else:
            return False


class AdjustmentType:
    change = 'Change'
    split = 'Split'
    specialdividendcash = 'Special Dividend Cash'
    specialdividendstock = 'Special Dividend Stock'

    @staticmethod
    def exists(value) -> bool:
        adjust_types = (
            AdjustmentType.change,
            AdjustmentType.split,
            AdjustmentType.specialdividendcash,
            AdjustmentType.specialdividendstock
        )

        if value in adjust_types:
            return True
        else:
            return False


class StockChangeType:
    symbolchange = 'Symbol Change'
    merger = 'Merger'
    spinoff = 'Spin Off'
    bankruptcy = 'Bankruptcy'
    buyout = 'Buy Out'

    @staticmethod
    def exists(value) -> bool:
        change_types = (
            StockChangeType.symbolchange,
            StockChangeType.merger,
            StockChangeType.spinoff,
            StockChangeType.bankruptcy,
            StockChangeType.buyout
        )

        if value in change_types:
            return True
        else:
            return False


class TransactionMatchType:
    taxadvantage = 'Tax Advantage'
    fifo = 'First in, First out'
    lifo = 'Last in, First out'

    @staticmethod
    def exists(value) -> bool:
        match_types = (
            TransactionMatchType.taxadvantage,
            TransactionMatchType.fifo,
            TransactionMatchType.lifo
        )

        if value in match_types:
            return True
        else:
            return False


class OutputLogType:
    errorlog = 'error-log'
    infolog = 'info-log'
    apilog = 'api-log'
    senderlog = 'sender-log'

    @staticmethod
    def exists(value) -> bool:
        log_types = (
            OutputLogType.errorlog,
            OutputLogType.infolog,
            OutputLogType.apilog,
            OutputLogType.senderlog
        )

        if value in log_types:
            return True
        else:
            return False
