# -*- coding: utf-8 -*-
"""
Created on Sat Apr  5 22:33:39 2014

@author: xueweuchen
"""

import requests
import urllib
import re

import logging
logging.basicConfig(level=logging.DEBUG)

session = requests.session()
def get_team():
    resp = session.get('http://nba.sports.sina.com.cn/teams.php?dpc=1')
    team_list = re.findall(r'http://nba.sports.sina.com.cn/team/[\w\s]+.shtml', 
                           urllib.parse.unquote(resp.content.decode('gbk')))
    team_list = list(set(team_list))
    for i in range(len(team_list)):
        addr_list = team_list[i].split('/')
        team_list[i] = addr_list[4][0:len(addr_list[4])-6]
    return team_list    

def get_players_of_team(team):
    player_list = list()
    resp = session.get('http://nba.sports.sina.com.cn/team/' + urllib.parse.quote(team) + '.shtml')
    player_list = re.findall(r'<td align="left" style="padding-left:5px;">\s+<a href="http://nba.sports.sina.com.cn/star/[\w\s-]+.shtml',
                            urllib.parse.unquote(resp.content.decode('gbk')))
    player_list = list(set(player_list))
    pl_name_list = [re.search(r'/[\w\s-]+.shtml', pl_name).group(0) for pl_name in player_list]
    player_name_list = [pl_name[1:len(pl_name)-6] for pl_name in pl_name_list]
    return player_name_list
    
def get_teams_of_player(player):
    resp = session.get('http://nba.sports.sina.com.cn/star/' + urllib.parse.quote(player) + '.shtml')
    team_list = re.findall(r'<a href="http://nba.sports.sina.com.cn/team/[\w\s-]+.shtml" target="_blank">', 
               urllib.parse.unquote(resp.content.decode('gbk')))
    team_list = list(set(team_list))
    tm_list = [re.search(r'/[\w\s-]+.shtml', tm_name).group(0) for tm_name in team_list]
    team_name_list = [team_name[1:len(team_name)-6] for team_name in tm_list]
    return team_name_list
    
#if __name__ == "__main__":
#    team_list = get_team()
#    with open('struct.txt', 'w', encoding = 'utf8') as fout:
#        for t in team_list:
#            print(t, file = fout)
#            for w in get_players_of_team(t):
#                print('\t' + w, file = fout)
#                for t in get_teams_of_player(w):
#                    print('\t\t' + t, file = fout)

if __name__ == "__main__":
    team_list = get_team()
    player_list = dict()
    for t in team_list:
        for w in get_players_of_team(t):
            player_list[w] = list()
            for wt in get_teams_of_player(w):
                player_list[w].append(wt)
    print(team_list)
    print(player_list)
    
    node = dict()
    with open('node.csv', 'a', encoding = 'utf8') as fout:
        for i in range(0, len(team_list)):
            print(team_list[i] + ',' + str(i+1), file = fout)
            node[team_list[i]] = i+1
            
    with open('node.csv', 'a', encoding = 'utf8') as foutNode:
        i = len(team_list)
        for p in player_list.keys():
            print(p + ',' + str(i+1), file = foutNode)
            node[p] = i+1
            i = i+1

    with open('edge.csv', 'a', encoding = 'utf8') as foutEdge:
        for p in player_list.keys():
            for t in player_list[p]:
                if node.get(p) != None and node.get(t) != None:
                    print(str(node[p]) + ',' + str(node[t]), file = foutEdge)
                
            