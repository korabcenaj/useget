# Branch Protection Policy

This repository uses protected branches to keep the promotion flow predictable:

- `dev` for feature integration
- `staging` for pre-release validation
- `main` for production-ready code

Apply the following branch protection rules in GitHub under repository settings.

## `main`

- Require a pull request before merging
- Require 1 approval
- Dismiss stale pull request approvals when new commits are pushed
- Require status checks to pass before merging
- Require branches to be up to date before merging
- Required status check: `build`
- Require conversation resolution before merging
- Require linear history
- Do not allow bypassing the above settings
- Do not allow force pushes
- Do not allow deletions

## `staging`

- Require a pull request before merging
- Require 1 approval
- Dismiss stale pull request approvals when new commits are pushed
- Require status checks to pass before merging
- Require branches to be up to date before merging
- Required status check: `build`
- Require conversation resolution before merging
- Require linear history
- Do not allow bypassing the above settings
- Do not allow force pushes
- Do not allow deletions

## `dev`

- Require a pull request before merging
- Require 1 approval
- Require status checks to pass before merging
- Required status check: `build`
- Require conversation resolution before merging
- Do not allow bypassing the above settings
- Do not allow force pushes
- Do not allow deletions

## Notes

- Use exact branch-name rules for `main`, `staging`, and `dev`.
- The required status check name comes from the CI job in `.github/python-app.yml`.
- If CI job names change, update the protected-branch required check accordingly.