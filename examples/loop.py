

def not_evaluated():
    """We won't show any values in this function b/c it's not evaluated."""
    silly_list = []

    for i in range(5):
        silly_list.append(i % 2 == 0)

    print(silly_list)

    ddd = {110+1: {220+2: 330+3}}
    ddd[111][222]


def evaluated():
    """We see values in here because it's evaluated."""
    silly_list = []

    for i in range(5):
        silly_list.append(i % 2 == 0)

    print(silly_list)

    ddd = {110+1: {220+2: 330+3}}
    ddd[111][222]

evaluated()
"bye!"
