import operator
from typing import Any, Dict, List

import praw

from .types import Redditor, SubNotFoundException


g_flattened_comments: praw.models.reddit.comment.Comment = []

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
            submission_descendants = get_descendant_metadata()
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



def get_descendant_metadata(submission: praw.models.reddit.submission.Submission) -> Dict[Redditor, int]:
    """Get author and score information from all descendants of submission.
        
        Args:
            submission (praw.models.reddit.submission.Submission): the submission who's descendants we're interested in
        
        Returns:
            A Dict[Redditor, int] of all descendants
    """

    
    for child in submission.comments:
        traverse_comment_chain(child)

    # add data from the flattened tree
    children_author_and_score: Dict[Redditor, int] = {}
    for comment in g_flattened_comments:
        children_author_and_score[comment.author] = comment.score
    
    return children_author_and_score


def traverse_comment_chain(comment: praw.models.reddit.comment.Comment) -> None:
    """Traverses all descendants of comment, differs from get_descendant_metadata in that it recurses down the tree.

        Args:
            comment (praw.models.reddit.comment.Comment): The root of the tree to traverse
    """
    g_flattened_comments.append(comment)

    if len(comment.replies) == 0:
        return None
    
    for child in comment.replies:
        traverse_comment_chain(child)
    