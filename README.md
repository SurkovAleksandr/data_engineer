Заметки по курсу [ИНЖЕНЕР ДАННЫХ](https://karpov.courses/dataengineer)

```shell
git filter-branch --force --index-filter \
'git rm --cached --ignore-unmatch ./project/project.md' \
--prune-empty --tag-name-filter cat -- --all
```

```shell
git reflog expire --expire=now --all && git gc --prune=now --aggressive
```

```shell
git push --force --all
```
1. [Задание для проекта](https://lab.karpov.courses/learning/355/module/3726/lesson/32154/89404/423009/)
