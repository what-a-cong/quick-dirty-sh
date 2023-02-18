#RUN: python %s

if True:
    import os
    import sys
    sys.path.insert(0, os.path.join(
        os.path.dirname(os.path.abspath(__file__)), '..', '..'))

if True:
    import qdsh as sh
    import os


game_file = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'guess_num.pyi')
cmd = 'python {}'.format(game_file)

low = 0
high = 1024
ans = None

while low < high:
    mid = (low + high) // 2
    print("{} {} {}".format(mid, low, high))
    sh(cmd + " {}".format(mid))
    if sh.exit_status == 0:
        ans = mid
        break
    elif sh.exit_status == 1:
        # too high
        high = mid
        pass
    elif sh.exit_status == 2:
        # too low
        low = mid+1
        pass
    else:
        assert False, "WTF?"

    pass


correct_answer = int(sh(cmd + ' 0 cheat'))

assert ans == correct_answer
