rm -rf ../../../output/cards/cmbcards/*
sh combineCards.sh
sh createWorskspace.sh
rm ../fit/*
sh runMLfit.sh
rm ../outputs/*
sh runPostfit.sh
rm ../plots/*
python drawPostfit.py

