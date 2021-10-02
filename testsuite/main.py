from sre_constants import RANGE_UNI_IGNORE
from testsuite import framework
import asyncio

def run_test(test, throw=False):
    state = ""
    err = None
    try:
        asyncio.run(asyncio.wait_for(test(), timeout=5))
        state = "OK"
    except AssertionError as e:
        state = "FAIL"
        err = e
        if throw: raise e
    except asyncio.TimeoutError as e:
        state = "TLE"
    except Exception as e:
        state = "ERR"
        err = e
        if throw: raise e
    stateCol = ""
    if state == "OK":
        stateCol += "\x1b[92m"
    else:
        stateCol += "\x1b[91m"
    print(f"[{stateCol}{state}\x1b[0m] {test.__name__}", end="")
    if state != "OK":
        print(f" - {stateCol}{err}\x1b[0m")
    else:
        print("")
    return state

def main(args):
    print("pp-juice Test Suite Made To Prevent Gog From Yelling At Me")
    print(f"{len(framework.TEST_LIST)} tests registered")
    if len(args) == 0:
        return run_matching()
    elif args[0] == "help":
        print("usage: test_suite.py <command> [args]")
        print("Commands:")
        print("  run-all - Runs all tests")
        print("  run-one <test> - Runs a specific test")
        print("  debug-all - Runs all tests without catching errors (for using debugger)")
        print("  debug-one <test> - Runs a specific test without catching")
    elif args[0] == "run-one":
        if len(args) < 2:
            print("not enough args")
            return
        return run_matching(name=args[1])
    elif args[0] == "run-all":
        return run_matching()
    elif args[0] == "debug":
        if len(args) < 2:
            print("not enough args")
            return
        return run_matching(name=args[1], throw=True)
    elif args[0] == "debug-all":
        return run_matching(throw=True)

def run_matching(name=None, group=None, throw=False):
    numSuccess = 0
    numFailed = 0
    numErrored = 0
    numTimeout = 0
    for test in framework.TEST_LIST:
        ctest, cgroup = test
        if  (name == None or name == ctest.__name__) and \
            (group == None or group == cgroup):
            result = run_test(ctest, throw)
            if result == "OK":
                numSuccess += 1
            elif result == "ERR":
                numErrored += 1
            elif result == "FAIL":
                numFailed += 1
            elif result == "TLE":
                numTimeout += 1
    if numSuccess + numFailed + numErrored + numTimeout == 0:
        print("no tests matched")
    else:
        print(f"{numSuccess} passed, {numFailed} failed, {numErrored} errored, {numTimeout} timed out")
    if numFailed or numErrored or numTimeout:
        return -1
    else:
        return 0