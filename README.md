# About the database models and tables
## Relationship between 'Subjects' and 'bookMaster'
- The relationship is established using a one-to-many relationship
- One `Subjects` record can be related to multiple 'bookMaster' records.
- Each `Subjects` record can be associated with multiple books in the `bookMaster` table.This is indicated by the `db.relationship` in the `bookMaster` class and the `SubId` foreign key in the 'bookMaster` table.
## Relationship between `userList` and `IssueReturn`
- Also a one-to-many relationship.
- One `userList` record can be related to multiple `IssueReturn` records, each user in the `usersList` table can have multiple issue/return transactions in the `IssueReturn` table.
- This is indicated by the `db.relationship` in the `IssueReturn` class and the `userID` foreign key in the `IssueReturn` table.