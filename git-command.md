1. git init
2. git status
3. git add [files name] or git add -A #means upload all
4. git commit -m "first commit"
5. git remote add origin https://github.com/shown440/database_independent_API.git
6. git push -u origin master

###################################
##### GIT Branching
###################################
1. git checkout -b dbcolumn_map [Create new branch]
2. git push origin dbcolumn_map [Push to the branch]
3. git switch dbcolumn_map | main [Switch git branches]
3. git checkout master | dbcolumn_map [Switch git branches]

4. git branch -a [Show all local and remote branches in git]
5. git branch -r [see remote branches]
6. git push origin --delete my-branch-name [To delete a remote branch]
7. git branch -d my-branch-name [To delete a local branch]

###################################
##### Merge GIT Branches
###################################

Merge a Branch

1. You'll want to make sure your working tree is clean and see what branch you're on. Run this command:
        
	a. git status

2. First, you must check out the branch that you want to merge another branch into (changes will be merged into this branch). If you're not already on the desired branch, run this command:
        
	b. git checkout master

        NOTE: Replace master with another branch name as needed.
3. Now you can merge another branch into the current branch. Run this command:
        
	c. git merge my-branch-name

        NOTE: When you merge, there may be a conflict. Refer to Handling Merge Conflicts (the next exercise) to learn what to do.
