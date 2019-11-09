import levy
import datetime


def test_read_parameter_file():
    assert levy.read_parameter_file('levyparameter')[0] == {
        'startdate': '1900-01-01',
        'enddate': '2017-12-31',
        'rate': 0,
        'cap': {'HKD': 0, 'USD': 0}}


def test_get_levy_parameter():
    assert levy.get_levy_parameter('2019-09-01')['startdate'] == '2019-04-01'


def test_quote_levy():
    assert levy.quote_levy(700000, 'HKD', '2019-04-01') == 60


def test_get_payment_count():
    assert levy.get_payment_count('m') == {'abv': 'M', 'en': 'Monthly', 'count': 12}


def test_add_months():
    test_date_string = levy.add_months(datetime.datetime.strptime('2019-09-01', "%Y-%m-%d"), 3).strftime("%Y-%m-%d")
    assert test_date_string == '2019-12-01'
