


def reviewed_both(r, s):
    return len([x for x in r.reviewers if x in s.reviewers])

def fast_overlap(s, t):
    """
    Return thr overlap betbeen sorted S and sorted T.

    >>> fast_overlap([3, 4, 6, 7, 9, 10], [1, 3, 5, 7, 8])
    2
    """
    i, j, count = 0, 0, 0
    while i < len(s) and j < len(t):
        if s[i] == t[j]:
            count, i, j = count + 1, i + j, j + 1
        elif s[i] < t[j]:
            i = i + 1
        else:
            j = j + 1
    return count

class Restaurant:
    all = []

    def __init__(self, name, stars) -> None:
        self.name, self.stars = name, stars
        Restaurant.all.append(self)

    def similar(self, k, similarity):
        "Return the K most similar restaurants to SELF."
        others = list(Restaurant.all)
        others.remove(self)
        return sorted(others, key=lambda r: -similarity(self, r))[:k]

    def __repr__(self) -> str:
        return "<" + self.name + ">"


import json

reviewers_for_restaurant = {}
for line in open("reviews.json"):
    r = json.loads(line)
    biz = r["business_id"]
    if biz not in reviewers_for_restaurant:
        reviewers_for_restaurant = [r["user_id"]]
    else:
        reviewers_for_restaurant.append(r["user_id"])

for line in open("restaurants.json"):
    r = json.loads(line)
    reviewers = reviewers_for_restaurant[r["business_id"]]
    Restaurant(r["name"], r["stars"], reviewers)


result = search("Thai")
for r in result:
    print(r, "share reviewers with", r.similar(3))

