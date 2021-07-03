import os
import shutil
import time
class TestRunner:
    def __init__(self):
        self.runner = None

    def runTests(self):
        upper_bound = 33
        test_fail = False
        test_failures = []
        for i in range(1, upper_bound + 1, 1):
            file_no_str = str(i)
            if i == 3 or i == 11 or i == 25:
                continue
            expected_file = 'testCases/testcase/input' + file_no_str + '.txt'
            print("\n " + str(i) + ": Running Test : ", expected_file)

            shutil.copyfile(expected_file,'input.txt')
            time.sleep(0.3)
            os.system('python homework.py')
            time.sleep(2)
            ifp = open('output.txt', 'r')
            test_run_output = ifp.readlines()
            ifp.close()

            ifp2 = open('testCases/testcase/output' + file_no_str + '.txt', 'r')
            expected_run_output = ifp2.readlines()
            ifp2.close()

            print(test_run_output)
            print(expected_run_output)
            if len(test_run_output) != len(expected_run_output):
                print('Test failed for : tests/input' + file_no_str + '.txt')
                test_fail = True
                test_failures.append(file_no_str)
            ind = 0
            while ind < len(test_run_output):
                if test_run_output[ind] != expected_run_output[ind]:
                    print('Test failed for : tests/input' + file_no_str + '.txt')
                    print('Test Output : ', test_run_output)
                    print('Expected Output : ', expected_run_output)
                    test_fail = True
                    break
                ind += 1
        if test_fail == False:
            print("All Tests Passed!")
        else:
            print("Tests failed for : ", test_failures)

t = TestRunner()
t.runTests()
