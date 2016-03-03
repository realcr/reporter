class ReporterError(Exception): pass
class InvalidInfoError(ReporterError): pass

CURRENCY_KEYWORD = "currency"
INNER_KEYWORD = "inner"
NUM_SPACES = 4

def canonicalize_amount(amount:float) -> str:
    """
    Canonicalize a floating point number to be of the form
    XXXX.XX (Two decimal positions after the dot).
    """
    if amount < 0 :
        raise ReporterError('Amount must be positive! Given amount: {}'.\
                format(amount))

    int_part = int(amount)
    frac_part = amount - int_part
    # Make sure that fractional part is not above 1:
    frac_part = min([1.0,frac_part])
    # Get two digits after point:
    after_point = int((frac_part * 100) + 0.5) 

    return '{}.{:02d}'.format(int_part,after_point)


def multi_amount_to_str(multi_amount):
    """
    Generate a string from amount of money that is made of
    more than one currency.
    """
    res_lst = []
    skeys = sorted(multi_amount.keys())
    for cur in skeys:
        amount = multi_amount[cur]
        res_lst.append('{} {}'.format(\
                canonicalize_amount(amount),\
                cur))

    return ', '.join(res_lst)

def add_multi_amounts(ma1,ma2):
    """
    Add two multi amounts.
    """
    # Union all possible currencies:
    currencies = set(ma1.keys())
    currencies.update(set(ma2.keys()))

    # Initialize resulting multi amount:
    ma = {}

    # Initialize all currencies to be 0:
    for c in currencies:
        ma[c] = 0

    # Add currencies from both multi amounts:
    for c in currencies:
        if c in ma1:
            ma[c] += ma1[c]
        if c in ma2:
            ma[c] += ma2[c]

    return ma

def make_spaces(num):
    """
    Make num spaces
    """
    return (" " * (num * NUM_SPACES))


def calc_tree_mamount(path,head_name,currency,info,cur_depth):
    """
    Return a tuple:
    (res_str, multi_amount)
    """

    if not isinstance(info,dict):
        # This is a terminal leaf which contains amount of money.
        return None,{currency:info}


    shallow_keys = list(info.keys())
    if INNER_KEYWORD in shallow_keys:
        if head_name is None:
            raise InvalidInfoError(\
                    'Error at {}: head_name is not known yet!'.format(path))

        if CURRENCY_KEYWORD in shallow_keys:
            if len(shallow_keys) != 2:
                raise InvalidInfoError(\
                    'Error at {}: Invalid combination of '
                    '{}, {} and other keys'.\
                    format(path,INNER_KEYWORD,CURRENCY_KEYWORD))

            # Update current currency:
            currency = info[CURRENCY_KEYWORD]
        else:
            if len(shallow_keys) != 1:
                raise InvalidInfoError(\
                    'Error at {}: Invalid combination of '
                    '{} and other keys'.\
                    format(path,INNER_KEYWORD))

        return calc_tree_mamount(\
                    path + [INNER_KEYWORD],\
                    head_name,\
                    currency,\
                    info[INNER_KEYWORD],cur_depth\
                    )


    if CURRENCY_KEYWORD in shallow_keys:
        raise InvalidInfoError(\
            'Error at {}: {} shows up without {}.'.format(\
            path,CURRENCY_KEYWORD,INNER_KEYWORD))

    # At this point we don't have CURRENCY_KEYWORD or INNER_KEYWORD

    new_depth = cur_depth
    if head_name is not None:
        new_depth += 1

    res_lst = []
    sum_multi_amount = {}
    skeys = sorted(info.keys())
    for key in skeys:
        val = info[key]
        key_res_str, key_multi_amount = calc_tree_mamount(\
                path + [key],\
                key,\
                currency,\
                info[key],\
                new_depth)

        key_str = "{}{} : {}".format(\
            make_spaces(new_depth),\
            key,\
            multi_amount_to_str(key_multi_amount))

        if key_res_str is not None:
            key_str += '\n' + key_res_str
        res_lst.append(key_str)

        # Add to total sum:
        sum_multi_amount = add_multi_amounts(\
                sum_multi_amount,key_multi_amount)

    # res_str = "{}".format(make_spaces(cur_depth))
    # if head_name is not None:
    #     res_str += "{}: {}".format(head_name,\
    #             multi_amount_to_str(sum_multi_amount))
    res_str = ('\n'.join(res_lst))

    return res_str, sum_multi_amount


def totals_str(info):
    """
    returns a string which is a tree of total amounts.
    """
    res_str, res_multi_amount = calc_tree_mamount([],None,None,info,0)
    return res_str

