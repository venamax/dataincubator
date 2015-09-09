OLD_GIT_SSH=$GIT_SSH
unset GIT_SSH
git push grader master
export GIT_SSH=$OLD_GIT_SSH
