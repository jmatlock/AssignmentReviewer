# Prototype: Run target program with inputs, view outputs, visual compare, attempt auto check
import runpy
import sys
import pyautogui
import time
import threading
import os


def simulate_input(file_input, stop):
    print(f'----Input {file_input} Begin----')
    time.sleep(1)
    if stop():
        print('ABORT')
        return
    with open(file_input, 'r') as f:
        for line in f:
            if stop():
                print('ABORT')
                return
            if line == 'END\n':
                break
            print(line.strip())
            pyautogui.typewrite(line.strip() + '\n')
    print(f'----Input {file_input} End----')


target_input_map = [('target1.py', 'input1.txt'),
                    ('target2.py', 'input2.txt'),
                    ('target3.py', 'input3.txt'),
                    ('target4.py', 'input4.txt')]


def get_student_list():
    results = os.listdir('grade_targets')
    results.remove('info.txt')
    return results


def main():
    student_list = get_student_list()
    print(f'{len(student_list)} students found. Running tests')
    sys.stdout = open('results.txt', 'w')
    simulated_input = None
    for student in student_list:
        print(f'======== {student} ========  START\n')
        for target_file, input_file in target_input_map:
            stop = False
            print(f'**** Target Start: {target_file}')
            try:
                simulated_input = threading.Thread(target=simulate_input, args=(input_file, lambda : stop, ))
                simulated_input.start()
                runpy.run_path(f"grade_targets/{student}/{target_file}")
            except Exception as e:
                stop = True
                simulated_input.join()
                print(f'Program failed:\n\t{e}')
            finally:
                simulated_input.join()
                print(f'**** Target End: {target_file}\n')
                pass
        print(f'======== {student} ========  END\n')


if __name__ == '__main__':
    main()
