import os
import shutil
import time
class TestRunner:
    def __init__(self):
        self.runner = None

    def runTests(self):
        upper_bound = 50
        test_fail = False
        total_time = 0
        test_failures = []
        for i in range(1, upper_bound + 1, 1):
            file_no_str = str(i)
            expected_file = 'largeTests/input_' + file_no_str + '.txt'
            print("\n " + str(i) + ": Running Test : ", expected_file)

            shutil.copyfile(expected_file,'input.txt')
            time.sleep(0.3)
            start_time = time.time()
            os.system('python homework.py')
            end_time = time.time()
            total_time += end_time - start_time
            time.sleep(2)
            ifp = open('output.txt', 'r')
            test_run_output = ifp.readlines()
            ifp.close()

            ifp2 = open('largeTests/output_' + file_no_str + '.txt', 'r')
            expected_run_output = ifp2.readlines()
            ifp2.close()

            print(test_run_output)
            print(expected_run_output)
            fail_cnt = 0
            if len(test_run_output) != len(expected_run_output):
                print('Test failed for : largeTests/input_' + file_no_str + '.txt')
                test_fail = True
                test_failures.append(file_no_str)
                # break
            ind = 0
            while ind < len(test_run_output):
                if test_run_output[ind] != expected_run_output[ind]:
                    print('Test failed for : largeTests/input_' + file_no_str + '.txt')
                    print('Test Output : ', test_run_output)
                    print('Expected Output : ', test_run_output)
                    test_fail = True
                    fail_cnt += 1
                    break
                ind += 1
            print("Test completed in : ", end_time - start_time)
        if test_fail == False:
            print("All Tests Passed!")
        else:
            print(test_failures, " tests failed!")
        print("Total Run time !", total_time)
t = TestRunner()
t.runTests()