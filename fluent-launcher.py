import os
import subprocess
import argparse
from status_manager import CheckStatus, StatusType


def read_case_list(path='case_list.txt'):
    output = []
    with open(path, 'r') as f:
        for i in f.readlines():
            line = i.strip()
            if line:
                output.append(line)
    return output


def write_journal(path, input_case, output_case, iteration=1500):
    default = """
/file/confirm-overwrite? no
/file/read-case-data #INPUT.cas.h5
/solve/iterate #ITER no yes
/file/write-case-data #OUTPUT.cas.h5
/exit yes"""

    with open(path+'/runner.jou', 'w') as f:
        f.write(default
                .replace('#ITER', str(iteration))
                .replace('#INPUT', input_case)
                .replace('#OUTPUT', output_case))


def run_fluent(path, fluent_path, core: int = 1, gpu=0):
    main_dir = os.getcwd()
    os.chdir(path)
    p = subprocess.call(
        [fluent_path, '3d', f'-t{core}', '-g', '-i', './runner.jou', f"-gpgpu={gpu}"],  shell=True, close_fds=True)
    # p.wait()
    # p.kill()
    # os.system(
    #     " ".join([fluent_path, '3d', f'-t{core}', '-g', '-i', 'runner.jou']))
    os.chdir(main_dir)


def main(input_name: str, output_name: str, max_iter: int, core: int, fluent_path: str, case_file: str, gpu: str):
    case_list = read_case_list(case_file)
    s = CheckStatus()
    current_dir = os.getcwd()
    for path in case_list:
        if s.check(path) != StatusType.finished:
            os.chdir(current_dir)
            s.write_status(path, StatusType.started)
            write_journal(path, input_name, output_name, max_iter)
            run_fluent(path, core=core, fluent_path=fluent_path,
                       gpu=gpu)
            s.write_status(path, StatusType.finished)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='fluent-launcher for run multiple case files')

    parser.add_argument('-t', '--core', type=int, required=True,
                        help='Number of CPU cores')

    parser.add_argument('-m', '--max_iter', type=int, required=True,
                        help='Number of maximum iterations')

    parser.add_argument('-i', '--input', type=str, required=True,
                        help='filename for input case without extensions')

    parser.add_argument('-o', '--output', type=str, required=True,
                        help='filename for output case without extensions')

    parser.add_argument('-c', '--case_list', type=str, required=False,
                        nargs='?', const=1,
                        default='case_list.txt',
                        help='file address of case_list.txt')

    parser.add_argument('--fluent', type=str, required=False,
                        nargs='?', const=1,
                        default='C:/Program Files/ANSYS Inc/v212/fluent/ntbin/win64/fluent.exe',
                        help="custom location of fluent.exe")

    parser.add_argument('--gpgpu', type=int, required=False,
                        nargs='?', const=1,
                        default=0,
                        help="number of gpu")

    args = parser.parse_args()

    main(input_name=args.input, output_name=args.output,
         max_iter=args.max_iter, core=args.core,
         case_file=args.case_list, fluent_path=args.fluent, gpu=args.gpgpu)
