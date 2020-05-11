from typing import Any, Dict
class Redditor:
    def __init__(self, username: str, post_count: int=0, post_score: int=0, comment_count: int=0, comment_score: int=0):
        self.username = username
        self.post_score = post_score
        self.post_count = post_count
        self.comment_score = comment_score
        self.comment_count = comment_count

    def update_post_score(self, new_post_score: int) -> int:
        """Increase the post score of the Redditor.

        Args:
            new_post_score (int): the post score to be added

        Returns:
            A float representing the new post score.

        """

        self.post_score += new_post_score
        self.post_count += 1

        return self.post_score;

    def update_comment_score(self, new_comment_score: int) -> int:
        """Increase the comment score of the Redditor.

        Args:
            new_comment_score (int): the comment score to be added

        Returns:
            An int representing the new comment score.
        """

        self.comment_score += new_comment_score
        self.comment_count += 1

        return self.comment_score

    def return_total_score(self) -> int:
        """Fetches the combined post and comment score of the Redditor.

        Returns:
            A float representing the combined post and comment score.
        """

        return self.comment_score + self.post_score;

    def return_total_count(self) -> int:
        """Fetches the total number of posts and comments.

        Returns:
            An int representing the combined number of posts and comments.
        """

        return self.post_count + self.comment_count

    def serialize(self) -> Dict[str, Any]:
        """Helper function to serialize"""

        return_dict = {
                "username": self.username,
                "post_score": self.post_score,
                "comment_score": self.comment_score,
                "post_count": self.post_count,
                "comment_count": self.comment_count,
                "total_count": self.return_total_count(),
                "total_score": self.return_total_score()
        }

        return return_dict


class SubNotFoundException(Exception):
    def __init__(self, *args):
        pass

    def __str__(self):
        return "Subreddit not found"