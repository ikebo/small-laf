import datetime

def format_advice(user_id, advice):
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    res = user_id + '  ' + time + '\n' + advice + '\n\n'
    return res
