from sre_constants import RANGE_UNI_IGNORE
from testsuite import framework

async def run_test(test, throw=False):
    state = ""
    err = None
    try:
        await test()
        state = "OK"
    except AssertionError as e:
        state = "FAIL"
        err = e
        if throw: raise e
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

async def main(args):
    print("pp-juice Test Suite Made To Prevent Gog From Yelling At Me")
    if len(args) == 0:
        await run_all()
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
        await run_one(args[1])
    elif args[0] == "run-all":
        await run_all()
    elif args[0] == "debug":
        if len(args) < 2:
            print("not enough args")
            return
        await run_one(args[1], True)
    elif args[0] == "debug-all":
        await run_all(True)

async def run_all(throw=False):
    print(f"{len(framework.TEST_LIST)} tests registered")
    numSuccess = 0
    numFailed = 0
    numErrored = 0
    for test in framework.TEST_LIST:
        result = await run_test(test, throw)
        if result == "OK":
            numSuccess += 1
        elif result == "ERR":
            numErrored += 1
        elif result == "FAIL":
            numFailed += 1
    print(f"{numSuccess} passed, {numFailed} failed, {numErrored} errored")

async def run_one(name, throw=False):
    ctest = None
    for test in framework.TEST_LIST:
        if test.__name__ == name:
            ctest = test
    if ctest == None:
        print(f"couldn't find test {name}")
        return
    run_test(ctest, throw)
