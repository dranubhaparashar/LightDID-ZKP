# GitHub upload steps

From the repository root:

```bash
git init
git add .
git commit -m "Initial LightDID-ZKP reproducibility package"
git branch -M main
git remote add origin https://github.com/<your-user>/LightDID-ZKP.git
git push -u origin main
```

Recommended repository description:

> Reproducible code and benchmark-result package for LightDID-ZKP, a policy- and resource-aware selector for BBS and AnonCreds decentralized-identity presentations.

Recommended topics:

```text
decentralized-identity verifiable-credentials bbs-signatures anoncreds zero-knowledge-proofs privacy caps-zk reproducibility
```
