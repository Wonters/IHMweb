#!/bin/bash

file_path=$(dirname "$(realpath $0)")

cd $file_path/..

pip install .

rm coverage/.coverage -f
rm -rf coverage/coverage_html_report/ -f


coverage run -a --rcfile=coverage/coveragerc acbbs-scheduler.py -d test -m "TEST" --simulate --channel 1 --noclimchamb
coverage run -a --rcfile=coverage/coveragerc acbbs-scheduler.py -d test -m "TEST" --simulate --channel 1

coverage run -a --rcfile=coverage/coveragerc test_coverage.py --simulate


#HTML report
coverage html --rcfile=coverage/coveragerc