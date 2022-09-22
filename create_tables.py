renamed_keys = {'id': 'global_event_id', 'eventid': 'local_event_id'}

modified_keys = {'cardType', 'outcomeType', 'period', 'time', 'type'}

parsed_keys = {'globalGameId', 'x', 'y', 'isShot', 'isTouch', 'isGoal', 'isOwnGoal' 'globalGameId', 'teamId',
               'playerId', 'relatedEventId', 'relatedPlayerId', 'field', 'endX',
               'endY', 'blockedX', 'blockedY', 'goalMouthY', 'goalMouthZ'}

value_quals = {30: 'involvedPlayers', 56: 'zoneGeneral', 130: 'teamFormation',
               131: 'teamPlayerFormation', 145: 'formationSlot', 194: 'captainPlayerId'}

bool_quals = {1: 'long_ball', 2: 'cross', 3: 'head_pass', 4: 'through_ball', 7: 'player_caught_offside',
              8: 'goal_disallowed', 13: 'foul', 14: 'last_man', 15: 'head', 29: 'assisted', 31: 'yellow_card',
              32: 'second_yellow_card', 33: 'red_card', 74: 'miss_high', 82: 'blocked', 88: 'high_claim',
              94: 'outfielder_block', 100: 'blocked_close', 101: 'saved_offLine', 154: 'intentional_assist',
              155: 'chipped', 156: 'lay_off', 169: 'leading_to_attempt', 170: 'leading_to_goal', 173: 'parried_safe',
              174: 'parried_danger', 177: 'collected', 178: 'standing_save', 179: 'diving_save', 185: 'blocked_cross',
              186: 'keeper_missed', 187: 'keeper_saved', 188: 'keeper_went_wide', 190: 'from_shot_off_target',
              210: 'shot_assist', 211: 'overrun', 214: 'big_chance', 241: 'indirect_freekick_taken', 242: 'obstruction',
              264: 'aerial_foul', 285: 'defensive', 286: 'offensive', 11111: 'intentional_goal_assist',
              11112: 'big_chance_created', 11113: 'key_pass', 11114: 'void_yellow_card',
              11115: 'keeper_save_in_the_box', 11116: 'keeper_save_in_six_yard', 11117: 'keeper_save_o_box'}

lists = [({15, 20, 21, 72, 182, 183}, 'body_part'),
         ({9, 22, 23, 24, 25, 26, 160}, 'shot_situation'),
         ({73, 74, 75, 76, 77, 78, 79, 80, 81}, 'direction'),
         ({16, 17, 18, 19, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71}, 'zone'),
         ({5, 6, 107, 123, 124}, 'pass_situation')]

ignored_keys = {'expandedMinute', 'second', 'qualifiers', 'minute', 'satisfiedeventstypes', '$idx', '$len',
                'minuteinfo', 'satisfiers', 'text'}
ignored_quals = {28, 55, 102, 103, 140, 141, 146, 147, 212, 213, 233}
