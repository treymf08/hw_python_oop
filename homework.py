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
        self.today = dt.date.today()

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        return sum(record.amount for record in self.records
                   if record.date == self.today)

    def get_week_stats(self):
        self.week = self.today - dt.timedelta(days=7)
        return sum(record.amount for record in self.records
                   if self.week < record.date <= self.today)


class CashCalculator(Calculator):
    """Посчет денег."""

    USD_RATE = 60.0
    EURO_RATE = 70.0
    RUB_RATE = 1

    def get_today_cash_remained(self, currency='rud'):
        dic_currency = {'rub': [1, 'руб'],
                        'eur': [self.EURO_RATE, 'Euro'],
                        'usd': [self.USD_RATE, 'USD']}

        if currency not in dic_currency:
            raise ValueError(f'Валюта "{currency}" не известна')

        today_stats = self.get_today_stats()

        cash = self.limit - today_stats

        cash_currency = round(cash / dic_currency[currency][0], 2)

        abs_cash = abs(cash_currency)

        if today_stats < self.limit:
            return (f'На сегодня осталось {cash_currency}'
                    f' {dic_currency[currency][1]}')
        elif today_stats == self.limit:
            return 'Денег нет, держись'
        return (f'Денег нет, держись: твой долг - {abs_cash}'
                f' {dic_currency[currency][1]}')


class CaloriesCalculator(Calculator):
    """Подсчет каллорий."""

    def get_calories_remained(self):
        kcal = self.limit - self.get_today_stats()
        if kcal <= 0:
            return 'Хватит есть!'
        return ('Сегодня можно съесть что-нибудь ещё,'
                f' но с общей калорийностью не более {kcal} кКал')
