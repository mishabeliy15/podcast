from django import template
register = template.Library()


@register.filter(name='dur_to_str')
def duration_to_str(value):
    s = int(value)
    time = [s % 60]
    m = s // 60
    if m >= 60:
        time.append(m % 60)
        time.append(m // 60)
    else:
        time.append(m)
    time.reverse()
    for i in range(len(time) - 1, int(len(time) > 2) - 1, -1):
        if time[i] < 10:
            time[i] = time[i] = "0" + str(time[i])
    time = list(map(str, time))
    if len(time) > 1:
        res = ':'.join(time)
    else:
        res = '00:' + ':'.join(time)
    return res
