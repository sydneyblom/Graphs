"""
Implement a function that shows all the friends in a user's extended social network and chain of friendships that link them. The number of connections between one user and another are called the degrees of separation.
How will the performance scale as more users join? Implement a feature that creates large numbers of users to the network and assigns them a random distribution of friends.
`populateGraph()` takes in a number of users to create and the average number of friends each user should have and creates them
To create N random friendships, you could create a list with all possible friendship combinations, shuffle the list, then grab the first N elements from the list. You will need to `import random` to get shuffle.
`addFriendship(1, 2)` is the same as `addFriendship(2, 1)`. You should avoid calling one after the other since it will do nothing but print a warning. You can avoid this by only creating friendships where user1 < user2.
`getAllSocialPaths()` takes a userID and returns a dictionary containing every user in that user's extended network along with the shortest friendship path between each.
What kind of graph search guarantees you a shortest path?
Instead of using a `set` to mark users as visited, you could use a `dictionary`. Similar to sets, checking if something is in a dictionary runs in O(1) time. If the visited user is the key, what would the value be?
"""

from util import Queue
import random

class User:
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return self.name

class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments
        Creates that number of users and a randomly distributed friendships
        between those users.
        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}

        # Add users
        for i in range(num_users):
            # call add_user function until the number of users is num_users
            self.add_user(f"User {i + 1}")

        # Create friendships
        # create a list with all possible friendships
        possible_friendships = []
        for user_id in self.users:
            # to avoid duplicates ensure that the first id is smaller than the 2nd id
            for friend_id in range(user_id + 1, self.last_id + 1):
                possible_friendships.append((user_id, friend_id))


        # Shuffle the list
        random.shuffle(possible_friendships)
        print("----")
        print(f"POSSIBLE FRIENDSHIPS: {possible_friendships}")
        print("----")

        # Grab(slice) the first N pairs from the list and create those friendships
        for i in range(num_users * avg_friendships // 2):
            friendship = possible_friendships[i]
            self.add_friendship(friendship[0], friendship[1])

        # avg_friendships = total_friendships / num_users
        # total_friendships = avg_friendships * num_users
        # N = avg_friendships * num_users // 2


    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument
        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.
        The key is the friend's ID and the value is the path.
        """
        visited = {}  # Note that this is a dictionary, not a set

        # create the queue
        q = Queue()
        # BFS(shortest path), so add start id to the queue
        # enqueue the user id in list, build possible path, keep a good one
        q.enqueue([user_id])
        # while the queue is not empty...
        while q.size() > 0:
            # create path
            path = q.dequeue()
            # create new user id
            new_user_id = path[-1]
            # check if the new user id had is visited...
            if new_user_id not in visited:
                # if not, set dict of path from starting to everyone else
                visited[new_user_id] = path
                # then for each neighbor in friendships of new user id...
                for neighbor in self.friendships[new_user_id]:
                    # Make a copy of the path then add
                    path_copy = path.copy()
                    path_copy.append(neighbor)
                    q.enqueue(path_copy)
        return visited


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(1000, 5)
    print(f"USERS: {sg.users}")
    print("----")
    print(f"FRIENDSHIPS: {sg.friendships}")
    print("----")
    connections = sg.get_all_social_paths(1)
    print(F"CONNECTIONS: {connections}")
    print("----")
    print(f"Users in extended social network: {len(connections) - 1}") # (-1 bc can't be friends with self)
    avg_degree_sep = 0
    for user_id in connections:
        avg_degree_sep += len(connections[user_id])
    print(f"Average degree of separation: {avg_degree_sep/len(connections)}")