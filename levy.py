import json
import datetime
import calendar


def read_parameter_file(type):
    if type == 'paymentmode':
        file = 'payment_mode.json'
    elif type == 'levyparameter':
        file = 'levy_parameter.json'
    else:
        raise NameError('Underfined variable type.')
    result = open(file).read()
    return json.loads(result)


def get_levy_parameter(quotationdate):
    levys = read_parameter_file('levyparameter')
    levy = [levy for levy in levys if
            ((levy['startdate'] <= quotationdate) and (levy['enddate'] >= quotationdate))]
    return levy[0]


def quote_levy(modalpremium, currency, quotationdate):
    levy = get_levy_parameter(quotationdate)
    levyrate = levy['rate']
    levymax = levy['cap'][currency]
    levyamount = min(round((modalpremium * levyrate), 2), levymax)
    return levyamount


def get_payment_count(abv):
    paymentmodes = read_parameter_file('paymentmode')
    mode = [mode for mode in paymentmodes if (mode['abv'] == abv.upper())]
    return mode[0]


def levy_schedule(modalpremium, paymentterm, mode, currency, startdate):
    paymentcount = get_payment_count(mode)['count']
    if mode == "S":
        levyamt = quote_levy(modalpremium, currency, startdate)
        payment = {"seq": 0,
                   "pytdate": startdate,
                   "levyamt": levyamt,
                   "acclevy":levyamt,
                   }
        return {
            "paymentschedule": payment
        }
    paymentschedule = []
    prevenddate = '2017-12-31'
    acclevy = 0
    for i in range(0, paymentterm * 12, int(12 / paymentcount)):
        pytdate = add_months(datetime.datetime.strptime(startdate, "%Y-%m-%d"), i)
        levyamt = quote_levy(modalpremium, currency, pytdate.strftime("%Y-%m-%d"))
        levyt = get_levy_parameter(pytdate.strftime("%Y-%m-%d"))
        # If current payment date is greater than last levy year end date, new period start and acc levy set to zero
        if pytdate.strftime("%Y-%m-%d") > prevenddate:
            acclevy = 0
        # If sum of acc levy and the latest premium in a specific year not reach cap, pay the differnce bewteen cap and the acc premium or levy which ever lower
        if acclevy + levyamt < levyt['cap'][currency]:
            levyfinalamt = round(min(levyt['cap'][currency] - acclevy, levyamt), 2)
        else:
            # If sum of acc levy and the latest premium in a specific year reach cap, pay the differnce bewteen the acc premium and cap or 0 which ever higher
            levyfinalamt = round(max(levyt['cap'][currency] - acclevy, 0), 2)
        acclevy += levyfinalamt
        if pytdate.strftime("%Y-%m-%d") < '2021-04-01':
            payment = {"seq": str(int(i * paymentcount / 12)),
                       "pytdate": pytdate.strftime("%Y-%m-%d"),
                       "levyamt": str(levyfinalamt),
                       "acclevy": str(round(acclevy,2))
                       }
            paymentschedule.append((payment))
            prevenddate = levyt['enddate']
        else:
            payment = {"seq": str(int(i * paymentcount / 12)) + ' and onward',
                       "pytdate": pytdate.strftime("%Y-%m-%d") + ' and onward',
                       "levyamt": str(levyfinalamt),
                       "acclevy": 'Annualized premium capped at ' + currency + str(levyt['cap'][currency])
                       }
            paymentschedule.append((payment))
            break
    return paymentschedule


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)
