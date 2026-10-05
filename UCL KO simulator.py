import random
import math

class Team:
    def __init__(self, name, rating):
        self.name = name # Name of the team/club.
        self.rating = rating # Rating of the team/club. Factors into the probability of winning a match. Higher rating = higher chance of winning.

teams = [
    Team("Bayern Munich", 100),
    Team("Arsenal", 100),
    Team("Barcelona", 100),
    Team("Paris Saint-Germain", 100),
    Team("Real Madrid", 94),
    Team("Inter Milan", 94),
    Team("Liverpool", 94),
    Team("Manchester City", 92),
    Team("Borussia Dortmund", 86),
    Team("Leverkusen", 82),
    Team("Atletico Madrid", 80),
    Team("Aston Villa", 78),
    Team("Roma", 68),
    Team("Tottenham", 64),
    Team("Porto", 62),
    Team("Fiorentina", 60)]
# Currently the top 16 teams according to UEFA coefficients. Ratings are made up.

current_teams_left = teams[:] # Current teams left in the tournament. This will be updated after each round.
current_bracket = None # Current bracket of the tournament. This will be updated after each round.
winner = None # Winner of the tournament. This will be updated after the final match.
finalists = None # Finalists of the tournament. This will be updated after the semi-final matches.

def update_bracket(current_teams_left):
    """
    Creates/updates a bracket for the current round of the tournament. The bracket is a list of tuples, where each tuple contains two teams that will face each other in the current round.
    
    Args:
        current_teams_left (list): A list of Team objects representing the teams left in the tournament.
    
    Returns:
        bracket: A list of tuples, where each tuple contains two Team objects that will face each other in the current round.
    """
    bracket = []
    while len(current_teams_left) > 0:
        team1, team2 = pick_team_for_bracket(current_teams_left)
        bracket.append((team1, team2))
    return bracket

def pick_team_for_bracket(current_teams_left):
    """
    Picks a team from the current teams left in the tournament to be placed in the bracket. Remove both teams from the current_teams_left list after they are placed in the bracket,
    the winner of the tie is later added back into the current_teams_left list after the tie. 

    Args:
        current_teams_left (list): A list of Team objects representing the teams left in the tournament.

    Returns:
        tuple: A tuple containing two Team objects that will face each other in the current round.
    """
    choice1 = random.choice(current_teams_left)
    current_teams_left.remove(choice1)
    choice2 = random.choice(current_teams_left)
    current_teams_left.remove(choice2)
    return choice1, choice2

def display_bracket(current_bracket):
    """
    Displays the current bracket of the tournament in a readable format.

    Args:
        current_bracket (list): A list of tuples, where each tuple contains two Team objects that will face each other in the current round.
    """
    print("Current Bracket:")
    for match in current_bracket:
        print(f"{match[0].name} vs {match[1].name}")

def simulate_match(home_team, away_team, is_final=False):
    """
    Simulates a match and returns the final score.

    A team's expected goals are based on their rating compared
    to their opponent's rating. Home teams also receive a small
    advantage.
    """

    home_rating = home_team.rating + 20
    if is_final:
        home_rating -= 20 # There is no home team advantage in the final.
    away_rating = away_team.rating

    # Calculate expected goals.
    home_xg = 1.35 + ((home_rating - away_rating) * 0.025)
    away_xg = 1.35 + ((away_rating - home_rating) * 0.025)

    # Prevent expected goals becoming unrealistically low.
    home_xg = max(0.25, home_xg)
    away_xg = max(0.25, away_xg)

    # Generate the final score instantly.
    home_team_number_of_goals = poisson(home_xg)
    away_team_number_of_goals = poisson(away_xg)

    return home_team_number_of_goals, away_team_number_of_goals


def poisson(expected_goals):
    """
    Generates a random number of goals based on the team's
    expected goals.

    Higher expected goals means a higher chance of scoring
    more goals. There is technically no maximum number of goals.
    """

    probability_limit = math.exp(-expected_goals)

    goals = 0
    probability = 1

    while probability > probability_limit:
        goals += 1
        probability *= random.random()

    return goals - 1

# Main program loop
while finalists is None:
    current_bracket = update_bracket(current_teams_left) # Create the initial bracket for the tournament.
    display_bracket(current_bracket)
    print("Press enter to simulate the first leg of the current round...")
    input() # Wait for user input before continuing.

    list_of_scores = [] # List to store the scores of the current tie.
    for match in current_bracket:
        list_of_scores.append((0, 0)) # Initialize the scores for the current tie.
    # Simulate first leg of the current round.
    for i, match in enumerate(current_bracket):
        home_team, away_team = match
        home_goals, away_goals = simulate_match(home_team, away_team)
        print(f"{home_team.name} {home_goals} - {away_goals} {away_team.name}")
        list_of_scores[i] = (home_goals, away_goals)
    print("Press enter to simulate the second leg of the current round...")
    input() # Wait for user input before continuing.

    # Simulate second leg of the current round.
    for i, match in enumerate(current_bracket):
        home_team, away_team = match
        away_goals, home_goals = simulate_match(away_team, home_team)
        print(f"{away_team.name} {away_goals} - {home_goals} {home_team.name}")
        list_of_scores[i] = (list_of_scores[i][0] + home_goals, list_of_scores[i][1] + away_goals)
    print("Press enter to see the results of the current round...")
    input() # Wait for user input before continuing.

    # Determine the winners of the current round and update the list of teams left in the tournament.
    results = ""
    for i, match in enumerate(current_bracket):
        home_team, away_team = match
        home_goals, away_goals = list_of_scores[i]
        if home_goals > away_goals:
            results += f"- {home_team.name} {home_goals} - {away_goals} {away_team.name}\n"
            current_teams_left.append(home_team)
        elif away_goals > home_goals:
            results += f"- {home_team.name} {home_goals} - {away_goals} {away_team.name}\n"
            current_teams_left.append(away_team)
        else:
            # Simulate penalties.
            home_penalties = 0
            away_penalties = 0

            # Each team takes up to 5 penalties.
            for penalty in range(5):
                if random.random() < 0.75:
                    home_penalties += 1

                if random.random() < 0.75:
                    away_penalties += 1

                # Check if the shootout has already been decided.
                home_remaining = 4 - penalty
                away_remaining = 4 - penalty

                if home_penalties > away_penalties + away_remaining:
                    break

                if away_penalties > home_penalties + home_remaining:
                    break

            # Sudden death if the teams are still level.
            while home_penalties == away_penalties:
                home_scored = random.random() < 0.75
                away_scored = random.random() < 0.75

                if home_scored:
                    home_penalties += 1

                if away_scored:
                    away_penalties += 1

                # One team scores and the other misses.
                if home_scored != away_scored:
                    break

            if home_penalties > away_penalties:
                results += f"- {home_team.name} {home_goals} - {away_goals} {away_team.name} ({home_penalties}-{away_penalties} on penalties)\n"
                current_teams_left.append(home_team)
            else:
                results += f"- {home_team.name} {home_goals} - {away_goals} {away_team.name} ({home_penalties}-{away_penalties} on penalties)\n"
                current_teams_left.append(away_team)
    print("Results of the current round:")
    print(results)
    print("Press enter to continue to the next round...")
    input() # Wait for user input before continuing.
    
    if len(current_teams_left) == 2:
        finalists = current_teams_left[:] # Update the finalists of the tournament after the semi-final matches.
print(f"Finalists of the tournament: {finalists[0].name} and {finalists[1].name}")
home_team, away_team = finalists
print("Press enter to simulate the final...")
home_goals, away_goals = simulate_match(home_team, away_team, is_final=True)
final_result = ""
if home_goals > away_goals:
    winner = home_team
    results = f"- {home_team.name} {home_goals} - {away_goals} {away_team.name}\n"
elif away_goals > home_goals:
    winner = away_team
    results = f"- {home_team.name} {home_goals} - {away_goals} {away_team.name}\n"
else:
    # Simulate penalties.
    home_penalties = 0
    away_penalties = 0

    # Each team takes up to 5 penalties.
    for penalty in range(5):
        if random.random() < 0.75:
            home_penalties += 1

        if random.random() < 0.75:
            away_penalties += 1

        # Check if the shootout has already been decided.
        home_remaining = 4 - penalty
        away_remaining = 4 - penalty

        if home_penalties > away_penalties + away_remaining:
            break

        if away_penalties > home_penalties + home_remaining:
            break

    # Sudden death if the teams are still level.
    while home_penalties == away_penalties:
        home_scored = random.random() < 0.75
        away_scored = random.random() < 0.75

        if home_scored:
            home_penalties += 1

        if away_scored:
            away_penalties += 1

        # One team scores and the other misses.
        if home_scored != away_scored:
            break

    if home_penalties > away_penalties:
        winner = home_team
        results = f"- {home_team.name} {home_goals} - {away_goals} {away_team.name} ({home_penalties}-{away_penalties} on penalties)\n"
    else:
        winner = away_team
        results = f"- {home_team.name} {home_goals} - {away_goals} {away_team.name} ({home_penalties}-{away_penalties} on penalties)\n"
print("Results of the final:")
print(results)
print(f"The winner of the tournament is {winner.name}!")
print("Press enter to exit the program...")
input() # Wait for user input before exiting the program.