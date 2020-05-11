import operator
from typing import Any, Dict, List

import praw

from .types import Redditor, SubNotFoundException


def get_subreddit_results(
    subreddit_name: str, limit_num: int, reddit: praw.Reddit
) -> List[Dict[Any, Any]]:
    """Gets highest contributing redditors to a specific subreddit.

    Args:
            subreddit_name (str): the name of the desired subreddit.
            limit_num (int): the number of posts to look at
            reddit (praw.Reddit): a praw instance to use
    """
    redditors: Dict[str, Redditor] = {}
    sub = reddit.subreddit(subreddit_name)

    try:
        for submission in sub.new(limit=int(limit_num)):
            if submission.author == None:
                continue
            author = submission.author.name
            if author not in redditors:
                redditors[author] = Redditor(
                    author, post_count=1, post_score=submission.score
                )
            else:
                redditors[author].update_post_score(submission.score)
    except:
        raise SubNotFoundException

    return_list = [r.serialize() for r in redditors.values()]
    sorted_return_list = sorted(return_list, key=lambda r: r["post_score"])
    sorted_return_list.reverse()

    for counter in range(0, len(sorted_return_list)):
        sorted_return_list[counter]["rank"] = counter + 1

    return sorted_return_list
