#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 16:14:20 2022

@author: maudrodsmoen
"""

import chess.pgn
import numpy as np

def getResults(string):
    if string == '1-0':
        return 1
    if string == '1/2-1/2':
        return 0.5
    else:
        return 0


def extractData(pgn_file_list,prelim=True):
    
    all_results = []
    
    for pgn_file in pgn_file_list:
    
        results = []
        i = 1
        while True:
            offset = pgn_file.tell()
            headers = chess.pgn.read_headers(pgn_file)
            if headers is None:
                break
            
            round_details = []
            round_number = headers.get("Round")
            round_details.append(round_number.split('.')[0])
            round_details.append(round_number.split('.')[1])
            
            time_control = ''
            
            round_ko = int(round_number.split('.')[1])
            
            if round_ko > 32:
                time_control = 'Armageddon'
            elif round_ko > 30:
                time_control = 'Blitz'
            else:
                time_control = 'Rapid'
            
            round_details.append(time_control)
    
            round_details.append(headers.get("White"))
            round_details.append(headers.get("Black"))
            round_details.append(getResults(headers.get("Result")))
            round_details.append(1-getResults(headers.get("Result")))
            round_details.append(headers.get("ECO"))
            round_details.append(headers.get("Opening"))
            round_details.append(headers.get("Date"))
            round_details.append(headers.get("Event"))
            i+=1
            all_results.append(round_details)
        
    return all_results
    


cct2 = open('airthingsmastp20.pgn')
cct2_ko = open('airthingsmastko20.pgn')

cct1 = open('skillingopp20.pgn')
cct1_ko = open('skillingopko20.pgn')

cct3 = open('operaeurp21.pgn')
cct3_ko = open('operaeurko21.pgn')

cct4 = open('mcpi21.pgn')
cct4_ko = open('mciko21.pgn')

cct5 = open('nicclassp21.pgn')
cct5_ko = open('nicclassko21.pgn')

cct6 = open('ftxcryptocup21.pgn')
cct6_ko = open('ftxcryptoko21.pgn')

cct7 = open('goldmoneyrapp21.pgn')
cct7_ko = open('goldmoneyrap21.pgn')

# Magnus did not participate in the 8th!
cct8 = open('chessablemastp21.pgn')
cct8_ko = open('chessablemast21.pgn')

cct9 = open('aimchessusp21.pgn')
cct9_ko = open('aimchessus21.pgn')

cct10 = open('meltwaterfin21.pgn')
        
airthingsdata = extractData([cct10])


cct_list = [1,2,3,4,5,6,7,9,10]


def create_all_data(list_of_ccts):
    for cct in list_of_ccts:
        prelim_string = 'cct'+str(cct)
        ko_string = 'cct'+str(cct)+'_ko'
        print(prelim_string, ",", ko_string)


ccts = [cct1, cct1_ko, cct2, cct2_ko, cct3, cct3_ko, cct4, cct4_ko, cct5, cct5_ko, cct6, cct6_ko, cct7, cct7_ko, cct8, cct8_ko, cct9 ,cct9_ko, cct10, cct10]

master_data = np.array(extractData(ccts))


def get_players(data):

    white_players = data[:,3]
    black_players = data[:,4]
    
    players = np.unique(np.concatenate((white_players,black_players),axis=0))
    
    return players


players = get_players(master_data)

np.save('participants2.npy',players)

def get_score(opponent, data, time):
    count = 0
    magnus_points = 0
    magnus_wins = 0
    magnus_losses = 0
    magnus_draws = 0
    
    for i in range(0,len(data)):
        
        if data[i][2] != time:
            continue
        
        white = data[i][3]
        black = data[i][4]
        
        white_score = float(data[i][5])
        black_score = float(data[i][6])
        
        
        if (white == opponent) and (black == 'Carlsen, Magnus'):
            #print(data[i])
            count += 1
            magnus_points += black_score
            if black_score == 1:
                magnus_wins += 1
            elif black_score == 0.5:
                magnus_draws += 1
            else:
                magnus_losses += 1
            
        elif (black == opponent) and (white == 'Carlsen, Magnus'):
            #print(data[i])
            count += 1
            magnus_points += white_score
            if white_score == 1:
                magnus_wins += 1
            elif white_score == 0.5:
                magnus_draws += 1
            else:
                magnus_losses += 1
            
            
    return magnus_wins, magnus_draws, magnus_losses


def getStats(opponent):
    
    rapid = get_score(opponent, master_data, 'Rapid')
    blitz = get_score(opponent, master_data, 'Blitz')
    arma = get_score(opponent, master_data, 'Armageddon')
    
    print(opponent)
    
    print("Rapid:", rapid[0], rapid[1], rapid[2])
    print("Blitz:", blitz[0], blitz[1], blitz[2])
    print("Armageddon:", arma[0], arma[1], arma[2])
    
    print ("------------")


getStats('Ding, Liren')
getStats('Nepomniachtchi, Ian')
getStats('Aronian, Levon')
getStats('Giri, Anish')
getStats('Mamedyarov, Shakhriyar')
getStats('Le, Quang Liem')
getStats('Duda, Jan-Krzysztof')
getStats('Hansen, Eric')
getStats('Artemiev, Vladislav')
getStats('Giri, Anish')
getStats('So, Wesley')


print("----------------------------------------------")

getStats('Praggnanandhaa, R')
getStats('Van Foreest, Jorden')
getStats('Anton Guijarro, David')
getStats('Jones, Gawain C B')


getStats('Vidit, Santosh Gujrathi')



