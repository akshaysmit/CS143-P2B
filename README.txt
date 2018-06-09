Question 1:

Input_id -> labeldem
Input_id -> labelgop
Input_id -> labeldjt

Question 2: There are a number of redundancies, listed below:

i) The subreddit name is being repeated for each comment in that subreddit
ii) can_gild is repeated each time a user posts a comment
iii）author_flair_text is repeated each time a user posts a comment
iv) author_flair_css_classString is repeated each time a user posts a comment
v) author_cakeday is repeated each time a user posts a comment

If, for instance, a user's can_gild ability or flair text changed, then we would potentially have to change
a very large number of tuples in this relation in order to reflect the change. Missing out a few tuples will
lead to our data being in inconsistent.

Let S be the set of attributes mentioned in i) through v).

We can decompose it into the following three relations:

user_details (username, can_gild, author_flair_text, author_flair_css_classString, author_cakeday)
comments (id, author, subreddit_id, ...all other attributes not in S...)
subreddit (subreddit_id, name)

Note comments.author is a foreign key referencing user_details.username and comments.subreddit_id is a
foreign key referencing subreddit.subreddit_id. We have eliminated the redundancies mentioned in i) through
v).

It is possible that the creator of the existing schema made it so because the large amount of data would
make joins quite expensive, especially when we are running spark only on our personal laptops with limited
RAM. 


