Data to text generation dataset. Original data from https://github.com/harvardnlp/boxscore-data
This is a sentence-splitted and data-aligned version.

There are train, validation and test set splits. Those *.src files contain the structured data used to generate the sentence. The format is space-delimited tokens. For each token, it is a data triplet delimited by "|", in form of "value|type|entity". Those corresponding *.tgt files are the target sentence ground truth for each line corresponding to the *.src files.

All possible types are as follows:

TEAM_NAME - Team full name
TEAM-AST - Number of team assists
TEAM-FG3_PCT - Percentage of 3 pointers made by team
TEAM-FG_PCT - Percentage of field goals made by team
TEAM-FT_PCT - Percentage of free throws made by team
TEAM-LOSSES - Team losses
TEAM-PTS - Total team points
TEAM-PTS_QTR1 - Team points in first quarter
TEAM-PTS_QTR2 - Team points in second quarter
TEAM-PTS_QTR3 - Team points in third quarter
TEAM-PTS_QTR4 - Team points in fourth quarter
TEAM-REB - Total team rebounds
TEAM-TOV - Total team turnovers
TEAM-WINS - Team wins
PLAYER-AST - Player assists
PLAYER-BLK - Player blocks
PLAYER-DREB - Player defensive rebounds
PLAYER-FG3A - Player 3-pointers attempted
PLAYER-FG3M - Player 3-pointers made
PLAYER-FG3_PCT - Player 3-pointer percentage
PLAYER-FGA - Player field goals attempted
PLAYER-FGM - Player field goals made
PLAYER-FG_PCT - Player field goal percentage 
PLAYER-FTA - Player free throws attempted
PLAYER-FTM - Player free throws made
PLAYER-FT_PCT - Player free throw percentage
PLAYER-MIN - Player minutes played
PLAYER-OREB - Player offensive rebounds
PLAYER-PF - Player personal fouls
PLAYER_NAME - Player full name
PLAYER-PTS - Player points
PLAYER-REB - Player total rebounds
PLAYER-STL - Player steals
PLAYER-TO - Player turnovers
