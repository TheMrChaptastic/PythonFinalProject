import pickle


class LeagueRepo:
    def __init__(self):
        self.leagues = []

    def add_league(self, league):
        for leg in self.leagues:
            if leg.oid == league.oid or leg.name == league.name:
                return False
        self.leagues.append(league)
        return True

    def edit_league(self, league):
        for i in range(len(self.leagues)):
            if self.leagues[i].oid == league.oid:
                self.leagues[i] = league
                return True
        return False

    def delete_league(self, league):
        for leg in self.leagues:
            if leg.oid == league.oid:
                self.leagues.remove(league)
                return True
        return False

    def add_team(self, league, team):
        for i in range(len(self.leagues)):
            if self.leagues[i].oid == league.oid:
                for j in range(len(self.leagues[i].teams)):
                    if self.leagues[i].teams[j].oid == team.oid or self.leagues[i].teams[j].name == team.name:
                        return False
                self.leagues[i].teams.append(team)
                return True
        return False

    def edit_team(self, league, team):
        for i in range(len(self.leagues)):
            if self.leagues[i].oid == league.oid:
                for j in range(len(self.leagues[i].teams)):
                    if self.leagues[i].teams[j].oid == team.oid:
                        self.leagues[i].teams[j] = team
                        return True
        return False

    def delete_team(self, league, team):
        for i in range(len(self.leagues)):
            if self.leagues[i].oid == league.oid:
                for j in range(len(self.leagues[i].teams)):
                    if self.leagues[i].teams[j].oid == team.oid:
                        self.leagues[i].teams.remove(team)
                        return True
        return False

    def add_member(self, league, team, member):
        for i in range(len(self.leagues)):
            if self.leagues[i].oid == league.oid:
                for j in range(len(self.leagues[i].teams)):
                    if self.leagues[i].teams[j].oid == team.oid:
                        for u in range(len(self.leagues[i].teams[j].members)):
                            if self.leagues[i].teams[j].members[u].oid == member.oid or self.leagues[i].teams[j].members[u].name == member.name and self.leagues[i].teams[j].members[u].email == member.email:
                                return False
                        self.leagues[i].teams[j].members.append(member)
                        return True
        return False

    def edit_member(self, league, team, member):
        for i in range(len(self.leagues)):
            if self.leagues[i].oid == league.oid:
                for j in range(len(self.leagues[i].teams)):
                    if self.leagues[i].teams[j].oid == team.oid:
                        for u in range(len(self.leagues[i].teams[j].members)):
                            if self.leagues[i].teams[j].members[u].oid == member.oid:
                                self.leagues[i].teams[j].members[u] = member
                                return True
        return False

    def delete_member(self, league, team, member):
        for i in range(len(self.leagues)):
            if self.leagues[i].oid == league.oid:
                for j in range(len(self.leagues[i].teams)):
                    if self.leagues[i].teams[j].oid == team.oid:
                        for u in range(len(self.leagues[i].teams[j].members)):
                            if self.leagues[i].teams[j].members[u].oid == member.oid:
                                self.leagues[i].teams[j].members.remove(member)
                                return True
        return False

    def get_teams(self, league):
        for lea in self.leagues:
            if lea.oid == league.oid:
                return lea.teams
        return []

    def get_members(self, league, team):
        for lea in self.leagues:
            if lea.oid == league.oid:
                for tem in lea.teams:
                    if tem.oid == team.oid:
                        return tem.members
        return []

    def load_repo(self, path):
        try:
            with open(path, 'rb') as f:
                self.leagues = pickle.load(f)
            return True
        except:
            return False

    def save_repo(self, path):
        try:
            with open(path, 'wb') as f:
                pickle.dump(self.leagues, f)
            return True
        except:
            return False
