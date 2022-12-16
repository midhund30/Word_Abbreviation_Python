from copy import deepcopy
from pprint import pprint

import typing
import re
import numpy as np

#To get the values of each letter and store it as a dictionary
def getPoints():
    values= open(r'C:\Users\91956\Desktop\python assignment\val.txt') #change to working python directory
    getPoints.points = [line.strip('\n').upper() for line in values]
    points      = {}

    for line in getPoints.points:
      points[line.split()[0]] = int(line.split()[1])
    getPoints.points = points

#To read the input file from user and store it as a list
def FRead():
    f = input("Enter the file name:")
    inputfile = open(r'C:\Users\91956\Desktop\python assignment\\'+f+'.txt') #change to working python directory
    names = inputfile.read()
    names = names.upper()
    names = re.sub(r'[^A-Z\n\s-]', '', names)
    FRead.names = names.replace('-',' ').split('\n')
    inputfile.close()

#To get the score value for each position
def getScorePos(pos):
        if pos == 1:
          return 0
        if pos == 2:
          return 1
        if pos == 3:
          return 2
        if pos > 3:
          return 3
#Add space to the end of the name
def addSpace(words):
    return words + " "

  '''
     1) Each abbreviation consists of the first letter of the name.
     2) Each abbreviation is given a score which indicates how good it is.
        * If a letter is the first letter of a word in the name then it has:
          - Score = 0
        * If a letter is the last letter of a word in the name then it has:
          - Score = 5
        * If last letter of a word in the name and letter is "E" then it has:
          - Score = 20
        * Neither Last or First:
          - Score = Position(Letter) + Uncommon/Common_Value
            - Position(Letter) = 2;    Score = 1
            - Position(Letter) = 3;    Score = 2
            - Position(Letter) = else; Score = 3

     3) Any abbreviation which can be formed from more than one name on the list is excluded.
     4) If no abbreviations are found write nothing
     5) If more than abbreviations are found write them separated with commas
  '''
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

      #To find the second letter of abbreviation and score
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

          #To find the third letter in abbreviation and score
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

              #Create a dictionary containing the abbreviation and score
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

#To create the final dictionary of all names combined with its abbreviation and score
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

#To remove any duplicate abbreviations and find the abbreviation with minimum score
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

#To output the abbreviations into a txt file
def main():
    final_abbreviations = reduceAbbreviations()

    with open(r'C:\Users\91956\Desktop\python assignment\RajanRenukaDevi_output_abbrevs.txt', 'w') as o:
      for word,abb in final_abbreviations.items():
        o.write(word + "\n" + abb + "\n")


main()
