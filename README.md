# Scehduling
Given a list of people who have certain items (where each item can have properties (which are constraints between items) or tags (so properties can match against groups instead of single items)), outputs a list of the items in an order that minimises the loss of the constrains.

Here is an example, runnable in `test.py`:
Imagine you have a grade full of people, each studying some number of subjects and you want a list of all the subjects for exams allowing the greatest time available for each person between exams. But also, you wanted every maths exam to be separate, and physics to be last.
