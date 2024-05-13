import random
from collections import deque

# This represents a like between 2 members of the social media app
class Like:
    def __init__(self, sender, receiver):
        self.sender = sender
        self.receiver = receiver

#This shows the comments between 2 members
class Comment:
    def __init__(self, sender, receiver, content):
        self.sender = sender
        self.receiver = receiver
        self.content = content

#Class that shows the member
class Member:
    def __init__(self, name):
        self.name = name
        self.fol = set()        #Stores followers
        self.likes_giv = []        #Stores the likes that were given
        self.com_given = []         # the comments

# the method that lets a member follow another
    def follow(self, other_memb):
        self.fol.add(other_memb)

#meythod for liking
    def like(self, other_memb):
        like = Like(self, other_memb)
        self.likes_giv.append(like)

#method for leaving a commnent
    def comment(self, other_memb, content):
        comment = Comment(self, other_memb, content)
        self.com_given.append(comment)

#method that calculates the total engagment rate of a member
    def tot_engag_rate(self):
        tot_likes = len(self.likes_giv)
        tot_com = len(self.com_given)
        return (tot_likes + tot_com) / len(self.fol) * 100 if self.fol else 0

#method to calculate the influence of a member to another member
    def influence(self, other_memb):
        like_other = sum(1 for like in self.likes_giv if like.receiver == other_memb)
        com_other = sum(1 for comment in self.com_given if comment.receiver == other_memb)
        tot_engag_rate = other_memb.tot_engag_rate()
        return (like_other + com_other) / tot_engag_rate if tot_engag_rate else 0

#class that represent the social network like the name suggests
class SocialNetwork:
    def __init__(self):
        self.membs = {}             #stores members

#method to add members
    def add_member(self, name):
        if name not in self.membs:
            self.membs[name] = Member(name)

#method that allows the random relationships between members
    def random_rel(self, probability=0.5):
        memb_names = list(self.membs.keys())
        for memb_name in self.membs:
            member = self.membs[memb_name]
            for other_memb_name in memb_names:
                if other_memb_name != memb_name:
                    if random.random() < probability:
                        self.follow(memb_name, other_memb_name)

#method that allows members to follow another
    def follow(self, foll_name, followed_name):
        if foll_name in self.membs and followed_name in self.membs:
            self.membs[foll_name].follow(self.membs[followed_name])
        else:
            print("Member not found.")

#method that makes the likes and comments in order to simulate the engagment for the members
    def sim_engags(self):
        for memb_name in self.membs:
            member = self.membs[memb_name]
            for _ in range(random.randint(0, 10)):
                foll_name = random.choice(list(self.membs.keys()))
                follower = self.membs[foll_name]
                if follower != member:
                    member.like(follower)
            for _ in range(random.randint(0, 5)):
                commenter_name = random.choice(list(self.membs.keys()))
                commenter = self.membs[commenter_name]
                if commenter != member:
                    comment_content = "Random comment"
                    member.comment(commenter, comment_content)

#method to calculate the engag rate of the member
    def cal_engag_rate(self, memb_name):
        if memb_name in self.membs:
            return self.membs[memb_name].tot_engag_rate()
        else:
            print("Member not found.")
            return 0

#calculates the influence of a meber 
    def cal_inf(self, influencer_name, influenced_name):
        if influencer_name in self.membs and influenced_name in self.membs:
            return self.membs[influencer_name].influence(self.membs[influenced_name])
        else:
            print("Member not found.")
            return 0

#calculates the shortests paths between members
    def shortest_path(self, start_name, end_name):
        if start_name not in self.membs or end_name not in self.membs:
            print("Member not found.")
            return None

        visited = set()
        queue = deque([(start_name, 0)])  # starts queue with start member and distance 0

        while queue:
            memb_name, distance = queue.popleft()
            if memb_name == end_name:
                return distance  # Return the distance when we reach the end member
            visited.add(memb_name)
            member = self.membs[memb_name]
            for follower in member.fol:
                if follower.name not in visited:
                    queue.append((follower.name, distance + 1))

        #If no path is found
        print("No path found.")
        return None

#method that finds the highest engag of 2 members
    def highest_engag(self, start_name, end_name, visited=None):
        if start_name not in self.membs or end_name not in self.membs:
            print("Member not found.")
            return None

        if visited is None:
            visited = set()

        visited.add(start_name)
        member = self.membs[start_name]
        best_path = None
        best_engag = 0

        #Base case: If start member is the end member
        if start_name == end_name:
            return [member.name], member.tot_engag_rate()

        #Other case: Explore followers of start member
        for follower in member.fol:
            if follower.name not in visited:
                path, engagement = self.highest_engag(follower.name, end_name, visited.copy())
                if path is not None and engagement > best_engag:
                    best_path = [member.name] + path
                    best_engag = engagement

        return best_path, best_engag


#Example Usage
if __name__ == "__main__":
    social_network = SocialNetwork()

    #Add membs
    social_network.add_member("Alice")
    social_network.add_member("Bob")
    social_network.add_member("Charlie")
    social_network.add_member("David")

    #Establish random follow relationships
    social_network.random_rel()

    #Simulate engagements
    social_network.sim_engags()

    #Calculate engagement rate for each member
    for memb_name in social_network.membs:
        engag_rate = social_network.cal_engag_rate(memb_name)
        print(f"{memb_name}'s engagement rate: {engag_rate}")

    #Find shortest path between membs
    shortest_path = social_network.shortest_path("Bob", "Charlie")
    print(f"Shortest path between Bob and Charlie: {shortest_path} steps")

    #Find path with highest engagement between membs
    start_member = "Alice"
    end_member = "David"
    path, engagement = social_network.highest_engag(start_member, end_member)
    if path:
        print(f"Path with highest engagement between {start_member} and {end_member}: {path}")
        print(f"Engagement: {engagement}")
    else:
        print(f"No path found between {start_member} and {end_member}.")
