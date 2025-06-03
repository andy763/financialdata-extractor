@echo off
echo Running SIX Group shares extractor...

python sixgroup_cli.py --csv ^
  https://www.six-group.com/en/market-data/etp/etp-explorer/etp-detail.CH1146882316USD4.html ^
  https://www.six-group.com/en/market-data/etp/etp-explorer/etp-detail.CH0496454155USD4.html ^
  https://www.six-group.com/en/market-data/etp/etp-explorer/etp-detail.CH0475552201USD4.html ^
  > sixgroup_shares.csv

echo Results saved to sixgroup_shares.csv
pause 