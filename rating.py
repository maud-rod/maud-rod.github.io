#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 18:58:46 2022

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
            #if ("Carlsen" in headers.get("White")) or ("Carlsen" in headers.get("Black")):
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
    


cct1 = open('skillingopp20.pgn')
cct1_ko = open('skillingopko20.pgn')

ccts = [cct1, cct1_ko]

master_data = np.array(extractData(ccts))

def generate_rating_table(players,init_rating,num_ccts):
    
    table = []
    
    for player in players:
        row = []
        row.append(player)
        row.append(init_rating)
        for i in range(1,num_ccts):
            row.append(0)
            
        table.append(row)
        
    return np.array(table)



def get_rating(player, cct_number):
    
    
    
    return 0


def get_players(data):

    white_players = data[:,3]
    black_players = data[:,4]
    
    players = np.unique(np.concatenate((white_players,black_players),axis=0))
    
    return players




playersLoaded = np.load('participants2.npy')
table = generate_rating_table(playersLoaded,2700,10)
print(table)


def calculate_ratings_after_tournament(prev_tournament, current_tournament, data):
    
    players = get_players(data)
    #print("this tournament",current_tournament,players)
    #print("--------",len(players))
    
        
    for player in table[:,0]:
        index = int(np.where(table[:,0] == player)[0][0])
        if player in players:
            update = get_tournament_rating_update(player, data, prev_tournament)
            
            table[index][current_tournament] = str(float(table[index][prev_tournament]) + update)
            
        else:
            table[index][current_tournament] = str(table[index][prev_tournament])
            
        
    
    
    
def get_k_factor(time):
    if time == 'Rapid':
        return 6
    if time == 'Blitz':
        return 5
    if time == 'Armageddon':
        return 3
    else:
        print("ERROR: NO TIME CONTROL FOUND")
        return 0
    


def calculate_change(our_player_rating, opponent_rating, our_score, time, our_color):
    expected_score = 1/(1+10**((our_player_rating-opponent_rating)/400))
    
    k = get_k_factor(time)
    
    if (time == 'Armageddon'):
        
        if our_score == 1:
            return (1 - expected_score)*k
        
        if our_score == 0.5 and our_color == 'Black':
            return (1 - expected_score)*k
        
        else:
            return (0 - expected_score)*k

    return (our_score - expected_score)*k


def get_tournament_rating_update(player, data, prev_tournament):
    
    change = 0
    
    for i in range(0,len(data)):
        
        white = data[i][3]
        black = data[i][4]
        white_score = float(data[i][5])
        black_score = float(data[i][6])
        print(white,black,"problem")
        index_white = int(np.where(table[:,0] == white)[0][0])
        index_black = int(np.where(table[:,0] == black)[0][0])
        white_rating = float(table[index_white][prev_tournament])
        black_rating = float(table[index_black][prev_tournament])
        
        if white_rating == '0':
            white_rating = '2700'
        if black_rating == '0':
            black_rating = '2700'
            
        
        if (white == player):
            #print(data[i])
            change += calculate_change(white_rating, black_rating, float(data[i][5]),data[i][2],'White')
            #print(change)
            
            
        if black == player:
            #print(data[i])
            change += calculate_change(black_rating, white_rating, float(data[i][6]),data[i][2],'Black')
            #print(change)
            
       
    return change



    


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

cct8 = open('chessablemastp21.pgn')
cct8_ko = open('chessablemast21.pgn')

cct9 = open('aimchessusp21.pgn')
cct9_ko = open('aimchessus21.pgn')

cct10 = open('meltwaterfin21.pgn')

ccts = [cct1, cct1_ko, cct2, cct2_ko, cct3, cct3_ko, cct4, cct4_ko, cct5, cct5_ko, cct6, cct6_ko, cct7, cct7_ko, cct8, cct8_ko, cct9 ,cct9_ko,cct10]




def calculate_all_updates():
    
    for i in range(0,17,2):
        print(ccts[i],ccts[i+1])

        data = np.array(extractData([ccts[i],ccts[i+1]]))
        
        num = int(i/2)
    
        calculate_ratings_after_tournament(num+1,num+2,data)
        
        
        
        
calculate_all_updates()


        
        
