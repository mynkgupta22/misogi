
posts = [
    {"id" : 1, "user" :"alice","content" : "love python programming", "likes" : 10, "tags" : ["python", "programming"]},
    {"id" : 2, "user" :"bob", "content" : "exploring data science", "likes" : 15, "tags" : ["data", "science"]},
    {"id" : 3, "user" :"alice", "content" : "python is great for data analysis", "likes" : 5, "tags" : ["python", "data analysis"]}

]

users = {
    "alice": {"followers" : 150, "following" : 75},
    "bob": {"followers" : 200, "following" : 100}
}

from collections import Counter, defaultdict
from typing import List, Dict, Any
# Most Popular Tags – Use collections.Counter to find the most frequent tags across posts.
def most_popular_tags(posts: List[Dict[str, Any]]) -> List[tuple]:
    tags = Counter(tag for post in posts for tag in post["tags"])
    print(tags.most_common())


most_popular_tags(posts)


# User Engagement Analysis – Use defaultdict to compute total likes per user.
def user_engagement(posts: List[Dict[str, Any]]) -> Dict[str, int]:
    engagement = defaultdict(int)
    for post in posts:
        engagement[post["user"]] += post["likes"]
        print(dict[engagement])

user_engagement(posts)

# Top Posts by Likes – Use sorted() to list posts in descending order of likes.
def top_posts_by_likes(posts: List[Dict[str, Any]]) -> List[Dict[str,Any]]:
    sorted_posts = sorted(posts, key = lambda x: x["likes"], reverse = True)
    print(sorted_posts)


top_posts_by_likes(posts)


# User Activity Summary – Combine post and user data to generate a summary per user (posts count, likes, followers, etc.).
def user_activity_summary(posts: List[Dict[str, Any]], users: [Dict[str, Any]]) -> List[Dict[str, Any]]:
    summary = []
    for user, data in users.items():
        user_posts = [post for post in posts if post["user"] == user]
        total_likes = sum(post["likes"] for post in user_posts)
        summary.append({
            "user": user,
            "post_count": len(user_posts),
            "total_likes": total_likes,
            "followers": data["followers"],
            "following": data["following"]
        })
        print(summary)

user_activity_summary(posts, users)       
