from copy import deepcopy
from pprint import pprint

import typing
import re
import numpy as np

def getPoints():
    values= open(r'C:\Users\91956\Desktop\python assignment\val.txt')
    getPoints.points = [line.strip('\n').upper() for line in values]
    points      = {}

    for line in getPoints.points:
      points[line.split()[0]] = int(line.split()[1])
    getPoints.points = points

def FRead():
    f = input("Enter the file name:")
    inputfile = open(r'C:\Users\91956\Desktop\python assignment\\'+f+'.txt')
    names = inputfile.read()
    names = names.upper()
    names = re.sub(r'[^A-Z\n\s-]', '', names)
    FRead.names = names.replace('-',' ').split('\n')
    inputfile.close()


def getScorePos(pos):
        if pos == 1:
          return 0
        if pos == 2:
          return 1
        if pos == 3:
          return 2
        if pos > 3:
          return 3

def addSpace(words):
    return words + " "

def findScore(words):

    abb   = []  #List to store the generated abbreviations
    abbs  = {}  #Dictionary to store words and their corresponding abbreviation + score

    ssi   = 1   #next Substring Starting Index
    pos   = 2   #Keep track of the POSitions
    score = 0   #Store SCORE based on position

    if len("".join(words.split())) >= 3:
      abbreviation = words[0]
      words = addSpace(words)
      abbs[words] = {}

      for index1, char1 in enumerate(words[1:]):
        substring1 = words[1:]

        if char1 != " ":
          abbreviation += char1
          if substring1[index1 + 1] == " ":
            if char1 == "E":
              score = score + 20
            else:
              score = score + 5
          else:
            if pos == 1:
              score = score + getScorePos(pos)
            else:
              score = score + getScorePos(pos) + getPoints.points[char1]
          pos += 1
          next_pos = pos

          for index2, char2 in enumerate(words[ssi + 1: ]):
            prev_score = score

            if char2 != " ":
              substring2 = words[ssi + 1:]
              abb_temp   = abbreviation
              abb_temp  += char2
              abb.append(abb_temp)

              if substring2[index2 + 1] == " ":
                if char2 == "E":
                  score = score + 20
                else:
                  score = score + 5
              else:
                if pos == 1:
                  score = score + getScorePos(pos)
                else:
                  score = score + getScorePos(pos) + getPoints.points[char2]
              pos += 1

              if abb_temp not in list(abbs[words].keys()):
                abbs[words][abb_temp] = []
                abbs[words][abb_temp].append(score)
              else:
                abbs[words][abb_temp].append(score)
            else:
              pos = 1
            score = prev_score

          abbreviation = words[0]
          ssi+=1
          pos = next_pos
          score = 0

        else:
          ssi += 1
          pos = 1

    else:
      abbs[words][""] = [0]
    return abbs

def createAbbreviations():
    createAbbreviations.abbreviations = {}
    getPoints()
    FRead()
    for words in FRead.names:
        abbreviations_dict = findScore(words)
        createAbbreviations.abbreviations[words] = abbreviations_dict[addSpace(words)]

        for key in createAbbreviations.abbreviations[words]:
          scores = createAbbreviations.abbreviations[words][key]
          createAbbreviations.abbreviations[words][key] = min(scores)

    return createAbbreviations.abbreviations

def reduceAbbreviations():
    createAbbreviations()
    abb_word_dict = createAbbreviations.abbreviations
    abbs_count, common_abbs = {}, []

    for words in FRead.names:
      for abbres in abb_word_dict[words].keys():
        if abbres not in list(abbs_count.keys()):
          abbs_count[abbres] = 1
        else:
          abbs_count[abbres] += 1

    for words in FRead.names:
      abb_dict      = abb_word_dict[words]
      abb_dict_temp = deepcopy(abb_dict)
      for abbres in abb_dict.keys():
        if abbs_count[abbres] > 1:
          abb_dict_temp.pop(abbres)
      if abb_dict_temp != {}:#Find abbreviations with minimum score after deleting repetitive abbreviations
        min_score_abb = min(abb_dict_temp, key = abb_dict.get)
        min_score     = abb_dict_temp[min_score_abb]
        min_score_abb = [abb for abb, score in abb_dict_temp.items() if score == min_score]
        min_score_abb = ' '.join(min_score_abb)
      else:
        min_score_abb = ""
      abb_word_dict[words] = min_score_abb

    return abb_word_dict

def main():
    final_abbreviations = reduceAbbreviations()

    with open(r'C:\Users\91956\Desktop\python assignment\RajanRenukaDevi_output_abbrevs.txt', 'w') as o:
      for word,abb in final_abbreviations.items():
        o.write(word + "\n" + abb + "\n")


main()
