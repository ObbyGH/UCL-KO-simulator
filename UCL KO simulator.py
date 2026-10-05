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
current_round = "R16" # Current round of the tournament. Can be R16, QF, SF, F.
current_bracket = [] # Current bracket of the tournament. This will be updated after each round.

def create_bracket(current_teams_left, current_round):
    """
    Creates a bracket for the current round of the tournament. The bracket is a list of tuples, where each tuple contains two teams that will face each other in the current round.
    """
    pass

def pick_team_for_bracket(current_teams_left):
    """
    Picks a team from the current teams left in the tournament to be placed in the bracket. Remove both teams from the current_teams_left list after they are placed in the bracket,
    the winner of the tie is later added back into the current_teams_left list after the tie.
    """
    pass