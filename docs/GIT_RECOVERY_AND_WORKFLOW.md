# Git Recovery and Workflow Guide

이 문서는 잘못 push한 commit을 되돌리고, 현재 로컬에 저장된 올바른 코드 기준으로 다시 push하는 방법을 정리한다.

---

## 1. 현재 상황

잘못 push한 commit message:

```text
Add step5 segment profiling notebook
```

main branch는 본인만 관리한다고 가정한다. 따라서 remote history를 정리해도 팀원 충돌 위험이 낮다.

가장 깔끔한 방법은 잘못된 마지막 commit을 로컬에서 취소한 뒤, 현재 저장된 파일 기준으로 다시 commit하고 `--force-with-lease`로 push하는 것이다.

---

## 2. 먼저 확인할 것

```bash
git status
git log --oneline -5
```

`git log`에서 가장 위 commit이 잘못된 commit인지 확인한다.

예:

```text
abc1234 Add step5 segment profiling notebook
...
```

가장 위 commit이 잘못된 commit일 때만 아래 방법을 사용한다.

---

## 3. 잘못된 마지막 commit 취소 후 현재 파일 기준으로 다시 push

현재 작업 파일은 유지하면서 commit만 취소한다.

```bash
git reset --soft HEAD~1
```

현재 상태 확인:

```bash
git status
```

필요하면 수정된 파일을 다시 add한다.

```bash
git add notebooks/05_segment_profiling.ipynb
```

README나 docs도 같이 수정했다면 함께 추가한다.

```bash
git add README.md docs/NOTEBOOK_MARKDOWN_BLOCKS.md docs/GIT_RECOVERY_AND_WORKFLOW.md
```

새 commit 생성:

```bash
git commit -m "Add step 5 segment profiling notebook"
```

remote main을 현재 commit으로 교체:

```bash
git push --force-with-lease origin main
```

`--force`가 아니라 `--force-with-lease`를 사용한다. 이는 remote가 예상과 다르게 바뀐 경우 덮어쓰지 않도록 막아주는 더 안전한 force push 방식이다.

---

## 4. 만약 잘못된 commit이 최신 commit이 아니라면

잘못된 commit이 최신이 아니라면 reset을 바로 쓰지 말고 해당 commit hash를 확인한다.

```bash
git log --oneline
```

그 다음 revert를 사용하는 것이 안전하다.

```bash
git revert <bad_commit_hash>
git push origin main
```

다만 이 방식은 잘못된 commit을 history에서 제거하는 것이 아니라, 반대 변경을 새 commit으로 추가하는 방식이다.

---

## 5. 앞으로의 권장 workflow

main branch는 본인이 관리하고, 팀원 파일은 직접 검토 후 반영한다.

일반적인 작업 흐름:

```bash
git status
git add <수정한 파일>
git commit -m "설명적인 commit message"
git push origin main
```

추천 commit message 예시:

```text
Add step 3.5 further preprocessing notebook
Add step 4 clustering model selection notebook
Add step 4.5 clustering visualization notebook
Add step 5 segment profiling notebook
Update project README and notebook documentation
```

---

## 6. data 폴더 commit 정책

기본적으로 다음 결과 폴더는 재생성 가능하므로 commit하지 않는다.

```text
data/processed/
data/analysis/
outputs/
```

단, 제출 편의상 결과 CSV나 그림을 함께 제출해야 한다면, 별도 zip으로 묶거나 `.gitignore` 정책을 임시로 조정한다.
