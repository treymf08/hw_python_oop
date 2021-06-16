import datetime as dt


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        date_format = '%d.%m.%Y'
        self.comment = comment

        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, date_format).date()


class Calculator(Record):
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        for record in self.records:
            if record.date == dt.date.today():
                today_stats += record.amount
        return today_stats

    def get_week_stats(self):
        self.week = dt.date.today() - dt.timedelta(days=7)
        week_stats = sum(i.amount for i in self.records
                         if i.date > self.week and i.date <= dt.date.today())
        return week_stats


class CashCalculator(Calculator):
    '''Посчет денег.'''

    def __init__(self, limit):
        super().__init__(limit)
    USD_RATE: float = 60.0
    EURO_RATE: float = 70.0
    RUB_RATE: float = 1

    def get_today_cash_remained(self, currency='rud'):
        dic_currency = {'rub': [1, 'руб'],
                        'eur': [self.EURO_RATE, 'Euro'],
                        'usd': [self.USD_RATE, 'USD']}
        self.currency = currency
        cash = self.limit - self.get_today_stats()

        if self.currency == 'rub':
            cash_currency = round(cash, 2)
        elif self.currency == 'eur':
            cash_currency = round(cash / dic_currency[currency][0], 2)
        elif self.currency == 'usd':
            cash_currency = round(cash / dic_currency[currency][0], 2)

        abs_cash = abs(cash_currency)

        if self.get_today_stats() < self.limit:
            return (f'На сегодня осталось {cash_currency}'
                    + f' {dic_currency[currency][1]}')
        elif self.get_today_stats() == self.limit:
            return('Денег нет, держись')
        elif self.get_today_stats() > self.limit:
            return (f'Денег нет, держись: твой долг - {abs_cash}'
                    + f' {dic_currency[currency][1]}')


class CaloriesCalculator(Calculator):
    def __init__(self, limit):
        super().__init__(limit)

    def get_calories_remained(self):
        kcal = self.limit - self.get_today_stats()
        if self.get_today_stats() >= self.limit:
            return ('Хватит есть!')
        else:
            return('Сегодня можно съесть что-нибудь ещё,'
                   + f' но с общей калорийностью не более {kcal} кКал')
