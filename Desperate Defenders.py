#S10243158G
#LiNG SAY KIAT
#CSF02

#Main idea is that the dictionary of the unit is put into the nested list 

import random
import json
import sys

# Game variables
game_vars = {
    'turn': 0,                      # Current Turn
    'monster_kill_target': 20,      # Number of kills needed to win
    'monsters_killed': 0,           # Number of monsters killed so far
    'num_monsters': 0,              # Number of monsters in the field
    'gold': 10,                     # Gold for purchasing units
    'threat': 0,
    'max_threat': 10,
    'danger_level': 1,
    }

archer = {'shortform' : 'ARCHR',
          'name': 'Archer',
          'health': 5,
          'maxHP': 5,
          'min_damage': 1,
          'max_damage': 4,
          'price': 5
          }
             
wall = {'shortform': 'WALL',
        'name': 'Wall',
        'health': 20,
        'maxHP': 20,
        'min_damage': 0,
        'max_damage': 0,
        'price': 3
        }
    
monster_units = {'ZOMBS': {'name': 'Zombie',
                    'shortform': 'ZOMBI',
                  'health': 15, 'maxHP': 15,
                  'min_damage': 3,
                  'max_damage': 6,
                  'moves' : 1,
                  'reward': 2},
                 'WOLF': {'name': 'Werewolf', 'shortform': 'WWOLF', 
                          'health': 10, 'maxHP': 10,
                          'min_damage': 1, 'max_damage': 4,
                          'moves': 2, 'reward': 3
                          }}

field = [ [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None] ]

row_letter = ['A', 'B', 'C', 'D', 'E']

#----------------------------------------------------------------------
# draw_field()  
#
#    Draws the field of play
#    The column numbers only go to 3 since players can only place units
#      in the first 3 columns
#----------------------------------------------------------------------

def draw_field(row_num):

    for k in range(row_num):

        print(4*' ' + str(k+1) + ' ',end = '')

    print(' ')

    #Print the row_num
    
    for i in range(len(field)):
        
        cols = field[i]
        letter = chr(i+65)

        for k in range(len(cols)):

            if k == 0:
                print(' +-----', end = '')

        #Prints out the starting spacing for the first + line

            else:
                print('+-----', end = '')

        print('+')

         #Prints +----- for the lanes except the last line

        print(letter, end = '')
        
        for x in range(2):
              
            if x == 0:
                
                for y in range(len(cols)):

                    if field[i][y] == None:
                        print('|' + 5*' ', end = '')

                    else:
                        print('|{:^5}'.format(field[i][y]['shortform']), end = '')

            #Prints the unit name

            if x == 1:

                print(' ', end = '')

                for z in range(len(cols)):

                    if field[i][z] == None:
                        print('|' + 5*' ', end = '')
                        
                    else:
                        health_bar = str(field[i][z]['health']) + '/' + str(field[i][z]['maxHP'])
                        
                        print('|{:^5}'.format(health_bar),end= '')
                        
                        #print('|{}/{}'.format(field[i][z]['health'], field[i][z]['maxHP'], end = '')), not sure why this doesn't work....
                    
            #Prints the unit health

            print('|')

        if i == len(field) - 1:

            #Ensures only prints the last line of +-----
            
            for z in range(len(cols)):
                
                if z == 0:
                    print(' +-----',end='')

            #Prints out the starting spacing
                    
                else:
                    print('+-----',end='')

            print('+')

    print('{}{:>3}{:>11} = [{:<10}] {:>16} {}'.format('Turn', game_vars['turn'], 'Threat', game_vars['threat']*'-', 'Danger Level', game_vars['danger_level']))
    print('{} = {:<4} {} = {}/{}'.format('Gold', game_vars['gold'], 'Monsters killed',\
                                      game_vars['monsters_killed'], game_vars['monster_kill_target']))
                
#----------------------------
# show_combat_menu()
#
#    Displays the combat menu
#----------------------------
def show_combat_menu(game_vars):

    print("1. Buy unit     2. End turn")
    print("3. Save game    4. Quit")
    
    options = ['1', '2', '3', '4']

    user = input('Your choice? ')

    if user == options[0]:
        buy_unit(field, game_vars)
        show_combat_menu(game_vars)

    elif user == options[1]:
        continue_game()
        show_combat_menu(game_vars)

    elif user == options[2]:
        save_game()

    elif user == options[3]:
        print('Hope you enjoyed your time!')
        print('See you again next time!')
        print(sys.exit())

    else:
        print('Invalid option, please choose again')
        return show_combat_menu(game_vars)

    #Checking user input for each option then continuing with the necessary function
    #If anything other than the valid options are input, an error message is printed
    
#----------------------------
# show_main_menu()
#
#    Displays the main menu
#----------------------------
def show_main_menu():
    print("1. Start new game")
    print("2. Load saved game")
    print("3. Quit")
    
    options = ['1', '2', '3']

    user = input('Your choice? ')

    while user not in options:
        print('Invalid option, please choose again!')
        user = input('Your choice? ')

    if user == options[0]:
        initialize_game()
        start_game()

    elif user == options[1]:
        load_game(game_vars)
        start_game()

    elif user == options[2]:
        print('Thanks for playing, hope to see you again!')
  
    #Checking user input for each option then continuing with the necessary function
    #If anything other than the valid options are input, an error message is printed
           
#-----------------------------------------------------
# place_unit()
#
#    Places a unit at the given position
#    This function works for both defender and monster
#    Returns False if the position is invalid
#       - Position is not on the field of play
#       - Position is occupied
#       - Defender is placed past the first 3 columns
#    Returns True if placement is successful
#-----------------------------------------------------

def place_unit(field, position, unit_name):
    
    if len(position) != 2:
        return False

    #Check length for position argument
    check = True
    row_list = ['a', 'b', 'c', 'd', 'e']
    col_list = ['1', '2', '3']

    try:
        row = row_list.index(position[0])
        col = position[1]

    except:
        print('Invalid choice, please choose again')
        show_combat_menu(game_vars)
        
    #Gives you row and col position based on the position argument
    #Exception handling for input validation
    
    if row == -1:
            
        check = False

        return check

    #Check for letter input
    #If index not found -1 is returned

    if col not in col_list:
            
        check = True
            
        return check

    #Check for number input

    col = int(col) - 1

    #Minus 1 cuz field col starts from 0 to 1 to 2

    if field[row][col] != None:
        
        check = False
        
        return False
    
    #Check if space is empty
    
    field[row][col] = unit_name
    
    return True

#-------------------------------------------------------------------
# buy_unit()
#
#    Allows player to buy a unit and place it using place_unit()
#-------------------------------------------------------------------
def buy_unit(field, game_vars):
    print('What unit do you wish to buy? ')
    print('1. {} ({} gold)'.format('Archer', archer['price']))
    print('2. {} ({} gold)'.format('Wall', wall['price']))
    print("3. Don't buy")
    
    options = ['1', '2', '3']
    unit = None

    user = input('Your choice? ')

    if user == options[0]:
        
        if game_vars['gold'] >= 5:
            unit = archer.copy()
        
        else:
            print('Insufficient gold, please choose again.')
            return show_combat_menu(game_vars)

    elif user == options[1]:

        if game_vars['gold'] >= 3:
            unit = wall.copy()

        else:
            print('Insufficent gold, please choose again.')
            return show_combat_menu(game_vars)

    elif user == options[2]:

        print('Returning to combat menu')
        return show_combat_menu(game_vars)

    else:
        print('Invalid option, please choose again')
        return show_combat_menu(game_vars)

    #Left side is the current HP
    
    position = input('Place where? ')
    position = position.lower()

    if place_unit(field, position, unit) == False:
        print("Sorry, you can't place your unit there")
        return show_combat_menu(game_vars)

    #Check if position entered is invalid

    game_vars['gold'] -= unit['price']
    continue_game()
    
    return 

#-----------------------------------------------------------
# defender_attack()
#
#    Defender unit attacks.
#
#-----------------------------------------------------------
def defender_attack(defender_name, field, row, col):
    
    if defender_name['name'] == 'Archer':

        for i in range(col + 1, 7):

            position = field[row][i]

            if position == None:
                continue
            
            #Checking for monsters in the field nested list

            if position['name'] in ['Zombie', 'Werewolf']:
                
                damage = random.randint(defender_name['min_damage'], defender_name['max_damage'])
                position['health'] -= damage
                print('Archer in lane {} shoots {} for {} damage!'.format(row_letter[row], position['name'],damage))

                #Archer damage

                if position['health'] <= 0:

                    if position['name'] == 'Zombie':
                        
                        print('Zombie has been killed')
                        print('You gain {} gold as your bounty'.format(position['reward']))
                        
                        game_vars['gold'] += position['reward']
                        field[row][i] = None
                        game_vars['monsters_killed'] += 1
                        game_vars['threat'] += position['reward']

                        #field[row][i] used instead of position as (position = None) would not change anything but redefine the variable

                    elif position['name'] == 'Werewolf':
                        
                        print('Werewolf has been killed')
                        print('You gain {} gold as your bounty'.format(position['reward']))
                        
                        game_vars['gold'] += position['reward']
                        field[row][i] = None
                        game_vars['monsters_killed'] += 1
                        game_vars['threat'] += position['reward']

                        #field[row][i] used instead of position as (position = None) would not change anything but redefine the variable
             
    return

#-----------------------------------------------------------
# monster_advance()
#
#    Monster unit advances.
#       - If it lands on a defender, it deals damage
#       - If it lands on a monster, it does nothing
#       - If it goes out of the field, player loses
#-----------------------------------------------------------
def monster_advance(monster_name, field, row, col):
    # Calculate the new position the monster intends to move to
    new_col = col - monster_name['moves']

    # Check if the new position is off the left side of the field
    if new_col < 0:
        print('Oh no! An undead creature has entered the city!')
        print('Defeat')
        print('See you in the next game!')
        sys.exit()

    # Check each space from the monster's current position to the new position
    for next_col in range(col - 1, new_col - 1, -1):
        # If the column is off the grid, the monster has reached the city
        if next_col < 0:
            print('A monster has reached the city!')
            sys.exit()

        next_position = field[row][next_col]

        # If the space is occupied by a defender, the monster attacks
        if next_position and next_position['name'] in ['Archer', 'Wall']:
            attack_defender(monster_name, next_position, row, next_col)
            return  # Monster's turn ends after an attack

        # If the space is occupied by another monster, the monster can't move
        elif next_position and next_position['name'] in ['Zombie', 'Werewolf']:
            print('{} in lane {} is blocked and can\'t advance.'.format(monster_name['name'], row_letter[row]))
            return  # Monster's turn ends

    # If there were no obstacles, move the monster to the new position
    if field[row][new_col] is None:
        field[row][new_col] = monster_name
        field[row][col] = None
        print('{} in lane {} advances!'.format(monster_name['name'], row_letter[row]))

def attack_defender(monster, defender, row, col):
    damage = random.randint(monster['min_damage'], monster['max_damage'])
    defender['health'] -= damage
    print('{} in lane {} hits {} for {} damage!'.format(monster['name'], row_letter[row], defender['name'], damage))
    if defender['health'] <= 0:
        print('{} in lane {} is destroyed by {}!'.format(defender['name'], row_letter[row], monster['name']))
        field[row][col] = None  # Defender is destroyed

#---------------------------------------------------------------------
# spawn_monster()
#
#    Spawns a monster in a random lane on the right side of the field.
#    Assumes you will never place more than 5 monsters in one turn.
#---------------------------------------------------------------------
def spawn_monster(field, monster_units):

    monster_list = ['ZOMBS', 'WOLF']
    monster_num = random.randint(0, len(monster_list)-1)
    row_num = random.randint(0,4)
    
    monster = monster_units[monster_list[monster_num]].copy()
    
    if field[row_num][-1] == None:
        field[row_num][-1] = monster

    #Putting the dictionary of the monster unit into the field position
        
    return field 

#-----------------------------------------
# save_game()
#
#    Saves the game in the file 'save.txt'
#-----------------------------------------
def save_game():
    
    defenders_game_file = open('save.json', 'w')
    json.dump({'game_vars':game_vars, 'field':field}, defenders_game_file)
    defenders_game_file.close()
    
    print('Game saved.')
    print('Hope to see you again soon!')

    #Using json as it is easier to save dictionaries

#-----------------------------------------
# load_game()
#
#    Loads the game from 'save.txt'
#-----------------------------------------
def load_game(game_vars):

    try:
        defenders_game_file = open('save.json')
        data = json.load(defenders_game_file)
        
        if 'game_vars' not in data:
            print('Error! No saved game file found')

        else:
            
            for i in data['game_vars']:
                
                game_vars[i] = data['game_vars'][i]

            for row in range(len(field)):

                for col in range(len(field[row])):
                    
                    field[row][col] = data['field'][row][col]

            draw_field(3)

        defenders_game_file.close()
        
    except FileNotFoundError:
        print('Error! No saved game file found')
        
    return

    #Using for loop to run through the data in the saved game file
    #The keys in the dictionary in the saved game file is replacing the keys in the dictionary in the current code

#-----------------------------------------------------
# initialize_game()
#
#    Initializes all the game variables for a new game
#-----------------------------------------------------
def initialize_game():
    game_vars['turn'] = 0
    game_vars['monster_kill_target'] = 20
    game_vars['monsters_killed'] = 0
    game_vars['num_monsters'] = 0
    game_vars['gold'] = 10
    game_vars['threat'] = 0
    game_vars['danger_level'] = 1
    

#-----------------------------------------
#               MAIN GAME
#-----------------------------------------

print("Desperate Defenders")
print("-------------------")
print("Defend the city from undead monsters!")
print()

# TO DO: ADD YOUR CODE FOR THE MAIN GAME HERE!
def start_game():
    if game_vars['turn'] == 0:
        continue_game()
    show_combat_menu(game_vars)
        
def continue_game():
    spawn_creeps = False  
        
    for row in range(len(field)):

        for col in range(len(field[row])):

            if game_vars['monsters_killed'] == game_vars['monster_kill_target']:

                draw_field(3)                                
                print('Congratulations, you are a Hero! You have saved the city from destruction!')
                print('You win!')
                print('See you next time!')
                
                print(sys.exit())

            if field[row][col] == None:
                continue

            #Check through the field nested list
    
            if field[row][col]['name'] == 'Archer':
                defender_attack(field[row][col], field, row, col)

                #Archer deals damage
                
            elif field[row][col]['name'] in ['Zombie', 'Werewolf']:
                spawn_creeps = True
                monster_advance(field[row][col], field, row, col)

                #Check if monster is on map
                #Advance monster

    if spawn_creeps == False:
        spawn_monster(field, monster_units)

        #Spawn monster if there is none on the map
        
    if game_vars['turn'] >= 1:
        
        game_vars['gold'] += 1
        game_vars['threat'] += random.randint(1, game_vars['danger_level']) 
       
    if game_vars['threat'] >= 10:
        
        game_vars['threat'] -= 10
        spawn_monster(field, monster_units)

    game_vars['turn'] += 1

    if game_vars['turn'] % 12 == 0:
        
        game_vars['danger_level'] += 1
        
        monster_units['ZOMBS']['min_damage'] += 1
        monster_units['ZOMBS']['max_damage'] += 1     
        monster_units['ZOMBS']['health'] += 1
        monster_units['ZOMBS']['maxHP'] += 1
        monster_units['ZOMBS']['reward'] += 1

        monster_units['WOLF']['min_damage'] += 1
        monster_units['WOLF']['max_damage'] += 1        
        monster_units['WOLF']['health'] += 1
        monster_units['WOLF']['maxHP'] += 1
        monster_units['WOLF']['reward'] += 1
        
    draw_field(3)   

show_main_menu()
